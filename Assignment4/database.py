import os
from pymongo import MongoClient, DESCENDING
from typing import List, Dict, Any

class MongoDBHandler:
    def __init__(self, uri: str = None, db_name: str = None, collection_name: str = None):
        self.uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = db_name or os.getenv("DB_NAME", "assignment4_db")
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "documents")
        
        self.client = None
        self.db = None
        self.collection = None
        
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            # Create a simple index on timestamp if we want to sort
            self.collection.create_index([("timestamp", DESCENDING)])
            print(f"Connected to MongoDB: {self.db_name}.{self.collection_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def insert_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Inserts a document with content and optional metadata."""
        if metadata is None:
            metadata = {}
        
        document = {
            "content": content,
            "metadata": metadata,
            # We can add a simple text index later if needed, but for now just raw storage
        }
        
        # Add timestamp if not present
        if "timestamp" not in document:
             import datetime
             document["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def retrieve_documents(self, limit: int = 5) -> List[Dict]:
        """
        Retrieves the most recent documents. 
        In a real RAG system, this would do vector search. 
        Here we simply get context from the DB.
        """
        cursor = self.collection.find().sort("timestamp", DESCENDING).limit(limit)
        return list(cursor)

    def search_documents_keyword(self, query: str) -> List[Dict]:
        """
        Simple keyword search implementation (requires text index) or regex.
        Using regex for simplicity in this assignment context without complex setups.
        """
        # Case insensitive regex search
        cursor = self.collection.find({"content": {"$regex": query, "$options": "i"}}).limit(5)
        return list(cursor)
