from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
from app.calculation import Calculation

class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculator: "Calculator", calc: Calculation) -> None: ...

class LoggingObserver(HistoryObserver):
    def update(self, calculator: "Calculator", calc: Calculation) -> None:
        calculator.logger.info(
            "Calculated %s(%s, %s) = %s",
            calc.operation, calc.operand1, calc.operand2, calc.result
        )

class AutoSaveObserver(HistoryObserver):
    def update(self, calculator: "Calculator", calc: Calculation) -> None:
        # Save entire history to CSV
        df = calculator.get_history_dataframe()
        path = Path(calculator.config.history_dir) / "calculator_history.csv"
        df.to_csv(path, index=False, encoding=calculator.config.default_encoding)
        calculator.logger.info("Auto-saved history to %s", path)
