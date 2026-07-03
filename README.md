# enhanced-calculator
# Enhanced Calculator

A command-line calculator application built with Python, featuring advanced arithmetic operations, undo/redo history, automatic logging, CSV-based persistence, and a REPL-style interface. Built using the Factory, Memento, and Observer design patterns.

## Features

- **Arithmetic operations:** add, subtract, multiply, divide, power, root, modulus, integer division, percentage, and absolute difference
- **Undo/Redo:** revert or restore calculations using the Memento pattern
- **Automatic logging:** every calculation is logged with operation, operands, result, and timestamp
- **Auto-save:** calculation history automatically saves to CSV after each operation (configurable)
- **Manual save/load:** explicitly save or load history on demand
- **Robust error handling:** custom exceptions for invalid operations, bad input, and configuration issues
- **Configurable via `.env`:** control history size, precision, auto-save behavior, and more

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/mansi961/enhanced-calculator.git
   cd enhanced-calculator
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables (defaults shown):


If a variable is omitted, the application falls back to the defaults above.

## Usage

Run the application:
```bash
python3 main.py
```

### Supported commands

| Command | Description |
|---|---|
| `add <a> <b>` | Add two numbers |
| `subtract <a> <b>` | Subtract b from a |
| `multiply <a> <b>` | Multiply two numbers |
| `divide <a> <b>` | Divide a by b |
| `power <a> <b>` | Raise a to the power of b |
| `root <a> <b>` | Compute the bth root of a |
| `modulus <a> <b>` | Remainder of a divided by b |
| `int_divide <a> <b>` | Integer division of a by b |
| `percent <a> <b>` | (a / b) * 100 |
| `abs_diff <a> <b>` | Absolute difference between a and b |
| `history` | Show calculation history |
| `clear` | Clear calculation history |
| `undo` | Undo the last calculation |
| `redo` | Redo the last undone calculation |
| `save` | Manually save history to CSV |
| `load` | Manually load history from CSV |
| `help` | Show available commands |
| `exit` | Exit the application |

### Example session

## Running Tests

Run the full test suite:
```bash
python3 -m pytest
```

Run tests with coverage report:
```bash
python3 -m pytest --cov=app --cov-report=term-missing
```

The project maintains 90%+ test coverage, enforced automatically in CI.

## Continuous Integration

This project uses GitHub Actions (`.github/workflows/python-app.yml`) to automatically:
- Check out the repository
- Set up Python
- Install dependencies
- Run the full test suite with coverage
- Fail the build if coverage drops below 90%

The workflow runs on every push and pull request to `main`.

## Project Structure


