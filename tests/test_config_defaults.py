import os
from pathlib import Path

from app.calculator_config import CalculatorConfig

def test_config_defaults(tmp_path, monkeypatch):
    # Clear possibly inherited env vars
    for k in list(os.environ.keys()):
        if k.startswith("CALCULATOR_"):
            monkeypatch.delenv(k, raising=False)

    cfg = CalculatorConfig(base_dir=tmp_path)
    cfg.validate()
    # Weak assertions: paths exist or are under tmp, and values are sane
    assert cfg.log_dir.exists()
    assert cfg.history_dir.exists()
    assert isinstance(cfg.max_history_size, int)
