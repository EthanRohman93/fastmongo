from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_db

class PriceData(BaseModel):
    timestamp: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float

class BatchStockData(BaseModel):
    ticker: str
    data: List[PriceData]

router = APIRouter(
    prefix="/price",
    tags=["price"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/{ticker}")
async def read_price(ticker: str, db=Depends(get_db)):
    collection = db[ticker]
    if collection is None:
        raise HTTPException(status_code=404, detail="Ticker not found")
    document = collection.find_one({"price": {"$exists": True}})
    if document is None:
        raise HTTPException(status_code=404, detail="Price data not found")
    return document["price"]

@router.post("/{ticker}")
async def add_records(ticker: str, batch_data: BatchStockData, db=Depends(get_db)):
    collection = db[ticker]
    if collection is None:
        raise HTTPException(status_code=404, detail="Ticker not found")
    documents = [data.model_dump() for data in batch_data.data]
    result = collection.update_one(
        {"price": {"$exists": True}},  # Filter to find the correct document
        {"$push": {"price": {"$each": documents}}}  # Update operation
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticker not found or document not found")
    return {"status": "success"}

