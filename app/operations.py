"""
Arithmetic operations for the calculator, implemented with the
Factory Design Pattern.

Each operation is a class with a single `execute(a, b)` method.
OperationFactory maps string names (as typed in the REPL) to the
correct operation instance, so the Calculator never needs to know
about operation classes directly.
"""

from abc import ABC, abstractmethod

from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all arithmetic operations."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Perform the operation on two numbers and return the result."""
        raise NotImplementedError  # pragma: no cover

    @property
    def name(self) -> str:
        """Human-readable name of the operation, used in logs/history."""
        return self.__class__.__name__.replace("Operation", "").lower()


class AddOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b


class PowerOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        try:
            return a ** b
        except (OverflowError, ValueError) as exc:
            raise OperationError(f"Invalid power operation: {exc}")


class RootOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        """Compute the bth root of a (e.g. root(9, 2) = 3)."""
        if b == 0:
            raise OperationError("Root degree cannot be zero.")
        if a < 0 and b % 2 == 0:
            raise OperationError(
                "Cannot compute an even root of a negative number."
            )
        try:
            if a < 0:
                return -((-a) ** (1 / b))
            return a ** (1 / b)
        except (OverflowError, ValueError) as exc:
            raise OperationError(f"Invalid root operation: {exc}")


class ModulusOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot compute modulus with divisor zero.")
        return a % b


class IntegerDivideOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot integer-divide by zero.")
        return float(a // b)


class PercentageOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        """Compute a as a percentage of b: (a / b) * 100."""
        if b == 0:
            raise OperationError("Cannot compute percentage with base zero.")
        return (a / b) * 100


class AbsoluteDifferenceOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)


class OperationFactory:
    """
    Factory for creating Operation instances by name.

    Centralizing operation creation here means new operations only
    need to be registered in one place (_operations dict), and the
    REPL/Calculator never needs to know about concrete classes.
    """

    _operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
        "modulus": ModulusOperation,
        "int_divide": IntegerDivideOperation,
        "percent": PercentageOperation,
        "abs_diff": AbsoluteDifferenceOperation,
    }

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """Return an instance of the operation matching operation_name."""
        operation_class = cls._operations.get(operation_name.lower())
        if operation_class is None:
            raise OperationError(f"Unknown operation: '{operation_name}'")
        return operation_class()

    @classmethod
    def available_operations(cls):
        """Return a list of all registered operation names."""
        return list(cls._operations.keys())
