from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.strategies.factory import SplitType


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    payer_id: int
    description: str = Field(min_length=1, max_length=200)
    category: str = Field(default="other", min_length=1, max_length=50)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    split_type: SplitType
    shares: dict[int, Decimal]


class ShareRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_id: int
    amount: Decimal


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    payer_id: int
    description: str
    category: str
    amount: Decimal
    created_at: datetime
    shares: list[ShareRead]