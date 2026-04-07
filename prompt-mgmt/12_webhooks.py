"""Lab 12: Webhooks
Learn how to use webhooks in Langfuse to trigger actions based on events."""
import os
from dotenv import load_dotenv
load_dotenv()
import json
import hmac
import hashlib
from flask import Flask, request, jsonify
from threading import Thread
import time

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_BASE_URL")

from langfuse import Langfuse

langfuse = Langfuse()
app = Flask(__name__)

# Webhook secret for signature verification
WEBHOOK_SECRET = "your-webhook-secret"

def verify_signature(payload: str, signature: str) -> bool:
    """Verify webhook payload signature"""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# Event handlers
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-Langfuse-Signature", "")
    payload = request.get_data(as_text=True)

    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401

    event = json.loads(payload)
    event_type = event.get("type")

    print(f"Received event: {event_type}")

    # Handle different event types
    if event_type == "prompt.created":
        print(f"  New prompt created: {event.get('data', {}).get('name')}")
    elif event_type == "prompt.updated":
        print(f"  Prompt updated: {event.get('data', {}).get('name')}")
    elif event_type == "trace.created":
        print(f"  New trace: {event.get('data', {}).get('id')}")
    elif event_type == "score.created":
        print(f"  New score: {event.get('data', {}).get('name')}")

    return jsonify({"status": "received"}), 200

# Start webhook server in background
def run_webhook_server():
    app.run(port=5000, debug=False)

print("=== Webhooks Demo ===\n")

# Start webhook server
server_thread = Thread(target=run_webhook_server, daemon=True)
server_thread.start()
time.sleep(1)
print("Webhook server running on http://localhost:5000/webhook\n")

# Configure webhook in Langfuse (via UI or API)
print("=== Webhook Configuration ===")
print("1. In Langfuse: Settings > Webhooks")
print("2. Add webhook URL: http://your-server:5000/webhook")
print("3. Set secret: your-webhook-secret")
print("4. Select events to subscribe to")
print("\nAvailable events:")
print("  - prompt.created, prompt.updated, prompt.deleted")
print("  - trace.created, trace.updated")
print("  - score.created, score.updated")
print("  - observation.created")

# Create a test event
print("\n=== Triggering Test Event ===")
try:
    langfuse.observers.create(
        name="webhook-test",
        metadata={"test": True}
    )
    print("Event would trigger webhook (when configured)")
except Exception as e:
    print(f"Note: {e}")

print("\nWebhook server still running for testing...")
print("Press Ctrl+C to stop")
time.sleep(2)
