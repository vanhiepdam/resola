# -*- coding: utf-8 -*-
from enum import Enum
from typing import Any


class ConstantEnum(Enum):
    @classmethod
    def get_choices(cls) -> list[tuple[Any, Any]]:
        return [(tag.value, tag.name) for tag in cls]
