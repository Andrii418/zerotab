from decimal import Decimal

from pydantic import BaseModel


class BalanceRead(BaseModel):
    person_id: int
    amount: Decimal


class TransferRead(BaseModel):
    payer_id: int
    receiver_id: int
    amount: Decimal