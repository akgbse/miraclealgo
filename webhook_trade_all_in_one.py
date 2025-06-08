import os
from flask import Flask, request, jsonify
import requests
from dhan_order import place_dhan_order
from telegram_alerts import send_telegram_alert
from trade_logger import log_trade

app = Flask(__name__)
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    header_token = request.headers.get("X-Secret-Token")
    print("DEBUG >> Header Token Received:", header_token)
    print("DEBUG >> SECRET_TOKEN from ENV:", SECRET_TOKEN)

    if header_token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    symbol = data.get("symbol", "")
    expiry = data.get("expiry_date", "")
    strike = data.get("strike_price", "")
    option_type = data.get("option_type", "")

    message = f"✅ SIGNAL: {symbol} {option_type} {strike} | Expiry: {expiry}"

    # Send alerts
    send_telegram_alert(message)
    send_whatsapp_alert(message)  # optional
    log_trade(symbol, expiry, strike, option_type)

    # Place order
    place_dhan_order(symbol, expiry, strike, option_type)

    return jsonify({"status": "Webhook received"}), 200

if __name__ == "__main__":
    app.run()







