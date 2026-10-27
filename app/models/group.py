from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.person import Person

if TYPE_CHECKING:
    from app.models.expense import Expense

group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", ForeignKey("expense_groups.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True),
)


class ExpenseGroup(Base):
    __tablename__ = "expense_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    members: Mapped[list[Person]] = relationship(secondary=group_members)
    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )