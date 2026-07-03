"""
Unit tests for app/operations.py — covers every operation and the
OperationFactory, including edge cases like division by zero and
invalid roots.
"""

import pytest

from app.exceptions import OperationError
from app.operations import (
    OperationFactory,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntegerDivideOperation,
    PercentageOperation,
    AbsoluteDifferenceOperation,
)


@pytest.mark.parametrize(
    "op_name, a, b, expected",
    [
        ("add", 2, 3, 5),
        ("subtract", 10, 4, 6),
        ("multiply", 3, 4, 12),
        ("divide", 10, 2, 5),
        ("power", 2, 10, 1024),
        ("root", 9, 2, 3),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 50, 200, 25),
        ("abs_diff", 3, 10, 7),
    ],
)
def test_operation_factory_execute(op_name, a, b, expected):
    op = OperationFactory.create_operation(op_name)
    assert op.execute(a, b) == expected


def test_factory_unknown_operation_raises():
    with pytest.raises(OperationError):
        OperationFactory.create_operation("not_a_real_operation")


def test_factory_available_operations_contains_all():
    ops = OperationFactory.available_operations()
    for name in ["add", "subtract", "multiply", "divide", "power",
                 "root", "modulus", "int_divide", "percent", "abs_diff"]:
        assert name in ops


def test_divide_by_zero_raises():
    with pytest.raises(OperationError):
        DivideOperation().execute(10, 0)


def test_modulus_by_zero_raises():
    with pytest.raises(OperationError):
        ModulusOperation().execute(10, 0)


def test_int_divide_by_zero_raises():
    with pytest.raises(OperationError):
        IntegerDivideOperation().execute(10, 0)


def test_percent_with_zero_base_raises():
    with pytest.raises(OperationError):
        PercentageOperation().execute(10, 0)


def test_root_with_zero_degree_raises():
    with pytest.raises(OperationError):
        RootOperation().execute(9, 0)


def test_root_even_of_negative_raises():
    with pytest.raises(OperationError):
        RootOperation().execute(-9, 2)


def test_root_odd_of_negative_number():
    # Cube root of -8 should be -2
    result = RootOperation().execute(-8, 3)
    assert round(result, 5) == -2


@pytest.mark.parametrize(
    "op_class, expected_name",
    [
        (AddOperation, "add"),
        (SubtractOperation, "subtract"),
        (MultiplyOperation, "multiply"),
        (DivideOperation, "divide"),
    ],
)
def test_operation_name_property(op_class, expected_name):
    assert op_class().name == expected_name


def test_negative_and_zero_operands():
    assert AddOperation().execute(-5, 5) == 0
    assert MultiplyOperation().execute(0, 100) == 0
    assert AbsoluteDifferenceOperation().execute(-5, -10) == 5
