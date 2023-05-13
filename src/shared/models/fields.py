from decimal import Decimal

from django.db import models


class MoneyField(models.DecimalField):
    DEFAULT_MAX_DIGITS = 20
    DEFAULT_DECIMAL_PLACES = 6
    DEFAULT_VALUE = Decimal("0.000000")

    def __init__(self, verbose_name=None, name=None, **kwargs):  # type: ignore
        if "max_digits" not in kwargs:
            kwargs["max_digits"] = self.DEFAULT_MAX_DIGITS
        if "decimal_places" not in kwargs:
            kwargs["decimal_places"] = self.DEFAULT_DECIMAL_PLACES
        if "default" not in kwargs:
            kwargs["default"] = self.DEFAULT_VALUE
        super().__init__(verbose_name, name, **kwargs)
