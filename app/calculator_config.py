# app/calculator_config.py

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class CalculatorConfig:
    """
    Central configuration for the calculator.

    You can either:
      - Construct directly with just base_dir (others default), e.g. CalculatorConfig(base_dir=tmp_path)
      - Or build from environment using from_env(base_dir)

    Environment variables (all optional):
      CALCULATOR_LOG_DIR
      CALCULATOR_HISTORY_DIR
      CALCULATOR_MAX_HISTORY_SIZE
      CALCULATOR_AUTO_SAVE           (true/false)
      CALCULATOR_PRECISION
      CALCULATOR_MAX_INPUT_VALUE
      CALCULATOR_DEFAULT_ENCODING
    """

    base_dir: Path
    log_dir: Optional[Path] = None
    history_dir: Optional[Path] = None
    max_history_size: int = 100
    auto_save: bool = True
    precision: int = 6
    max_input_value: float = 1e12
    default_encoding: str = "utf-8"

    # Derived file paths
    @property
    def log_file(self) -> Path:
        return self.log_dir / "calculator.log"  # type: ignore[arg-type]

    @property
    def history_file(self) -> Path:
        return self.history_dir / "history.csv"  # type: ignore[arg-type]

    def __post_init__(self) -> None:
        # Normalize to Path and set default dirs if not provided
        self.base_dir = Path(self.base_dir)
        self.log_dir = Path(self.log_dir) if self.log_dir is not None else self.base_dir / "logs"
        self.history_dir = Path(self.history_dir) if self.history_dir is not None else self.base_dir / "history"
        # Ensure directories exist
        self.validate()

    def validate(self) -> None:
        """Create directories and lightly sanity-check settings."""
        self.log_dir.mkdir(parents=True, exist_ok=True)      # type: ignore[union-attr]
        self.history_dir.mkdir(parents=True, exist_ok=True)  # type: ignore[union-attr]
        if self.max_history_size <= 0:
            self.max_history_size = 100
        if self.precision < 0:
            self.precision = 6
        if self.max_input_value <= 0:
            self.max_input_value = 1e12
        if not self.default_encoding:
            self.default_encoding = "utf-8"

    @classmethod
    def from_env(cls, base_dir: Path | None = None) -> "CalculatorConfig":
        """
        Build a config from environment variables (optionally anchored at base_dir).
        Falls back to sensible defaults if vars are missing.
        """
        load_dotenv()
        bd = Path(base_dir) if base_dir is not None else Path.cwd()

        def _get_path(name: str, default_subdir: str) -> Path:
            val = os.getenv(name)
            return Path(val) if val else (bd / default_subdir)

        def _get_int(name: str, default: int) -> int:
            try:
                return int(os.getenv(name, str(default)))
            except ValueError:
                return default

        def _get_float(name: str, default: float) -> float:
            try:
                return float(os.getenv(name, str(default)))
            except ValueError:
                return default

        def _get_bool(name: str, default: bool) -> bool:
            val = os.getenv(name)
            if val is None:
                return default
            return val.strip().lower() in {"1", "true", "yes", "on"}

        log_dir = _get_path("CALCULATOR_LOG_DIR", "logs")
        history_dir = _get_path("CALCULATOR_HISTORY_DIR", "history")
        max_history_size = _get_int("CALCULATOR_MAX_HISTORY_SIZE", 100)
        auto_save = _get_bool("CALCULATOR_AUTO_SAVE", True)
        precision = _get_int("CALCULATOR_PRECISION", 6)
        max_input_value = _get_float("CALCULATOR_MAX_INPUT_VALUE", 1e12)
        default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        return cls(
            base_dir=bd,
            log_dir=log_dir,
            history_dir=history_dir,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
        )
