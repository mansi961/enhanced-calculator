"""
History persistence for the calculator, using pandas for CSV
serialization and deserialization.

HistoryManager converts a list of Calculation instances to a pandas
DataFrame and writes it to CALCULATOR_HISTORY_FILE, and can read that
file back into a list of Calculation instances. Handles missing or
malformed files gracefully by raising HistoryError.
"""

import os
import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError

REQUIRED_COLUMNS = ["operation", "operand_a", "operand_b", "result", "timestamp"]


class HistoryManager:
    """Handles saving and loading calculation history via pandas/CSV."""

    def __init__(self, config: CalculatorConfig = None):
        self.config = config or CalculatorConfig()

    def save(self, history: list) -> None:
        """
        Save a list of Calculation instances to the configured CSV file.
        """
        try:
            records = [calc.to_dict() for calc in history]
            df = pd.DataFrame(records, columns=REQUIRED_COLUMNS)
            df.to_csv(self.config.history_file, index=False)
        except Exception as exc:
            raise HistoryError(f"Failed to save history: {exc}")

    def load(self) -> list:
        """
        Load calculation history from the configured CSV file.

        Returns an empty list if the file does not exist yet (first
        run). Raises HistoryError if the file exists but is malformed.
        """
        if not os.path.exists(self.config.history_file):
            return []

        try:
            df = pd.read_csv(self.config.history_file)
        except Exception as exc:
            raise HistoryError(f"Failed to read history file: {exc}")

        if df.empty:
            return []

        missing = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise HistoryError(
                f"History file is malformed. Missing columns: {missing}"
            )

        try:
            return [
                Calculation.from_dict(row.to_dict())
                for _, row in df.iterrows()
            ]
        except Exception as exc:
            raise HistoryError(f"Failed to parse history file: {exc}")
