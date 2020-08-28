import flask
import requests
import json
import ast
import uuid
import jwt
import datetime
import time
from components.pagedata import *
from flask import request, jsonify
from flask import send_file,make_response
from flask import Flask, request, redirect, jsonify, send_file
from flask_cors import CORS,cross_origin
import base64
from flask_cors import CORS
app = flask.Flask(__name__)
from bachend_insert import insert_data
app.config["DEBUG"] = True
import os
import pandas as pd
import psycopg2
from datetime import datetime
import pytz
conn = psycopg2.connect(database="allotment", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="allotment", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")

JWT_EXP_DELTA_SECONDS = 86400

cur = conn.cursor()
cors = CORS(app, resources={r"/": {"origins": "*"}})
cust_id = {"id":''}
cur = conn.cursor()

import urllib.request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Assets'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/multiple-files-upload', methods=['POST', 'GET','OPTIONS'])
@cross_origin(supports_credentials=True)
def upload_file():
    # if request.method == 'POST':
    # return 'sss'
	# if 'files[]' not in request.files:
    print(request.files)
    if 'attachments' not in request.files:
        
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
	#
	# #files = request.files.getlist('files[]')
    files = request.files.getlist('attachments')
    print("file : ",files)
    errors = {}
    success = False
    for file in files:
        print("file : ",file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save("Assets/"+filename)
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        insert_data()
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

    if success:
        insert_data()
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
    return resp

@app.route('/template', methods=['POST', 'GET','OPTIONS'])
@cross_origin(supports_credentials=True)
def download():
    print(os.path.abspath("master.xlsx"))
    return send_file('Assets/master.xlsx', attachment_filename='master.xlsx')
	


def valid_user(token):
    #below is token validation fetch user details one by one from user table and try to decode the token
    cur.execute("select cust_email,cust_password from customer")
    user_info = cur.fetchall()
    for each_user in user_info:
        try:
            print("\n\n\n each user",each_user,"\n\n\n")
            decode = jwt.decode(token,each_user[1], algorithm='HS256')
            print("\n\n\n decode",decode,"\n\n\n")
            if decode['user_id'] == each_user[0]:
                print("\n\n valid token \n\n")
                return {"status":"ok"}
            
        except:
            print("\n\n\nerror in jwt\n\n\n")
            continue
    return {"data":'False'}

cors = CORS(app, resources={r"/project": {"origins": "*"}})
@app.route('/project', methods=['GET','POST'])
def session_start():
    output = []
    link = "https://drive.google.com/drive/folders/1XNhn3Ji0WP7JXGBti3hpY5xm0lu4m4Dp?usp=sharing"
    output = [  {"p_id":"101","project_name":"Project 1","project_details":"Description","project_docs":link,"project_man_over":1,"project_type":"Airtel","project_tl":"franklin","p_actual_start_date":"11-08-2020 10:00AM","p_actual_end_date":"Not yet Completed","project_chain_loop":[{"u_id":"ut101","role":"CE","name":"ajith","status":"Done","details":"details","start":"11-08-2020 10:00AM","end":"11-08-2020 4:00PM"},{"u_id":"ut102","role":"QC","name":"sankar","status":"Done","details":"details","start":"11-08-2020 5:00PM","end":"11-08-2020 6:00PM"},{"u_id":"ut103","role":"APP","name":"tej","status":"In complete","details":"details","start":"12-08-2020 10:00AM","end":"Not Completed"}],"project_state":"In approval"},
                {"p_id":"102","project_name":"Project 2","project_details":"Description","project_docs":link,"project_man_over":0,"project_type":"Vodafone","project_tl":"cyril","p_actual_start_date":"12-08-2020 11:00AM","p_actual_end_date":"Not yet Completed","project_chain_loop":[{"u_id":"ut103","role":"CE","name":"sri pradha","status":"Done","details":"details","start":"12-08-2020 10:00AM","end":"12-08-2020 2:00PM"},{"u_id":"ut104","role":"QC","name":"vinoodh","status":"InCompleted","details":"details","start":"12-08-2020 03:30PM","end":"Not Completed"}],"project_state":"In quality check"},
                {"p_id":"103","project_name":"Project 3","project_details":"Description","project_docs":link,"project_man_over":1,"project_type":"Idea","project_tl":"franklin","p_actual_start_date":"10-08-2020 09:00AM","p_actual_end_date":"10-08-2020 4:00 PM","project_chain_loop":[{"u_id":"ut101","role":"CE","name":"ajith","status":"Done","details":"details","start":"12-08-2020 10:00AM","end":"12-08-2020 1:00PM"},{"u_id":"ut102","role":"QC","name":"sankar","status":"Done","details":"details","start":"12-08-2020 1:00PM","end":"12-08-2020 3:00PM"},{"u_id":"ut103","role":"APP","name":"tej","status":"Done","details":"details","start":"12-08-2020 6:00PM","end":"12-08-2020 8:00PM"}],"project_state":"Done"},
                {"p_id":"104","project_name":"Project 4","project_details":"Description","project_docs":link,"project_man_over":0,"project_type":"TMobile","project_tl":"cyril","p_actual_start_date":"11-08-2020 10:00AM","p_actual_end_date":"Not yet Completed","project_chain_loop":[{"u_id":"ut101","role":"CE","name":"ajith","status":"Incomplete","details":"details","start":"11-08-2020 5:00PM","end":"Not Completed"}],"project_state":"Authering"},
                {"p_id":"105","project_name":"Project 5","project_details":"Description","project_docs":link,"project_man_over":1,"project_type":"Jio","project_tl":"cyril","p_actual_start_date":"Not started","p_actual_end_date":"Not started","project_chain_loop":[],"project_state":"To be alloted"}]
    return {"table":output,"total_items":5}
# dict_ = request.data.decode("UTF-8")
# print("\n\n\n at receiving comming",dict_,"\n\n\n")
# mydata1 = ast.literal_eval(dict_) 
# print(mydata1)
# cur.execute("select * from project")
# proj_list = cur.fetchall()
# output = []
# for each_proj in proj_list:
#     if(each_proj[10] != 0):
#         allot = datetime.fromtimestamp(each_proj[10])
#     else:
#         allot = "-"

#     if(each_proj[11] != 0):
#         done = datetime.fromtimestamp(each_proj[11])
#     else:
#         done = "-"

#     if(each_proj[12] != 0):
#         rem = datetime.fromtimestamp(each_proj[12])
#     else:
#         rem = "-"

#     output.append({"i_id":str(each_proj[0]),"project_name":each_proj[1],"project_details":each_proj[2],"project_docs":each_proj[3],"project_man_over":each_proj[4],"project_type":each_proj[5],"project_tl":each_proj[6],"project_check":each_proj[7],"project_estimate":each_proj[8],"project_CE":each_proj[9],"project_allot_time":allot ,"project_done_time":done,"project_last_rem":rem,"project_total_rem":each_proj[13],"project_status":each_proj[14]})
    
    

# print(output)
# if(mydata1['search'] != ''):
#     after_search = search(output,mydata1['search'],['i_id','project_name','project_details','project_docs','project_type','project_tl','project_CE'],['text','text','text','text','text','text','text'],['i_id','project_name','project_details','project_docs','project_type','project_tl','project_CE'])
#     actual_out = []
#     mydata1['from_no'],mydata1['to_no']
#     for each in output:
#         print("\n org : ",each['i_id'],"####",after_search)
#         if(each['i_id'] in after_search):
#             actual_out.append(each)
#     print(actual_out)
        
        
#     from_no = mydata1['from_no']
#     to_no = mydata1['to_no']
#     if(mydata1["required"]=="view"):
#         try:
#             return {"table":actual_out[from_no - 1:to_no],"total_items":len(actual_out)}
#         except:
#             try:
#                 return {"table":actual_out[from_no - 1: len(table_data)],"total_items":len(actual_out)}
#             except:
#                 return {"table":actual_out,"total_items":len(actual_out)}
#     else:
#         return {"table":actual_out}  
    
# else:
#     from_no = mydata1['from_no']
#     to_no = mydata1['to_no']
#     if(mydata1["required"]=="view"):
#         try:
#             return {"table":output[from_no - 1:to_no],"total_items":len(output)}
#         except:
#             try:
#                 return {"table":output[from_no - 1: len(output)],"total_items":len(output)}
#             except:
#                 return {"table":output,"total_items":len(output)}
#         # return {"table":output,"total_items":len(output)}
#     else:
#         return {"table":output}


cors = CORS(app, resources={r"/filecheck": {"origins": "*"}})
@app.route('/filecheck', methods=['GET','POST'])
def faq_update():
    if(os.path.isfile('./master.csv')):
        return {"status":"ok"}
    else:
        return {"status":"false"}
    

cors = CORS(app, resources={r"/table_info": {"origins": "*"}})
@app.route('/table_info', methods=['GET','POST'])
def table_info():
    cur.execute("select * from project")
    proj_list = cur.fetchall()
    if(len(proj_list) > 0):
        return {"status":"ok"}
    else:
        return {"status":"no"}



cors = CORS(app, resources={r"/valtoken": {"origins": "*"}})
@app.route('/valtoken', methods=['GET','POST'])
def valtoken():
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    return valid_user(mydata['token'])#use valid function for validation

cors = CORS(app, resources={r"/checklogin": {"origins": "*"}})
@app.route('/checklogin', methods=['GET','POST'])
def signin():
    from datetime import datetime, timedelta
    global user_info
    ##print("login",request.data)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    print("login",mydata)
    payload = {
        'user_id': mydata['userName'],
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    #prepare token for new user
    encoded = jwt.encode( payload, mydata['password'], algorithm='HS256')
    print("\n\n\n encoded \n\n\n",encoded)
    cur.execute("select * from customer where cust_email = %s ",(mydata['userName'],))
    user_info = cur.fetchone()
    print(user_info)
    if(user_info and user_info[2] == mydata['password']):
        print("\n\n\n return token \n\n\n",encoded)
        return {"data":encoded.decode("UTF-8")}
    else:
        return {"data":'False'}


@app.route("/test")
def hello2():
    return "1234"

@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"

if __name__ == "__main__":
    app.run(port = 5000,use_reloader=False)