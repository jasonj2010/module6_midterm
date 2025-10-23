from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, List
from app.calculation import Calculation

class HistoryObserver(Protocol):
    def update(self, calculator: "Calculator", calc: Calculation) -> None:  # pragma: no cover (interface)
        ...

@dataclass
class LoggingObserver:
    """Observer that logs each calculation using the calculator's configured logger."""
    def update(self, calculator: "Calculator", calc: Calculation) -> None:
        # Reuse calculator.logger
        calculator.logger.info(
            "calc: %s(%s, %s) = %s @ %s",
            calc.operation,
            calc.operand1,
            calc.operand2,
            calc.result,
            calc.timestamp,
        )

@dataclass
class AutoSaveObserver:
    """Observer that auto-saves history after each successful calculation."""
    def update(self, calculator: "Calculator", calc: Calculation) -> None:
        # Only save if config says so
        if calculator.config.auto_save:
            calculator.save_history()
