"""
Unit tests for app/calculator_config.py — covers default values,
custom .env values, and validation errors.
"""

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_defaults_when_no_env_vars(monkeypatch, tmp_path):
    monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_HISTORY_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_MAX_HISTORY_SIZE", raising=False)
    monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)
    monkeypatch.delenv("CALCULATOR_PRECISION", raising=False)
    monkeypatch.delenv("CALCULATOR_MAX_INPUT_VALUE", raising=False)
    monkeypatch.delenv("CALCULATOR_DEFAULT_ENCODING", raising=False)
    monkeypatch.chdir(tmp_path)

    config = CalculatorConfig()
    assert config.log_dir == "logs"
    assert config.history_dir == "history"
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 4
    assert config.max_input_value == 1_000_000.0
    assert config.default_encoding == "utf-8"


def test_custom_env_values(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "mylogs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "myhistory"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")

    config = CalculatorConfig()
    assert config.max_history_size == 50
    assert config.auto_save is False
    assert config.precision == 2


def test_invalid_max_history_size_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "not_a_number")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_negative_max_history_size_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "-5")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_negative_precision_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_PRECISION", "-1")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_invalid_max_input_value_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "not_a_number")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_zero_max_input_value_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "0")
    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_directories_are_created(monkeypatch, tmp_path):
    log_dir = tmp_path / "createdlogs"
    history_dir = tmp_path / "createdhistory"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(history_dir))

    CalculatorConfig()
    assert log_dir.exists()
    assert history_dir.exists()


def test_repr_contains_key_settings(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
