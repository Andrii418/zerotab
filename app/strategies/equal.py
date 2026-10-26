from decimal import Decimal

from app.exceptions import InvalidSplitError
from app.money import from_cents, to_cents
from app.strategies.base import SplitStrategy


class EqualSplitStrategy(SplitStrategy):
    def __init__(self, participant_ids: list[int]) -> None:
        if not participant_ids:
            raise InvalidSplitError("At least one participant is required")
        if len(set(participant_ids)) != len(participant_ids):
            raise InvalidSplitError("Participants must be unique")
        self._participant_ids = participant_ids

    def _calculate(self, total: Decimal) -> dict[int, Decimal]:
        base_cents, remainder = divmod(to_cents(total), len(self._participant_ids))
        return {
            participant_id: from_cents(base_cents + (1 if index < remainder else 0))
            for index, participant_id in enumerate(self._participant_ids)
        }