import logging
from pathlib import Path

def get_logger(log_dir: Path) -> logging.Logger:
    log_file = Path(log_dir) / "calculator.log"
    logger = logging.getLogger("calculator")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_file, encoding="utf-8", delay=True)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger
