# app/models/user.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app.extensions import mongo

class User(UserMixin):
    def __init__(self, user_doc):
        """
        Initialize a User object from a MongoDB document.
        """
        self.id = str(user_doc["_id"])
        self.email = user_doc.get("email", "")
        self.password_hash = user_doc.get("password_hash", "")

        # Optionally store additional fields if your collection has them:
        self.first_name = user_doc.get("first_name", "")
        self.last_name = user_doc.get("last_name", "")
        self.phone = user_doc.get("phone", "")
        self.time_zone = user_doc.get("time_zone", "")
        self.about_me = user_doc.get("about_me", "")

    def verify_password(self, password):
        """
        Returns True if the given plaintext `password` matches the stored hash.
        """
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        """
        Retrieve a user by Mongo ObjectId string, or return None if not found.
        """
        doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if doc:
            return User(doc)
        return None

    @staticmethod
    def get_by_email(email):
        """
        Find a user by their email, or return None if not found.
        """
        user_doc = mongo.db.users.find_one({"email": email})
        if user_doc:
            return User(user_doc)
        return None

    @staticmethod
    def create(first_name, last_name, email, password):
        """
        Insert a new user document into Mongo, returning a User object.
        """
        password_hash = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password_hash": password_hash
        }).inserted_id
        return User.get(user_id)

    def reload_from_db(self):
        """
        Optional method to refresh this User object from Mongo.
        """
        user_doc = mongo.db.users.find_one({"_id": ObjectId(self.id)})
        if user_doc:
            self.email = user_doc.get("email", "")
            self.password_hash = user_doc.get("password_hash", "")
            self.first_name = user_doc.get("first_name", "")
            self.last_name = user_doc.get("last_name", "")
            self.phone = user_doc.get("phone", "")
            self.time_zone = user_doc.get("time_zone", "")
            self.about_me = user_doc.get("about_me", "")