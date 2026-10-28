from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ExpenseGroup, Person


class GroupRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, name: str, members: list[Person]) -> ExpenseGroup:
        group = ExpenseGroup(name=name, members=members)
        self._session.add(group)
        self._session.commit()
        return group

    def get(self, group_id: int) -> ExpenseGroup | None:
        return self._session.get(ExpenseGroup, group_id)

    def list_all(self) -> list[ExpenseGroup]:
        return list(self._session.scalars(select(ExpenseGroup).order_by(ExpenseGroup.name)))

    def add_member(self, group: ExpenseGroup, person: Person) -> None:
        if person not in group.members:
            group.members.append(person)
            self._session.commit()

    def delete(self, group: ExpenseGroup) -> None:
        self._session.delete(group)
        self._session.commit()