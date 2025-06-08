from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    # Simple test logic
    print("Received:", data)
    return jsonify({"status": "Webhook received", "data": data}), 200

if __name__ == "__main__":
    app.run(debug=True)
