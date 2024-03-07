import pytest
from api import create_app, config

@pytest.fixture(scope="session")
def app():
    app = create_app(config.TestConfig)

    yield app

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()