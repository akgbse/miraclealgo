from flask import Flask, request, jsonify
import os
from dhan_order import place_dhan_order
from telegram_alerts import send_telegram_alert
from trade_logger import log_trade

app = Flask(__name__)

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Process trade signal
    symbol = data.get("symbol")
    expiry_date = data.get("expiry_date")
    strike_price = data.get("strike_price")
    option_type = data.get("option_type")

    if not all([symbol, expiry_date, strike_price, option_type]):
        return jsonify({"error": "Missing required fields"}), 400

    order_response = place_dhan_order(symbol, expiry_date, strike_price, option_type)
    alert_msg = f"Trade Placed: {symbol} {strike_price} {option_type} | {order_response}"
    send_telegram_alert(alert_msg)
    log_trade(symbol, expiry_date, strike_price, option_type, order_response)

    return jsonify({"status": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(debug=True)








