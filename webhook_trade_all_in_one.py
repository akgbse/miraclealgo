from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import csv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Load environment variables
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

@app.route("/", methods=["GET"])
def home():
    return "✅ MiracleAlgo Webhook Server is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Secret-Token")

print("DEBUG >> Header Token Received:", token)
print("DEBUG >> SECRET_TOKEN from .env:", SECRET_TOKEN)

if token != SECRET_TOKEN:
    return jsonify({"error": "Unauthorized"}), 401


    try:
        data = request.json

        # Format message
        message = f"""
🚨 New Trade Signal 🚨
Symbol: {data.get("symbol1")}
Expiry: {data.get("expiry_date")}
Strike: {data.get("strike_price")}
Type: {data.get("option_type")}
Time: {datetime.now().strftime('%H:%M:%S')}
"""

        # Send SMS
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message.strip(),
            from_=TWILIO_FROM_NUMBER,
            to=TO_NUMBER
        )

        # Save log to CSV
        with open("trade_log.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                data.get("symbol1"),
                data.get("strike_price"),
                data.get("expiry_date"),
                data.get("option_type"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

        return jsonify({"data": data, "status": "Webhook received"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)




