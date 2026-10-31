from decimal import Decimal

import pytest

from app.exceptions import InvalidSplitError
from app.strategies.equal import EqualSplitStrategy


def test_split_gives_extra_cent_to_first_participants():
    # Arrange
    strategy = EqualSplitStrategy([1, 2, 3])

    # Act
    result = strategy.split(Decimal("100.00"))

    # Assert
    assert result == {1: Decimal("33.34"), 2: Decimal("33.33"), 3: Decimal("33.33")}


@pytest.mark.parametrize("total", ["0.01", "10.00", "99.99", "1000.01"])
def test_split_shares_always_sum_to_total(total):
    # Arrange
    strategy = EqualSplitStrategy([1, 2, 3, 4, 5, 6, 7])

    # Act
    result = strategy.split(Decimal(total))

    # Assert
    assert sum(result.values()) == Decimal(total)


def test_split_single_participant_pays_whole_amount():
    # Arrange
    strategy = EqualSplitStrategy([5])

    # Act
    result = strategy.split(Decimal("42.50"))

    # Assert
    assert result == {5: Decimal("42.50")}


def test_split_smallest_amount_goes_to_first_participant_only():
    # Arrange
    strategy = EqualSplitStrategy([1, 2, 3])

    # Act
    result = strategy.split(Decimal("0.01"))

    # Assert
    assert result == {1: Decimal("0.01"), 2: Decimal("0.00"), 3: Decimal("0.00")}


def test_constructor_rejects_empty_participant_list():
    # Arrange
    participants: list[int] = []

    # Act
    action = lambda: EqualSplitStrategy(participants)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


def test_constructor_rejects_duplicate_participants():
    # Arrange
    participants = [1, 2, 2]

    # Act
    action = lambda: EqualSplitStrategy(participants)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


@pytest.mark.parametrize("total", ["0", "-5.00", "0.001"])
def test_split_rejects_non_positive_total(total):
    # Arrange
    strategy = EqualSplitStrategy([1, 2])

    # Act
    action = lambda: strategy.split(Decimal(total))

    # Assert
    with pytest.raises(InvalidSplitError):
        action()