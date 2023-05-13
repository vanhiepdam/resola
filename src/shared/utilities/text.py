import string
import uuid
from random import SystemRandom
from typing import Union

DEFAULT_RANDOM_TEXT = string.ascii_lowercase + string.ascii_uppercase + string.digits
DEFAULT_RANDOM_TEXT_UPPER_CASE = string.ascii_uppercase + string.digits
DEFAULT_RANDOM_NUMBERS = string.digits


class TextUtil:
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def generate_random_text(
        length: int = 10, choices: Union[list[str], str] = DEFAULT_RANDOM_TEXT
    ) -> str:
        return "".join((SystemRandom().choice(choices) for _ in range(length)))

    @staticmethod
    def generate_random_string_of_numbers(length: int = 10) -> str:
        return TextUtil.generate_random_text(length=length, choices=DEFAULT_RANDOM_NUMBERS)
