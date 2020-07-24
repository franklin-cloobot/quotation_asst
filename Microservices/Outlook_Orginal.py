from urllib.parse import quote, urlencode
import base64
import json
import ast
import pandas as pd
from datetime import datetime
import flask
import requests
import uuid
from time import sleep,time
from dateutil import tz,parser as date_parser
import re
from flask import request, jsonify,redirect,url_for
from pandas.io.json import json_normalize
from flask_cors import CORS
from bs4 import BeautifulSoup
import webbrowser

API_ROOT = "rpm.cloobot.ai"
OUTLOOK_PORT = 8204

# don't forget to init the library first
# it loads machine learning classifiers



#initialize the global variables
skipINCREMENT = 1000
skipValue = 0
access_token_flag = 0
access_token = None
refresh_token = None
access_token_start_time = None
data_frame_excel = pd.DataFrame()
uniqueMessage_dataFrame = pd.DataFrame()
huge_messages = []
stopValue = 1000
headers={ 'Content-Type' : 'application/json' }

# Redirect_uri is used to get the token and it is created by admin of this app and he will create azure app and register the details of permissions for getting all user's data
redirect_uri = "https://"+API_ROOT+":"+ str(OUTLOOK_PORT) +"/tutorial/gettoken/"
redirect_uri_2 = "https://"+API_ROOT+":"+ str(OUTLOOK_PORT) +"/logout" # logout url to unknown address

# Client ID and secret
graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# this id and secret is admin which will create an app in azure
client_id = '19757c90-9580-4c95-b5da-6101553756cd'
client_secret = 'JpA]?O=.NWOAzKKGYgPhM4ogoU7aK2s3'

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = [ 'openid',
           'offline_access',
           'User.Read',
           'Mail.Read',
           'Mail.Send',
           'Notifications.ReadWrite.CreatedByApp' ]

#logout url
logout_url = "https://login.windows.net/common/oauth2/logout?post_logout_redirect_uri="

# def get_outlook_server_details():
#     return API_ROOT, str(OUTLOOK_PORT)

# sign in form from the microsoft and after user sign_in with his credentials and allow permissions to access his data

def get_signin_url(redirect_uri):
    # Build the query parameters for the signin url
    params = { 'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code',
                'scope': ' '.join(str(i) for i in scopes)
                }

    signin_url = authorize_url.format(urlencode(params))
    return signin_url


# getting token using auth_code and redirect_uri
def get_token_from_code(auth_code, redirect_uri):
    # Build the post form for the token request
    post_data = { 'grant_type': 'authorization_code',
                    'code': auth_code,
                    'redirect_uri': redirect_uri,
                    'scope': ' '.join(str(i) for i in scopes),
                    'client_id': client_id,
                    'client_secret': client_secret
                }

    r = requests.post(token_url, data = post_data)

    try:
        return r.json()
        
    except:
        print("\n text type :" , type(r.text),'\n')
        r=eval(r.text)
        
        return r





# refershing token if the current access token expires
def get_token_from_refresh_token(refresh_token, redirect_uri):
    # api call for refresh token 
    # new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)
    
    print("\n\n\n\n\n Calling Refresh Token \n\n\n\n\n")
    # Build the post form for the token request
    post_data = { 'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'redirect_uri': redirect_uri,
                    'scope': ' '.join(str(i) for i in scopes),
                    'client_id': client_id,
                    'client_secret': client_secret
                }

    r = requests.post(token_url, data = post_data)

    try:
        return r.json()
    except:
        print("\n text type :" , type(r.text),'\n')
        r=eval(r.text)
    
        return r




# getting auth code and redirect uri to combine to get the token
# getting token from the respect user id with his permissions

def gettoken(request):
    auth_code = request.args.get('code')
    print("#########@!$@#$@!#@!###########V           ",auth_code)
    token = get_token_from_code(auth_code,redirect_uri)
    access_token = token['access_token']
    refresh_token = token['refresh_token']
    # print("User has been LogOut the session")
    print("\n access token : {0}\n".format(access_token))
    return access_token,refresh_token
    
  
# Generic API Sending
def make_api_call(method, url, token, payload = None, parameters = None):
    # Send these headers with all API calls

    headers = { 'User-Agent' : 'python_tutorial/1.0',
                'Authorization' : 'Bearer {0}'.format(token),
                'Accept' : 'application/json'}

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = { 'client-request-id' : request_id,
                        'return-client-request-id' : 'true' }

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers = headers, params = parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

    return response



#send_mail method
cors = CORS(app, resources={r"/sendMail": {"origins": "*"}})
@app.route('/sendMail', methods=['GET','POST'])
def send_mail():    
    get_me_url = graph_endpoint.format('/me/sendMail')
    
    send_data = json.loads(request.data)["send_data"]
    
    print('\n\n\n\n SEND MAIL TOKEN : ',access_token,'\n\n\n\n\n')

    r = make_api_call('POST', get_me_url, access_token, payload=send_data,parameters="")

    if (r.status_code == 202):
        print("{0}: {1}".format(r.status_code, r.text))
        output_status = {'status':r.status_code}
        return output_status
    else:
        print("{0}: {1}".format(r.status_code, r.text))
        output_status = {'status':r.status_code}
        return output_status
        

