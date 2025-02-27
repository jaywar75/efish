# app/models.py

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        # Add other attributes as needed

    def get_id(self):
        return self.id