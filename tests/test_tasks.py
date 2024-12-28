# tests/test_tasks.py

import unittest
from app import create_app, mongo
from app.models import User
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from config import TestConfig  # Ensure TestConfig is imported


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client and initialize the test database.
        """
        # Initialize the app with TestConfig
        self.app = create_app(config_class=TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Clear the test database
        mongo.db.users.delete_many({})
        mongo.db.tasks.delete_many({})

        # Create a test user
        hashed_password = generate_password_hash('password123')
        self.test_user_id = mongo.db.users.insert_one({
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': hashed_password
        }).inserted_id

    def tearDown(self):
        """
        Clean up after each test.
        """
        # Clear the test database
        mongo.db.users.delete_many({})
        mongo.db.tasks.delete_many({})

        # Close the MongoClient connection
        if mongo.cx:
            mongo.cx.close()

        # Remove app context
        self.app_context.pop()

    def login(self, username, password):
        """
        Helper method to log in a user.
        """
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_add_task(self):
        """
        Test adding a new task.
        """
        # Login first
        response = self.login('testuser', 'password123')
        self.assertIn(b'Logged in successfully.', response.data)

        # Add a task with 'completed' unchecked (defaults to False)
        response = self.client.post('/tasks/add', data=dict(
            title='Test Task',
            description='This is a test task.'
            # 'completed' field is omitted to simulate unchecked checkbox
        ), follow_redirects=True)
        self.assertIn(b'Task added successfully!', response.data)

        # Verify task exists in the database
        task = mongo.db.tasks.find_one({'title': 'Test Task'})
        self.assertIsNotNone(task)
        self.assertEqual(task['description'], 'This is a test task.')
        self.assertFalse(task['completed'])

    def test_edit_task(self):
        """
        Test editing an existing task.
        """
        # Login first
        self.login('testuser', 'password123')

        # Add a task directly to the database
        task_id = mongo.db.tasks.insert_one({
            'user_id': str(self.test_user_id),
            'title': 'Original Task',
            'description': 'Original description.',
            'completed': False
        }).inserted_id

        # Edit the task via the application
        response = self.client.post(f'/tasks/edit/{task_id}', data=dict(
            title='Updated Task',
            description='Updated description.',
            completed=True
        ), follow_redirects=True)
        self.assertIn(b'Task updated successfully!', response.data)

        # Verify the task has been updated in the database
        task = mongo.db.tasks.find_one({'_id': task_id})
        self.assertEqual(task['title'], 'Updated Task')
        self.assertEqual(task['description'], 'Updated description.')
        self.assertTrue(task['completed'])

    def test_complete_task(self):
        """
        Test marking a task as completed.
        """
        # Login first
        self.login('testuser', 'password123')

        # Add a task directly to the database
        task_id = mongo.db.tasks.insert_one({
            'user_id': str(self.test_user_id),
            'title': 'Task to Complete',
            'description': 'This task will be marked as completed.',
            'completed': False
        }).inserted_id

        # Complete the task via the application
        response = self.client.post(f'/tasks/complete/{task_id}', follow_redirects=True)
        self.assertIn(b'Task marked as completed!', response.data)

        # Verify the task's completion status in the database
        task = mongo.db.tasks.find_one({'_id': task_id})
        self.assertTrue(task['completed'])

        # Attempt to complete the same task again to test idempotency
        response = self.client.post(f'/tasks/complete/{task_id}', follow_redirects=True)
        self.assertIn(b'Task is already completed.', response.data)

    def test_delete_task(self):
        """
        Test deleting a task.
        """
        # Login first
        self.login('testuser', 'password123')

        # Add a task directly to the database
        task_id = mongo.db.tasks.insert_one({
            'user_id': str(self.test_user_id),
            'title': 'Task to Delete',
            'description': 'This task will be deleted.',
            'completed': False
        }).inserted_id

        # Delete the task via the application
        response = self.client.post(f'/tasks/delete/{task_id}', follow_redirects=True)
        self.assertIn(b'Task deleted successfully!', response.data)

        # Verify the task has been removed from the database
        task = mongo.db.tasks.find_one({'_id': task_id})
        self.assertIsNone(task)


if __name__ == '__main__':
    unittest.main()