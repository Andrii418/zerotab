from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.group import ExpenseGroup
from app.models.person import Person
from app.money import from_cents


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("expense_groups.id"))
    payer_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    description: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50), default="other")
    amount_cents: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    group: Mapped[ExpenseGroup] = relationship(back_populates="expenses")
    payer: Mapped[Person] = relationship()
    shares: Mapped[list["ExpenseShare"]] = relationship(
        back_populates="expense", cascade="all, delete-orphan"
    )

    @property
    def amount(self) -> Decimal:
        return from_cents(self.amount_cents)


class ExpenseShare(Base):
    __tablename__ = "expense_shares"

    id: Mapped[int] = mapped_column(primary_key=True)
    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    amount_cents: Mapped[int]

    expense: Mapped[Expense] = relationship(back_populates="shares")
    person: Mapped[Person] = relationship()

    @property
    def amount(self) -> Decimal:
        return from_cents(self.amount_cents)