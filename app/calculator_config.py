# app/calculator_config.py

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def _as_bool(val: str | bool) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass
class CalculatorConfig:
    """
    Configuration for the calculator. Supports being constructed with only `base_dir`;
    all other values are pulled from environment variables (via .env) with sensible defaults.

    Expected env vars (all optional):
      - CALCULATOR_LOG_DIR
      - CALCULATOR_HISTORY_DIR
      - CALCULATOR_MAX_HISTORY_SIZE
      - CALCULATOR_AUTO_SAVE
      - CALCULATOR_PRECISION
      - CALCULATOR_MAX_INPUT_VALUE
      - CALCULATOR_DEFAULT_ENCODING
    """

    # Required input
    base_dir: Path

    # Optional inputs (can be omitted; will be derived in __post_init__)
    log_dir: Optional[Path] = None
    history_dir: Optional[Path] = None
    max_history_size: Optional[int] = None
    auto_save: Optional[bool] = None
    precision: Optional[int] = None
    max_input_value: Optional[float] = None
    default_encoding: Optional[str] = None

    # Derived paths
    log_file: Path = field(init=False)
    history_file: Path = field(init=False)

    def __post_init__(self) -> None:
        # Load .env (if present) but don't override already-set process env
        load_dotenv(override=False)

        # Ensure base_dir is a Path and absolute
        self.base_dir = Path(self.base_dir).resolve()

        # Directories (env overrides; else default under base_dir)
        self.log_dir = Path(
            os.getenv("CALCULATOR_LOG_DIR", str((self.log_dir or (self.base_dir / "logs")).resolve()))
        )
        self.history_dir = Path(
            os.getenv("CALCULATOR_HISTORY_DIR", str((self.history_dir or (self.base_dir / "history")).resolve()))
        )

        # Simple scalars with defaults
        self.max_history_size = int(
            os.getenv("CALCULATOR_MAX_HISTORY_SIZE", str(self.max_history_size if self.max_history_size is not None else 100))
        )
        self.auto_save = _as_bool(
            os.getenv("CALCULATOR_AUTO_SAVE", str(self.auto_save if self.auto_save is not None else True))
        )
        self.precision = int(
            os.getenv("CALCULATOR_PRECISION", str(self.precision if self.precision is not None else 8))
        )
        self.max_input_value = float(
            os.getenv("CALCULATOR_MAX_INPUT_VALUE", str(self.max_input_value if self.max_input_value is not None else 1e9))
        )
        self.default_encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING",
            self.default_encoding if self.default_encoding is not None else "utf-8",
        )

        # Ensure dirs exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

        # Files
        self.log_file = self.log_dir / "calculator.log"
        self.history_file = self.history_dir / "history.csv"

        # Validate final values
        self.validate()

    def validate(self) -> None:
        if self.max_history_size <= 0:
            raise ValueError("max_history_size must be > 0")
        if self.precision < 0:
            raise ValueError("precision must be >= 0")
        if self.max_input_value <= 0:
            raise ValueError("max_input_value must be > 0")
        if not isinstance(self.auto_save, bool):
            raise ValueError("auto_save must be a bool")
        if not self.default_encoding:
            raise ValueError("default_encoding must be a non-empty string")
