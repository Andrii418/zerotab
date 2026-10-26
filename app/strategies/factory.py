from collections.abc import Callable
from decimal import Decimal
from enum import Enum

from app.strategies.base import SplitStrategy
from app.strategies.equal import EqualSplitStrategy
from app.strategies.exact import ExactAmountSplitStrategy
from app.strategies.percentage import PercentageSplitStrategy


class SplitType(str, Enum):
    EQUAL = "equal"
    PERCENTAGE = "percentage"
    EXACT = "exact"


StrategyBuilder = Callable[[dict[int, Decimal]], SplitStrategy]

_BUILDERS: dict[SplitType, StrategyBuilder] = {
    SplitType.EQUAL: lambda shares: EqualSplitStrategy(list(shares)),
    SplitType.PERCENTAGE: PercentageSplitStrategy,
    SplitType.EXACT: ExactAmountSplitStrategy,
}


def create_split_strategy(split_type: SplitType, shares: dict[int, Decimal]) -> SplitStrategy:
    return _BUILDERS[split_type](shares)