# app/services/user_service.py

from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from app.extensions import mongo
from app.models.user import User

def create_new_account():
    """
    Inserts a new doc in the 'accounts' collection and returns its _id.
    """
    doc = {
        "account_name": "New Account",
        "plan_type": "free",
        "created_at": datetime.utcnow()
    }
    result = mongo.db.accounts.insert_one(doc)
    return result.inserted_id

def create_user_with_account_option(first_name, last_name, email, password, existing_acct_id):
    """
    Creates a user. If existing_acct_id == "NEW", we generate a new account doc.
    Otherwise, we treat existing_acct_id as a hex string referencing an existing account.

    :param first_name:         The user's first name
    :param last_name:          The user's last name
    :param email:              The user's email address
    :param password:           Plaintext password to be hashed
    :param existing_acct_id:   "NEW" (to create a new account) or a valid 24-hex string
    :return:                   The newly created user's _id (ObjectId)
    """
    if existing_acct_id == "NEW":
        account_id = create_new_account()
    else:
        # Attempt to convert to ObjectId
        try:
            account_id = ObjectId(existing_acct_id)
        except:
            # If invalid, fallback to creating a new account
            account_id = create_new_account()

        # Optionally verify the account doc actually exists
        if not mongo.db.accounts.find_one({"_id": account_id}):
            account_id = create_new_account()

    # Now create the user doc referencing account_id
    password_hash = generate_password_hash(password)
    user_doc = {
        "first_name": first_name,
        "last_name":  last_name,
        "email":      email.lower(),
        "password_hash": password_hash,
        "account_id": account_id,
        "created_at": datetime.utcnow()
    }
    new_user_id = mongo.db.users.insert_one(user_doc).inserted_id
    return new_user_id