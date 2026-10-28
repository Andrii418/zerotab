import heapq
from dataclasses import dataclass

from app.exceptions import InvalidBalancesError


@dataclass(frozen=True)
class Transfer:
    payer_id: int
    receiver_id: int
    amount_cents: int


def minimize_transfers(balances: dict[int, int]) -> list[Transfer]:
    if sum(balances.values()) != 0:
        raise InvalidBalancesError("Balances must sum to zero")

    creditors = [(-amount, person_id) for person_id, amount in balances.items() if amount > 0]
    debtors = [(amount, person_id) for person_id, amount in balances.items() if amount < 0]
    heapq.heapify(creditors)
    heapq.heapify(debtors)

    transfers: list[Transfer] = []
    while creditors and debtors:
        negative_credit, creditor_id = heapq.heappop(creditors)
        negative_debt, debtor_id = heapq.heappop(debtors)
        credit, debt = -negative_credit, -negative_debt
        amount = min(credit, debt)
        transfers.append(Transfer(debtor_id, creditor_id, amount))
        if credit > amount:
            heapq.heappush(creditors, (-(credit - amount), creditor_id))
        if debt > amount:
            heapq.heappush(debtors, (-(debt - amount), debtor_id))
    return transfers