from decimal import Decimal
from random import SystemRandom
from typing import Optional, Union


class NumberUtil:
    @staticmethod
    def to_decimal(value: Union[str, int, float]) -> Decimal:
        return Decimal(str(value))

    @staticmethod
    def generate_random_number(_from: int, _to: Optional[int] = None) -> int:
        """
        :param _from: start of range
        :param _to: end of range. If none, result will be below _from.
        Can not use negative _from with _to = None
        :return: integer
        """
        return SystemRandom().randrange(start=_from, stop=_to)
