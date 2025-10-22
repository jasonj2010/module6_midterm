import os
from pathlib import Path
import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

@pytest.fixture
def temp_calc(tmp_path):
    cfg = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(cfg)
    return calc

def test_history_and_undo_redo(temp_calc):
    c = temp_calc
    r1 = c.perform("add", 2, 3); assert r1 == 5
    r2 = c.perform("multiply", 5, 2); assert r2 == 10
    # history length 2
    df = c.get_history_dataframe()
    assert len(df.index) == 2

    # undo once -> back to 1 entry
    assert c.undo() is True
    df2 = c.get_history_dataframe()
    assert len(df2.index) == 1

    # redo -> back to 2 entries
    assert c.redo() is True
    df3 = c.get_history_dataframe()
    assert len(df3.index) == 2

def test_save_and_load_history(temp_calc, tmp_path):
    c = temp_calc
    c.perform("subtract", 10, 4)  # 6
    c.perform("divide", 6, 2)     # 3
    c.save_history()

    # Ensure file exists and has 2 rows
    csv_path = c.config.history_file
    assert csv_path.exists()
    df = pd.read_csv(csv_path)
    assert len(df.index) == 2

    # New calculator loads from same file
    c2 = Calculator(c.config)
    c2.load_history()
    df2 = c2.get_history_dataframe()
    assert len(df2.index) >= 2  # allow prior history lines too depending on your implementation
