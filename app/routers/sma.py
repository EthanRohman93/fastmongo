from fastapi import APIRouter

router = APIRouter(
    prefix="/sma",
    tags=["sma"],
    responses={404: {"description": "Not Found"}},
)

prices = [1,2,3,4]

@router.get("/{ticker}")
async def read_price():
    return prices