# getting user name of the respect credentials user id
def get_me(access_token):
    get_me_url = graph_endpoint.format('/me')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {'$select': 'displayName,mail'}

    r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

    if (r.status_code == 200):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)



# getting messages using the accessing tokens for the respect email id based on url

def get_my_messages(access_token,skipValue):
    get_messages_url = graph_endpoint.format('/me/messages')

    # For Checking 
    print(skipValue)

    # Use OData query parameters to control the results
    #  - Only first 10 results returned
    #  - Only return the ReceivedDateTime, Subject, and From fields
    #  - Sort the results by the ReceivedDateTime field in descending order
    query_parameters = {'$top': '10',
                        '$select': 'sentDateTime,subject,from,ToRecipients,ReplyTo,ConversationId,ccRecipients,isDraft,body,uniqueBody',
                        '$orderby': 'sentDateTime DESC',
                        '$skip': str(skipValue)}

    r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

    if (r.status_code == 200):
        return r.json()
    elif (r.status_code == 504):
        print("{0}: {1}".format(r.status_code, r.text))
        sleep(5)
        get_my_messages(access_token,skipValue)
    else:
        print("{0}: {1}".format(r.status_code, r.text))
        sleep(5)
        get_my_messages(access_token,skipValue)



# Function which extract messages into "From,To,Subject,Body,Thread_Id"

def extractingMessages(huge_messages):  
    global data_frame_excel
    From = []
    To = []
    Sub = []
    Body = []
    Thread_id = []
    resp = []
    Recipients = []
    full_body = []
    Date = []
    count = 0
    # india_timezone = tz.gettz('Asia/Kolkata')
    for huge_msg in huge_messages:
        for each_mes in huge_msg['value']:
            to_list = []
            signatures = ''
            signatures1 = ''
            signatures2 = ''
            text = ''
            text1 = ''
            text2 = ''
            count = count+1
            print(count)
            if each_mes['isDraft'] == False:
                try:
                    for iterate in each_mes['toRecipients']:
                        to_list.append(iterate['emailAddress']['address'])
                    To.append(to_list)
                    # To.append(each_mes['toRecipients'][0]['emailAddress']['address'])
                except KeyError:
                    To.append("UnkownEmailId")
                except IndexError:
                    To.append("UnkownEmailId")
                try:
                    From.append(each_mes['from']['emailAddress']['address'])
                except KeyError:
                    From.append("UnkownEmailId")
                except IndexError:
                    From.append("UnkownEmailId")
                try:
                    Sub.append(each_mes['subject'])
                except KeyError:
                    Sub.append("No Subject")
                except IndexError:
                    Sub.append("No Subject")
                try:
                    resp = [each_mes['from']['emailAddress']['address']]
                    for i in each_mes['ccRecipients']:
                        resp.append(i['emailAddress']['name'])
                    Recipients.append(resp)
                except:
                    Recipients.append("Unknown")
                try:
                    soup = BeautifulSoup(each_mes['uniqueBody']['content'], 'html.parser')
                    elements = soup.find_all("div", id="Signature")
                    for element in elements:
                        element.decompose()
                    body_str = soup.get_text().encode("ascii", "ignore").decode("utf-8")
                    body_str = re.sub(r'(\n\s*)+\n+', '\n\n', body_str) 
                    
                    body_str = re.sub('<!--(.*?|\n)*?-->',"",body_str)
                    Body.append(body_str)
                    # full_body.append(body_str)
                    # if('From:' in body_str):
                    #     body_str = body_str.split('From:')[0]
                    # individual_body_splitted_recepients = []
                    # for i in resp:
                    #     text, signatures = signature.extract(body_str,sender=i)
                    #     text1, signatures1 = signature.extract(str(text)+"None",sender=i)
                    #     text2, signatures2 = signature.extract(str(signatures)+"None",sender=i)
                    #     individual_body_splitted_recepients.append(re.sub("None","",(str(text1)+str(text2))))
                    # if(individual_body_splitted_recepients == []):
                    #     Body.append('No Body Content')
                    # else:
                    #     Body.append(min(individual_body_splitted_recepients))   # taking minimum because parsed body will have less length
                except KeyError:
                    Body.append("No Body Content")
                except IndexError:
                    Body.append("No Body Content")
                try:
                    Thread_id.append(each_mes['conversationId'])
                except KeyError:
                    Thread_id.append("No Thread_Id")
                except IndexError:
                    Thread_id.append("No Thread_Id")
                try:
                    # print(date_parser.parse(each_mes['sentDateTime'],fuzzy=True))
                    Date.append(date_parser.parse(each_mes['sentDateTime'],fuzzy=True).replace(tzinfo=None))
                except KeyError:
                    Date.append("No DateTime")
                except IndexError:
                    Date.append("No DateTime")

    # dump all the list value in the dataframe
    data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

    # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime
    data_frame_excel = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)

    try:
        data_frame_excel['TimeDate'] = data_frame_excel['TimeDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    except AttributeError:
        data_frame_excel['TimeDate'] = data_frame_excel['TimeDate'].astype(str)

    # for reference to save as csv file 
    data_frame_excel.to_csv("huge.csv")
    return data_frame_excel



# Function is getting token from the microsoft authority and getting huge number of messages and extracting to form the dataframe for columns like "From,To,Subject,Body,Thread_Id"

cors = CORS(app, resources={r"/tutorial/gettoken/": {"origins": "*"}})
@app.route('/tutorial/gettoken/', methods=['GET','POST'])
def getting_DataFromOutlook():
    
    global access_token
    global access_token_flag
    global refresh_token
    global access_token_start_time
    

    access_token,refresh_token =  gettoken(request)

    if access_token!=None:
        access_token_flag = 1

    print("\n access token 2 :{0} \n".format(access_token))

    access_token_start_time = datetime.fromtimestamp(time())

    print("Current Time To Check",access_token_start_time)

    return "The authentication flow has completed. You may close this window."





cors = CORS(app, resources={r"/getMessages_fromOutlook": {"origins": "*"}})
@app.route('/getMessages_fromOutlook', methods=['GET','POST'])
def getData_fromOutlook():
    print("\n\n\n\n\n\n++++++++++++++++++++++++++++++++++++++Get My Messages++++++++++++++++++++++++++++++++++++++++++++++\n\n\n\n\n")

    global skipValue
    global skipINCREMENT
    global huge_messages
    global stopValue
    global access_token
    global refresh_token
    global access_token_start_time

    print("\n\n\n\n\n\nAccess Token For Getting Messages\n",access_token,"\n\n\n\n\n")
    
    expires_time = datetime.fromtimestamp(time()) - access_token_start_time
    seconds = expires_time.total_seconds()
    minutes = (seconds % 3600) // 60


    if minutes > 29:
        new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)
        refresh_token = new_tokens['refresh_token']
        access_token = new_tokens['access_token']
        access_token_start_time = datetime.fromtimestamp(time())

    
    skipValue = 0
    huge_messages = []

    while(True):
        messages = get_my_messages(access_token,skipValue)
        huge_messages.append(messages)
        skipValue = skipValue + skipINCREMENT
        if skipValue == stopValue:
            break
    # print(huge_messages)
    
    data_frame_excel = extractingMessages(huge_messages)


    output_dict = {'data_frame':(data_frame_excel).to_json()}
    

    return json.dumps(str(output_dict))








