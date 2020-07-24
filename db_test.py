
import psycopg2
# import calendar;
# import time;
# import ast
import requests
# # from Microservices.gmail import *
# # ts = calendar.timegm(time.gmtime())
# # print(ts)
# conn = psycopg2.connect(database="quotationbot", user = "postgres", password = "Logapriya@213", host = "127.0.0.1", port = "5432")


# cur = conn.cursor()
# import flask
# import requests
import json
import ast
# import uuid
# import jwt
# import ast
# from flask import request, jsonify
# from flask import send_file,make_response
# import base64
# from flask_cors import CORS
# app = flask.Flask(__name__)
# app.config["DEBUG"] = True
# import pandas as pd
# # from Microservices.gmail import *
# # output = []
# from datetime import datetime, timedelta
# cur.execute("SELECT f_id,f_anstext,ts_rank(to_tsvector('english', f_anstext) || to_tsvector('english', f_anslink) , to_tsquery('english', 'how to')) AS rank FROM faq WHERE to_tsvector('english', f_anstext) || to_tsvector('english', f_anslink) @@ to_tsquery('english','how to') ORDER BY rank DESC;")
# issues = cur.fetchall()
# print(issues)
# for row in issues:
#     print(row[3])
#     cur.execute("select p_code from product where p_id = %s",(row[3],))
#     product = cur.fetchall()[0]
#     cur.execute("select * from customer where c_id = %s",(row[2],))
#     customer = cur.fetchall()
#     customer_name = customer[0][0]
#     customer_phone = customer[0][5]
#     customer_mail = customer[0][4]
#     customer_location = customer[0][3]
#     mydata = ast.literal_eval(row[4])
#     output.append({"center":"center","product":product,"name":customer_name,"phone":customer_phone,"email":customer_mail,"querry":'',"response":'',"date":'',"location":customer_location,"conversations":mydata})
# print(output)

# cur.execute("select * from customer where c_phone = '9944556677'")
# li = list(cur.fetchone())
# print(li)

# seconds = int(time.time())
# print(seconds)
# timer = time.localtime(seconds)
# print(timer)

# cur.execute("select * from issues;")
# iss_len = len(cur.fetchall())
# print(iss_len)
# import datetime;
# ts = int(datetime.datetime.now().timestamp())
# ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
# print(ts)

# JWT_EXP_DELTA_SECONDS = 200
# import jwt
# # payload = {
# #         'user_id': 'frank@cloobot.com',
# #         'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
# #     }
# # encoded = jwt.encode(payload, 'Logapriya@213', algorithm='HS256')
# # print(encoded)
# decode = jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZnJhbmtAY2xvb2JvdC5jb20iLCJleHAiOjE1OTI5MTczMzd9.BxZ2ldwgwfDJzH4mZSkqL0sOS2HLOeYKQax1FsRyKHc', 'tpl1', algorithm='HS256')
# print(decode)
    # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
# print(recieve_push_notifiction())

# cors = CORS(app, resources={r"/": {"origins": "*"}})
# @app.route('/', methods=['GET','POST'])
# def push_notification():
#     dict_ = request.data.decode("UTF-8")
#     mydata = ast.literal_eval(dict_)
#     dict_2 = base64.urlsafe_b64decode(mydata['message']['data']).decode("UTF-8")
#     mydata2 = ast.literal_eval(dict_2)
#     print("\n\n\n",mydata2,"\n\n\n")

#     # history = service.users().messages().get(userId='me', id=msg).execute()
#     # hist_list = ListHistory(59169)
#     # print("\n\n\n message : ", hist_list , "\n\n\n")
#     # old_history = mydata2['historyId']
#     try:
#         mess_id = hist_list[0]['messages'][0]['id']
#         print("\n\n\nmess_id",mess_id,"\n\n\n")

#         mess = GetMessage('me',"172c765b7bf41f66")
#         print("\n\n\n",mess,"\n\n\n")
#     except:
#         return "True"
    
    
#     return "True"
# GetMessage('me',"172c765b7bf41f66")
# app.run(port='8001',use_reloader=False)
# {'id': '172c765b7bf41f66', 'threadId': '172c765b7bf41f66', 'labelIds': ['SENT']} 

# from components.pagedata import *

# print(get_page_data(6,10,2,'faq'))



