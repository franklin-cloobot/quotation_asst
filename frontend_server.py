import flask
import requests
import json
import ast
import uuid
import jwt
import decimal
decimal.getcontext().prec = 5

import datetime
import time
from .components.pagedata import *
from .components.valtoken import *
from .bachend_insert import *
# from components.pagedata import *
# from components.valtoken import *
# from bachend_insert import *
from flask import request, jsonify
from flask import send_file,make_response,render_template
from flask import Flask, request, redirect, jsonify, send_file
from flask_cors import CORS,cross_origin
import base64
from flask_cors import CORS
# app = flask.Flask(__name__)
app = flask.Flask(__name__, template_folder="templates")
app.config["DEBUG"] = True




import psycopg2
import pandas as pd
conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="quotationbot", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")

JWT_EXP_DELTA_SECONDS = 86400

cur = conn.cursor()
from functools import wraps
UPLOAD_FOLDER = 'Assets'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

errors = {}
success = False
def save(files,dirrectory,filename):
    for file in files:
        print("file : ",file)
        if file and allowed_file(file.filename):
            file.save("Assets/"+dirrectory+ filename)
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    return success,errors
@app.route('/multiple-files-upload', methods=['POST', 'GET','OPTIONS'])
@cross_origin(supports_credentials=True)
def upload_file():
    # if request.method == 'POST':
    # return 'sss'
	# if 'files[]' not in request.files:
    org_id = request.form.get('org_id')
    print(org_id)
    
    if 'user' not in request.files and 'client' not in request.files and 'product' not in request.files:
        print("no attachments")
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
	#
    
    
    ts = datetime.datetime.now().strftime("_%H_%M_%S_%f")
	# #files = request.files.getlist('files[]')
    if 'user' in request.files:
        
        filename = "user" + ts + ".xlsx"
        files = request.files.getlist('user')
        success,errors = save(files,"user/",filename)
        user_id = request.form.get('user_id')
        insert_user(filename,org_id,user_id)
    elif 'client' in request.files:
        filename = "client" + ts+ ".xlsx"
        files = request.files.getlist('client')
        success,errors = save(files,"client/",filename)
        insert_client(filename,org_id)
    else:
        filename = "product" + ts + ".xlsx"
        files = request.files.getlist('product')
        success,errors = save(files,"product/",filename)
        
        insert_product(filename,org_id)
    print("file : ",files)

    

    if success and errors:
        # insert_data()
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

    if success:
        # insert_data()
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
    return resp



