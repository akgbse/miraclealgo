from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        # Check for required keys
        required_keys = ["symbol", "expiry_date", "strike_price", "option_type"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing field: {key}"}), 400

        # Log received payload
        print("Received Webhook Data:", data)

        # Respond
        return jsonify({
            "status": "Webhook received",
            "data": data
        }), 200

    except Exception as e:
        print("Webhook processing error:", str(e))
        return jsonify({"error": str(e)}), 500


