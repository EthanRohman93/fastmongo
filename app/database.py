from pymongo import MongoClient

client = None
db = None

def connect_to_mongo():
    global client, db
    client = MongoClient('mongodb://localhost:27017')
    db = client['stock_data']

def close_mongo_connection():
    global client
    if client:
        client.close()
