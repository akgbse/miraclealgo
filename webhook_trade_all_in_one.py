from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

# Secret token for security
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_token_123")

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

def send_sms(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=TO_NUMBER
        )
    except Exception as e:
        print("SMS Error:", e)

@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        symbol = data.get("symbol")
        expiry = data.get("expiry_date")
        strike = data.get("strike_price")
        opt_type = data.get("option_type")

        # Compose SMS message
        sms_text = f"🔔 Signal:\nSymbol: {symbol}\nExpiry: {expiry}\nStrike: {strike}\nType: {opt_type}"
        send_sms(sms_text)

        return jsonify({
            "status": "Webhook received",
            "data": data
        }), 200

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)


    except Exception as e:
        print("Webhook processing error:", str(e))
        return jsonify({"error": str(e)}), 500


