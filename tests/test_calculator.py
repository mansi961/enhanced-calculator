"""
Unit tests for app/calculator.py — covers the Calculator core,
undo/redo (Memento), and the Observer pattern (LoggingObserver,
AutoSaveObserver).

Uses tmp_path + monkeypatch to redirect log/history directories so
tests don't pollute the real project's logs/ and history/ folders.
"""

import pytest

from app.calculator import Calculator, LoggingObserver, AutoSaveObserver, Observer
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import HistoryError


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """A CalculatorConfig pointed at temporary directories."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "3")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    return CalculatorConfig()


@pytest.fixture
def calculator(isolated_config):
    return Calculator(config=isolated_config)


def test_perform_operation_adds_to_history(calculator):
    result = calculator.perform_operation("add", 2, 3)
    assert result.result == 5
    assert len(calculator.get_history()) == 1


def test_perform_multiple_operations(calculator):
    calculator.perform_operation("add", 2, 3)
    calculator.perform_operation("multiply", 4, 5)
    history = calculator.get_history()
    assert len(history) == 2
    assert history[0].operation == "add"
    assert history[1].operation == "multiply"


def test_undo_reverts_last_calculation(calculator):
    calculator.perform_operation("add", 2, 3)
    calculator.perform_operation("multiply", 4, 5)
    calculator.undo()
    history = calculator.get_history()
    assert len(history) == 1
    assert history[0].operation == "add"


def test_redo_restores_calculation(calculator):
    calculator.perform_operation("add", 2, 3)
    calculator.perform_operation("multiply", 4, 5)
    calculator.undo()
    calculator.redo()
    history = calculator.get_history()
    assert len(history) == 2
    assert history[1].operation == "multiply"


def test_undo_with_nothing_to_undo_raises(calculator):
    with pytest.raises(HistoryError):
        calculator.undo()


def test_redo_with_nothing_to_redo_raises(calculator):
    calculator.perform_operation("add", 2, 3)
    with pytest.raises(HistoryError):
        calculator.redo()


def test_clear_history(calculator):
    calculator.perform_operation("add", 2, 3)
    calculator.clear_history()
    assert calculator.get_history() == []


def test_clear_history_can_be_undone(calculator):
    calculator.perform_operation("add", 2, 3)
    calculator.clear_history()
    calculator.undo()
    assert len(calculator.get_history()) == 1


def test_max_history_size_enforced(calculator):
    # config sets max_history_size=3
    calculator.perform_operation("add", 1, 1)
    calculator.perform_operation("add", 2, 2)
    calculator.perform_operation("add", 3, 3)
    calculator.perform_operation("add", 4, 4)
    history = calculator.get_history()
    assert len(history) == 3
    # oldest (1+1) should have been dropped
    assert history[0].operand_a == 2


def test_save_and_load_history(calculator):
    calculator.perform_operation("add", 2, 3)
    calculator.perform_operation("multiply", 4, 5)
    calculator.save_history()

    new_calculator = Calculator(config=calculator.config)
    new_calculator.load_history()
    loaded = new_calculator.get_history()
    assert len(loaded) == 2
    assert loaded[0].operation == "add"
    assert loaded[1].operation == "multiply"


def test_logging_observer_writes_to_log_file(isolated_config):
    calculator = Calculator(config=isolated_config)
    calculator.add_observer(LoggingObserver(config=isolated_config))
    calculator.perform_operation("add", 2, 3)

    with open(isolated_config.log_file) as f:
        contents = f.read()
    assert "add" in contents
    assert "5" in contents


def test_autosave_observer_saves_history_file(isolated_config):
    calculator = Calculator(config=isolated_config)
    calculator.add_observer(AutoSaveObserver(calculator, config=isolated_config))
    calculator.perform_operation("add", 2, 3)

    import os
    assert os.path.exists(isolated_config.history_file)


def test_autosave_observer_respects_auto_save_flag(isolated_config, monkeypatch):
    isolated_config.auto_save = False
    calculator = Calculator(config=isolated_config)
    calculator.add_observer(AutoSaveObserver(calculator, config=isolated_config))
    calculator.perform_operation("add", 2, 3)

    import os
    assert not os.path.exists(isolated_config.history_file)


def test_observer_abstract_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Observer()


def test_multiple_observers_all_notified(isolated_config):
    calls = []

    class SpyObserver(Observer):
        def update(self, calculation):
            calls.append(calculation)

    calculator = Calculator(config=isolated_config)
    calculator.add_observer(SpyObserver())
    calculator.add_observer(SpyObserver())
    calculator.perform_operation("add", 2, 3)

    assert len(calls) == 2
