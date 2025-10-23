from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal, getcontext

class Operation(ABC):
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal: ...

    def __str__(self) -> str:  # pragma: no cover (stringly)
        return self.__class__.__name__

class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b

class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b

class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b

class Division(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

class Power(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a ** int(b)

class Root(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ZeroDivisionError("zero root")
        # nth root => a ** (1/b)
        getcontext().prec += 4
        result = a.__pow__(Decimal(1) / b)
        getcontext().prec -= 4
        return result

class Modulus(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ZeroDivisionError("mod by zero")
        return a % b

class IntDivide(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ZeroDivisionError("int divide by zero")
        return (a // b)

class Percent(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ZeroDivisionError("percent of zero base")
        return (a / b) * Decimal(100)

class AbsDiff(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return abs(a - b)

FACTORY = {
    "add": Addition,
    "subtract": Subtraction,
    "multiply": Multiplication,
    "divide": Division,
    "power": Power,
    "root": Root,
    "modulus": Modulus,
    "int_divide": IntDivide,
    "percent": Percent,
    "abs_diff": AbsDiff,
}

def get_operation(name: str) -> Operation:
    cls = FACTORY.get(name.lower())
    if not cls:
        raise ValueError(f"unknown operation: {name}")
    return cls()
