from flask import Flask, request, redirect, url_for
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# Twilio client setup
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)
call_sid = None  # store call_sid here after initiating the call

@app.route('/start_call', methods=['POST'])
def start_call():
    global call_sid
    call = client.calls.create(
        to='+your_phone_number',
        from_='+twilio_phone_number',
        url=url_for('greeting', _external=True)
    )
    call_sid = call.sid
    return 'Call started!'

@app.route('/greeting', methods=['POST'])
def greeting():
    response = VoiceResponse()
    response.say("Hello! Press 1 to hear the first message or press 2 to hear the second.")
    
    gather = Gather(input="dtmf", num_digits=1, action=url_for('handle_choice', _external=True))
    response.append(gather)
    
    return str(response)

@app.route('/handle_choice', methods=['POST'])
def handle_choice():
    response = VoiceResponse()
    digits = request.form.get('Digits')

    if digits == '1':
        response.say("Here is your first message!")
    elif digits == '2':
        response.say("Here is your second message!")
    else:
        response.say("Invalid input. Please try again.")
        response.redirect(url_for('greeting', _external=True))
    
    return str(response)

@app.route('/send_custom_message', methods=['POST'])
def send_custom_message():
    # This can be called by a button in the Flask app to update Twilio's message mid-call.
    custom_message = "Your custom message here."
    response = VoiceResponse()
    response.say(custom_message)
    client.calls(call_sid).update(twiml=response)  # Update the call TwiML
    
    return "Custom message sent."

@app.route('/end_call', methods=['POST'])
def end_call():
    if call_sid:
        client.calls(call_sid).update(status="completed")
    return "Call ended."

if __name__ == '__main__':
    app.run(debug=True)
