"""
Represents a single calculation performed by the calculator.

A Calculation stores the operation name, the two operands, the
resulting value, and the timestamp of when it was performed.
Instances are immutable-by-convention (fields are set once at
creation) and are used throughout history, memento, logging,
and CSV persistence.
"""

from datetime import datetime


class Calculation:
    """A record of a single arithmetic operation and its result."""

    def __init__(
        self,
        operation: str,
        operand_a: float,
        operand_b: float,
        result: float,
        timestamp: str = None,
    ):
        self.operation = operation
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = result
        self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        """Convert this calculation to a dict, e.g. for CSV serialization."""
        return {
            "operation": self.operation,
            "operand_a": self.operand_a,
            "operand_b": self.operand_b,
            "result": self.result,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        """Reconstruct a Calculation instance from a dict (e.g. a CSV row)."""
        return cls(
            operation=data["operation"],
            operand_a=float(data["operand_a"]),
            operand_b=float(data["operand_b"]),
            result=float(data["result"]),
            timestamp=data.get("timestamp"),
        )

    def __eq__(self, other):
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation
            and self.operand_a == other.operand_a
            and self.operand_b == other.operand_b
            and self.result == other.result
        )

    def __repr__(self):
        return (
            f"Calculation(operation={self.operation!r}, "
            f"operand_a={self.operand_a}, operand_b={self.operand_b}, "
            f"result={self.result}, timestamp={self.timestamp!r})"
        )

    def __str__(self):
        return (
            f"{self.operation}({self.operand_a}, {self.operand_b}) "
            f"= {self.result}"
        )
