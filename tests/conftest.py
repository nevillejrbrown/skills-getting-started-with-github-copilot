from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def isolate_activities():
    original_activities = deepcopy(app_module.activities)

    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(original_activities)
