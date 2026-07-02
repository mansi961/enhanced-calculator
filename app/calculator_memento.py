"""
Memento Design Pattern for undo/redo functionality.

CalculatorMemento stores a snapshot of the calculation history at a
point in time. CalculatorCaretaker manages the undo and redo stacks,
allowing the Calculator to revert to or restore a previous state
without knowing how history is represented internally.
"""

from copy import deepcopy

from app.exceptions import HistoryError


class CalculatorMemento:
    """A snapshot of the calculator's history list at a point in time."""

    def __init__(self, history: list):
        # Deepcopy so later mutations to the live history list don't
        # accidentally alter this saved snapshot.
        self._state = deepcopy(history)

    def get_state(self) -> list:
        """Return a copy of the snapshot's history state."""
        return deepcopy(self._state)


class CalculatorCaretaker:
    """
    Manages undo/redo stacks of CalculatorMemento snapshots.

    - save_state() is called before each new calculation, pushing the
      current history onto the undo stack and clearing the redo stack.
    - undo() pops the most recent snapshot off the undo stack and
      returns it, after pushing the current state onto the redo stack.
    - redo() does the reverse.
    """

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def save_state(self, history: list):
        """Save the current history state before a new calculation."""
        self._undo_stack.append(CalculatorMemento(history))
        self._redo_stack.clear()

    def undo(self, current_history: list) -> list:
        """
        Revert to the previous history state.

        The current state is pushed onto the redo stack so it can be
        restored later with redo().
        """
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")
        self._redo_stack.append(CalculatorMemento(current_history))
        memento = self._undo_stack.pop()
        return memento.get_state()

    def redo(self, current_history: list) -> list:
        """
        Restore a history state that was previously undone.

        The current state is pushed onto the undo stack so it can be
        undone again later.
        """
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")
        self._undo_stack.append(CalculatorMemento(current_history))
        memento = self._redo_stack.pop()
        return memento.get_state()

    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0
