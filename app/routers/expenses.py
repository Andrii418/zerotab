from fastapi import APIRouter, status

from app.dependencies import ExpenseServiceDep
from app.models import Expense
from app.schemas.expense import ExpenseCreate, ExpenseRead

router = APIRouter(tags=["expenses"])


@router.post(
    "/groups/{group_id}/expenses",
    response_model=ExpenseRead,
    status_code=status.HTTP_201_CREATED,
)
def add_expense(group_id: int, payload: ExpenseCreate, service: ExpenseServiceDep) -> Expense:
    return service.add_expense(
        group_id=group_id,
        payer_id=payload.payer_id,
        description=payload.description,
        category=payload.category,
        amount=payload.amount,
        split_type=payload.split_type,
        shares=payload.shares,
    )


@router.get("/groups/{group_id}/expenses", response_model=list[ExpenseRead])
def list_expenses(group_id: int, service: ExpenseServiceDep) -> list[Expense]:
    return service.list_expenses(group_id)


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, service: ExpenseServiceDep) -> None:
    service.delete_expense(expense_id)