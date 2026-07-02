"""
Logging configuration for the calculator application.

Provides a single get_logger() function that returns a configured
logger writing to the log file specified in CalculatorConfig. Used
by the Calculator core, the LoggingObserver, and other modules that
need to record events.
"""

import logging

from app.calculator_config import CalculatorConfig


def get_logger(name: str = "calculator", config: CalculatorConfig = None) -> logging.Logger:
    """
    Return a configured logger that writes to the log file defined
    in the calculator's configuration.

    Safe to call multiple times: handlers are only attached once per
    logger name, avoiding duplicate log lines.
    """
    config = config or CalculatorConfig()
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(
            config.log_file, encoding=config.default_encoding
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
