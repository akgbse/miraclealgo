from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Fetch secret token from environment or use fallback
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_token_123")

@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Secret-Token")

    print("DEBUG >> Header Token Received:", token)
    print("DEBUG >> SECRET_TOKEN from .env:", SECRET_TOKEN)

    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Business logic starts here
    return jsonify({"status": "Webhook received"}), 200





