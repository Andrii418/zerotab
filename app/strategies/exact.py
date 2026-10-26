from decimal import Decimal

from app.exceptions import InvalidSplitError
from app.money import to_money
from app.strategies.base import SplitStrategy


class ExactAmountSplitStrategy(SplitStrategy):
    def __init__(self, amounts: dict[int, Decimal]) -> None:
        if not amounts:
            raise InvalidSplitError("At least one participant is required")
        if any(amount < 0 for amount in amounts.values()):
            raise InvalidSplitError("Amounts must not be negative")
        self._amounts = {participant_id: to_money(amount) for participant_id, amount in amounts.items()}

    def _calculate(self, total: Decimal) -> dict[int, Decimal]:
        if sum(self._amounts.values()) != total:
            raise InvalidSplitError("Amounts must sum to the total")
        return dict(self._amounts)