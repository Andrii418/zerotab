from dataclasses import dataclass
from decimal import Decimal

from app.money import from_cents
from app.services.settlement import Transfer


@dataclass(frozen=True)
class BalanceRow:
    person_name: str
    amount: Decimal


@dataclass(frozen=True)
class TransferRow:
    payer_name: str
    receiver_name: str
    amount: Decimal


def build_balance_rows(balances: dict[int, int], names: dict[int, str]) -> list[BalanceRow]:
    return [
        BalanceRow(person_name=name, amount=from_cents(balances.get(person_id, 0)))
        for person_id, name in names.items()
    ]


def build_transfer_rows(transfers: list[Transfer], names: dict[int, str]) -> list[TransferRow]:
    return [
        TransferRow(
            payer_name=names[transfer.payer_id],
            receiver_name=names[transfer.receiver_id],
            amount=from_cents(transfer.amount_cents),
        )
        for transfer in transfers
    ]