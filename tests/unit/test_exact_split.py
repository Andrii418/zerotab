from decimal import Decimal

import pytest

from app.exceptions import InvalidSplitError
from app.strategies.exact import ExactAmountSplitStrategy


def test_split_returns_given_amounts_when_they_match_total():
    # Arrange
    strategy = ExactAmountSplitStrategy({1: Decimal(60), 2: Decimal(40)})

    # Act
    result = strategy.split(Decimal("100.00"))

    # Assert
    assert result == {1: Decimal("60.00"), 2: Decimal("40.00")}


def test_split_rejects_amounts_not_matching_total():
    # Arrange
    strategy = ExactAmountSplitStrategy({1: Decimal(60), 2: Decimal(30)})

    # Act
    action = lambda: strategy.split(Decimal("100.00"))

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


def test_constructor_rejects_negative_amount():
    # Arrange
    amounts = {1: Decimal(110), 2: Decimal(-10)}

    # Act
    action = lambda: ExactAmountSplitStrategy(amounts)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


def test_constructor_rejects_empty_amounts():
    # Arrange
    amounts: dict[int, Decimal] = {}

    # Act
    action = lambda: ExactAmountSplitStrategy(amounts)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()