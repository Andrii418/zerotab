import pytest

from app.exceptions import InvalidBalancesError
from app.services.settlement import Transfer, minimize_transfers

BALANCE_SCENARIOS = [
    {1: 5000, 2: -2000, 3: -3000, 4: 1000, 5: -1000},
    {1: 100, 2: 100, 3: -200},
    {1: 1, 2: 1, 3: 1, 4: -3},
    {1: 7000, 2: -2500, 3: -2500, 4: -2000},
]


def count_non_zero(balances: dict[int, int]) -> int:
    return sum(1 for amount in balances.values() if amount != 0)


def test_minimize_transfers_returns_empty_list_for_empty_balances():
    # Arrange
    balances: dict[int, int] = {}

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert result == []


def test_minimize_transfers_returns_empty_list_when_everyone_is_settled():
    # Arrange
    balances = {1: 0, 2: 0, 3: 0}

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert result == []


def test_minimize_transfers_creates_single_transfer_for_two_people():
    # Arrange
    balances = {1: 2500, 2: -2500}

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert result == [Transfer(payer_id=2, receiver_id=1, amount_cents=2500)]


def test_minimize_transfers_ignores_people_with_zero_balance():
    # Arrange
    balances = {1: 0, 2: 500, 3: -500}

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert result == [Transfer(payer_id=3, receiver_id=2, amount_cents=500)]


def test_minimize_transfers_lets_each_debtor_pay_single_creditor():
    # Arrange
    balances = {1: 6666, 2: -3333, 3: -3333}

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert set(result) == {
        Transfer(payer_id=2, receiver_id=1, amount_cents=3333),
        Transfer(payer_id=3, receiver_id=1, amount_cents=3333),
    }


def test_minimize_transfers_avoids_extra_transfers_in_larger_group():
    # Arrange
    balances = {1: 5000, 2: -2000, 3: -3000, 4: 1000, 5: -1000}

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert set(result) == {
        Transfer(payer_id=3, receiver_id=1, amount_cents=3000),
        Transfer(payer_id=2, receiver_id=1, amount_cents=2000),
        Transfer(payer_id=5, receiver_id=4, amount_cents=1000),
    }


def test_minimize_transfers_rejects_balances_not_summing_to_zero():
    # Arrange
    balances = {1: 100, 2: -50}

    # Act
    action = lambda: minimize_transfers(balances)

    # Assert
    with pytest.raises(InvalidBalancesError):
        action()


@pytest.mark.parametrize("balances", BALANCE_SCENARIOS)
def test_minimize_transfers_settles_all_balances_to_zero(balances):
    # Arrange
    remaining = dict(balances)

    # Act
    for transfer in minimize_transfers(balances):
        remaining[transfer.payer_id] += transfer.amount_cents
        remaining[transfer.receiver_id] -= transfer.amount_cents

    # Assert
    assert all(amount == 0 for amount in remaining.values())


@pytest.mark.parametrize("balances", BALANCE_SCENARIOS)
def test_minimize_transfers_uses_at_most_n_minus_one_transfers(balances):
    # Arrange
    people_involved = count_non_zero(balances)

    # Act
    result = minimize_transfers(balances)

    # Assert
    assert len(result) <= people_involved - 1