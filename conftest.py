# tests/conftest.py
import pytest
import data.constants
import utils.api_utils
import requests
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    """
    Provides a reusable APIClient with a single underlying requests.Session.
    Tests should use api_client.get/post(...) instead of raw requests.
    """
    session = requests.Session()
    session.headers.update({"Cache-Control": "no-cache", "Pragma": "no-cache"})
    client = APIClient(session=session)
    yield client
    client.close()

@pytest.fixture(scope="session")
def get_advice_endpoint():
    return data.constants.EndPoints.ADVICE_ENDPOINT

@pytest.fixture(scope="session")
def get_advice_search_endpoint():
    return data.constants.EndPoints.ADVICE_SEARCH_ENDPOINT

@pytest.fixture
def get_logger(request):
    test_name = request.node.name
    return utils.api_utils.get_logger(test_name)