import pytest
from fixtures import django_db_setup  # noqa F401


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    for item in items:
        marker = item.get_closest_marker("django_db")
        if marker:
            databases = marker.kwargs.get("database", ["default"])
            marker.kwargs["databases"] = databases

    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "structure" in item.name:
            item.add_marker(pytest.mark.model_structure)
        if "model_migration" in item.name:
            item.add_marker(pytest.mark.model_migration)
