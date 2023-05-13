# type: ignore
from decimal import Decimal, InvalidOperation

import pytest
from shared.utilities.number import NumberUtil


class TestNumberUtil:
    @pytest.mark.parametrize("value", ["1.5", 1.5, 1])
    def test_success__convert_to_decimal(self, value):
        # action
        result = NumberUtil.to_decimal(value)

        # assert
        assert isinstance(result, Decimal)

    @pytest.mark.parametrize("value", [None, "abc"])
    def test_failed__convert_to_decimal__invalid_input(self, value):
        with pytest.raises(InvalidOperation):
            NumberUtil.to_decimal(value)

    @pytest.mark.parametrize("_from,_to", [(1, 10), (-10, -1), (10, None)])
    def test_success__generate_random_number___pass_both_from_and_to(self, _from, _to):
        # action
        result = NumberUtil.generate_random_number(_from, _to)

        # assert
        if _to is not None:
            assert _from <= result <= _to
        else:
            assert _from >= result

    @pytest.mark.parametrize("_from,_to", [(6, None)])
    def test_success__generate_random_number__pass_from_only(self, _from, _to):
        # action
        result = NumberUtil.generate_random_number(_from)

        # assert
        assert _from >= result

    @pytest.mark.parametrize("_from,_to", [(6, 2)])
    def test_failed__generate_random_number__pass_from_greater_than_to(self, _from, _to):
        with pytest.raises(ValueError):
            NumberUtil.generate_random_number(_from, _to)

    @pytest.mark.parametrize("_from,_to", [(-1, None)])
    def test_failed__generate_random_number__pass_to_none_and_negative_from(self, _from, _to):
        with pytest.raises(ValueError):
            NumberUtil.generate_random_number(_from, _to)
