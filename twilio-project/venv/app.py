# app.py
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# Endpoint to handle incoming calls
@app.route("/incoming-call", methods=['POST'])
def incoming_call():
    response = VoiceResponse()
    response.say("Hello! Thank you for calling. We will connect you shortly.")
    # Additional call handling (e.g., forwarding to another number) can go here
    return str(response)

# Start the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
