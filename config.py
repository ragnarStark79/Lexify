import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

# Model configuration
# Switch to Mistral Instruct model
DEFAULT_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
# Previous: "google/flan-t5-large"
# Note: This model is large (~14GB) and requires significant resources.

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "chat_enhancer_data")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "interactions")

