# Module 6 Midterm - Advanced Calculator

## Overview
This project is a full-featured command-line calculator that demonstrates multiple object-oriented design patterns and CI/CD integration. The application performs advanced arithmetic operations, maintains an undo/redo history using the Memento Pattern, logs and auto-saves results using the Observer Pattern, and supports configuration management through .env variables. Continuous Integration via GitHub Actions enforces a minimum 90% test coverage.

## Features
- Factory Pattern for dynamic operation creation  
- Memento Pattern for undo/redo history management  
- Observer Pattern with Logging and AutoSave observers  
- Configuration Management through .env and environment variables  
- Comprehensive Logging with Python’s logging module  
- Data Persistence of calculation history via pandas (CSV)  
- Command-Line REPL supporting arithmetic operations and history control  
- Continuous Integration workflow enforcing coverage ≥ 90%  
- Test Coverage: 93% (22 tests passed)

## Directory Structure
module6_midterm/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── operations.py
│   ├── logger.py
│   └── calculator_repl.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculator_extras.py
│   ├── test_observers.py
│   ├── test_operations.py
│   └── ...
├── .env.example
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── python-app.yml

## Installation
1. Clone the repository  
   git clone <your-repo-url>  
   cd module6_midterm  

2. Create a virtual environment  
   python -m venv venv  
   source venv/Scripts/activate  (Windows)  
   source venv/bin/activate      (macOS/Linux)  

3. Install dependencies  
   pip install -r requirements.txt  

## Configuration
Copy .env.example to .env and adjust as needed:  
CALCULATOR_LOG_DIR=./logs  
CALCULATOR_HISTORY_DIR=./history  
CALCULATOR_MAX_HISTORY_SIZE=100  
CALCULATOR_AUTO_SAVE=true  
CALCULATOR_PRECISION=6  
CALCULATOR_MAX_INPUT_VALUE=1000000000000  
CALCULATOR_DEFAULT_ENCODING=utf-8  

Ensure .env is included in .gitignore to protect configuration values.

## Usage
Start the calculator’s REPL interface:  
python -m app.calculator_repl  

### Supported Commands
add, subtract, multiply, divide – Basic arithmetic  
power – Exponentiation  
root – nth root calculation  
modulus – Remainder of division  
int_divide – Integer division  
percent – (a / b) × 100  
abs_diff – Absolute difference  
undo / redo – Revert or reapply last calculation  
history – Show past operations  
clear – Clear history  
save / load – Manually save or load history  
help – Display command list  
exit – Quit the program  

### Example Session
add 4 9  
power 2 8  
percent 25 200  
history  
undo  
redo  
save  
exit  

## Testing
Run the full test suite with coverage:  
pytest  

Generate detailed coverage report:  
pytest --cov=app --cov-report=html  

Coverage reports are written to htmlcov/index.html.  

Latest Local Results:  
22 passed, 0 failed  
Total coverage: 93%  

## Continuous Integration (GitHub Actions)
A workflow in .github/workflows/python-app.yml automatically:  
- Checks out the repository  
- Installs dependencies  
- Runs all tests with pytest  
- Enforces minimum 90% coverage  

Example step:  
Run tests with pytest and enforce 90% coverage  
pytest --cov=app --cov-fail-under=90  

## Design Patterns Implemented
- Factory Pattern: Creates operation objects dynamically  
- Memento Pattern: Enables undo/redo of calculation history  
- Observer Pattern: LoggingObserver and AutoSaveObserver respond to events  
- Decorator/Command Pattern (optional): Extensible for extra credit  

## Logging and History
- Logs are stored in the directory defined by CALCULATOR_LOG_DIR.  
- Calculation history is persisted as a CSV file (history/calculator_history.csv).  
- Auto-saving occurs automatically when CALCULATOR_AUTO_SAVE=true.  
