from decimal import Decimal

import pytest

from app.strategies.equal import EqualSplitStrategy
from app.strategies.exact import ExactAmountSplitStrategy
from app.strategies.factory import SplitType, create_split_strategy
from app.strategies.percentage import PercentageSplitStrategy


@pytest.mark.parametrize(
    ("split_type", "shares", "expected_class"),
    [
        (SplitType.EQUAL, {1: Decimal(1), 2: Decimal(1)}, EqualSplitStrategy),
        (SplitType.PERCENTAGE, {1: Decimal(60), 2: Decimal(40)}, PercentageSplitStrategy),
        (SplitType.EXACT, {1: Decimal(6), 2: Decimal(4)}, ExactAmountSplitStrategy),
    ],
)
def test_create_split_strategy_returns_matching_strategy(split_type, shares, expected_class):
    # Arrange
    requested_type = split_type

    # Act
    strategy = create_split_strategy(requested_type, shares)

    # Assert
    assert isinstance(strategy, expected_class)

def test_create_equal_strategy_uses_only_participant_ids():
    # Arrange
    shares = {1: Decimal(5), 2: Decimal(99)}

    # Act
    result = create_split_strategy(SplitType.EQUAL, shares).split(Decimal("10.00"))

    # Assert
    assert result == {1: Decimal("5.00"), 2: Decimal("5.00")}

def test_split_type_is_parsed_from_string_value():
    # Arrange
    raw_value = "percentage"

    # Act
    split_type = SplitType(raw_value)

    # Assert
    assert split_type is SplitType.PERCENTAGE

def test_split_type_rejects_unknown_value():
    # Arrange
    raw_value = "weighted"

    # Act
    action = lambda: SplitType(raw_value)

    # Assert
    with pytest.raises(ValueError):
        action()