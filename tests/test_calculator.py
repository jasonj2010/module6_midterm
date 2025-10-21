from app.calculator import Calculator

def test_perform_add(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    c = Calculator(base_dir=tmp_path)
    r = c.perform("add", "2", "3")
    assert str(r) == "5"
    assert len(c.history) == 1
