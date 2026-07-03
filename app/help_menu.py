"""
Dynamic help menu generation using the Decorator Design Pattern.

HelpMenuComponent is the base interface. BaseHelpMenu is the core
component. CommandHelpDecorator wraps a component and adds one
command's help line to it. By looping over OperationFactory's
registered operations and wrapping a new decorator for each one,
the help menu automatically reflects any new operations added to
the factory -- no manual edits to a hardcoded string are needed.
"""

from abc import ABC, abstractmethod

from app.operations import OperationFactory

# Human-readable descriptions for arithmetic operations. If a new
# operation is added to OperationFactory without an entry here, it
# still appears in the help menu with a generic fallback description.
OPERATION_DESCRIPTIONS = {
    "add": "Add two numbers",
    "subtract": "Subtract the second number from the first",
    "multiply": "Multiply two numbers",
    "divide": "Divide the first number by the second",
    "power": "Raise the first number to the power of the second",
    "root": "Compute the nth root of a number",
    "modulus": "Compute the remainder of division",
    "int_divide": "Perform integer (floor) division",
    "percent": "Compute (a / b) * 100",
    "abs_diff": "Compute the absolute difference between two numbers",
}

# Non-arithmetic commands, which don't come from OperationFactory
# and so are registered separately.
UTILITY_COMMANDS = {
    "history": "Display calculation history",
    "clear": "Clear calculation history",
    "undo": "Undo the last calculation",
    "redo": "Redo the last undone calculation",
    "save": "Manually save calculation history to file",
    "load": "Manually load calculation history from file",
    "help": "Display this help message",
    "exit": "Exit the application",
}


class HelpMenuComponent(ABC):
    """Abstract component in the Decorator pattern."""

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError  # pragma: no cover


class BaseHelpMenu(HelpMenuComponent):
    """The core component that all decorators wrap around."""

    def render(self) -> str:
        return "Available commands:\n"


class HelpMenuDecorator(HelpMenuComponent):
    """Base decorator: wraps a HelpMenuComponent and delegates to it."""

    def __init__(self, wrapped: HelpMenuComponent):
        self._wrapped = wrapped

    def render(self) -> str:
        return self._wrapped.render()


class CommandHelpDecorator(HelpMenuDecorator):
    """Adds a single command's help line on top of the wrapped menu."""

    def __init__(self, wrapped: HelpMenuComponent, command_name: str, description: str):
        super().__init__(wrapped)
        self.command_name = command_name
        self.description = description

    def render(self) -> str:
        base = self._wrapped.render()
        return base + f"  {self.command_name:<12} - {self.description}\n"


def build_help_menu() -> str:
    """
    Dynamically build the full help menu by decorating a BaseHelpMenu
    with one CommandHelpDecorator per registered operation, plus the
    fixed utility commands. New operations registered in
    OperationFactory automatically appear here without any changes
    to this function.
    """
    menu: HelpMenuComponent = BaseHelpMenu()

    for op_name in OperationFactory.available_operations():
        description = OPERATION_DESCRIPTIONS.get(
            op_name, f"Perform the '{op_name}' operation"
        )
        menu = CommandHelpDecorator(menu, f"{op_name} <a> <b>", description)

    for command_name, description in UTILITY_COMMANDS.items():
        menu = CommandHelpDecorator(menu, command_name, description)

    return menu.render()