# SELECT id,
#   title,
#   ts_rank(
#     to_tsvector('english', title) || to_tsvector('english', description),
#     to_tsquery('english', 'ruby & rails')
#   ) AS rank
# FROM jobs
# WHERE
#   to_tsvector('english', title) || to_tsvector('english', description) @@
#   to_tsquery('english', 'ruby & rails')
# ORDER BY rank DESC



# SELECT f_id,f_anstext,ts_rank(to_tsvector('english', f_anstext) || to_tsvector('english', f_anslink) , to_tsquery('english', 'how to') AS rank FROM faq WHERE to_tsvector('english', f_anstext) || to_tsvector('english', f_anslink) @@ to_tsquery('english', 'how to') ORDER BY rank DESC;





# create table demo (id serial,doc text,doc2 text,doc3 text,tsv tsvector);
# create trigger tcvupdate before insert or update on demo for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',doc,doc2,doc3);
# create index fts_idx_new on demo using gin(tsv);
# insert into demo (doc,doc2,doc3) values('[46] How to find the hardware version on a TP-Link device?','text2','text3'),('[78] How do I configure the basic wireless settings for my TP-Link 11N Wireless Router?','txt2','txt3'),('[87] How do I log into the web-based Utility (Management Page) of TP-Link wireless router?','2','3');
#  with q as (select to_tsquery('tp | link') as query),ranked as (select id,doc,doc2,doc3,ts_rank_cd(tsv, query) as rank from demo,q where q.query @@ tsv order by rank desc) select id, ts_headline(doc3,q.query),ts_headline(doc, q.query),ts_headline(doc2, q.query) from ranked,q order by ranked desc;
# with q as (select to_tsquery('test') as query),ranked as (select id, doc,doc2,doc3,ts_rank_cd(tsv, query) as rank from demo,q where q.query @@ tsv order by rank desc limit 10) select id, ts_headline(doc, q.query) from ranked,q order by ranked desc;
 
 
 
# #  create table faq(id serial,doc text,doc2 text,doc3 text,tsv tsvector);
# # insert into demo (doc,doc2,doc3) values('[46] How to find the hardware version on a TP-Link device?','text2','text3'),('[78] How do I configure the basic wireless settings for my TP-Link 11N Wireless Router?','txt2','txt3'),('[87] How do I log into the web-based Utility (Management Page) of TP-Link wireless router?','2','3');
# create trigger tcvupdate before insert or update on faq for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',f_topic,f_anstext,f_anslink);
# create index fts_idx on faq using gin(tsv);
# with q as (select to_tsquery('11n') as query),ranked as (select f_id,f_topic,f_anstext,f_anslink,ts_rank_cd(tsv, query) as rank from faq,q where q.query @@ tsv order by rank desc) select f_id, ts_headline(f_topic,q.query),ts_headline(f_anslink, q.query) from ranked,q order by ranked desc;



# cur.execute("create table for_search(i_id text,center text,email text,product text,location text,name text,phone text);")
# cur.execute("create trigger tcvupdate before insert or update on for_search for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',email,name,location,phone,center,product);")
# cur.execute("create index fts_idex on for_search using gin(tsv);")


# a = [(1,"hi"),(2),(3),(4)]
# if 2 in a:
#     print("s")
# myobj = {'from_id': 'franklin@cloobot.com','to_id':"frankjos1998@gmail.com","subject":"testing","message":"hi this is just a test"}
# url = "http://127.0.0.1:8002/"
# headers = {'content-type': 'application/json'}
# send_mail = requests.post("https://script.googleapis.com/v1/scripts/{scriptId}:run")
# print(send_mail)
# cur.execute("select product_constraints from users where user_id = 'utpl1'")

# constraints = cur.fetchone()[0]

# cons_list = ast.literal_eval(constraints)
# if(len(cons_list) == 1):
#     cons_list = (cons_list[0])
# cons_list = str(tuple(cons_list))

# cur.execute("select location_constraints from users where user_id = 'utpl1'")
# constraints2 = cur.fetchone()[0]
# cons_list2 = ast.literal_eval(constraints2)
# if(len(cons_list2) == 1):
#     cons_list2 = (cons_list2[0])

# cons_list2 = str(tuple(cons_list2))

