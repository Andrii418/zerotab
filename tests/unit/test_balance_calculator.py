from app.models import Expense, ExpenseShare
from app.services.balance_calculator import calculate_balances


def build_expense(payer_id: int, amount_cents: int, shares: dict[int, int]) -> Expense:
    return Expense(
        payer_id=payer_id,
        amount_cents=amount_cents,
        shares=[ExpenseShare(person_id=person_id, amount_cents=cents) for person_id, cents in shares.items()],
    )

def test_calculate_balances_returns_empty_dict_without_expenses():
    # Arrange
    expenses: list[Expense] = []

    # Act
    result = calculate_balances(expenses)

    # Assert
    assert result == {}

def test_calculate_balances_credits_payer_and_debits_participants():
    # Arrange
    expense = build_expense(1, 10000, {1: 3334, 2: 3333, 3: 3333})

    # Act
    result = calculate_balances([expense])

    # Assert
    assert result == {1: 6666, 2: -3333, 3: -3333}

def test_calculate_balances_accumulates_multiple_expenses():
    # Arrange
    hotel = build_expense(1, 9000, {1: 3000, 2: 3000, 3: 3000})
    taxi = build_expense(2, 3000, {1: 1000, 2: 1000, 3: 1000})

    # Act
    result = calculate_balances([hotel, taxi])

    # Assert
    assert result == {1: 5000, 2: -1000, 3: -4000}

def test_calculate_balances_payer_covering_only_own_share_has_zero_balance():
    # Arrange
    expense = build_expense(1, 1000, {1: 1000})

    # Act
    result = calculate_balances([expense])

    # Assert
    assert result == {1: 0}

def test_calculate_balances_payer_outside_split_is_fully_credited():
    # Arrange
    expense = build_expense(1, 1000, {2: 1000})

    # Act
    result = calculate_balances([expense])

    # Assert
    assert result == {1: 1000, 2: -1000}

def test_calculate_balances_always_sum_to_zero():
    # Arrange
    expenses = [
        build_expense(1, 10001, {1: 3334, 2: 3334, 3: 3333}),
        build_expense(3, 777, {2: 400, 3: 377}),
        build_expense(2, 5000, {1: 5000}),
    ]

    # Act
    result = calculate_balances(expenses)

    # Assert
    assert sum(result.values()) == 0
