from typing import Any, Generator, Optional

import pytest
from rest_framework.test import APIClient
from testcontainers.postgres import PostgresContainer

from main import settings


class PostgresContainerEx(PostgresContainer):
    # workaround for the issue in WSL2
    # https://github.com/testcontainers/testcontainers-python/issues/108
    def get_connection_url(self, host: Optional[str] = None) -> Any:
        return super().get_connection_url(host=host).replace("localnpipe", "localhost")


@pytest.fixture(scope="session", autouse=True)
def postgres_container() -> Generator[None, None, None]:
    with PostgresContainerEx(
        image="postgres:14.8-alpine",
        dbname=settings.DATABASES["default"]["NAME"],
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
    ).with_bind_ports(5432, settings.DATABASES["default"]["PORT"]):
        yield


@pytest.fixture
def api_client() -> APIClient:
    client = APIClient()
    return client
