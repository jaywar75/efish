# app/services/account_service.py

from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from app.extensions import mongo
from app.models.account import Account

def get_next_sequence(counter_name):
    """
    Atomically increments and returns the next integer in a 'counters' collection
    for building sequential account numbers, tenant IDs, etc.
    """
    doc = mongo.db.counters.find_one_and_update(
        {"_id": counter_name},
        {"$inc": {"seq": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return doc["seq"]

def create_account(account_name=""):
    """
    Creates a new Account document in MongoDB, leveraging:
      - A sequential account number (optional).
      - A created_at timestamp.

    Returns an Account object.
    """
    # Possibly use get_next_sequence if you want a numeric portion:
    next_seq = get_next_sequence("account_counter")  # e.g. returns 1001, 1002,...
    account_number = f"efish-{next_seq:07d}"  # zero-pad to 7 digits for example

    # Insert the doc directly, storing created_at
    new_doc = {
        "account_number": account_number,
        "account_name": account_name,
        "created_at": datetime.utcnow(),
        "updated_at": None,     # or also set = datetime.utcnow() initially
        # other fields like 'tenant_id' if needed
    }

    result = mongo.db.accounts.insert_one(new_doc)

    # Return an Account model instance (assuming your Account class can load this doc)
    return Account.get(result.inserted_id)

def update_account_plan(account_id, new_plan):
    """
    Updates the plan_type of an existing Account doc, sets updated_at,
    and returns the updated Account model. Leverages ObjectId to locate the doc.
    """
    # Convert string to ObjectId if needed
    if not isinstance(account_id, ObjectId):
        account_id = ObjectId(account_id)

    account = Account.get(account_id)
    if not account:
        return None

    # Example: your Account model might have update_plan, or we can do raw:
    updated_data = {
        "plan_type": new_plan,
        "updated_at": datetime.utcnow()
    }

    mongo.db.accounts.update_one(
        {"_id": account_id},
        {"$set": updated_data}
    )
    # Keep the in-memory object in sync by calling account.update_plan(new_plan)
    # or reloading from DB:
    account.update_plan(new_plan)  # if your Account model has this method
    return account

def raw_update_account(account_id, fields):
    """
    A generic raw updater, for demonstration:
      - fields is a dict of key: value to update
      - sets updated_at automatically
    """
    if not isinstance(account_id, ObjectId):
        account_id = ObjectId(account_id)

    fields["updated_at"] = datetime.utcnow()
    mongo.db.accounts.update_one({"_id": account_id}, {"$set": fields})
    return Account.get(account_id)