"""
Configuration management for the calculator application.

Loads settings from environment variables (via a .env file) using
python-dotenv, falling back to sensible defaults when a variable
is not set. Validates values on load and raises ConfigurationError
for invalid entries.
"""

import os
from dotenv import load_dotenv

from app.exceptions import ConfigurationError

# Load variables from .env into the process environment
load_dotenv()


def _get_bool(value: str) -> bool:
    """Convert a string environment variable to a boolean."""
    return value.strip().lower() in ("true", "1", "yes")


class CalculatorConfig:
    """
    Holds and validates all configuration settings for the calculator.

    Settings are read once at construction time from environment
    variables, with defaults applied for anything missing.
    """

    def __init__(self):
        self.log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        self.history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")

        self.max_history_size = self._parse_int(
            "CALCULATOR_MAX_HISTORY_SIZE", default=100
        )
        self.auto_save = _get_bool(os.getenv("CALCULATOR_AUTO_SAVE", "true"))

        self.precision = self._parse_int("CALCULATOR_PRECISION", default=4)
        self.max_input_value = self._parse_float(
            "CALCULATOR_MAX_INPUT_VALUE", default=1_000_000.0
        )
        self.default_encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )

        # Derived file paths
        self.log_file = os.path.join(self.log_dir, "calculator.log")
        self.history_file = os.path.join(self.history_dir, "history.csv")

        self._validate()
        self._ensure_directories()

    def _parse_int(self, key: str, default: int) -> int:
        raw = os.getenv(key)
        if raw is None:
            return default
        try:
            return int(raw)
        except ValueError:
            raise ConfigurationError(
                f"Invalid integer value for {key}: '{raw}'"
            )

    def _parse_float(self, key: str, default: float) -> float:
        raw = os.getenv(key)
        if raw is None:
            return default
        try:
            return float(raw)
        except ValueError:
            raise ConfigurationError(
                f"Invalid numeric value for {key}: '{raw}'"
            )

    def _validate(self):
        """Ensure configuration values are within acceptable ranges."""
        if self.max_history_size <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be a positive integer."
            )
        if self.precision < 0:
            raise ConfigurationError(
                "CALCULATOR_PRECISION cannot be negative."
            )
        if self.max_input_value <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be positive."
            )

    def _ensure_directories(self):
        """Create log and history directories if they don't exist."""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

    def __repr__(self):
        return (
            f"CalculatorConfig(log_dir={self.log_dir!r}, "
            f"history_dir={self.history_dir!r}, "
            f"max_history_size={self.max_history_size}, "
            f"auto_save={self.auto_save}, "
            f"precision={self.precision}, "
            f"max_input_value={self.max_input_value}, "
            f"default_encoding={self.default_encoding!r})"
        )
