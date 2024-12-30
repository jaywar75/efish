import pytest
from flask import url_for
from bson.objectid import ObjectId

@pytest.fixture
def example_document():
    """Fixture for a fake document record, ready to be inserted or used in tests."""
    return {
        "_id": ObjectId(),
        "title": "Example Document",
        "description": "A test document fixture.",
        "user_id": "fake_user_id",
        "created_at": "2024-12-30T10:00:00Z",
        # Any other relevant fields...
    }

def test_list_documents_unauthorized(client):
    """Ensure we get redirected or a 401/403 when not logged in."""
    response = client.get(url_for("documents.list_documents"), follow_redirects=True)
    # Expect some form of unauthorized response, depending on your login requirement:
    assert response.status_code in (302, 401, 403), "Expected redirect or unauthorized for anonymous user."

def test_list_documents_authorized(client, example_document, mocker):
    """Check that we can list documents for a logged-in user."""
    # If you have a login fixture or a mocking approach, you'd do it here:
    mocker.patch("app.documents.routes.mongo.db.documents.find", return_value=[example_document])

    # You might need to log in first if your blueprint is protected:
    # e.g., client.post(url_for('auth.login'), data={"username": ..., "password": ...})

    response = client.get(url_for("documents.list_documents"))
    assert response.status_code == 200
    # Optionally parse the response to ensure the doc title appears in the HTML
    assert example_document["title"] in response.text