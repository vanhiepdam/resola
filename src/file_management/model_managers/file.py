from django.db.models import QuerySet

from shared.models.base_manager import BaseManager


class FileQuerySet(QuerySet):
    def filter_by_user_id(self, user_id: int) -> QuerySet:
        return self.filter(uploaded_by_id=user_id)


class FileManager(BaseManager):
    def get_queryset(self) -> QuerySet:
        return FileQuerySet(self.model, using=self._db)
