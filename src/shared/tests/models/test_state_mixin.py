# type: ignore
import pytest

from shared.models.state_mixin import BaseStateSetting


class MockInstanceStateSetting(BaseStateSetting):
    STATE_TRANSITIONS = {
        "state_1": {"state_2", "state_3"},
        "state_2": {"state_3", "state_4"},
        "state_3": {"state_1", "state_4"},
        "state_4": ["state_5"],
    }


class TestBaseStateSetting:
    @pytest.mark.parametrize(
        "original_status,target_status",
        (
            ("state_1", "state_4"),
            ("state_1", "state_5"),
            ("state_2", "state_1"),
            ("state_2", "state_5"),
            ("state_3", "state_2"),
            ("state_3", "state_5"),
            ("state_4", "state_1"),
            ("state_4", "state_2"),
            ("state_4", "state_3"),
            ("state_1", "state_1"),
            ("state_2", "state_2"),
            ("state_3", "state_3"),
            ("state_4", "state_4"),
            ("state_5", "state_1"),
            ("state_6", "state_1"),
            ("state_6", "state_2"),
            ("state_6", "state_3"),
            ("state_6", "state_4"),
            ("state_6", "state_5"),
        ),
    )
    def test_failed__transaction_to_not_valid_state(self, original_status, target_status):
        # action
        result = MockInstanceStateSetting.can_transition(
            from_status=original_status, to_status=target_status
        )

        # assert
        assert result is False

    @pytest.mark.parametrize(
        "original_status,target_status",
        (
            ("state_1", "state_2"),
            ("state_1", "state_3"),
            ("state_2", "state_3"),
            ("state_2", "state_4"),
            ("state_3", "state_1"),
            ("state_3", "state_4"),
            ("state_4", "state_5"),
        ),
    )
    def test_success__transaction_to_valid_state(self, original_status, target_status):
        # action
        result = MockInstanceStateSetting.can_transition(
            from_status=original_status, to_status=target_status
        )

        # assert
        assert result is True