#flask process to host
cors = CORS(app, resources={r"/outlook_run": {"origins": "*"}})
@app.route('/outlook_run', methods=['GET','POST'])
def outlook_main():
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
    webbrowser.open(get_signin_url('https://'+API_ROOT+':'+ str(OUTLOOK_PORT) +'/tutorial/gettoken/'))

    while data_frame_excel.empty:
        continue
    
    print("*********************Data Had Been Stored********************************")  
    output_dict = {'data_frame':(data_frame_excel).to_json()}
    return json.dumps(str(output_dict))

    

#flask process to host
cors = CORS(app, resources={r"/businessOutlook": {"origins": "*"}})
@app.route('/businessOutlook', methods=['GET','POST'])
def outlookSync():
    print("\n\n\n\n\n\n++++++++++++++++++++++++++++++++++++++BusinessOutlook++++++++++++++++++++++++++++++++++++++++++++++\n\n\n\n\n")
    webbrowser.open(get_signin_url('https://'+API_ROOT+':'+ str(OUTLOOK_PORT) +'/tutorial/gettoken/'))
    
    while access_token_flag == 0:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
    
    return "TRUE"




#flask process to host
cors = CORS(app, resources={r"/logout": {"origins": "*"}})
@app.route('/logout',methods=['GET','POST'])
def logout_session():

    # redirecting url to logout the outlook
    url = logout_url+redirect_uri_2
    webbrowser.open(url)

    sleep(3)
    return "Logged Out Successfully. You may close this window."


print("\n\nOpen a browser and ping this url:\n", get_signin_url('https://'+API_ROOT+':'+ str(OUTLOOK_PORT) +'/tutorial/gettoken/'))

context = ('/etc/letsencrypt/live/rpm.cloobot.ai/fullchain.pem', '/etc/letsencrypt/live/rpm.cloobot.ai/privkey.pem')

app.run(port=OUTLOOK_PORT,host="0.0.0.0",use_reloader=False,ssl_context=context)