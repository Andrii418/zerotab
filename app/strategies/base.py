from abc import ABC, abstractmethod
from decimal import Decimal


class SplitStrategy(ABC):
    @abstractmethod
    def split(self, total: Decimal) -> dict[int, Decimal]:
        ...