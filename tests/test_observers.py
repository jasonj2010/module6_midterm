import os
import types
import pytest
from pathlib import Path
from app.calculator import Calculator

@pytest.fixture
def calc_autosave(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    c = Calculator(base_dir=tmp_path)
    return c

def test_autosave_observer_triggers_save(calc_autosave, monkeypatch, tmp_path):
    # Spy on save_history
    calls = {"n": 0}
    def fake_save_history(self):
        calls["n"] += 1
        return Path(tmp_path / "history" / "history.csv")
    monkeypatch.setattr(Calculator, "save_history", fake_save_history, raising=True)

    calc_autosave.perform("add", 1, 2)
    assert calls["n"] >= 1  # was called at least once

def test_logging_observer_logs(calc_autosave, monkeypatch):
    # Spy on logger.info
    msgs = []
    def fake_info(self, msg, *args, **kwargs):
        msgs.append(msg % args if args else msg)
    monkeypatch.setattr(calc_autosave.logger, "info", types.MethodType(fake_info, calc_autosave.logger))

    calc_autosave.perform("multiply", 2, 3)
    assert any("calc:" in m for m in msgs)
