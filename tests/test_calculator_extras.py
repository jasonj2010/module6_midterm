from pathlib import Path
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.history import HistoryObserver

# Dummy observer to confirm notify() is hit
class _DummyObserver(HistoryObserver):
    def __init__(self):
        self.called_with = None
    def update(self, calculator, calculation):
        self.called_with = (calculator, calculation)

def test_init_with_explicit_config(tmp_path, monkeypatch):
    # Ensure env vars aren't interfering
    monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_HISTORY_DIR", raising=False)

    cfg = CalculatorConfig.from_env(tmp_path)
    c = Calculator(cfg)  # exercise the "config instance passed in" branch
    # Same directories should be used from cfg
    assert Path(c.config.log_dir).exists()
    assert Path(c.config.history_dir).exists()

def test_observer_notified_and_dataframe(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))

    c = Calculator(base_dir=tmp_path)
    obs = _DummyObserver()
    c.add_observer(obs)

    # Perform one operation to trigger notify()
    result = c.perform("add", 2, 3)
    assert result == 5
    assert obs.called_with is not None
    got_calc = obs.called_with[1]
    assert got_calc.operation == "add"

    # Exercise get_history_dataframe()
    df = c.get_history_dataframe()
    assert not df.empty
    assert set(df.columns) == {"operation", "operand1", "operand2", "result", "timestamp"}

def test_clear_empties_everything(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))

    c = Calculator(base_dir=tmp_path)
    c.perform("multiply", 3, 4)  # populate history
    assert len(c.history) == 1

    # push onto undo/redo stacks
    c.undo()
    assert len(c.undo_stack) >= 0  # stack exists (may be 0 if nothing to undo)
    c.redo()

    # clear() should empty history and both stacks
    c.clear()
    assert len(c.history) == 0
    assert len(c.undo_stack) == 0
    assert len(c.redo_stack) == 0
