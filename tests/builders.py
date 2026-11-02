from app.models import Expense, ExpenseGroup, ExpenseShare, Person


def build_group(group_id: int = 1, member_ids: tuple[int, ...] = (1, 2, 3)) -> ExpenseGroup:
    members = [Person(id=person_id, name=f"Person {person_id}") for person_id in member_ids]
    return ExpenseGroup(id=group_id, name="Trip", members=members)


def build_expense(payer_id: int, amount_cents: int, shares: dict[int, int]) -> Expense:
    return Expense(
        payer_id=payer_id,
        amount_cents=amount_cents,
        shares=[ExpenseShare(person_id=person_id, amount_cents=cents) for person_id, cents in shares.items()],
    )