# #  'from': 1593858413158, 'to': 1594463213158, 
# cur.execute("select * from quotes where p_id  in (select p_id from product where upper(p_code) in "+cons_list+" ) and c_id in (select c_id from client where lower(c_address) in "+cons_list2+" )")
# all =  cur.fetchall()
# print("\n all  \n",all)

# print(get_mail_info('9988776655'))
# prepare the attachment with email
from email import encoders 
import os.path
from os import path
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
from os.path import basename
# def CreateMessageWithAttachment(file_dir,filename):
#   """Create a message for an email.
#   Args:
#     sender: Email address of the sender.
#     to: Email address of the receiver.
#     subject: The subject of the email message.
#     message_text: The text of the email message.
#     file_dir: The directory containing the file to be attached.
#     filename: The name of the file to be attached.
#   Returns:
#     An object containing a base64url encoded email object.
#   """
  
  
  

#   path = os.path.join(file_dir, filename)
#   content_type, encoding = mimetypes.guess_type(path)

#   if content_type is None or encoding is not None:
#     content_type = 'application/octet-stream'
#   main_type, sub_type = content_type.split('/', 1)
#   if main_type == 'text':
#     fp = open(path, 'rb')
#     msg = MIMEApplication(fp.read(), _subtype=sub_type,Name=basename(path))
#     fp.close()
#   elif main_type == 'image':
#     fp = open(path, 'rb')
#     msg = MIMEImage(fp.read(), _subtype=sub_type)
#     fp.close()
#   elif main_type == 'audio':
#     fp = open(path, 'rb')
#     msg = MIMEAudio(fp.read(), _subtype=sub_type)
#     fp.close()
#   else:
#     fp = open(path, 'rb')
#     msg = MIMEBase(main_type, sub_type)
#     msg.set_payload(fp.read())
#     encoders.encode_base64(msg)
    
#     fp.close()

#   msg.add_header('Content-Disposition', 'attachment', filename=filename)
#   return msg
# file = CreateMessageWithAttachment(r"C:\Users\Clooot\Desktop\programs\voice assistant",'quotation.xlsx')
# send_mail = requests.get("https://script.google.com/macros/s/AKfycbw9Ugx8zLu0F_nlew0vDY4vRvIU66qqbFzqEUCQPbpMFHvrFVMk/exec?file ="+str(file))
# # print(send_mail.text)
url = "https://script.google.com/macros/s/AKfycbw9Ugx8zLu0F_nlew0vDY4vRvIU66qqbFzqEUCQPbpMFHvrFVMk/exec"


files = {'file': (r"C:\Users\Clooot\Desktop\programs\voice assistant\quotation.xlsx", open(r"C:\Users\Clooot\Desktop\programs\voice assistant\quotation.xlsx", 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
# files = {'file':  open(r"C:\Users\Clooot\Desktop\programs\voice assistant\quotation.xlsx", 'rb')}

foo = requests.post(url, files=files)
print(foo.text)



# headers = {'content-type': 'application/json'}
# response_status = requests.post(url,data= json.dumps({'data':{'to':"frank",'cc':"franklin"}}),headers=headers)
# print(response_status.text)


# #!/usr/bin/python
# import smtplib,ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# from email.utils import formatdate
# from email import encoders

# def send_mail(send_from,send_to,subject,text,server,port,username='',password='',isTls=True):
#     msg = MIMEMultipart()
#     msg['From'] = send_from
#     msg['To'] = send_to
#     msg['Date'] = formatdate(localtime = True)
#     msg['Subject'] = subject
#     msg.attach(MIMEText(text))

#     part = MIMEBase('application', "octet-stream")
#     part.set_payload(open(r"C:\Users\Clooot\Desktop\programs\voice assistant\quotation.xlsx", "rb").read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', 'attachment; filename="quotation.xlsx"')
#     msg.attach(part)

#     #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
#     #SSL connection only working on Python 3+
#     smtp = smtplib.SMTP(server, port)
#     if isTls:
#         smtp.starttls()
#     smtp.login(username,password)
#     smtp.sendmail(send_from, send_to, msg.as_string())
#     smtp.quit()
#     print("mail sent")



# send_mail("frankjos1998@gmail.com","franklin@cloobot.com","tetsting using smtp","hi praba",'smtp.gmail.com',587,username='frankjos1998@gmail.com',password='Logapriya@frank',isTls=True)
