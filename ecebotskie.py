import random
import keys

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
bot = Bot(keys.ACCESS_TOKEN)

@app.route('/conversion_layer', methods=['POST', 'GET'])
def verify_token():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        if token == keys.VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return 'Invalid verification token'
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def get_message():
    sample_responses = ["Sprikitik!", "Sano kita mangangarigo?"]
    return random.choice(sample_responses)


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run(debug=True, port=4000 )
