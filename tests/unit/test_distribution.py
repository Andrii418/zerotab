from decimal import Decimal

import pytest

from app.strategies.distribution import distribute_cents


def test_distribute_gives_leftover_cent_to_largest_remainder():
    # Arrange
    weights = {1: Decimal(50), 2: Decimal(30), 3: Decimal(20)}

    # Act
    result = distribute_cents(10001, weights)

    # Assert
    assert result == {1: 5001, 2: 3000, 3: 2000}

def test_distribute_equal_weights_spreads_single_leftover_cent():
    # Arrange
    weights = {1: Decimal(1), 2: Decimal(1), 3: Decimal(1)}

    # Act
    result = distribute_cents(100, weights)

    # Assert
    assert sorted(result.values()) == [33, 33, 34]

def test_distribute_single_participant_gets_everything():
    # Arrange
    weights = {7: Decimal(100)}

    # Act
    result = distribute_cents(1234, weights)

    # Assert
    assert result == {7: 1234}

@pytest.mark.parametrize("total_cents", [1, 2, 99, 100, 101, 9999, 123457])
def test_distribute_shares_always_sum_to_total(total_cents):
    # Arrange
    weights = {1: Decimal("33.33"), 2: Decimal("33.33"), 3: Decimal("33.34")}

    # Act
    result = distribute_cents(total_cents, weights)

    # Assert
    assert sum(result.values()) == total_cents