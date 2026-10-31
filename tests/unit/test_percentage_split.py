from decimal import Decimal

import pytest

from app.exceptions import InvalidSplitError
from app.strategies.percentage import PercentageSplitStrategy


def test_split_divides_total_by_percentages():
    # Arrange
    strategy = PercentageSplitStrategy({1: Decimal(50), 2: Decimal(30), 3: Decimal(20)})

    # Act
    result = strategy.split(Decimal("100.00"))

    # Assert
    assert result == {1: Decimal("50.00"), 2: Decimal("30.00"), 3: Decimal("20.00")}


def test_split_gives_leftover_cent_to_largest_remainder():
    # Arrange
    strategy = PercentageSplitStrategy({1: Decimal(50), 2: Decimal(30), 3: Decimal(20)})

    # Act
    result = strategy.split(Decimal("100.01"))

    # Assert
    assert result == {1: Decimal("50.01"), 2: Decimal("30.00"), 3: Decimal("20.00")}


def test_split_shares_sum_to_total_with_uneven_percentages():
    # Arrange
    percentages = {1: Decimal("33.33"), 2: Decimal("33.33"), 3: Decimal("33.34")}
    strategy = PercentageSplitStrategy(percentages)

    # Act
    result = strategy.split(Decimal("10.00"))

    # Assert
    assert result == {1: Decimal("3.33"), 2: Decimal("3.33"), 3: Decimal("3.34")}
    assert sum(result.values()) == Decimal("10.00")


def test_constructor_rejects_percentages_not_summing_to_hundred():
    # Arrange
    percentages = {1: Decimal(50), 2: Decimal(30)}

    # Act
    action = lambda: PercentageSplitStrategy(percentages)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


@pytest.mark.parametrize("invalid_value", ["0", "-10"])
def test_constructor_rejects_non_positive_percentage(invalid_value):
    # Arrange
    percentages = {1: Decimal(invalid_value), 2: Decimal(100)}

    # Act
    action = lambda: PercentageSplitStrategy(percentages)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


def test_constructor_rejects_empty_percentages():
    # Arrange
    percentages: dict[int, Decimal] = {}

    # Act
    action = lambda: PercentageSplitStrategy(percentages)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()