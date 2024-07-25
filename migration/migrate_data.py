import requests
import json

# Define the Django API base URL and FastAPI base URL
DJANGO_API_BASE_URL = "http://dough-flow.com/api/"
FASTAPI_BASE_URL = "http://localhost:8000/"

# Read tickers from tickers.json
with open('../tickers.json', 'r') as file:
    tickers = json.load(file)

def fetch_data_from_django(ticker, endpoint):
    url = f"{DJANGO_API_BASE_URL}{ticker}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}")
        return None

def transform_data(ticker, endpoint, data):
    if endpoint == "price":
        return {
            "ticker": ticker,
            "data": [
                {
                    "timestamp": item["timestamp"],
                    "open_price": item["open_price"],
                    "high_price": item["high_price"],
                    "low_price": item["low_price"],
                    "close_price": item["close_price"]
                } for item in data
            ]
        }
    elif endpoint == "vol":
        return {
            "ticker": ticker,
            "data": [
                {
                    "timestamp": item["timestamp"],
                    "vol": item["volume"]
                } for item in data
            ]
        }
    elif endpoint == "rsi":
        return {
            "ticker": ticker,
            "data": [
                {
                    "timestamp": item["timestamp"],
                    "rsi": item["rsi"]
                } for item in data
            ]
        }
    elif endpoint == "sma":
        return {
            "ticker": ticker,
            "data": [
                {
                    "timestamp": item["timestamp"],
                    "sma": item["sma"]
                } for item in data
            ]
        }
    return data

def post_data_to_fastapi(ticker, endpoint, data):
    url = f"{FASTAPI_BASE_URL}{endpoint}/{ticker}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Successfully posted data to {url}")
    else:
        print(f"Failed to post data to {url}, Status Code: {response.status_code}, Response: {response.text}")

def main():
    endpoints_mapping = {
        "2y": "price",
        "rsi/2y": "rsi",
        "vol/2y": "vol",
        "sma/2y": "sma"
    }

    for ticker in tickers:
        for django_endpoint, fastapi_endpoint in endpoints_mapping.items():
            data = fetch_data_from_django(ticker, django_endpoint)
            if data:
                transformed_data = transform_data(ticker,fastapi_endpoint, data)
                post_data_to_fastapi(ticker, fastapi_endpoint, transformed_data)

if __name__ == "__main__":
    main()

