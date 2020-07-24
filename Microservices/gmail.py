from __future__ import print_function
from pandas import DataFrame
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from datetime import date
import email
import os.path
from os import path
import pickle
import urllib
import datetime
import pandas as pd
from email import encoders 
import urllib.request
import wget
import time
import webbrowser
import shutil
import re
from dateutil import parser as date_parser
from apiclient.http import BatchHttpRequest
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
from os.path import basename
from apiclient import errors
import flask
import requests
import json
import ast
import uuid
from flask import request, jsonify
from flask_cors import CORS
app = flask.Flask(__name__)
app.config["DEBUG"] = True
global service
#its automatically finds the download file path in any windows program
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


#its a url provided for google API
# SCOPES = [
#           'https://www.googleapis.com/auth/gmail.send',
#           'https://mail.google.com/',
#           'https://www.googleapis.com/auth/gmail.readonly',
#           'https://www.googleapis.com/auth/gmail.compose',
#           'https://www.googleapis.com/auth/gmail.labels',
#           'https://www.googleapis.com/auth/gmail.insert',
#           'https://www.googleapis.com/auth/gmail.modify',
#           'https://www.googleapis.com/auth/gmail.metadata',
#           'https://www.googleapis.com/auth/gmail.settings.basic',
#           'https://www.googleapis.com/auth/gmail.settings.sharing']
SCOPES =  ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.metadata',
          'https://www.googleapis.com/auth/gmail.addons.current.message.metadata',
          'https://www.googleapis.com/auth/gmail.addons.current.message.readonly',
          'https://www.googleapis.com/auth/gmail.addons.current.message.action']







def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  #   return {'raw': base64.urlsafe_b64encode(message.as_string())}
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}




# prepare the attachment with email
def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename,cc):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['Cc'] = cc
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEApplication(fp.read(), _subtype=sub_type,Name=basename(path))
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    encoders.encode_base64(msg)
    
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}



#function to fetch gmail mail based on no_of_days since which you want
def gmailIntegration(mails_Under_given_days):
    #delete the token.pickle which is unique for different users
    if(path.exists('token.pickle')):
        os.remove('token.pickle')
    #if the credentials.json is not present then only we go for a new one. if it is present we can use for n number of times.
    if(not path.exists('credentials.json')):
        #this gives the path where the credentials will be download
        src = get_download_path()
        #varialble to store the credentials path
        cred_path=''

        
        cred_path = src+'\credentials.json'
        #URL to open google page to enable GOOGLE API
        url='https://developers.google.com/gmail/api/quickstart/dotnet'

        #its for open in new tab
        webbrowser.open_new_tab(url)
        #wait before going to next step untill the credentials downloaded
        while(not path.exists(cred_path)):
            continue
        #move the downloaded credentials to the current dirrectory
        shutil.move(cred_path , os.getcwd())
        
    creds = None
    
    #these are all the steps to download token.pickle file (up to line 87)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)


    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return creds
    # # request for service from gmail
    service = build('gmail', 'v1', credentials=creds)
    return service







service =   gmailIntegration(1)
cors = CORS(app, resources={r"/sendmail": {"origins": "*"}})
@app.route('/sendmail', methods=['GET','POST'])
def api_send_mail():
    print(service)
    print("\n\n",request.data)
    # dict_ = request.data.decode('utf-8')
    mydata =  json.loads(request.data)["data"]
    print("request to send mail",mydata)
    message = CreateMessage(mydata['from_id'],mydata['to_id'],mydata['subject'],mydata['message'])
    mess = service.users().messages().send(userId='me', body=message).execute()
    return mess

#part that send the mail with attachment
cors = CORS(app, resources={r"/sendmail/Attachment": {"origins": "*"}})
@app.route('/sendmail/Attachment', methods=['GET','POST'])
def api_send_mail_attachment():
    print(service)
    mydata =  json.loads(request.data)["data"]
    print("request to send mail",mydata)
    print("request to send mail with attachment")
    message = CreateMessageWithAttachment("franklin@cloobot.com",mydata['to'],"send via gmail","Testing",r"C:\Users\Clooot\Desktop\programs\voice assistant",'quotation.xlsx',mydata['cc'])
    mess = service.users().messages().send(userId='me', body=message).execute()
    return mess
  
