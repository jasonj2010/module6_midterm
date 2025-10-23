from dataclasses import dataclass
from typing import List
from app.calculation import Calculation

@dataclass
class CalculatorMemento:
    history: List[Calculation]
