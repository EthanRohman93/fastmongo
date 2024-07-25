from pymongo import MongoClient
import json

client = None
db = None

with open("../tickers.json") as file:
    tickers = json.load(file)

def create_doc_structure(db):
    collections = db.list_collection_names()
    if not collections:
        for ticker in tickers:
            db[ticker].insert_one({
                "price": [],
                "vol": [],
                "sma": [],
                "rsi": []
            })
            print(f"Created document structure for {ticker}")
    else:
        print("Collection(s) already exist")

def connect_to_mongo():
    global client, db
    client = MongoClient('mongodb://localhost:27017')
    db = client['stock_data']
    create_doc_structure(db)

def get_db():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    return db

def close_mongo_connection():
    global client
    if client:
        client.close()

if __name__ == "__main__":
    connect_to_mongo()
    print("successfully connected")
    close_mongo_connection()
    print("successfully closed connection")
