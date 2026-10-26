from decimal import Decimal

from app.exceptions import InvalidSplitError
from app.money import from_cents, to_cents
from app.strategies.base import SplitStrategy
from app.strategies.distribution import distribute_cents


class PercentageSplitStrategy(SplitStrategy):
    def __init__(self, percentages: dict[int, Decimal]) -> None:
        if not percentages:
            raise InvalidSplitError("At least one participant is required")
        if any(percentage <= 0 for percentage in percentages.values()):
            raise InvalidSplitError("Percentages must be positive")
        if sum(percentages.values()) != Decimal("100"):
            raise InvalidSplitError("Percentages must sum to 100")
        self._percentages = percentages

    def _calculate(self, total: Decimal) -> dict[int, Decimal]:
        shares = distribute_cents(to_cents(total), self._percentages)
        return {participant_id: from_cents(cents) for participant_id, cents in shares.items()}