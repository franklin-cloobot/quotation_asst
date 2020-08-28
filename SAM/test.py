import pandas
import difflib
import psycopg2
import calendar;
import time;
import datetime

conn = psycopg2.connect(database="allotment", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
cur = conn.cursor()
# phone = '7598543704'
# cur.execute("select user_name from users where user_phone = %s",(phone,))
# user = cur.fetchone()[0]
# print(user)

# import requests 
# import json


# url_appsScript = 'https://script.google.com/macros/s/AKfycbxc1YGJ8-s2EMzr6RagyA1Ad0JRGYhsB2qXhCyVzDcX03rt82X8/exec'

import dateutil.relativedelta






# headers = {'content-type': 'application/json'}

# # r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject))
# # r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format("franklin","franklin@cloobot.com","frankjos1998@gmail.com","new mail","new allot for frank"))

# print(r.text,type(r.text))

# cur.execute("update project set p_check = %s,p_ce = %s,p_alot_time = %s",(0,'',''))
# conn.commit()
# curr_time = time.strftime('%H:%M', time.localtime(1596971753))
# print(type(curr_time),curr_time)

# dt1 = datetime.datetime.fromtimestamp(1596978943) # 1973-11-29 22:33:09
# dt2 = datetime.datetime.fromtimestamp(1596978957) # 1977-06-07 23:44:50
# rd = dateutil.relativedelta.relativedelta (dt2, dt1)
# datetime.datetime.now(1596978957).timestamp()
# print("%d years, %d months, %d days, %d hours, %d minutes and %d seconds" % (rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))
# datetime_London = datetime.now(tz_London)
# print(datetime_London.strftime('%H:%M', time.localtime(datetime.datetime.now().timestamp())))
from datetime import datetime
import pytz
import json
import requests
# 

# print("##### : ",datetime_India)
# tz_India = pytz.timezone('Asia/Calcutta')
# datetime_India = datetime.now(tz_India)
# print("India time:", datetime_India.strftime("Date : %Y-%m-%d Time : %H:%M:%S"))

# print(datetime.fromtimestamp(1596988336, pytz.timezone("Asia/Calcutta")))


# dt1 = datetime.fromtimestamp(1597045330, pytz.timezone("Asia/Calcutta")) 
# print("#dti#:",dt1)
# tz_India = pytz.timezone('Asia/Calcutta')
# datetime_India = datetime.now(tz_India)
# dt2 = datetime_India 
# rd = dateutil.relativedelta.relativedelta (dt1, dt1)
# print(rd.minutes,rd.seconds)
# cur.execute("select * from project")
# proj_list = cur.fetchall()
# output = []
# for each_proj in proj_list:
#     output.append({"project_name":each_proj[1],"project_details":each_proj[2],"project_docs":each_proj[3],"project_man_over":each_proj[4],"project_type":each_proj[5],"project_tl":each_proj[6],"project_estimate":each_proj[7],"project_CE":each_proj[8],"project_allot_time":each_proj[9],"project_done_time":each_proj[10],"project_last_rem":each_proj[11],"project_total_rem":each_proj[12],"project_status":each_proj[13]})
# print(output)
def watsapp2():
    phone = "919944019577"
    message = """watsapp()
Approval received from Rajesh for Quote  

ANC - 4 items - Rs. 4,00,101 - 29th July 2020

I have sent you an email with the quote"""
    sampleDict = {  "channel" : "whatsapp",
                        "source" : "917834811114",
                        "destination" : phone,
                        "src.name":"quotetest",
                        "message" : json.dumps({
                            "isHSM":"true",
                            "type": "text",
                            "text": message
                                })
                                }
    # jsonData = json.dumps(sampleDict)
    # print(type(jsonData))
    r=requests.post("https://api.gupshup.io/sm/api/v1/msg", 
        headers={"apikey":"9a21ca22fb234722c747925571537486"},
        data=sampleDict)

    print("\n\nresponse from watsapp",r.text)


def watsapp():
    phone = "919944019577"
    message = """Any new updates on ANC Enterprises

1. Register a visit / call

2. Create a quote

3. Remind at a later date

4. Mark as dead lead"""
    sampleDict = {  "channel" : "whatsapp",
                        "source" : "917834811114",
                        "destination" : phone,
                        "src.name":"quotetest",
                        "message" : json.dumps({
                            "isHSM":"true",
                            "type": "text",
                            "text": message
                                })
                                }
    # jsonData = json.dumps(sampleDict)
    # print(type(jsonData))
    r=requests.post("https://api.gupshup.io/sm/api/v1/msg", 
        headers={"apikey":"9a21ca22fb234722c747925571537486"},
        data=sampleDict)

    print("\n\nresponse from watsapp",r.text)


# def sendmail(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject):
#     # importing the requests library 
#     import requests 
#     import json
#     url_appsScript = 'https://script.google.com/macros/s/AKfycbxc1YGJ8-s2EMzr6RagyA1Ad0JRGYhsB2qXhCyVzDcX03rt82X8/exec'







#     headers = {'content-type': 'application/json'}

#     r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject))
#     # r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format("franklin","franklin@cloobot.com","frankjos1998@gmail.com","new mail","new allot for frank"))

#     print(r.text,type(r.text))
#     return r.text

# response_mail_message = ("CE name : ajith"+\
#                           "\nQC name : Sankar"+\
#                            "\nProject Name : Project 3"+\
#                             "\nProduct Details : Description"+\
#                                 "\nDocuments : https://drive.google.com/drive/folders/1XNhn3Ji0WP7JXGBti3hpY5xm0lu4m4Dp?usp=sharing"+\
#                                     "\nDead line : 2 hrs")
                        
# response_mail_subject = "Project Markesd as incomplete by QC"
# sendmail("franklin","frankjos1998@gmail.com","franklin@cloobot.com",response_mail_message,response_mail_subject)
