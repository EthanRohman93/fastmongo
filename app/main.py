from fastapi import FastAPI
from routers import price, rsi, sma, vol
from database import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.include_router(price.router)
app.include_router(rsi.router)
app.include_router(sma.router)
app.include_router(vol.router)

@app.get("/")
async def root():
   return {"message": "Root Endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
