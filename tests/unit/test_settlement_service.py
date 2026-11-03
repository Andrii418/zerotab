from unittest.mock import MagicMock

import pytest

from app.repositories.expense_repository import ExpenseRepository
from app.services.settlement import Transfer
from app.services.settlement_service import SettlementService
from tests.builders import build_expense


@pytest.fixture
def expense_repository():
    return MagicMock(spec=ExpenseRepository)


@pytest.fixture
def service(expense_repository):
    return SettlementService(expense_repository)


def test_get_balances_sums_expenses_of_group(service, expense_repository):
    # Arrange
    expense_repository.list_by_group.return_value = [
        build_expense(1, 9000, {1: 3000, 2: 3000, 3: 3000}),
        build_expense(2, 3000, {1: 1000, 2: 1000, 3: 1000}),
    ]

    # Act
    balances = service.get_balances(7)

    # Assert
    assert balances == {1: 5000, 2: -1000, 3: -4000}
    expense_repository.list_by_group.assert_called_once_with(7)


def test_get_balances_returns_empty_dict_for_group_without_expenses(service, expense_repository):
    # Arrange
    expense_repository.list_by_group.return_value = []

    # Act
    balances = service.get_balances(1)

    # Assert
    assert balances == {}


def test_get_transfers_returns_minimal_settlement(service, expense_repository):
    # Arrange
    expense_repository.list_by_group.return_value = [
        build_expense(1, 9000, {1: 3000, 2: 3000, 3: 3000}),
        build_expense(2, 3000, {1: 1000, 2: 1000, 3: 1000}),
    ]

    # Act
    transfers = service.get_transfers(1)

    # Assert
    assert set(transfers) == {
        Transfer(payer_id=3, receiver_id=1, amount_cents=4000),
        Transfer(payer_id=2, receiver_id=1, amount_cents=1000),
    }


def test_get_transfers_returns_no_transfers_when_everyone_paid_own_share(service, expense_repository):
    # Arrange
    expense_repository.list_by_group.return_value = [build_expense(1, 1000, {1: 1000})]

    # Act
    transfers = service.get_transfers(1)

    # Assert
    assert transfers == []