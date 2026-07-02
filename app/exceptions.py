"""
Custom exception classes for the calculator application.
"""


class CalculatorError(Exception):
    """Base class for all calculator-specific exceptions."""
    pass


class OperationError(CalculatorError):
    """Raised when an arithmetic operation cannot be completed."""
    pass


class ValidationError(CalculatorError):
    """Raised when user input fails validation."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when the application configuration is invalid."""
    pass


class HistoryError(CalculatorError):
    """Raised when saving, loading, or manipulating history fails."""
    pass
