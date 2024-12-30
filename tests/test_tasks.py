# tests/test_tasks.py

def test_add_task(test_app, clean_db):
    # First, you may need to login if /tasks/add is protected
    login_resp = test_app.post(
        "/login",
        data={"username": "testuser", "password": "testpass"},
        follow_redirects=True
    )
    assert login_resp.status_code == 200

    # Then add a new task
    response = test_app.post(
        "/tasks/add",
        data={
            "title": "Test Task",
            "description": "Task for testing",
            "completed": False
        },
        follow_redirects=True
    )
    assert response.status_code in (200, 302)

    # Optionally, fetch tasks and assert we see the new one
    tasks_page = test_app.get("/tasks")
    assert b"Test Task" in tasks_page.data