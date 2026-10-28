from app.repositories.expense_repository import ExpenseRepository
from app.services.balance_calculator import calculate_balances
from app.services.settlement import Transfer, minimize_transfers


class SettlementService:
    def __init__(self, expense_repository: ExpenseRepository) -> None:
        self._expenses = expense_repository

    def get_balances(self, group_id: int) -> dict[int, int]:
        return calculate_balances(self._expenses.list_by_group(group_id))

    def get_transfers(self, group_id: int) -> list[Transfer]:
        return minimize_transfers(self.get_balances(group_id))