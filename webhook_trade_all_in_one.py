from flask import Flask, request, jsonify
from telegram_alerts import send_telegram_alert
import os

app = Flask(__name__)

# Load secret token from environment
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

@app.route("/")
def home():
    return "Webhook Server Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        # Check secret token
        token = request.headers.get("X-Secret-Token")
        if token != SECRET_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()

        # Extract fields
        symbol = data.get("symbol")
        strike_price = data.get("strike_price")
        expiry_date = data.get("expiry_date")
        option_type = data.get("option_type")

        # Compose and send Telegram alert
        alert_msg = (
            f"🚀 *Trade Alert Received!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Strike:* `{strike_price}`\n"
            f"*Type:* `{option_type}`\n"
            f"*Expiry:* `{expiry_date}`"
        )
        send_telegram_alert(alert_msg)

        # (Future) Place Dhan order or send SMS etc.

        return jsonify({"status": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(debug=True)






