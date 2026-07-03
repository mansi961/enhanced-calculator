"""
Core Calculator class, tying together the Factory, Memento, and
Observer design patterns.

- Factory: operations are created via OperationFactory.
- Memento: undo/redo is handled via CalculatorCaretaker.
- Observer: registered observers are notified after every calculation
  (used for logging and auto-save).
"""

from abc import ABC, abstractmethod

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorCaretaker
from app.exceptions import HistoryError
from app.history import HistoryManager
from app.logger import get_logger
from app.operations import OperationFactory


class Observer(ABC):
    """Abstract base class for observers notified of new calculations."""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        raise NotImplementedError  # pragma: no cover


class LoggingObserver(Observer):
    """Logs each new calculation's details to the log file."""

    def __init__(self, config: CalculatorConfig = None):
        self.logger = get_logger(config=config)

    def update(self, calculation: Calculation) -> None:
        self.logger.info(
            "Calculation performed: %s(%s, %s) = %s",
            calculation.operation,
            calculation.operand_a,
            calculation.operand_b,
            calculation.result,
        )


class AutoSaveObserver(Observer):
    """Automatically saves the full history to CSV after each calculation."""

    def __init__(self, calculator: "Calculator", config: CalculatorConfig = None):
        self.calculator = calculator
        self.history_manager = HistoryManager(config)

    def update(self, calculation: Calculation) -> None:
        if self.calculator.config.auto_save:
            self.history_manager.save(self.calculator.history)


class Calculator:
    """
    The core calculator engine.

    Manages calculation history, delegates arithmetic to
    OperationFactory, supports undo/redo via CalculatorCaretaker,
    and notifies registered observers after each calculation.
    """

    def __init__(self, config: CalculatorConfig = None):
        self.config = config or CalculatorConfig()
        self.history: list[Calculation] = []
        self._caretaker = CalculatorCaretaker()
        self._observers: list[Observer] = []
        self._history_manager = HistoryManager(self.config)

    # ---- Observer management ----

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def _notify_observers(self, calculation: Calculation) -> None:
        for observer in self._observers:
            observer.update(calculation)

    # ---- Core calculation logic ----

    def perform_operation(self, operation_name: str, a: float, b: float) -> Calculation:
        """
        Execute an operation, record it in history, and notify observers.
        Saves the pre-calculation state for undo before mutating history.
        """
        operation = OperationFactory.create_operation(operation_name)
        result = operation.execute(a, b)

        # Save state for undo BEFORE adding the new calculation
        self._caretaker.save_state(self.history)

        calculation = Calculation(operation_name, a, b, result)
        self.history.append(calculation)

        # Enforce max history size (drop oldest if exceeded)
        if len(self.history) > self.config.max_history_size:
            self.history.pop(0)

        self._notify_observers(calculation)
        return calculation

    # ---- History management ----

    def get_history(self) -> list:
        return list(self.history)

    def clear_history(self) -> None:
        self._caretaker.save_state(self.history)
        self.history.clear()

    def undo(self) -> None:
        """Revert to the previous history state."""
        self.history = self._caretaker.undo(self.history)

    def redo(self) -> None:
        """Restore a history state that was previously undone."""
        self.history = self._caretaker.redo(self.history)

    # ---- Manual save/load (REPL 'save' and 'load' commands) ----

    def save_history(self) -> None:
        self._history_manager.save(self.history)

    def load_history(self) -> None:
        self.history = self._history_manager.load()
