from pytest import fixture
from fastapi.testclient import TestClient
from main import app

@fixture(scope="function")
def client() -> TestClient:
    return TestClient(app)