from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.exceptions import EntityNotFoundError, InvalidExpenseError, InvalidSplitError
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.group_repository import GroupRepository
from app.services.expense_service import ExpenseService
from app.strategies.factory import SplitType
from tests.builders import build_group

EVERYONE = {1: Decimal(1), 2: Decimal(1), 3: Decimal(1)}


@pytest.fixture
def expense_repository():
    repository = MagicMock(spec=ExpenseRepository)
    repository.add.side_effect = lambda expense: expense
    return repository


@pytest.fixture
def group_repository():
    repository = MagicMock(spec=GroupRepository)
    repository.get.return_value = build_group()
    return repository


@pytest.fixture
def service(expense_repository, group_repository):
    return ExpenseService(expense_repository, group_repository)


def add_expense(service, **overrides):
    arguments = {
        "group_id": 1,
        "payer_id": 1,
        "description": "Hotel",
        "category": "travel",
        "amount": Decimal("100.00"),
        "split_type": SplitType.EQUAL,
        "shares": EVERYONE,
    }
    arguments.update(overrides)
    return service.add_expense(**arguments)


def test_add_expense_saves_expense_with_cent_exact_shares(service):
    # Arrange
    amount = Decimal("100.00")

    # Act
    expense = add_expense(service, amount=amount)

    # Assert
    assert expense.amount_cents == 10000
    assert [share.amount_cents for share in expense.shares] == [3334, 3333, 3333]


def test_add_expense_passes_created_expense_to_repository(service, expense_repository):
    # Arrange
    description = "Hotel"

    # Act
    expense = add_expense(service, description=description)

    # Assert
    expense_repository.add.assert_called_once_with(expense)


def test_add_expense_trims_description(service):
    # Arrange
    description = "  Hotel  "

    # Act
    expense = add_expense(service, description=description)

    # Assert
    assert expense.description == "Hotel"


def test_add_expense_rounds_amount_to_cents(service):
    # Arrange
    amount = Decimal("10.005")

    # Act
    expense = add_expense(service, amount=amount, shares={1: Decimal(1)})

    # Assert
    assert expense.amount_cents == 1001


def test_add_expense_allows_payer_outside_split(service):
    # Arrange
    shares = {2: Decimal(1), 3: Decimal(1)}

    # Act
    expense = add_expense(service, payer_id=1, amount=Decimal("10.00"), shares=shares)

    # Assert
    assert expense.payer_id == 1
    assert [share.person_id for share in expense.shares] == [2, 3]
    assert [share.amount_cents for share in expense.shares] == [500, 500]


def test_add_expense_rejects_unknown_group(service, group_repository):
    # Arrange
    group_repository.get.return_value = None

    # Act
    action = lambda: add_expense(service, group_id=42)

    # Assert
    with pytest.raises(EntityNotFoundError):
        action()


@pytest.mark.parametrize("description", ["", "   "])
def test_add_expense_rejects_blank_description(service, description):
    # Arrange
    blank_description = description

    # Act
    action = lambda: add_expense(service, description=blank_description)

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()


def test_add_expense_rejects_payer_outside_group(service):
    # Arrange
    outsider_id = 99

    # Act
    action = lambda: add_expense(service, payer_id=outsider_id)

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()


def test_add_expense_rejects_participant_outside_group(service):
    # Arrange
    shares = {1: Decimal(1), 99: Decimal(1)}

    # Act
    action = lambda: add_expense(service, shares=shares)

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()


def test_add_expense_does_not_save_when_split_is_invalid(service, expense_repository):
    # Arrange
    shares = {1: Decimal(50), 2: Decimal(30)}

    # Act
    action = lambda: add_expense(service, split_type=SplitType.PERCENTAGE, shares=shares)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()
    expense_repository.add.assert_not_called()


def test_list_expenses_returns_expenses_of_group(service, expense_repository):
    # Arrange
    stored_expenses = [MagicMock(), MagicMock()]
    expense_repository.list_by_group.return_value = stored_expenses

    # Act
    result = service.list_expenses(1)

    # Assert
    assert result == stored_expenses
    expense_repository.list_by_group.assert_called_once_with(1)


def test_delete_expense_removes_existing_expense(service, expense_repository):
    # Arrange
    stored_expense = MagicMock()
    expense_repository.get.return_value = stored_expense

    # Act
    service.delete_expense(5)

    # Assert
    expense_repository.delete.assert_called_once_with(stored_expense)


def test_delete_expense_rejects_unknown_expense(service, expense_repository):
    # Arrange
    expense_repository.get.return_value = None

    # Act
    action = lambda: service.delete_expense(5)

    # Assert
    with pytest.raises(EntityNotFoundError):
        action()
    expense_repository.delete.assert_not_called()