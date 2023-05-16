# type: ignore
import pytest

from file_management.models import File
from file_management.tests.factories.file import FileFactory
from user.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


class TestFileModelManager:
    def test_success__filter_by_user_id(self):
        # given
        user = UserFactory()
        file = FileFactory(uploaded_by=user)

        # give noise file
        FileFactory()

        # when
        files = File.objects.all().filter_by_user_id(user_id=user.id)

        # then
        assert files.count() == 1
        assert files.first() == file

    def test_success__full_prefetch(self):
        # given
        user = UserFactory()
        file = FileFactory(uploaded_by=user)

        # when
        files = File.objects.all().full_prefetch()

        # then
        assert files.count() == 1
        assert files.first() == file
