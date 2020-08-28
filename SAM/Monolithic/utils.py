import pandas
import difflib
import psycopg2
import calendar;
import time;
import datetime
from datetime import datetime
import pytz
import json
import requests
# conn = psycopg2.connect(database="allotment", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
conn = psycopg2.connect(database="allotment", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
cur = conn.cursor()



from .constants import *


def populate_from_excel(info_mode, excel_filepath,phone):
   
    sheetname = ''
    usecols = ''

   
    if info_mode == INFO_DEALERS:
        table_name = 'client'
        col_name = 'c_name'
    if info_mode == INFO_PRODUCTS:
        table_name = 'product'
        col_name = 'p_desc'
    if info_mode == INFO_PART_CODE:
        table_name = 'product'
        col_name = 'p_code'
    if info_mode == INFO_PRICE:
        sheetname = 'Product and Price List'
        usecols = 'Unit Price'
    cur.execute("select org_id from users where user_phone = %s",(phone,))
    user_org_id = cur.fetchone()[0]
    cur.execute("select "+col_name+" from "+table_name+" where org_id = %s",(user_org_id,))
    
    data = cur.fetchall()
    return [x[0].lower() for x in data]
 
def check_for_pending(phone):
    cur.execute("select p_name from project where p_ce = (select user_email from users where user_phone = %s) and p_status = 0 and p_manual_override = '0'",(phone,))
    project_list = list(cur.fetchall())
    if(len(project_list)>0):
        print("\nthere is a pending : ",project_list)
        return project_list[0][0]
    else:
        print("there is no pending")
        return 0
def mark_as_done(proj_name):
    # ts = datetime.now().timestamp()
    ts = int(datetime.now().timestamp())
    # ts = datetime_India.strftime("Date : %Y-%m-%d Time : %H:%M:%S")
    cur.execute("update project set p_status = 1,p_done_time = %s where p_name = %s",(ts,proj_name))
    conn.commit()
    print("\n project complted : ",proj_name)
    return 1

def manually_overide(proj_name):
    cur.execute("update project set p_manual_override = 1 where p_name = %s",(proj_name,))
    conn.commit()
    print("\n project overided : ",proj_name)
    return 1

def check_for_new(phone):
    cur.execute("select user_proj_type from users where user_phone = %s",(phone,))
    type_list = cur.fetchone()[0]
    type_list = tuple(type_list.split(','))
    print("\n type list : ",type_list)
    try :
        cur.execute("select * from project where p_type in "+str(type_list)+" and p_manual_override = '0' and p_status = 0")
        new_project = list(cur.fetchone())
    except :
        new_project = 0
    print("\n New project : ",new_project)
    if(new_project):
        #  p_check |p_ce | p_alot_time
        user = get_user(phone)
        ts = int(datetime.now().timestamp())
        cur.execute("update project set p_check = %s,p_ce = %s,p_alot_time = %s where p_name = %s",(1,user[1],ts,new_project[1]))
        conn.commit()
        print("\n master updated")
        return list(new_project)
    else:
        return 0


def get_mail_info(phone):
    cur.execute("select user_email,manager_id from users where user_phone = %s",(phone,))
    user = cur.fetchone()
    sales_mail = user[0]
    cur.execute("select user_email from users where user_id = %s",(user[1],))
    manager = cur.fetchone()[0]
    return sales_mail,manager


def get_user(phone):
    cur.execute("select user_name,user_email,user_tl from users where user_phone = %s",(phone,))
    try:
        user = list(cur.fetchone())
        return user
    except:
        return "new"

def get_allotime(proj_name):
    cur.execute("select * from project where p_name = %s",(proj_name,))
    return cur.fetchone()[10]


def sendmail(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject):
    # importing the requests library 
    import requests 
    import json
    url_appsScript = 'https://script.google.com/macros/s/AKfycbxc1YGJ8-s2EMzr6RagyA1Ad0JRGYhsB2qXhCyVzDcX03rt82X8/exec'







    headers = {'content-type': 'application/json'}

    r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject))
    # r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format("franklin","franklin@cloobot.com","frankjos1998@gmail.com","new mail","new allot for frank"))

    print(r.text,type(r.text))
    return r.text
    

def watsapp_message(phone,message):
    print("\n\nwhatsapp called : ",phone,message)
    sampleDict = {  "channel" : "whatsapp",
                    "source" : "917834811114",
                    "destination" : phone,
                    "src.name":"CloobotServiceBot",
                    "message" : json.dumps({
                        "isHSM":"true",
                        "type": "text",
                        "text": message
                            })
                            }
    # jsonData = json.dumps(sampleDict)
    # print(type(jsonData))
    r=requests.post("https://api.gupshup.io/sm/api/v1/msg", 
        headers={"apikey":"3868773c5a0d4064c0084f6da93fabba"},
        data=sampleDict)
    
    print("\n\nresponse from watsapp",r.text)
    return 1
    
    