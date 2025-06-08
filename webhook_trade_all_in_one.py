from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_token_123")

@app.route("/webhook", methods=["POST"])
def webhook():
    # Check secret token
    token = request.headers.get("X-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Log to file
    with open("logs.txt", "a") as f:
        f.write(f"Received: {data}\n")

    # Step 1: Extract info
    symbol = data.get("symbol")
    expiry_date = data.get("expiry_date")
    strike_price = data.get("strike_price")
    option_type = data.get("option_type")

    # Step 2: Placeholder - Real Dhan call logic will go here
    option_data = {
        "symbol": symbol,
        "expiry": expiry_date,
        "strike": strike_price,
        "type": option_type,
        "price": "Mocked LTP 142.50"
    }

    # Step 3: SMS alert (mock message for now)
    from twilio.rest import Client
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    sms_body = f"[Trade Alert] {symbol} {strike_price}{option_type} Exp:{expiry_date} @ {option_data['price']}"
    client.messages.create(
        body=sms_body,
        from_=os.getenv("TWILIO_FROM_NUMBER"),
        to=os.getenv("TO_NUMBER")
    )

    return jsonify({
        "status": "Trade alert sent",
        "data": option_data
    }), 200

# Gunicorn expects this object
if __name__ == "__main__":
    app.run()

