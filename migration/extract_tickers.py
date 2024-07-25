import json

def extract_tickers(data):
    tickers = [item["ticker"] for item in data]
    return tickers

if __name__ == "__main__":
    # Load the data from stocks.json
    with open('../stocks.json', 'r') as file:
        data = json.load(file)

    # Extract the tickers
    tickers = extract_tickers(data)

    # Save the tickers to tickers.json
    with open('../tickers.json', 'w') as file:
        json.dump(tickers, file, indent=4)

    print("Tickers have been written to tickers.json")
