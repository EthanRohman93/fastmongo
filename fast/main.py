from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
client = MongoClient("mongodb://localhost:27017")
db = client["test"]

@app.get("/")
def read_root():
   return {"Hello": "World"}