cors = CORS(app, resources={r"/allquote": {"origins": "*"}})
@app.route('/allquote', methods=['GET','POST'])
def session_start():
    output = []
    dict_ = request.data.decode("UTF-8")
    #print("\n\n\n at receiving comming",dict_,"\n\n\n")
    mydata1 = ast.literal_eval(dict_) 
    # #print(mydata1)
    if valid_user(mydata1['token'])['data'] == 'True':#check whether the user is valid
        # fetch issue between selected dates
        cur.execute("select lower(product_constraints),lower(location_constraints) from users where user_id  = %s",(mydata1['data']['user_id'],))
        user_constraints = cur.fetchone()
        constraints = user_constraints[0]

        cons_list = ast.literal_eval(constraints)
        if(len(cons_list) == 1):
            cons_list = (cons_list[0])
        cons_list = str(tuple(cons_list))

        
        constraints2 = user_constraints[1]
        cons_list2 = ast.literal_eval(constraints2)
        if(len(cons_list2) == 1):
            cons_list2 = (cons_list2[0])

        cons_list2 = str(tuple(cons_list2))

        #  'from': 1593858413158, 'to': 1594463213158,
        # cur.execute("select * from quotes where p_id  in (select p_id from product where upper(p_code) in "+cons_list+" ) and c_id in (select c_id from client where lower(c_address) in "+cons_list2+" ) and timestamp >= %s and timestamp <= %s and org_id = %s order by timestamp desc;",(mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
        print("\n constraints : ",constraints,constraints2)
        print("\n constraints : ",cons_list,cons_list2)
        try:
            cur.execute("select * from quotes where p_id  in (select p_id from product where lower(p_code) in "+cons_list+" ) and c_id in (select c_id from client where lower(c_address) in "+cons_list2+" ) and timestamp >= %s and timestamp <= %s and org_id = %s order by timestamp desc;",(mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
            # cur.execute("select * from quotes where timestamp >= %s and timestamp <= %s;",(mydata1['from']/1000,mydata1['to']/1000))
            issues = cur.fetchall()
        except:
            cur.execute("rollback;")
            conn.commit()
            issues = []

        for row in issues:
            print("\n\n\n\n row : ",row,row[2],"\n\n\n\n")
            cur.execute("select user_name from users where user_id  = %s",(row[2],))
            user = cur.fetchone()[0]
            
            cur.execute("select p_code,p_desc from product where p_id = %s;",(row[4],))
            prod_details = cur.fetchone()
            product = prod_details[0]
            prod_desc = prod_details[1]
            cur.execute("select c_name from client where c_id = %s;",(row[3],))
            client = cur.fetchone()[0]
            #print("\n user : id ==> ",row[8])
            cur.execute("select user_name from users where user_id = %s;",(row[8],))
            manager = cur.fetchone()[0]
            #print("\n manager ==> ",manager)
            output.append({"q_id":row[0],"client":client,"descr":prod_desc,"part":product,"quantity":row[5],"Unit_price":row[6],"sal_ex":user,"manager":manager,"total":row[5] * row[6],"Date":row[11]})
        
        if(mydata1['search'] != ''):
            after_search = search(output,mydata1['search'],['q_id','client','descr','part','sal_ex','manager'],['text','text','text','text','text','text'],['client','descr','part','sal_ex','manager'])
            actual_out = []
            for each in output:
                #print("\n org : ",each['q_id'],"####",after_search)
                if(each['q_id'] in after_search):
                    actual_out.append(each)
            
            
            from_no = mydata1['from_no']
            to_no = mydata1['to_no']
            if(mydata1["required"]=="view"):
                try:
                    return {"table":actual_out[from_no - 1:to_no],"total_items":len(actual_out)}
                except:
                    try:
                        return {"table":actual_out[from_no - 1: len(table_data)],"total_items":len(actual_out)}
                    except:
                        return {"table":actual_out,"total_items":len(actual_out)}
            else:
                return {"table":actual_out}  
            
        else:
            from_no = mydata1['from_no']
            to_no = mydata1['to_no']
            if(mydata1["required"]=="view"):
                try:
                    return {"table":output[from_no - 1:to_no],"total_items":len(output)}
                except:
                    try:
                        return {"table":output[from_no - 1: len(output)],"total_items":len(output)}
                    except:
                        return {"table":output,"total_items":len(output)}
                # return {"table":output,"total_items":len(output)}
            else:
                return {"table":output}
        
    
    else:
        #print("invalid access")
        return {"status":"failed"}


cors = CORS(app, resources={r"/authcheck": {"origins": "*"}})
@app.route('/authcheck', methods=['GET','POST'])
def faq_update():
    
    dict_ = request.data.decode("UTF-8")
    mydata1 = ast.literal_eval(dict_) 
    #print("api data",mydata1['data'])
    if valid_user(mydata1['token'])['data'] == 'True':#check whether the user is valid
        # if(int(mydata1['data']['auth_level']) >= 3):
        if(mydata1['data']>=3):
            
            return {'status':'ok'}
        else:
            return {'status':'denied'}
    else:
        #print("invalid access")
        return {"status":"failed"}

# cors = CORS(app, resources={r"/GetpageNo": {"origins": "*"}})
# @app.route('/GetpageNo', methods=['GET','POST'])
# def total_page():
#     dict_ = request.data.decode("UTF-8")
#     mydata1 = ast.literal_eval(dict_) 
#     #print("\n\n\n ************************* : ",mydata1,"\n\n\n")
#     if valid_user(mydata1['token'])['data'] == 'True':#check whether the user is valid
#         return {"total_items":get_page_no('faq',mydata1['search'])}
#     else:
#         #print("invalid access")
#         return {"status":"failed"}
        
cors = CORS(app, resources={r"/report_graph": {"origins": "*"}})
@app.route('/report_graph', methods=['GET','POST'])
def repot_page_graph():
    dict_ = request.data.decode("UTF-8")
    mydata1 = ast.literal_eval(dict_) 
    #print("\n\n\n ************************* : ",mydata1,"\n\n\n")
    output = []
    if valid_user(mydata1['token'])['data'] == 'True':#check whether the user is valid
        if mydata1['request_type'] ==  'sales_exec':
            try :
                cur.execute("select user_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value,(select sum(unit_price * qty)/count(distinct(user_id)) as average from quotes where org_id = %s) from quotes where timestamp >= %s and timestamp <= %s and org_id = %s group by user_id order by total_numer desc;",(mydata1['data']['user_org_id'],mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select user_name from users where user_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"name":user,"total_number":each[1],"total_value":float(decimal.Decimal(each[2])/decimal.Decimal(1000000)),"avg":float(decimal.Decimal(each[3])/decimal.Decimal(1000000))})
            #print("\n######output : ",output)
            return {"graph":output}
        if mydata1['request_type'] ==  'manager':
            try : 
                cur.execute("select sales_manager_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value,(select sum(unit_price * qty)/count(distinct(sales_manager_id)) as average from quotes where org_id = %s) from quotes where timestamp >= %s and timestamp <= %s and org_id = %s group by sales_manager_id order by total_numer desc;",(mydata1['data']['user_org_id'],mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select user_name from users where user_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"name":user,"total_number":each[1],"total_value":float(decimal.Decimal(each[2])/decimal.Decimal(1000000)),"avg":float(decimal.Decimal(each[3])/decimal.Decimal(1000000))})
            #print("\n######output : ",output)
            return {"graph":output}
        if mydata1['request_type'] ==  'product':
            
            cur.execute("select lower(product_constraints) from users where user_id  = %s",(mydata1['data']['user_id'],))
            constraints = cur.fetchone()[0]

            cons_list = ast.literal_eval(constraints)
            if(len(cons_list) == 1):
                cons_list = (cons_list[0])
            cons_list = str(tuple(cons_list))
            try :
                cur.execute("select p_id,count(p_id) as total_numer,sum(unit_price * qty) as total_value,(select sum(unit_price * qty)/count(distinct(p_id)) as average from quotes where org_id = %s) from quotes where timestamp >= %s and timestamp <= %s and p_id  in (select p_id from product where lower(p_code) in "+cons_list+" ) and org_id = %s group by p_id order by total_numer desc;",(mydata1['data']['user_org_id'],mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                # cur.execute("select p_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value,(select sum(unit_price * qty)/count(distinct(p_id)) as average from quotes) from quotes where timestamp >= %s and timestamp <= %s group by p_id order by total_numer desc;",(mydata1['from']/1000,mydata1['to']/1000))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select p_code from product where p_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"name":user,"total_number":each[1],"total_value":float(decimal.Decimal(each[2])/decimal.Decimal(1000000)),"avg":float(decimal.Decimal(each[3])/decimal.Decimal(1000000))})
            #print("\n######output : ",output)
            return {"graph":output}
        if mydata1['request_type'] ==  'client':
            cur.execute("select lower(location_constraints) from users where user_id  = %s",(mydata1['data']['user_id'],))
            constraints2 = cur.fetchone()[0]
            cons_list2 = ast.literal_eval(constraints2)
            if(len(cons_list2) == 1):
                cons_list2 = (cons_list2[0])

            cons_list2 = str(tuple(cons_list2))
            try :
                cur.execute("select c_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value,(select sum(unit_price * qty)/count(distinct(c_id)) as average from quotes where org_id = %s) from quotes where timestamp >= %s and timestamp <= %s and c_id in (select c_id from client where lower(c_address) in "+cons_list2+" ) and org_id = %s group by c_id order by total_numer desc;",(mydata1['data']['user_org_id'],mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                # cur.execute("select c_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value,(select sum(unit_price * qty)/count(distinct(c_id)) as average from quotes) from quotes where timestamp >= %s and timestamp <= %s group by c_id order by total_numer desc;",(mydata1['from']/1000,mydata1['to']/1000))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select c_name from client where c_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"name":user,"total_number":each[1],"total_value":float(decimal.Decimal(each[2])/decimal.Decimal(1000000)),"avg":float(decimal.Decimal(each[3])/decimal.Decimal(1000000))})
            #print("\n######output : ",output)
            return {"graph":output}

        # return {"total_items":get_page_no('faq',mydata1['search'])}
        
    else:
        #print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/report_table": {"origins": "*"}})
@app.route('/report_table', methods=['GET','POST'])
def repot_page_table():
    dict_ = request.data.decode("UTF-8")
    mydata1 = ast.literal_eval(dict_) 
    #print("\n\n\n ************************* : ",mydata1,"\n\n\n")
    output = []
    if valid_user(mydata1['token'])['data'] == 'True':#check whether the user is valid
        if mydata1['request_type'] ==  'sales_exec':
            try :
                cur.execute("select user_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value from quotes where timestamp >= %s and timestamp <= %s and org_id = %s group by user_id order by total_numer desc;",(mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select user_name from users where user_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"id":each[0],"name":user,"total_number":each[1],"total_value":each[2]})
            #print("\n######output : ",output)
           
        
        if mydata1['request_type'] ==  'manager':
            try :
                cur.execute("select sales_manager_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value from quotes where timestamp >= %s and timestamp <= %s and org_id = %s group by sales_manager_id order by total_numer desc;",(mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select user_name from users where user_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"id":each[0],"name":user,"total_number":each[1],"total_value":each[2]})
            #print("\n######output : ",output)
            # return {"graph":output}
            
        if mydata1['request_type'] ==  'product':
            cur.execute("select lower(product_constraints) from users where user_id  = %s",(mydata1['data']['user_id'],))
            constraints = cur.fetchone()[0]

            cons_list = ast.literal_eval(constraints)
            if(len(cons_list) == 1):
                cons_list = (cons_list[0])
            cons_list = str(tuple(cons_list))
            try :
                cur.execute("select p_id,count(p_id) as total_numer,sum(unit_price * qty) as total_value from quotes where timestamp >= %s and timestamp <= %s and p_id  in (select p_id from product where lower(p_code) in "+cons_list+" ) and org_id = %s group by p_id order by total_numer desc;",(mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select p_code from product where p_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"id":each[0],"name":user,"total_number":each[1],"total_value":each[2]})
            #print("\n######output : ",output)
            # return {"graph":output}
        if mydata1['request_type'] ==  'client':
            cur.execute("select lower(location_constraints) from users where user_id  = %s",(mydata1['data']['user_id'],))
            constraints2 = cur.fetchone()[0]
            cons_list2 = ast.literal_eval(constraints2)
            if(len(cons_list2) == 1):
                cons_list2 = (cons_list2[0])

            cons_list2 = str(tuple(cons_list2))
            try :
                cur.execute("select c_id,count(user_id) as total_numer,sum(unit_price * qty) as total_value from quotes where timestamp >= %s and timestamp <= %s and c_id in (select c_id from client where lower(c_address) in "+cons_list2+" ) and org_id = %s group by c_id order by total_numer desc;",(mydata1['from']/1000,mydata1['to']/1000,mydata1['data']['user_org_id']))
                quote_data = cur.fetchall()
            except :
                cur.execute("rollback;")
                conn.commit()
                quote_data = []
            #print("$$$$$$$ quote data : ",quote_data)
            for each in quote_data:
                cur.execute("select c_name from client where c_id = %s",(each[0],))
                user = cur.fetchone()[0]
                output.append({"id":each[0],"name":user,"total_number":each[1],"total_value":each[2]})
            #print("\n######output : ",output)
            # return {"graph":output}

        # return {"total_items":get_page_no('faq',mydata1['search'])}
        if(mydata1['search'] != ''):
                after_search = search_report(output,mydata1['search'],['id','name'],['text','text'],['name'])
                actual_out = []
                for each in output:
                    #print("\n org : ",each['id'],"####",after_search)
                    if(each['id'] in after_search):
                        actual_out.append(each)
                # #print(actual_out)
                from_no = mydata1['from_no']
                to_no = mydata1['to_no']
                if(mydata1["required"]=="view"):
                    try:
                        return {"table":actual_out[from_no - 1:to_no],"total_items":len(actual_out)}
                    except:
                        try:
                            return {"table":actual_out[from_no - 1: len(table_data)],"total_items":len(actual_out)}
                        except:
                            return {"table":actual_out,"total_items":len(actual_out)}
                else:
                    return {"table":actual_out}  
            
        else:
            from_no = mydata1['from_no']
            to_no = mydata1['to_no']
            if(mydata1["required"]=="view"):
                try:
                    return {"table":output[from_no - 1:to_no],"total_items":len(output)}
                except:
                    try:
                        return {"table":output[from_no - 1: len(output)],"total_items":len(output)}
                    except:
                        return {"table":output,"total_items":len(output)}
                # return {"table":output,"total_items":len(output)}
            else:
                return {"table":output}
        
    else:
        #print("invalid access")
        return {"status":"failed"}


cors = CORS(app, resources={r"/invite": {"origins": "*"}})
@app.route('/invite', methods=['GET','POST'])
def invite():
    # below fetch the details of users 
    output = []
    #print("\n\n\n invite values ###########",request.data,"\n\n\n")
    dict_ = request.data.decode("UTF-8")
    mydata1 = ast.literal_eval(dict_)
    if valid_user(mydata1['token'])['data'] == 'True': #check whether the user is valid
        print("*** valid token ******")
        print(mydata1,mydata1['data']['user_org_id'])
        cur.execute("select * from users where org_id = %s",(mydata1['data']['user_org_id'],))
        user = cur.fetchall()
        
        cur.execute("select p_code from product where org_id = %s",(mydata1['data']['user_org_id'],))
        products = list(cur.fetchall())
        #print("\n\n\n",products)
        location = ['chennai','bangalore','coimbatore','mumbai','delhi','pune']
        for each_user in user:
            output.append({"u_id":each_user[0],"name":each_user[2],"user_pwd":each_user[3],"user_phone":each_user[4],"mail":each_user[5],"auth_level":each_user[6],"manager_id":each_user[7],"product_constraints":ast.literal_eval(each_user[9]),"location_constraints":ast.literal_eval(each_user[10])})
        return {"table":output,"products":products,"location":location}
        # return {"table":output}
    else:
        #print("invalid access")
        return {"status":"failed"}



cors = CORS(app, resources={r"/valtoken": {"origins": "*"}})
@app.route('/valtoken', methods=['GET','POST'])
def valtoken():
    #check for token comes here
    #print("validate token",request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    #print("\n\n\n valtoken \n\n\n",mydata)
    return valid_user(mydata['token'])#use valid function for validation




cors = CORS(app, resources={r"/add_user": {"origins": "*"}})
@app.route('/add_user', methods=['GET','POST'])
def add_user():
    designation = ''
    #print(request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    #print("\n\n new data : ",mydata)
    if valid_user(mydata['token'])['data'] == 'True':#check whether the user is valid
        ts = int(datetime.datetime.now().timestamp()) 
        prod_cons_list = []
        location_cons_list = []
        
        for each in mydata['user']['product_constraints']:
            if(each['item_text'][0] not in prod_cons_list):
                prod_cons_list.append(each['item_text'][0])
        for each in mydata['user']['location_constraints']:
            if(each['item_text'] not in location_cons_list):
                location_cons_list.append(each['item_text'])
        cur.execute("select * from users where org_id = %s",(mydata['data']['user_org_id'],))
        #print("\n\ngoing to added : ",location_cons_list,prod_cons_list)
        user_len = len(cur.fetchall())+1
        if( 'man' in mydata['user']['Designation']):
            designation = mydata['data']['user_id'][:4]+str(user_len)
        else:
            designation = mydata['data']['user_id']
        # insert new user
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | product_constraints | location_constraints
        cur.execute("insert into users (user_id,org_id,user_name,user_password,user_phone,user_email,auth_level,manager_id,timestamp,product_constraints,location_constraints) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(mydata['data']['user_id'][:4]+str(user_len),mydata['data']['user_org_id'],mydata['user']['name'],mydata['user']['user_pwd'],mydata['user']['user_phone'],mydata['user']['mail_id'],mydata['user']['auth_level'],designation,ts,str(prod_cons_list),str(location_cons_list)))
        conn.commit()
        #print("\n\n\n new user added \n\n\n")
        return {"status":"ok"}
    else:
        #print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/edit_user": {"origins": "*"}})
@app.route('/edit_user', methods=['GET','POST'])
def edit_user():
    #print(request)
    designation = ''
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    if valid_user(mydata['token'])['data'] == 'True':
        ts = int(datetime.datetime.now().timestamp()) 
        prod_cons_list = []
        location_cons_list = []
        for each in mydata['edit_user']['product_constraints']:
            if(each['item_text'][0] not in prod_cons_list):
                prod_cons_list.append(each['item_text'][0])
        for each in mydata['edit_user']['location_constraints']:
            if(each['item_text'] not in location_cons_list):
                location_cons_list.append(each['item_text'])
        if( 'man' in mydata['edit_user']['Designation']):
            designation = mydata['edit_user']['u_id']
        else:
            designation = mydata['data']['user_id']
       
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | product_constraints | location_constraints
        cur.execute("update users set user_name = %s,user_password=%s,user_phone=%s,user_email = %s,auth_level = %s,manager_id=%s,timestamp = %s,product_constraints = %s,location_constraints = %s where user_id = %s;",(mydata['edit_user']['name'],mydata['edit_user']['user_pwd'],mydata['edit_user']['user_phone'],mydata['edit_user']['mail_id'],mydata['edit_user']['auth_level'],designation,ts,str(prod_cons_list),str(location_cons_list),mydata['edit_user']['u_id']))
        conn.commit()
        #print("\n\n\n user updated \n\n\n")
        return {"status":"ok"}
       
    else:
        #print("invalid access")
        return {"status":"failed"}


cors = CORS(app, resources={r"/delete_user": {"origins": "*"}})
@app.route('/delete_user', methods=['GET','POST'])
def delete_user():
    #print(request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    if valid_user(mydata['token'])['data'] == 'True':
       
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | product_constraints | location_constraints
        cur.execute("delete from users where user_id = %s",(mydata['del_user'],))
        conn.commit()
        #print("\n\n\n user deleted \n\n\n")
        return {"status":"ok"}
       
    else:
        #print("invalid access")
        return {"status":"failed"}



cors = CORS(app, resources={r"/product": {"origins": "*"}})
@app.route('/product', methods=['GET','POST'])
def product():
    # below fetch the details of users 
    output = []
    #print("\n\n\n invite values ###########",request.data,"\n\n\n")
    dict_ = request.data.decode("UTF-8")
    mydata1 = ast.literal_eval(dict_)
    if valid_user(mydata1['token'])['data'] == 'True': #check whether the user is valid
        #print("*** valid token ******")
        #print(mydata1)
        cur.execute("select * from product where org_id = %s",(mydata1['data']['user_org_id'],))
        product = cur.fetchall()
        for each_prod in product:
            output.append({"p_id":each_prod[0],"p_desc":each_prod[2],"p_code":each_prod[4],"p_category":each_prod[3]})
        return {"table":output}
        # return {"table":output}
    else:
        #print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/add_product": {"origins": "*"}})
@app.route('/add_product', methods=['GET','POST'])
def add_product():
    designation = ''
    #print(request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    #print("\n\n new data : ",mydata)
    cur.execute("select count(p_id) from product")
    p_count = cur.fetchone()[0]
    if valid_user(mydata['token'])['data'] == 'True':#check whether the user is valid
        ts = int(datetime.datetime.now().timestamp()) 
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | product_constraints | location_constraints
        cur.execute("insert into product (p_id,p_desc,p_code,p_category,org_id,timestamp) values(%s,%s,%s,%s,%s,%s);",('ptpl'+str(p_count),mydata['product']['p_desc'],mydata['product']['p_code'],mydata['product']['p_category'],mydata['data']['user_org_id'],ts))
        conn.commit()
        #print("\n\n\n new product added \n\n\n")
        return {"status":"ok"}
    else:
        #print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/edit_product": {"origins": "*"}})
@app.route('/edit_product', methods=['GET','POST'])
def edit_product():
    #print(request)
    designation = ''
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    if valid_user(mydata['token'])['data'] == 'True':
        ts = int(datetime.datetime.now().timestamp()) 
        
       
        cur.execute("update product set p_code = %s,p_desc=%s,p_category=%s,timestamp = %s where p_id = %s;",(mydata['edit_product']['p_code'],mydata['edit_product']['p_desc'],mydata['edit_product']['p_category'],ts,mydata['edit_product']['p_id']))
        conn.commit()
        #print("\n\n\n product updated \n\n\n")
        return {"status":"ok"}
       
    else:
        #print("invalid access")
        return {"status":"failed"}


cors = CORS(app, resources={r"/delete_product": {"origins": "*"}})
@app.route('/delete_product', methods=['GET','POST'])
def delete_product():
    #print(request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    #print("mydata : ",mydata)
    if valid_user(mydata['token'])['data'] == 'True':
       
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | product_constraints | location_constraints
        cur.execute("delete from product where p_id = %s",(mydata['del_product'],))
        conn.commit()
        #print("\n\n\n product deleted \n\n\n")
        return {"status":"ok"}
       
    else:
        #print("invalid access")
        return {"status":"failed"}


cors = CORS(app, resources={r"/client": {"origins": "*"}})
@app.route('/client', methods=['GET','POST'])
def client():
    # below fetch the details of users 
    output = []
    #print("\n\n\n invite values ###########",request.data,"\n\n\n")
    dict_ = request.data.decode("UTF-8")
    mydata1 = ast.literal_eval(dict_)
    if valid_user(mydata1['token'])['data'] == 'True': #check whether the user is valid
        #print("*** valid token ******")
        #print(mydata1)
        cur.execute("select * from client where org_id = %s",(mydata1['data']['user_org_id'],))
        client = cur.fetchall()
        for each_client in client:
            output.append({"c_id":each_client[0],"c_name":each_client[2],"c_phone":each_client[3],"c_mail":each_client[4],"c_address":each_client[5]})
        return {"table":output}
        # return {"table":output}
    else:
        ##print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/add_client": {"origins": "*"}})
@app.route('/add_client', methods=['GET','POST'])
def add_client():
    designation = ''
    ##print(request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    ##print("\n\n new data : ",mydata)
    cur.execute("select count(c_id) from client")
    c_count = cur.fetchone()[0]
    if valid_user(mydata['token'])['data'] == 'True':#check whether the user is valid
        ts = int(datetime.datetime.now().timestamp()) 
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | product_constraints | location_constraints
        cur.execute("insert into client (c_id,c_name,c_phone,c_mail,c_address,org_id,timestamp) values(%s,%s,%s,%s,%s,%s,%s);",('ctpl'+str(c_count),mydata['client']['c_name'],mydata['client']['c_phone'],mydata['client']['c_mail'],mydata['client']['c_address'],mydata['data']['user_org_id'],ts))
        conn.commit()
        ##print("\n\n\n new client added \n\n\n")
        return {"status":"ok"}
    else:
        ##print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/edit_client": {"origins": "*"}})
@app.route('/edit_client', methods=['GET','POST'])
def edit_client():
    ##print(request)
    designation = ''
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    if valid_user(mydata['token'])['data'] == 'True':
        ts = int(datetime.datetime.now().timestamp()) 
        
       
        cur.execute("update client set c_name = %s,c_phone=%s,c_mail=%s,c_address=%s,timestamp = %s where c_id = %s;",(mydata['edit_client']['c_name'],mydata['edit_client']['c_phone'],mydata['edit_client']['c_mail'],mydata['edit_client']['c_address'],ts,mydata['edit_client']['c_id']))
        conn.commit()
        ##print("\n\n\n client updated \n\n\n")
        return {"status":"ok"}
       
    else:
        ##print("invalid access")
        return {"status":"failed"}


cors = CORS(app, resources={r"/delete_client": {"origins": "*"}})
@app.route('/delete_client', methods=['GET','POST'])
def delete_client():
    ##print(request)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    ##print("mydata : ",mydata)
    if valid_user(mydata['token'])['data'] == 'True':
       
        # user_id | org_id | user_name | user_pwd | user_phone |     user_mail     | user_auth_lvl | manager_id | timestamp  | client_constraints | location_constraints
        cur.execute("delete from client where c_id = %s",(mydata['del_client'],))
        conn.commit()
        ##print("\n\n\n client deleted \n\n\n")
        return {"status":"ok"}
       
    else:
        ##print("invalid access")
        return {"status":"failed"}

cors = CORS(app, resources={r"/checklogin": {"origins": "*"}})
@app.route('/checklogin', methods=['GET','POST'])
def signin():
    from datetime import datetime, timedelta
    global user_info
    ##print("login",request.data)
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    payload = {
        'user_id': mydata['e'],
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    #prepare token for new user
    encoded = jwt.encode( payload, mydata['p'], algorithm='HS256')
    ##print("\n\n\n encoded \n\n\n",encoded)
    cur.execute("select * from users where user_email = %s ",(mydata['e'],))
    user_info = cur.fetchone()
    ##print(user_info)
    user_info = list(user_info)
    if(user_info and user_info[3] == mydata['p']):
        ##print("\n\n\n return token \n\n\n",encoded)
        return {"data":encoded.decode("UTF-8"),'user_info':mydata['e'],"auth_level":user_info[6],"prod_cons":user_info[9],"location_cons":user_info[10],"user_id":user_info[0],"user_org_id":user_info[1]}
    else:
        return {"data":'False'}


cors = CORS(app, resources={r"/register": {"origins": "*"}})
@app.route('/register', methods=['GET','POST'])
def register():
    ##print(request)
    ts = int(datetime.datetime.now().timestamp()) 
    dict_ = request.data.decode("UTF-8")
    mydata = ast.literal_eval(dict_)
    cur.execute("insert into organisation (org_id,org_name,timestamp) values(%s,%s,%s);",(mydata['company_name'][:3]+"101",mydata['company_name'][:3],ts))
    cur.execute(" INSERT INTO users (user_id,org_id,user_name,user_password,user_phone,user_email,auth_level,manager_id,timestamp,product_constraints,location_constraints) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",('u'+mydata['company_name'][:3]+'1',mydata['company_name'][:3]+"101",mydata['user_name'],mydata['password'],mydata['phone'][3:],mydata['email_id'],4,'u'+mydata['company_name'][:3]+'1',ts,'[]','[]'))
    conn.commit()
    print("mydata : ",mydata)
    return {"status":"ok"}

cors = CORS(app, resources={r"/product_list": {"origins": "*"}})
@app.route('/product_list', methods=['GET','POST'])
def product_table():
    ##print(request)
    name = "franklin"
    phone = request.args.get('phone')
    print("\n phone : ",phone)
    cur.execute("select * from product where org_id = (select org_id from users where user_phone = %s)",(phone,))
    products = [list(each) for each in cur.fetchall()]
    print("\n products : ",products)
    print(products)
    return render_template('index.html', table = products)


@app.route("/test")
def hello2():
    return "1234"

@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"

if __name__ == "__main__":
    app.run(port = 8001,use_reloader=False)