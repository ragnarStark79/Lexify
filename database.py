from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import config
import datetime

class DatabaseHandler:
    def __init__(self):
        self.client = None
        self.db = None
        self.interactions_collection = None
        self.users_collection = None
        try:
            self.client = MongoClient(config.MONGO_URI)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self.db = self.client[config.MONGO_DB_NAME]
            self.interactions_collection = self.db[config.MONGO_COLLECTION_NAME]
            self.users_collection = self.db['users'] # New collection for users
            print("Successfully connected to MongoDB.")
        except ConnectionFailure:
            print("MongoDB connection failed. Please ensure MongoDB server is running and accessible.")
            # Handle connection error appropriately in a real application
            # For now, we'll allow the object to be created but methods will fail
        except Exception as e:
            print(f"An error occurred during MongoDB initialization: {e}")

    def log_interaction(self, original_text, enhanced_text, model_name, user_feedback=None, user_id=None): # Add user_id
        """Logs the interaction details to MongoDB."""
        if self.interactions_collection is None:
            print("Cannot log interaction: MongoDB collection not available.")
            return None

        log_entry = {
            "timestamp": datetime.datetime.utcnow(),
            "model_name": model_name,
            "original_text": original_text,
            "enhanced_text": enhanced_text,
            "user_feedback": user_feedback, # e.g., rating, correction, acceptance
            "user_id": user_id # Store user ID if available
            # Add other relevant metadata like user ID (anonymized), session ID etc.
        }
        try:
            insert_result = self.interactions_collection.insert_one(log_entry)
            # Make sure logging confirmation happens *before* returning
            print(f"Interaction logged with ID: {insert_result.inserted_id}")
            return insert_result.inserted_id
        except Exception as e:
            print(f"Failed to log interaction to MongoDB: {e}")
            return None

    def add_user(self, name, email, hashed_password):
        """Adds a new user to the users collection."""
        if self.users_collection is None: # Changed check
            print("User collection not initialized.")
            return None
        if self.users_collection.find_one({"email": email}):
            return None # User already exists
        try:
            user_data = {
                "name": name, # Added name field
                "email": email,
                "username": email, # Use email as username to satisfy unique index
                "password": hashed_password,
                "registered_on": datetime.datetime.utcnow()
            }
            result = self.users_collection.insert_one(user_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error adding user: {e}")
            return None

    def find_user_by_email(self, email):
        """Finds a user by their email address."""
        if self.users_collection is None: # Changed check
            print("User collection not initialized.")
            return None
        try:
            return self.users_collection.find_one({"email": email})
        except Exception as e:
            print(f"Error finding user: {e}")
            return None

    def find_user_by_id(self, user_id):
        """Finds a user by their MongoDB ObjectId."""
        if self.users_collection is None:
            print("User collection not initialized.")
            return None
        try:
            from bson.objectid import ObjectId # Import here to avoid circular dependency issues if DatabaseHandler is imported elsewhere
            return self.users_collection.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None

    def update_user_profile(self, user_id, name, email):
        """Updates a user's name and email."""
        if self.users_collection is None:
            print("User collection not initialized.")
            return False
        try:
            from bson.objectid import ObjectId
            # Check if the new email is already taken by another user
            existing_user = self.users_collection.find_one({"email": email, "_id": {"$ne": ObjectId(user_id)}})
            if existing_user:
                print(f"Email {email} is already in use by another account.")
                return False # Email already taken

            result = self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"name": name, "email": email}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False

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

