from dotenv import load_dotenv
import finnhub
import json
import os
import requests

load_dotenv()

finnhub_api_key = os.getenv("FINNHUB_API_KEY")
if not finnhub_api_key:
    raise ValueError("FINNHUB_API_KEY environment variable is not set.")

def lookup(symbol):
    """
    finnhub_client = finnhub.Client(api_key=finnhub_api_key)
    output = finnhub_client.symbol_lookup(symbol)
    data = output.json()
    for item in data['result']:
        if item['symbol'] == symbol:
            return item['currentPrice']
    """

    try:
        response = requests.get(f"https://finance.cs50.io/quote?symbol={symbol.upper}")
        response.raise_for_status()
        data = response.json()
        return {
            "name": data["companyName"],
            "price": data["latestPrice"],
            "symbol": symbol.upper()
        }
    
    except requests.RequestException as e:
        print(f"Error getting request: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error parsing data: {e}")
    except Exception as e:
        print(f"Some other error I didn't think of")
    
    return None