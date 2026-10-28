from collections import defaultdict

from app.models import Expense


def calculate_balances(expenses: list[Expense]) -> dict[int, int]:
    balances: dict[int, int] = defaultdict(int)
    for expense in expenses:
        balances[expense.payer_id] += expense.amount_cents
        for share in expense.shares:
            balances[share.person_id] -= share.amount_cents
    return dict(balances)