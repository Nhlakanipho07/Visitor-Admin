import os
from pymongo import MongoClient


class MongoDBConnectionManager:
    def __init__(self, default_uri="mongodb://localhost:27017"):
        self.uri = os.getenv("MONGODB_URI", default_uri)

    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client["CompanyName"]
        self.visitors = self.db["Visitor"]
        return self.visitors

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
