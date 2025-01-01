# app/models/account.py

from datetime import datetime
from app.extensions import mongo
from bson.objectid import ObjectId

class Account:
    def __init__(self, doc):
        self.id = str(doc["_id"])
        self.account_number = doc.get("account_number", "")
        self.account_name = doc.get("account_name", "")
        self.tenant_id = doc.get("tenant_id", "")
        self.plan_type = doc.get("plan_type", "free")
        self.addons = doc.get("addons", [])
        self.created_at = doc.get("created_at", datetime.utcnow())

    @staticmethod
    def get(account_id):
        doc = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
        return Account(doc) if doc else None

    @staticmethod
    def create(account_number, account_name):
        new_doc = {
            "account_number": account_number,
            "account_name": account_name,
            "tenant_id": "",        # or generate if doing multi-tenant
            "plan_type": "free",
            "addons": [],
            "created_at": datetime.utcnow()
        }
        result = mongo.db.accounts.insert_one(new_doc)
        return Account.get(result.inserted_id)

    def update_plan(self, new_plan):
        mongo.db.accounts.update_one(
            {"_id": ObjectId(self.id)},
            {"$set": {"plan_type": new_plan}}
        )
        self.plan_type = new_plan  # to keep in-memory object in sync