from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

@dataclass
class CalculatorConfig:
    base_dir: Path
    log_dir: Path
    history_dir: Path
    max_history_size: int
    auto_save: bool
    precision: int
    max_input_value: float
    default_encoding: str

    @classmethod
    def from_env(cls, base_dir: Path) -> "CalculatorConfig":
        load_dotenv(override=False)
        log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", base_dir / "logs"))
        history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", base_dir / "history"))
        max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
        auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
        precision = int(os.getenv("CALCULATOR_PRECISION", "28"))
        max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e12"))
        default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
        return cls(
            base_dir=base_dir,
            log_dir=Path(log_dir),
            history_dir=Path(history_dir),
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
        )

    def validate(self) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        if self.max_history_size <= 0:
            raise ValueError("max_history_size must be positive")
        if self.precision <= 0:
            raise ValueError("precision must be positive")
