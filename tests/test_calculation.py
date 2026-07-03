"""
Unit tests for app/calculation.py — covers construction, dict
conversion round-tripping, equality, and string representations.
"""

import pytest

from app.calculation import Calculation


def test_calculation_basic_attributes():
    c = Calculation("add", 2, 3, 5)
    assert c.operation == "add"
    assert c.operand_a == 2
    assert c.operand_b == 3
    assert c.result == 5
    assert c.timestamp is not None


def test_calculation_custom_timestamp():
    c = Calculation("add", 2, 3, 5, timestamp="2026-01-01T00:00:00")
    assert c.timestamp == "2026-01-01T00:00:00"


def test_to_dict_contains_all_fields():
    c = Calculation("multiply", 4, 5, 20)
    d = c.to_dict()
    assert d["operation"] == "multiply"
    assert d["operand_a"] == 4
    assert d["operand_b"] == 5
    assert d["result"] == 20
    assert "timestamp" in d


def test_from_dict_round_trip():
    original = Calculation("power", 2, 10, 1024)
    data = original.to_dict()
    restored = Calculation.from_dict(data)
    assert restored == original


def test_from_dict_missing_timestamp_defaults():
    data = {
        "operation": "add",
        "operand_a": "2",
        "operand_b": "3",
        "result": "5",
    }
    c = Calculation.from_dict(data)
    assert c.operation == "add"
    assert c.operand_a == 2.0
    assert c.timestamp is not None


def test_equality_ignores_timestamp():
    c1 = Calculation("add", 2, 3, 5, timestamp="2026-01-01T00:00:00")
    c2 = Calculation("add", 2, 3, 5, timestamp="2026-06-06T12:00:00")
    assert c1 == c2


def test_equality_different_values_not_equal():
    c1 = Calculation("add", 2, 3, 5)
    c2 = Calculation("add", 2, 4, 6)
    assert c1 != c2


def test_equality_with_non_calculation_returns_notimplemented():
    c = Calculation("add", 2, 3, 5)
    assert c.__eq__("not a calculation") is NotImplemented
    assert c != "not a calculation"


def test_repr_contains_key_fields():
    c = Calculation("add", 2, 3, 5)
    r = repr(c)
    assert "Calculation(" in r
    assert "operation='add'" in r
    assert "result=5" in r


def test_str_format():
    c = Calculation("add", 2, 3, 5)
    assert str(c) == "add(2, 3) = 5"
