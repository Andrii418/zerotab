from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Expense


class ExpenseRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, expense: Expense) -> Expense:
        self._session.add(expense)
        self._session.commit()
        return expense

    def get(self, expense_id: int) -> Expense | None:
        return self._session.get(Expense, expense_id)

    def list_by_group(self, group_id: int) -> list[Expense]:
        statement = (
            select(Expense)
            .where(Expense.group_id == group_id)
            .order_by(Expense.created_at.desc())
        )
        return list(self._session.scalars(statement))

    def delete(self, expense: Expense) -> None:
        self._session.delete(expense)
        self._session.commit()