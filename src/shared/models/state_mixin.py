from abc import abstractmethod
from typing import Any, Union

from django.core.exceptions import ValidationError
from django.db import transaction


class CanNotChangeStateException(ValidationError):
    pass


class StateMachineModelMixin:
    @property
    @abstractmethod
    def status_field(self) -> str:
        pass

    @abstractmethod
    def can_change_status(self, status: Any) -> bool:
        pass

    def get_new_status(self, status: Any) -> Any:
        return status

    def do_after_changing_status(self) -> None:
        pass

    @transaction.atomic
    def change_status(self, status: Any) -> None:
        err_msg = f"Can not change to status {status}"
        if not self.can_change_status(status):
            raise CanNotChangeStateException(err_msg)

        new_status = self.get_new_status(status)
        setattr(self, self.status_field, new_status)
        self.save()  # type: ignore
        self.do_after_changing_status()


class BaseStateSetting:
    STATE_TRANSITIONS: dict[Any, Union[list[Any], set[Any]]] = {}

    @classmethod
    def can_transition(cls, from_status: Any, to_status: Any) -> bool:
        if from_status not in cls.STATE_TRANSITIONS:
            return False
        return to_status in cls.STATE_TRANSITIONS[from_status]
