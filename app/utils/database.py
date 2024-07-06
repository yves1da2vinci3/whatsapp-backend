from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client.whatsapp_db
test_db = client.whatsapp_db_test

def get_db():
    return db

def get_test_db():
    return db
