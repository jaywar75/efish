# tests/conftest.py

import pytest
from app import create_app
from config.testing import TestingConfig
from app.extensions import mongo


@pytest.fixture(scope="session")
def test_app():
    """
    Creates and configures a new app instance for each test session using TestingConfig.
    """
    # Initialize the Flask app using our dedicated testing config
    app = create_app(TestingConfig)

    # Because we need the app context to use test_client, we wrap in `app.test_client()`
    with app.test_client() as client:
        yield client


@pytest.fixture
def client(test_app):
    """
    If you want each test function to have a 'client' fixture,
    you can either:
    - direct 'test_app' to yield the client directly,
    OR
    - have 'test_app' yield the Flask app and call 'test_app.test_client()' here.

    The way it's currently structured, 'test_app' already yields 'client',
    so this fixture might be redundant.
    But if you'd rather 'test_app' yield the app, do that and then
    this fixture can do 'with test_app.test_client() as client: yield client'.
    """
    return test_app


@pytest.fixture(scope="session", autouse=True)
def clean_db_session(test_app):
    """
    Optionally wipe the entire test database one time before all tests run.
    The 'autouse=True' means it applies automatically for the test session.

    If you prefer a fully fresh DB for *each test*, consider a function-scope fixture.
    """
    with test_app.application.app_context():
        # e.g., drop the entire "efish_test_db"
        mongo.db.client.drop_database("efish_test_db")
        # or selectively drop certain collections:
        # mongo.db.users.drop()
        # mongo.db.tasks.drop()

    yield

    # Optionally, after all tests, do final cleanup if desired
    # with test_app.application.app_context():
    #     mongo.db.client.drop_database("efish_test_db")


@pytest.fixture(scope="function")
def clean_db_function(test_app):
    """
    If you need certain collections cleared before *each test function* runs:
    """
    with test_app.application.app_context():
        # Example: empty out relevant collections
        mongo.db.users.delete_many({})
        mongo.db.tasks.delete_many({})
        # ... etc.

    yield

    # After test function cleanup if you want