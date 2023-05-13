# type: ignore
import pytest

pytestmark = [pytest.mark.django_db]


class TestAPIDoc:
    def test_success__api_doc_working(self, client):
        response = client.get("/api/schema/")
        assert response.status_code == 200
