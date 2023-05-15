import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

database = client["bookstore"]
collection = database["books"]

# collection.create_index([("title", pymongo.TEXT)])
# collection.create_index([("author", pymongo.TEXT)])
# collection.create_index([("price", pymongo.ASCENDING)])