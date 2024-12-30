# tests/test_auth.py
def test_register_and_login(test_app, clean_db):
    """
    1. Register a new user
    2. Log in with that user
    """

    # 1. Register
    response = test_app.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass"
        },
        follow_redirects=True
    )
    # Typically, a registration might redirect, check for 302
    assert response.status_code in (200, 302)

    # 2. Login
    response = test_app.post(
        "/login",
        data={"username": "testuser", "password": "testpass"},
        follow_redirects=True
    )
    # Expecting a success page (or a dashboard)
    assert response.status_code == 200
    assert b"Dashboard" in response.data