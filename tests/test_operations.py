from decimal import Decimal
from app.operations import get_operation

def test_add():
    op = get_operation("add")
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("5")
