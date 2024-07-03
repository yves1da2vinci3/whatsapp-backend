from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client.whatsapp_db

def get_db():
    return db
