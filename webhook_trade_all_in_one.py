from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

# Secret for validating webhook
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_token_123")

# Twilio function
def send_sms(message):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_FROM_NUMBER"),
        to=os.getenv("TO_NUMBER")
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        symbol = data.get("symbol")
        strike = data.get("strike_price")
        opt_type = data.get("option_type")
        expiry = data.get("expiry_date")

        message = (
            f"📈 Trade Signal\n"
            f"Symbol: {symbol}\n"
            f"Strike: {strike} {opt_type}\n"
            f"Expiry: {expiry}"
        )

        send_sms(message)

        return jsonify({"status": "Webhook received", "data": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Render gunicorn deployment
if __name__ == "__main__":
    app.run(debug=True)



    except Exception as e:
        print("Webhook processing error:", str(e))
        return jsonify({"error": str(e)}), 500


