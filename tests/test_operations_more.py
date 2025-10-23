import math
import pytest

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError

@pytest.fixture
def calc():
    return Calculator()

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 8),           # power
    (9, 2, 3),           # root (square root of 9)
    (10, 3, 1),          # modulus
    (7, 2, 3),           # int_divide
    (50, 200, 25),       # percent: (50/200)*100
    (5, 9, 4),           # abs_diff: |5-9|
])
def test_extended_operations(calc, a, b, expected):
    # op names map to your factory strings; adjust if you used different labels
    mapping = {
        (2,3,8): "power",
        (9,2,3): "root",
        (10,3,1): "modulus",
        (7,2,3): "int_divide",
        (50,200,25): "percent",
        (5,9,4): "abs_diff",
    }
    op = mapping[(a,b,expected)]
    result = calc.perform(op, a, b)
    # For root, allow float closeness
    if op == "root":
        assert math.isclose(result, expected, rel_tol=1e-9)
    else:
        assert result == expected

@pytest.mark.parametrize("a,b", [
    (1, 0),      # divide by zero
    (10, 0),     # int_divide by zero
    (10, 0),     # modulus by zero
])
def test_zero_division_like(calc, a, b):
    # Map to relevant ops and assert they raise
    with pytest.raises(OperationError):
        calc.perform("divide", a, b)
    with pytest.raises(OperationError):
        calc.perform("int_divide", a, b)
    with pytest.raises(OperationError):
        calc.perform("modulus", a, b)

@pytest.mark.parametrize("a,b", [
    ("x", 2),
    (2, "y"),
    ("foo", "bar"),
])
def test_validation_errors(calc, a, b):
    with pytest.raises(ValidationError):
        calc.perform("add", a, b)
