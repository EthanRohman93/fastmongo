from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_db

class VolData(BaseModel):
    timestamp: str
    vol: int

class BatchStockData(BaseModel):
    ticker: str
    data: List[VolData]

router = APIRouter(
    prefix="/vol",
    tags=["vol"],
    responses={404: {"description": "Not Found"}},
)

prices = [1,2,3,4]

@router.get("/{ticker}")
async def read_price():
    return prices

@router.post("/{ticker}")
async def add_records(ticker: str, batch_data: BatchStockData, db=Depends(get_db)):
    collection = db[ticker]
    if collection is None:
        raise HTTPException(status_code=404, detail="Ticker not found")
    documents = [data.model_dump() for data in batch_data.data]
    result = collection.update_one(
        {"vol": {"$exists": True}},  # Filter to find the correct document
        {"$push": {"vol": {"$each": documents}}}  # Update operation
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticker not found or document not found")
    return {"status": "success"}


