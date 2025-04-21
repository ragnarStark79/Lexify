from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import config
import datetime

class DatabaseHandler:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        try:
            self.client = MongoClient(config.MONGO_URI)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self.db = self.client[config.MONGO_DB_NAME]
            self.collection = self.db[config.MONGO_COLLECTION_NAME]
            print("Successfully connected to MongoDB.")
        except ConnectionFailure:
            print("MongoDB connection failed. Please ensure MongoDB server is running and accessible.")
            # Handle connection error appropriately in a real application
            # For now, we'll allow the object to be created but methods will fail
        except Exception as e:
            print(f"An error occurred during MongoDB initialization: {e}")


    def log_interaction(self, original_text, enhanced_text, model_name, user_feedback=None):
        """Logs the interaction details to MongoDB."""
        # Corrected check: Compare with None explicitly
        if self.collection is None:
            print("Cannot log interaction: MongoDB collection not available.")
            return None

        log_entry = {
            "timestamp": datetime.datetime.utcnow(),
            "model_name": model_name,
            "original_text": original_text,
            "enhanced_text": enhanced_text,
            "user_feedback": user_feedback # e.g., rating, correction, acceptance
            # Add other relevant metadata like user ID (anonymized), session ID etc.
        }
        try:
            insert_result = self.collection.insert_one(log_entry)
            # Make sure logging confirmation happens *before* returning
            print(f"Interaction logged with ID: {insert_result.inserted_id}")
            return insert_result.inserted_id
        except Exception as e:
            print(f"Failed to log interaction to MongoDB: {e}")
            return None

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

# Singleton instance (optional, but often useful)
db_handler = DatabaseHandler()

def get_db_handler():
    """Returns the singleton database handler instance."""
    # This simple approach assumes the handler is always needed.
    # In more complex apps, you might initialize it on demand.
    return db_handler