# cors = CORS(app, resources={r"/push-notify": {"origins": "*"}})
# @app.route('/push-notify', methods=['GET','POST'])
def recieve_push_notifiction():
  # return {"status":"ok"}
  print(service)
  print("request to send push notification")
  request = {
  'labelIds': ['INBOX'],
  'topicName': 'projects/quickstart-1592291459270/topics/quickstart'}
  print("request for subscription succesful")
  mess = service.users().watch(userId='me', body=request).execute()
  return mess

# cors = CORS(app, resources={r"/readmail": {"origins": "*"}})
# @app.route('/readmail', methods=['GET','POST'])
def api_get_mail_attachment():
    print(service)
    print("request to get mail with attachment")
    #list to extend(store) messages in corresponding pages
    messages = []

    # Call the Gmail API to fetch INBOX
    # get initialy upto 500 messages
    results = service.users().messages().list(userId='me',maxResults=500).execute()
    print("first res       :          ",len(results))
    #extract messages to messages varialbe from result becaue we use "result" varialbe for n times
    messages.extend(results['messages'])

    batch = BatchHttpRequest()
    message_batch=[]
    batch_count = 0
    def callback(request_id, response, exception):
        
        if exception is not None:
            pass
        else:
            message_batch.append(response)
            
    for mes in messages:
        batch.add(service.users().messages().get(userId='me', id=mes['id']),callback = callback)
    batch.execute()
    #collect all messages based on pagetoken wise
    batch_count = 1
    while('nextPageToken' in results):
        batch_count =batch_count + 1
        print(batch_count)
        messages = []
        page_token = results['nextPageToken']
        results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=500).execute()
        messages.extend(results['messages'])
        print("messages length : ",len(messages))
        print("result length : ",len(results))
        for mes in messages:
            batch.add(service.users().messages().get(userId='me', id=mes['id']),callback = callback)
        batch.execute()
        batch = BatchHttpRequest()
        print("batch {0} ended".format(batch_count))
        if(batch_count == 2):
            break

    print(messages)
    for message in message_batch:
      try:
        for part in message['payload']['parts']:
          if part['filename']:
            if 'data' in part['body']:
              data = part['body']['data']
            else:
              print("\n\n\n\n\n\nHere it is\n\n\n\n\n\n")
              att_id = part['body']['attachmentId']
              att = service.users().messages().attachments().get(userId='me', messageId=message['id'],id=att_id).execute()
              print("\n\n\att",att)
              data = att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            print('\n\n',part['filename'],'\n\n')
            path = part['filename']
            with open(path, 'wb') as f:
              f.write(file_data)
            f.close()
            print("\n\nfile close\n\n")  
     
      except:
        print("error")
     
    return "file in your dirrectory"

def get_message(msg_id):
  m = service.users().messages().get(userId='me', id=msg_id).execute()
  return m


def ListHistory(start_history_id):
  print("\n\n\n",start_history_id,"\n\n\n")
  """List History of all changes to the user's mailbox.

  Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      start_history_id: Only return Histories at or after start_history_id.

  Returns:
      A list of mailbox changes that occurred after the start_history_id.
  """
  try:
    history = (service.users().history().list(userId='me',
                                            startHistoryId=start_history_id)
            .execute())
    changes = history['history'] if 'history' in history else []
    while 'nextPageToken' in history:
      page_token = history['nextPageToken']
      history = (service.users().history().list(userId='me',
                                          startHistoryId=start_history_id,
                                          pageToken=page_token).execute())
      changes.extend(history['history'])

    return changes
  except errors.HttpError:
    print('error')
def GetMessage( user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  # try:
  #   # message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    
    # print("Message snippet",message['snippet'])
  message = service.users().messages().get(userId='me', id = msg_id).execute()
  print("\nhi\n")
  print(message)
  return message
  # except errors.HttpError:
  #   print("error")
# print(gmailIntegration(1))

app.run(port='8002',use_reloader=False)