# Module 6 Midterm - Advanced Calculator

A modular, testable, and configurable command-line calculator featuring advanced arithmetic, design patterns (Factory, Memento, Observer), persistent history with pandas, comprehensive error handling, and CI coverage enforcement.

## Features
- Performs advanced arithmetic operations: add, subtract, multiply, divide, power, root, modulus, integer division, percent, and absolute difference.  
- Maintains full calculation history with undo/redo using the Memento design pattern.  
- Uses the Observer pattern for logging and auto-save.  
- Saves and loads calculation history to CSV using pandas.  
- Reads environment-based configuration via CalculatorConfig.  
- Structured logging for debugging and audit trails.  
- Achieves over 90% test coverage with pytest and pytest-cov.  
- CI workflow validates tests and coverage automatically on each push or pull request.

## Directory Structure
app/  
 calculator.py  
 calculator_config.py  
 calculation.py  
 calculator_memento.py  
 history.py  
 operations.py  
 logger.py  
tests/  
 test_calculator.py  
 test_history_undo_redo.py  
 test_operations_more.py  
 test_calculator_extras.py  
.github/workflows/  
 python-app.yml  
.gitignore  
.coveragerc  
requirements.txt  
README.md

## Setup
### Create and activate a virtual environment
Windows (PowerShell):  
python -m venv venv  
venv\Scripts\Activate.ps1  

macOS/Linux:  
python3 -m venv venv  
source venv/bin/activate  

### Install dependencies
pip install -r requirements.txt  

### Run tests with coverage
pytest --cov=app --cov-report=term-missing  

### (Optional) Run interactively
python -m app.calculator_repl  

## Example Usage
from app.calculator import Calculator  
calc = Calculator()  
print(calc.perform("add", 10, 5))  
calc.save_history()  

## Design Patterns
**Factory + Strategy:** operations.py builds and executes operations dynamically.  
**Memento:** calculator_memento.py handles undo/redo by snapshotting history.  
**Observer:** history.py triggers logging and auto-save on new calculations.  
**Facade:** calculator.py exposes a simple interface while coordinating internal modules.

## Error Handling
- Invalid or non-numeric input raises ValidationError.  
- Division by zero and invalid roots raise OperationError.  
- Out-of-bounds inputs are prevented by configurable limits.  
- Directories and files are auto-created when missing.

## Testing & CI
All 20 tests pass successfully.  
Coverage achieved: **91.11%**.  
Continuous integration enforces coverage >= 90% and runs pytest automatically for all branches and pull requests.

## Reflection
This midterm project demonstrated full-cycle software development practices—using design patterns, environment-based configuration, structured logging, and disciplined version control. Building the calculator as modular components clarified the value of test-driven design. Achieving high coverage ensured reliability and maintainability. Incremental commits, consistent documentation, and continuous integration mirrored professional engineering workflows and emphasized quality at every stage.
