from __future__ import annotations
from decimal import Decimal, getcontext
from pathlib import Path
from typing import List
import pandas as pd
from datetime import datetime, UTC

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.operations import get_operation
from app.logger import get_logger


class Calculator:
    def __init__(self, base_dir: Path | CalculatorConfig | None = None):
        """
        Accept either:
          - a CalculatorConfig instance (already constructed), or
          - a Path (base_dir) / None (use cwd) and build config via from_env().
        """
        if isinstance(base_dir, CalculatorConfig):
            self.config = base_dir
        else:
            base_dir = base_dir or Path.cwd()
            self.config = CalculatorConfig.from_env(base_dir)

        self.config.validate()
        self.logger = get_logger(self.config.log_dir)

        # precision
        getcontext().prec = self.config.precision

        self.history: List[Calculation] = []
        self.observers: List[HistoryObserver] = []
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

    # ---- observers
    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)
        self.logger.info("Observer added: %s", observer.__class__.__name__)

    def notify(self, calc: Calculation) -> None:
        for ob in self.observers:
            ob.update(self, calc)

    # ---- utils
    def _validate_number(self, x: str | int | float) -> Decimal:
        try:
            d = Decimal(str(x))
        except Exception as e:  # pragma: no cover - Decimal edge parse
            raise ValidationError(f"Invalid number: {x}") from e
        if abs(d) > Decimal(str(self.config.max_input_value)):
            raise ValidationError(f"Value out of bounds: {x}")
        return d

    # ---- public API
    def perform(self, op_name: str, a, b) -> Decimal:
        op = get_operation(op_name)
        da, db = self._validate_number(a), self._validate_number(b)

        # save state for undo
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.redo_stack.clear()

        try:
            result = op.execute(da, db)
        except Exception as e:
            raise OperationError(str(e)) from e

        calc = Calculation(op_name, da, db, result, datetime.now(UTC))
        self.history.append(calc)
        # truncate history if needed
        if len(self.history) > self.config.max_history_size:
            self.history.pop(0)

        # observers
        self.notify(calc)
        return result

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        m = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = m.history.copy()
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        m = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = m.history.copy()
        return True

        # persistence
    def save_history(self) -> Path:
        df = self.get_history_dataframe()
        path = Path(self.config.history_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding=self.config.default_encoding)
        self.logger.info("History saved to %s", path)
        return path

    def load_history(self) -> None:
        path = Path(self.config.history_file)
        if not path.exists():
            self.logger.info("No history file at %s", path)
            return
        df = pd.read_csv(path)
        self.history = [
            Calculation.from_dict({
                "operation": r["operation"],
                "operand1": r["operand1"],
                "operand2": r["operand2"],
                "result": r["result"],
                "timestamp": r["timestamp"],
            })
            for _, r in df.iterrows()
        ]
        self.logger.info("Loaded %d history records", len(self.history))

    def clear(self) -> None:
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.logger.info("History cleared")

    def get_history_dataframe(self) -> pd.DataFrame:
        rows = [c.to_dict() for c in self.history]
        return pd.DataFrame(rows, columns=["operation", "operand1", "operand2", "result", "timestamp"])
