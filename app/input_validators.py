"""
Input validation for calculator operands.

Ensures user-supplied values are numeric strings and fall within the
allowed range defined by CalculatorConfig (CALCULATOR_MAX_INPUT_VALUE).
Raises ValidationError with a clear message when input is invalid,
so the REPL can display it and prompt the user again.
"""

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def validate_number(value: str, config: CalculatorConfig = None) -> float:
    """
    Convert a string to a float and validate it is within the allowed
    input range. Raises ValidationError on failure.
    """
    config = config or CalculatorConfig()

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(
            f"Invalid input: '{value}' is not a valid number."
        )

    if abs(number) > config.max_input_value:
        raise ValidationError(
            f"Input {number} exceeds the maximum allowed value "
            f"of {config.max_input_value}."
        )

    return number


def validate_operands(a: str, b: str, config: CalculatorConfig = None) -> tuple:
    """
    Validate two operand strings and return them as a tuple of floats.
    """
    config = config or CalculatorConfig()
    return validate_number(a, config), validate_number(b, config)
