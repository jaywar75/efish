import pytest
from flask import url_for

@pytest.mark.parametrize("endpoint", [
    "api.ping",         # Suppose you have a ping or health-check endpoint
    "api.some_feature", # Possibly a placeholder if you intend an /api/some_feature
])
def test_api_endpoints(client, endpoint):
    """Simple smoke tests for API endpoints."""
    # `client` could be a pytest fixture in `conftest.py` that provides a test client.
    response = client.get(url_for(endpoint))
    # We expect a 200 or 404 if it's not implemented yet. For placeholders, just check for 200:
    assert response.status_code == 200

def test_api_json_response(client):
    """Check if an API endpoint returns valid JSON."""
    # You can do something more targeted if you have a /api/ping that returns JSON.
    response = client.get("/api/ping")  # Hard-coded path if you prefer
    assert response.status_code == 200
    # Maybe the API returns {"status": "ok"} or similar
    data = response.get_json()
    assert data is not None
    assert data.get("status") == "ok"