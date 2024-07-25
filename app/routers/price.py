from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

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

prices = [1,2,3,4]

@router.get("/{ticker}")
async def read_price():
    return prices

# @router.post(

# )
# async def add_records
