from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)

# This creates database automatically when first data is inserted
db = client["object_detection"]

# This creates collections automatically
detections_collection = db["detections"]
users_collection = db["users"]