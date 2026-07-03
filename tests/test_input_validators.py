"""
Unit tests for app/input_validators.py — covers valid numbers,
invalid (non-numeric) input, and out-of-range values.
"""

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import validate_number, validate_operands


@pytest.fixture
def config(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000")
    return CalculatorConfig()


def test_validate_number_valid_integer(config):
    assert validate_number("5", config) == 5.0


def test_validate_number_valid_float(config):
    assert validate_number("3.14", config) == 3.14


def test_validate_number_valid_negative(config):
    assert validate_number("-42", config) == -42.0


def test_validate_number_non_numeric_raises(config):
    with pytest.raises(ValidationError):
        validate_number("abc", config)


def test_validate_number_none_raises(config):
    with pytest.raises(ValidationError):
        validate_number(None, config)


def test_validate_number_exceeds_max_raises(config):
    with pytest.raises(ValidationError):
        validate_number("5000", config)


def test_validate_number_exceeds_max_negative_raises(config):
    with pytest.raises(ValidationError):
        validate_number("-5000", config)


def test_validate_number_at_exact_max_boundary(config):
    # exactly at the limit should be allowed
    assert validate_number("1000", config) == 1000.0


def test_validate_operands_both_valid(config):
    a, b = validate_operands("10", "20", config)
    assert a == 10.0
    assert b == 20.0


def test_validate_operands_first_invalid_raises(config):
    with pytest.raises(ValidationError):
        validate_operands("abc", "20", config)


def test_validate_operands_second_invalid_raises(config):
    with pytest.raises(ValidationError):
        validate_operands("10", "xyz", config)
