from pymongo import MongoClient # type: ignore

client = MongoClient("mongodb://localhost:27017/")
db = client.whatsapp_db

def get_db():
    return db
