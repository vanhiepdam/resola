# type: ignore
import uuid

from shared.utilities.text import DEFAULT_RANDOM_NUMBERS, DEFAULT_RANDOM_TEXT, TextUtil


class TestTextUtil:
    def test_success__generate_uuid(self):
        # action
        result = TextUtil.generate_uuid()

        # assert
        test = uuid.UUID(result)
        assert isinstance(test, uuid.UUID)

    def test_success__generate_random_text__without_choices(self):
        # arrange
        length = 10

        # action
        result = TextUtil.generate_random_text(length=length)

        # assert
        assert len(result) == length
        assert set(list(result)).issubset(DEFAULT_RANDOM_TEXT)

    def test_success__generate_random_text__with_choices(self):
        # arrange
        length = 20
        choices = "123"

        # action
        result = TextUtil.generate_random_text(length=length, choices=choices)

        # assert
        assert len(result) == length
        assert set(list(result)).issubset(choices)

    def test_success__generate_random_string_of_numbers(self):
        # arrange
        length = 20

        # action
        result = TextUtil.generate_random_string_of_numbers(length=length)

        # assert
        assert len(result) == length
        assert set(list(result)).issubset(DEFAULT_RANDOM_NUMBERS)
