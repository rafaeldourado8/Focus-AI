"""
WhatsApp Bot Example using Cerberus AI

Requires: twilio, cerberus-ai-python
"""

from twilio.rest import Client
from cerberus_ai import CerberusAI
import os

# Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CERBERUS_API_KEY = os.getenv("CERBERUS_API_KEY")

# Initialize clients
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
cerberus = CerberusAI(api_key=CERBERUS_API_KEY)


def handle_message(from_number: str, message: str):
    """Handle incoming WhatsApp message"""
    try:
        # Get response from Cerberus AI
        response = cerberus.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant on WhatsApp."},
                {"role": "user", "content": message}
            ],
            model="cerberus-lite"
        )
        
        reply = response["choices"][0]["message"]["content"]
        
        # Send WhatsApp message
        twilio_client.messages.create(
            body=reply,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{from_number}'
        )
        
    except Exception as e:
        print(f"Error: {e}")


# Flask webhook
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    from_number = request.form.get("From").replace("whatsapp:", "")
    message = request.form.get("Body")
    handle_message(from_number, message)
    return "", 200

if __name__ == "__main__":
    app.run(port=5000)
