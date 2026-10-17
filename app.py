import os
import sys

# Ensure current directory is always in sys.path for robust imports across all environments
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
import chatbot

app = Flask(__name__)

# Security & limits: Maximum payload size (16 KB is more than plenty for chat messages)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024


@app.route("/")
def home():
    """Renders the main BlueDesk help desk web interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat_api():
    """
    Accepts JSON payload: {"message": "user input"}
    Returns JSON response: {"reply": "chatbot response", "status": "success"}
    """
    try:
        # Verify content type and parse JSON
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Invalid request format. Request body must be JSON."
            }), 400

        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Malformed JSON payload."
            }), 400

        user_message = data.get("message")
        if user_message is None or not isinstance(user_message, str):
            return jsonify({
                "status": "error",
                "message": "The 'message' field is required and must be a string."
            }), 400

        # Pass message to the Python rule-based engine
        reply = chatbot.get_response(user_message)

        return jsonify({
            "status": "success",
            "reply": reply
        }), 200

    except Exception:
        # Secure failure handling: Never leak internal traceback to client
        return jsonify({
            "status": "error",
            "message": "An internal error occurred while processing your message."
        }), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Resource not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify({"status": "error", "message": "Message is too large"}), 413


if __name__ == "__main__":
    # Local development server (debug set to False for standard safe operation)
    print("Starting BlueDesk server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=False)
