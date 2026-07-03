"""
Command-line REPL (Read-Eval-Print Loop) for the enhanced calculator.

Run with: python main.py
Type 'help' at the prompt to see available commands.
"""

from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.exceptions import CalculatorError
from app.input_validators import validate_operands

ARITHMETIC_COMMANDS = {
    "add", "subtract", "multiply", "divide", "power",
    "root", "modulus", "int_divide", "percent", "abs_diff",
}

HELP_TEXT = """
Available commands:
  add, subtract, multiply, divide, power, root,
  modulus, int_divide, percent, abs_diff   - perform a calculation (usage: <command> <a> <b>)
  history                                  - show calculation history
  clear                                    - clear calculation history
  undo                                     - undo the last calculation
  redo                                     - redo the last undone calculation
  save                                     - save history to file
  load                                     - load history from file
  help                                     - show this help message
  exit                                     - exit the application
"""


def build_calculator() -> Calculator:
    """Create a Calculator with logging and auto-save observers attached."""
    calculator = Calculator()
    calculator.add_observer(LoggingObserver(config=calculator.config))
    calculator.add_observer(AutoSaveObserver(calculator, config=calculator.config))
    return calculator


def print_history(calculator: Calculator) -> None:
    history = calculator.get_history()
    if not history:
        print("History is empty.")
        return
    for i, calc in enumerate(history, start=1):
        print(f"{i}. {calc}")


def handle_arithmetic(calculator: Calculator, command: str, args: list) -> None:
    if len(args) != 2:
        print(f"Error: '{command}' requires exactly 2 numbers, e.g. '{command} 4 5'")
        return
    try:
        a, b = validate_operands(args[0], args[1], calculator.config)
        result = calculator.perform_operation(command, a, b)
        print(f"Result: {result.result}")
    except CalculatorError as e:
        print(f"Error: {e}")


def run_repl() -> None:
    calculator = build_calculator()
    print("Enhanced Calculator REPL. Type 'help' for commands, 'exit' to quit.")

    while True:
        try:
            raw_input_line = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting calculator. Goodbye!")
            break

        if not raw_input_line:
            continue

        parts = raw_input_line.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "exit":
            print("Exiting calculator. Goodbye!")
            break
        elif command == "help":
            print(HELP_TEXT)
        elif command == "history":
            print_history(calculator)
        elif command == "clear":
            calculator.clear_history()
            print("History cleared.")
        elif command == "undo":
            try:
                calculator.undo()
                print("Undo successful.")
            except CalculatorError as e:
                print(f"Error: {e}")
        elif command == "redo":
            try:
                calculator.redo()
                print("Redo successful.")
            except CalculatorError as e:
                print(f"Error: {e}")
        elif command == "save":
            try:
                calculator.save_history()
                print("History saved.")
            except CalculatorError as e:
                print(f"Error: {e}")
        elif command == "load":
            try:
                calculator.load_history()
                print("History loaded.")
            except CalculatorError as e:
                print(f"Error: {e}")
        elif command in ARITHMETIC_COMMANDS:
            handle_arithmetic(calculator, command, args)
        else:
            print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")


if __name__ == "__main__":
    run_repl()
