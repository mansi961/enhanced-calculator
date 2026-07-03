"""
Unit tests for app/history.py — covers saving, loading, missing
files, and malformed CSV handling using pandas.
"""

import pytest

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError
from app.history import HistoryManager


@pytest.fixture
def config(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    return CalculatorConfig()


@pytest.fixture
def history_manager(config):
    return HistoryManager(config)


def test_save_and_load_round_trip(history_manager):
    calcs = [
        Calculation("add", 2, 3, 5),
        Calculation("multiply", 4, 5, 20),
    ]
    history_manager.save(calcs)
    loaded = history_manager.load()

    assert len(loaded) == 2
    assert loaded[0].operation == "add"
    assert loaded[0].result == 5.0
    assert loaded[1].operation == "multiply"
    assert loaded[1].result == 20.0


def test_load_when_file_does_not_exist_returns_empty(history_manager):
    assert history_manager.load() == []


def test_save_empty_history(history_manager):
    history_manager.save([])
    loaded = history_manager.load()
    assert loaded == []


def test_load_malformed_csv_raises(history_manager, config):
    import os
    os.makedirs(config.history_dir, exist_ok=True)
    with open(config.history_file, "w") as f:
        f.write("not,the,right,columns\n1,2,3,4\n")

    with pytest.raises(HistoryError):
        history_manager.load()


def test_save_creates_csv_with_correct_columns(history_manager, config):
    history_manager.save([Calculation("add", 1, 1, 2)])
    with open(config.history_file) as f:
        header = f.readline().strip()
    assert header == "operation,operand_a,operand_b,result,timestamp"


def test_load_preserves_order(history_manager):
    calcs = [
        Calculation("add", 1, 1, 2),
        Calculation("subtract", 5, 2, 3),
        Calculation("power", 2, 3, 8),
    ]
    history_manager.save(calcs)
    loaded = history_manager.load()
    assert [c.operation for c in loaded] == ["add", "subtract", "power"]
