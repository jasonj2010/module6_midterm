from dataclasses import dataclass, asdict
from decimal import Decimal
from datetime import datetime

@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal
    timestamp: datetime

    def to_dict(self) -> dict:
        d = asdict(self)
        d["operand1"] = str(self.operand1)
        d["operand2"] = str(self.operand2)
        d["result"] = str(self.result)
        d["timestamp"] = self.timestamp.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Calculation":
        return cls(
            operation=d["operation"],
            operand1=Decimal(str(d["operand1"])),
            operand2=Decimal(str(d["operand2"])),
            result=Decimal(str(d["result"])),
            timestamp=datetime.fromisoformat(str(d["timestamp"])),
        )
