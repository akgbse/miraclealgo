import os
import requests

def place_dhan_order(symbol, expiry_date, strike_price, option_type):
    url = "https://api.dhan.co/orders"
    headers = {
        "access-token": os.getenv("ACCESS_TOKEN"),
        "Content-Type": "application/json",
        "Client-Id": os.getenv("CLIENT_ID")
    }

    # Construct Dhan symbol
    full_symbol = f"{symbol}{expiry_date.replace('-', '')}{strike_price}{option_type.upper()}"
    
    order_data = {
        "security_id": full_symbol,
        "exchange_segment": "NSE_EQ",   # adjust if needed (e.g., "NSE_OPTIDX")
        "product_type": "INTRADAY",
        "order_type": "MARKET",
        "transaction_type": "BUY",
        "quantity": 50  # one lot, change if needed
    }

    response = requests.post(url, json=order_data, headers=headers)
    print("Dhan Response:", response.status_code, response.text)
