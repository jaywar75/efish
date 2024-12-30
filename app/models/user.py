# app/models/user.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app.extensions import mongo

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = str(user_dict['_id'])
        self.username = user_dict['username']
        self.email = user_dict['email']
        self.password_hash = user_dict['password_hash']
        # Add other fields as necessary

    @staticmethod
    def get(user_id):
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            return User(user)
        return None

    @staticmethod
    def get_by_email(email):
        user = mongo.db.users.find_one({'email': email})
        if user:
            return User(user)
        return None

    @staticmethod
    def create(username, email, password):
        password_hash = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password_hash': password_hash
        }).inserted_id
        return User.get(user_id)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)