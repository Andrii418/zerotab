from fastapi import Request, status
from fastapi.responses import HTMLResponse

from app.repositories.person_repository import PersonRepository
from app.services.expense_service import ExpenseService
from app.services.group_service import GroupService
from app.services.settlement_service import SettlementService
from app.strategies.factory import SplitType
from app.web.presenters import build_balance_rows, build_transfer_rows
from app.web.templating import templates


class GroupPage:
    def __init__(
        self,
        groups: GroupService,
        expenses: ExpenseService,
        settlement: SettlementService,
        people: PersonRepository,
    ) -> None:
        self._groups = groups
        self._expenses = expenses
        self._settlement = settlement
        self._people = people

    def render(self, request: Request, group_id: int, error: str | None = None) -> HTMLResponse:
        group = self._groups.get_group(group_id)
        names = {member.id: member.name for member in group.members}
        context = {
            "group": group,
            "available_people": [p for p in self._people.list_all() if p.id not in names],
            "expenses": self._expenses.list_expenses(group_id),
            "balances": build_balance_rows(self._settlement.get_balances(group_id), names),
            "transfers": build_transfer_rows(self._settlement.get_transfers(group_id), names),
            "split_types": list(SplitType),
            "error": error,
        }
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT if error else status.HTTP_200_OK
        return templates.TemplateResponse(request, "group.html", context, status_code=status_code)