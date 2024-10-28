from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# Endpoint to handle incoming calls
@app.route("/incoming-call", methods=['POST'])
def incoming_call():
    response = VoiceResponse()
    response.say("Hello class, welcome to Sprint Presentation 2 from the Healthcare team. This is a test. Please leave a message after the beep.")
    # Record the caller's message and transcribe it
    response.record(transcribe=True, transcribe_callback="/transcription")
    return str(response)

# Endpoint to receive transcription
@app.route("/transcription", methods=['POST'])
def transcription():
    transcription_text = request.form['TranscriptionText']
    print("Transcription received:", transcription_text)
    
    # Save the transcription to a text file
    with open("transcriptions.txt", "a") as f:
        f.write(transcription_text + "\n")
    
    return "Transcription received", 200

# Start the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
