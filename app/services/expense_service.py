from decimal import Decimal

from app.exceptions import EntityNotFoundError, InvalidExpenseError
from app.models import Expense, ExpenseShare
from app.money import to_cents, to_money
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.group_repository import GroupRepository
from app.strategies.factory import SplitType, create_split_strategy


class ExpenseService:
    def __init__(self, expense_repository: ExpenseRepository, group_repository: GroupRepository) -> None:
        self._expenses = expense_repository
        self._groups = group_repository

    def add_expense(
        self,
        group_id: int,
        payer_id: int,
        description: str,
        category: str,
        amount: Decimal,
        split_type: SplitType,
        shares: dict[int, Decimal],
    ) -> Expense:
        group = self._groups.get(group_id)
        if group is None:
            raise EntityNotFoundError(f"Group {group_id} not found")
        if not description.strip():
            raise InvalidExpenseError("Description must not be blank")

        member_ids = {member.id for member in group.members}
        if payer_id not in member_ids:
            raise InvalidExpenseError("Payer must be a member of the group")
        if not set(shares) <= member_ids:
            raise InvalidExpenseError("All participants must be members of the group")

        total = to_money(amount)
        amounts = create_split_strategy(split_type, shares).split(total)
        expense = Expense(
            group_id=group_id,
            payer_id=payer_id,
            description=description.strip(),
            category=category,
            amount_cents=to_cents(total),
            shares=[
                ExpenseShare(person_id=person_id, amount_cents=to_cents(share))
                for person_id, share in amounts.items()
            ],
        )
        return self._expenses.add(expense)

    def list_expenses(self, group_id: int) -> list[Expense]:
        return self._expenses.list_by_group(group_id)

    def delete_expense(self, expense_id: int) -> None:
        expense = self._expenses.get(expense_id)
        if expense is None:
            raise EntityNotFoundError(f"Expense {expense_id} not found")
        self._expenses.delete(expense)