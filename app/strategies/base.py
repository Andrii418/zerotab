from abc import ABC, abstractmethod
from decimal import Decimal

from app.exceptions import InvalidSplitError
from app.money import to_money


class SplitStrategy(ABC):
    def split(self, total: Decimal) -> dict[int, Decimal]:
        rounded_total = to_money(total)
        if rounded_total <= 0:
            raise InvalidSplitError("Total must be positive")
        return self._calculate(rounded_total)

    @abstractmethod
    def _calculate(self, total: Decimal) -> dict[int, Decimal]:
        ...