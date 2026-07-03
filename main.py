"""
Command-line REPL (Read-Eval-Print Loop) for the enhanced calculator.

Run with: python main.py
Type 'help' at the prompt to see available commands.
"""

from colorama import init, Fore, Style

from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.exceptions import CalculatorError
from app.input_validators import validate_operands
from app.help_menu import build_help_menu

init(autoreset=True)

ARITHMETIC_COMMANDS = {
    "add", "subtract", "multiply", "divide", "power",
    "root", "modulus", "int_divide", "percent", "abs_diff",
}


def build_calculator() -> Calculator:
    """Create a Calculator with logging and auto-save observers attached."""
    calculator = Calculator()
    calculator.add_observer(LoggingObserver(config=calculator.config))
    calculator.add_observer(AutoSaveObserver(calculator, config=calculator.config))
    return calculator


def print_history(calculator: Calculator) -> None:
    history = calculator.get_history()
    if not history:
        print(f"{Fore.YELLOW}History is empty.{Style.RESET_ALL}")
        return
    for i, calc in enumerate(history, start=1):
        print(f"{i}. {calc}")


def handle_arithmetic(calculator: Calculator, command: str, args: list) -> None:
    if len(args) != 2:
        print(f"{Fore.RED}Error: '{command}' requires exactly 2 numbers, e.g. '{command} 4 5'{Style.RESET_ALL}")
        return
    try:
        a, b = validate_operands(args[0], args[1], calculator.config)
        result = calculator.perform_operation(command, a, b)
        print(f"{Fore.GREEN}Result: {result.result}{Style.RESET_ALL}")
    except CalculatorError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def run_repl() -> None:
    calculator = build_calculator()
    print(f"{Fore.CYAN}Enhanced Calculator REPL. Type 'help' for commands, 'exit' to quit.{Style.RESET_ALL}")

    while True:
        try:
            raw_input_line = input(f"{Fore.CYAN}>>> {Style.RESET_ALL}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}Exiting calculator. Goodbye!{Style.RESET_ALL}")
            break

        if not raw_input_line:
            continue

        parts = raw_input_line.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "exit":
            print(f"{Fore.CYAN}Exiting calculator. Goodbye!{Style.RESET_ALL}")
            break
        elif command == "help":
            print(build_help_menu())
        elif command == "history":
            print_history(calculator)
        elif command == "clear":
            calculator.clear_history()
            print(f"{Fore.GREEN}History cleared.{Style.RESET_ALL}")
        elif command == "undo":
            try:
                calculator.undo()
                print(f"{Fore.GREEN}Undo successful.{Style.RESET_ALL}")
            except CalculatorError as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        elif command == "redo":
            try:
                calculator.redo()
                print(f"{Fore.GREEN}Redo successful.{Style.RESET_ALL}")
            except CalculatorError as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        elif command == "save":
            try:
                calculator.save_history()
                print(f"{Fore.GREEN}History saved.{Style.RESET_ALL}")
            except CalculatorError as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        elif command == "load":
            try:
                calculator.load_history()
                print(f"{Fore.GREEN}History loaded.{Style.RESET_ALL}")
            except CalculatorError as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        elif command in ARITHMETIC_COMMANDS:
            handle_arithmetic(calculator, command, args)
        else:
            print(f"{Fore.RED}Unknown command: '{command}'. Type 'help' for a list of commands.{Style.RESET_ALL}")


if __name__ == "__main__":
    run_repl()
