import flask
import urllib.request
import json
import requests
import ast
from flask import request, jsonify
from flask_cors import CORS
import pickle

from .constants import *
from .allotment_bot import assistant_act3, CONTACT_TEXT, HELP_TEXT

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#flask process to host and allow cors
cors = CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/getwhatsappmessage', methods=['POST'])
def getwhatsappmessage():
    print('Getwhatsapp')
    print(request.data)
    eventsDict = json.loads(request.data)
    print('Getwhatsapp---json\n\n')
    print(eventsDict)

# {
#   "app": "DemoApp",
#   "timestamp": 1580227766370,
#   "version": 2,
#   "type": "message",
#   "payload": {
#     "id": "ABEGkYaYVSEEAhAL3SLAWwHKeKrt6s3FKB0c",
#     "source": "918x98xx21x4",
#     "type": "text",
#     "payload": {
#       "text": "Hi"
#     },
#     "sender": {
#       "phone": "918x98xx21x4",
#       "name": "Smit"
#     }
#   }
# }
    if eventsDict :
        resp = 'Please connect with us \n'+CONTACT_TEXT+'\n\n'+HELP_TEXT
        
        if 'type' in eventsDict and eventsDict['type'] == 'message':
            if 'payload' in eventsDict and 'payload' in eventsDict['payload'] and 'text' in eventsDict['payload']['payload']:
            
                input_data = eventsDict['payload']['payload']['text']
                phone = eventsDict['payload']['sender']['phone']

                print('Input from whatsappuser::',phone[2:],'::',input_data)

                flag, resp = assistant_act3(input_data, phone[2:], MODE_WHATSAPP)

                print('output from assistant_act1::',flag,'::',resp)
        
        elif 'type' in eventsDict and eventsDict['type'] == 'user-event':
            if 'payload' in eventsDict and 'type' in eventsDict['payload'] and eventsDict['payload']['type'] == 'opted-in':

                input_data = 'hi'
                phone = eventsDict['payload']['phone']

                print('Input from whatsappuser::',phone,'::',input_data)

                flag, resp = assistant_act3(input_data, phone[2:], MODE_WHATSAPP)

                print('output from assistant_act1::',flag,'::',resp)
        # elif 'type' in eventsDict and eventsDict['type'] == 'user-event'
    

    return resp, 201

def start_whatsapp_conversation_server():
    app.run(port=WHATSAPP_SERVER_PORT,host="0.0.0.0",use_reloader=False)