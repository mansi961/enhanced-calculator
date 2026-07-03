"""
Unit tests for app/help_menu.py — covers the Decorator pattern
implementation for dynamically building the help menu.
"""

import pytest

from app.help_menu import (
    build_help_menu,
    BaseHelpMenu,
    HelpMenuDecorator,
    CommandHelpDecorator,
    HelpMenuComponent,
)
from app.operations import OperationFactory


def test_base_help_menu_renders_header():
    menu = BaseHelpMenu()
    assert menu.render() == "Available commands:\n"


def test_command_help_decorator_adds_line():
    base = BaseHelpMenu()
    decorated = CommandHelpDecorator(base, "add", "Add two numbers")
    result = decorated.render()
    assert "Available commands:" in result
    assert "add" in result
    assert "Add two numbers" in result


def test_decorators_stack_in_order():
    base = BaseHelpMenu()
    step1 = CommandHelpDecorator(base, "add", "Add two numbers")
    step2 = CommandHelpDecorator(step1, "subtract", "Subtract numbers")
    result = step2.render()
    # base menu appears first, then add, then subtract
    add_index = result.index("add")
    subtract_index = result.index("subtract")
    assert add_index < subtract_index


def test_build_help_menu_contains_all_operations():
    menu = build_help_menu()
    for op_name in OperationFactory.available_operations():
        assert op_name in menu


def test_build_help_menu_contains_utility_commands():
    menu = build_help_menu()
    for command in ["history", "clear", "undo", "redo", "save", "load", "help", "exit"]:
        assert command in menu


def test_build_help_menu_starts_with_header():
    menu = build_help_menu()
    assert menu.startswith("Available commands:")


def test_help_menu_component_is_abstract():
    with pytest.raises(TypeError):
        HelpMenuComponent()


def test_help_menu_decorator_delegates_to_wrapped():
    base = BaseHelpMenu()
    wrapper = HelpMenuDecorator(base)
    assert wrapper.render() == base.render()


def test_unknown_operation_gets_fallback_description(monkeypatch):
    # Temporarily register a fake operation with no description entry
    original_operations = OperationFactory._operations.copy()
    OperationFactory._operations["fake_op"] = list(original_operations.values())[0]

    try:
        menu = build_help_menu()
        assert "fake_op" in menu
        assert "Perform the 'fake_op' operation" in menu
    finally:
        OperationFactory._operations = original_operations
