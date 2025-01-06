import pytest
from django.core.management import call_command

from tests.utils.test_database_container import start_database_container


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    container = start_database_container()
    try:
        print(container.ports)
        with django_db_blocker.unblock():
            print("Running migration")
            call_command("migrate")
            print("migrations done!")
        yield
    finally:
        container.stop()
        container.remove()
        print("database teardown")
