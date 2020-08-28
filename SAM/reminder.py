import pandas
import difflib
import psycopg2
import calendar;
import time;
import datetime
from datetime import datetime
import pytz
import dateutil.relativedelta
from time import strftime
import json
import requests

def watsapp_message(phone,message):

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
    return 1


conn = psycopg2.connect(database="allotment", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="allotment", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
cur = conn.cursor()


def count_update(proj_name):
    ts = int(datetime.now().timestamp())
    cur.execute("update project set p_last_rem = %s,p_total_rem = p_total_rem + 1 where p_name = %s",(ts,proj_name))
    conn.commit()
    print("\n count updated")
    return 1


def get_user(u_email):
    cur.execute("select user_name,user_phone,user_tl from users where user_email = %s",(u_email,))
    try:
        user = list(cur.fetchone())
        print(user)
        return user[0],user[1],user[2]
    except:
        return "new"

def manually_overide(proj_name):
    cur.execute("update project set p_manual_override = 1 where p_name = %s",(proj_name,))
    conn.commit()
    print("\n project overided : ",proj_name)
    return 1

def sendmail(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject):
    # importing the requests library 
    import requests 
    import json
    url_appsScript = 'https://script.google.com/macros/s/AKfycbxc1YGJ8-s2EMzr6RagyA1Ad0JRGYhsB2qXhCyVzDcX03rt82X8/exec'
    headers = {'content-type': 'application/json'}

    r = requests.post(url_appsScript+'?name={0}&user_mail={1}&user_tl_mail={2}&message={3}&subject={4}'.format(person_name,user_mail,user_tl_mail,response_mail_message,response_mail_subject))
    print(r.text,type(r.text))
    return r.text


def remind():
    cur.execute("select * from project where p_status = 0 and p_manual_override = '0' and p_check = 1")
    project_list = cur.fetchall()
    
    for each_pend_proj in project_list:
        user_name,user_phone,user_tl = get_user(each_pend_proj[9])
        ending = datetime.fromtimestamp(int(each_pend_proj[10])+ each_pend_proj[8]* 60* 60, pytz.timezone("Asia/Calcutta")) 
        print("\n user : ",user_name,user_phone)
        tz_India = pytz.timezone('Asia/Calcutta')
        datetime_India = datetime.now(tz_India)
        dt2 = datetime_India
        rd = dateutil.relativedelta.relativedelta (ending, dt2)
        if(rd.hours == 1 and rd.minutes in [51,52,53,54,55,56,57,58,59,50] and each_pend_proj[13] == 0):
            count_update(each_pend_proj[1])
            print("hi")
            message = ("Project "+each_pend_proj[1]+" is due in 2 hours\n"+\
                        "Keep going! Remember to self check before sending to QC.\n"+\
                        "Type 1 to mark Done.")

            print(message)
            watsapp_message('91'+user_phone,message)

        if(rd.hours == 0 and rd.minutes in [51,52,53,54,55,56,57,58,59,50] and each_pend_proj[13] == 1):
            count_update(each_pend_proj[1])
            print("hi")
            message = ("Project "+each_pend_proj[1]+" is due in 1 hours\n"+\
                        "Time to wrap it up and send to QC!\n"+\
                        "Type 1 to mark Done.")

            print(message)
            watsapp_message('91'+user_phone,message)

        if(rd.hours == 0 and rd.minutes in [21,22,23,24,25,26,27,28,29,30] and each_pend_proj[13] == 2):
            count_update(each_pend_proj[1])
            print("hi")
            message = ("Project "+each_pend_proj[1]+" is due in  30 mins\n"+\
                        "Hope final checking is done by now\n"+\
                        "Type 1 to mark Done.")

            print(message)
            watsapp_message('91'+user_phone,message)

        if(rd.hours == 0 and rd.minutes in [-1,-2,-3,-4,-5,-6,-7,-8,-9,0] and each_pend_proj[13] == 3):
            count_update(each_pend_proj[1])
            print("hi")
            message = ("Project "+each_pend_proj[1]+" is due now immediately\n"+\
                        "Type 1 to mark Done.")

            print(message)
            watsapp_message('91'+user_phone,message)

        if(rd.hours == 0 and rd.minutes in [-21,-22,-23,-24,-25,-26,-27,-28,-29,-30] and each_pend_proj[13] == 4):
            count_update(each_pend_proj[1])
            print("hi")
            response_mail_message = ("CE name : "+user_name+\
                                            "\nProject Name : "+each_pend_proj[1]+\
                                                "\nDelayed By : "+str(rd.hours)+" Hrs "+str(rd.minutes)+" Mins")
            response_mail_subject = "Delay in project submission"
            sendmail(user_name,each_pend_proj[9],user_tl,response_mail_message,response_mail_subject)

            message = ("Project "+each_pend_proj[1]+" Delayed By : "+str(rd.hours)+" Hrs "+str(rd.minutes)+" Mins\n"+\
                         "\nI am intimating the TL\n"+\
                        "Type 1 to mark Done.")

            print(message)
            watsapp_message('91'+user_phone,message)

        if(rd.hours == -1 and each_pend_proj[13] == 5):
            count_update(each_pend_proj[1])
            print("hi")
            response_mail_message = ("CE name : "+user_name+\
                                            "\nProject Name : "+each_pend_proj[1]+\
                                                "\nDelayed By : "+str(rd.hours)+" Hrs "+str(rd.minutes)+" Mins")
            response_mail_subject = "Delay in project submission"
            sendmail(user_name,each_pend_proj[9],user_tl,response_mail_message,response_mail_subject)

            message = ("Project "+each_pend_proj[1]+" is Delayed By : "+str(rd.hours)+" Hrs "+str(rd.minutes)+" Mins\n"+\
                         "\nI am intimating the TL\n"+\
                        "Type 1 to mark Done.")

            print(message)
            watsapp_message('91'+user_phone,message)

        if(rd.hours == -2 and each_pend_proj[13] == 6):
            count_update(each_pend_proj[1])
            print("hi")
            response_mail_message = ("CE name : "+user_name+\
                                            "\nProject Name : "+each_pend_proj[1]+\
                                                "\nDelayed By : "+str(rd.hours)+" Hrs "+str(rd.minutes)+" Mins")
            response_mail_subject = "Delay in project submission project overrided"

            sendmail(user_name,each_pend_proj[9],user_tl,response_mail_message,response_mail_subject)

            message = ("Project "+each_pend_proj[1]+" is overrided becase of delay\n"+\
                         "\nI am intimating the TL\n")
            manually_overide(each_pend_proj[1])
            print(message)
            watsapp_message('91'+user_phone,message)

        
        



        print(rd.hours,rd.minutes)
    # print(project_list)
    time.sleep(2)
    remind()



remind()
