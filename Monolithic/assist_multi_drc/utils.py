import pandas
import difflib
import psycopg2
import calendar;
import time;
import datetime
import ast
# conn = psycopg2.connect(database="quotationbot", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
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
 


def get_similar_matches(keyword, targetlist,phone):
    return difflib.get_close_matches(keyword, targetlist , cutoff=0.3 , n=MAX_SEARCH_RESULTS  )

def get_price_list_from_excel(excel_filepath,phone):
    sheetname = 'Product and Price List'
    excel_data_df = pandas.read_excel(excel_filepath, sheet_name=sheetname)
    print("\n\n i do know why \n\n")
    return excel_data_df.to_dict(orient='record')
   
def check_product_details(command,phone):
    commasep_list = command.split(',')
    if len(commasep_list) != 3:
        return None, None, None, None
    else:
        prod_str = commasep_list[0].strip().lower()
        qty_str = commasep_list[1].strip().lower()
        price_str = commasep_list[2].strip().lower()

        #check numbers
        qty = isQty(qty_str,phone)
        price = isPrice(price_str,phone)
        prod, opts = check_prod(prod_str,phone)
        print('In check prod details::',prod_str,'::',prod,'::',opts)
        return prod, opts, qty, price

   
def isQty(inputString,phone):
    inputString = inputString.replace('units','').replace('nos','').replace('items','')
    l = inputString.split(' ')
    for i in l:
        if(str(int(float(i))).isdigit()):
            return float(i)
    return 0

def isPrice(inputString,phone):
    inputString = inputString.replace('inr','').replace('rs.','').replace('rs','')
    tmp = None
    try:
        tmp = float(inputString)
    except ValueError:
        pass
    return tmp


def check_prod(command,phone):
    products = populate_from_excel(INFO_PRODUCTS, DEF_EXCEL_FILE,phone)
    parts = populate_from_excel(INFO_PART_CODE, DEF_EXCEL_FILE,phone)

    options = []
   
    for j in products:
        
        if(command==j.strip().lower()):
            return j, options

    
    for j in parts:
        if(command==j.strip().lower()):
            return j, options

    options = get_similar_matches(command, products,phone)
    if len(options) > 0:
        return None, options

    options = get_similar_matches(command, parts,phone)
    if len(options) > 0:
        return None, options

    return None, options

def create_new_session(phone):
    
    cur.execute("select user_id from users where user_phone = %s",(phone,))
    u_id = cur.fetchone()[0]
    ts = int(datetime.datetime.now().timestamp())
    cur.execute("insert into session(u_id,conversation,timestamp,current_option) values(%s,%s,%s,%s);",(u_id,'[]',ts,0))
    conn.commit()
    print("\n\n new session is created \n\n")

def check_for_pending(phone):
    ts = int(datetime.datetime.now().timestamp())
    cur.execute("select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1;",(phone,))
    sess_id = cur.fetchone()[0]
    cur.execute("select * from temp where u_id = (select user_id from users where user_phone = %s) and status = 'no' and session_id = %s;",(phone,sess_id))
    check = cur.fetchone()
    print("\n check \n",check)
    if( check == None ):
        print("\n new data \n")
        return 1
    else:
        print("\n Not a new data \n")
        return 0

def store_in_temp(command,phone):
    print("\n store temp called\n")
    if(' ' in command):
        commands = command.split(" ")
    elif('\n' in command):
        commands = command.split('\n')
    else:
        commands = [command]
    cur.execute("select session_id,dealer from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1;",(phone,))
    data = cur.fetchone()
    print("\n session details : ",data,'\n')
    sess_id = data[0]
    dealer = data[1]
    cur.execute("select * from users where user_phone = %s",(phone,))
    user_id = cur.fetchone()[0]
    sno = 1
    ts = int(datetime.datetime.now().timestamp())
    for i in commands:
        print("each command : ",i)
        prod, options, qty, price = check_product_details(i,phone)
        if(prod != None):
            status = 'yes'
        else:
            status = 'no'
        cur.execute("insert into temp(u_id,command,status,timestamp,n_th_input,session_id,dealer,options,product,price,quantity) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(user_id,i,status,ts,sno,sess_id,dealer,str(options),prod,str(price),str(qty)))
        sno = sno+1
    conn.commit()
    print("\ntemp data stored\n")

def get_unstored_from_temp(phone):
    cur.execute("select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1;",(phone,))
    sess_id = cur.fetchone()[0]
    cur.execute("select temp_id,options from temp where u_id = (select user_id from users where user_phone = %s) and status = 'no' and session_id = %s order by n_th_input asc limit 1;",(phone,sess_id))
    res = cur.fetchall()
    return res

def store_dealers_in_session(phone,dealer):
    cur.execute("select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1;",(phone,))
    sess_id = cur.fetchone()[0]
    cur.execute("update session set dealer = %s where session_id = %s",(dealer,sess_id))
    conn.commit()
    print("\n\n Dealer added to session \n\n")


def store_confirmed_product(temp_id,option):
    print("\n temp id stored in premanent",temp_id,option)
    cur.execute("update temp set product = %s,status = %s where temp_id = %s;",(option,'yes',temp_id[0]))
    conn.commit()
    cur.execute("select * from temp where temp_id = %s",(temp_id[0],))
    data = cur.fetchone()
    print(" permanent storing data",data)

def get_for_check(phone):
    cur.execute("select temp_id,product,quantity,price from temp where session_id = (select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1); ",(phone,))
    data = cur.fetchall()
    print("\n temp data : ",data)
    return data

def store_current_option(phone,option):
    print("\n going to set option \n")
    cur.execute("update session set current_option = %s where session_id = (select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1);",(option,phone))
    print(" current option stored \n")
    conn.commit()
    print("\n option stored in db")

def get_current_option(phone):
    
    cur.execute("select current_option from session where session_id = (select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1); ",(phone,))
    
    return cur.fetchone()[0]

def change_the_details(command,phone):
    current_option = get_current_option(phone)
    current_row = int(current_option/3)
    if(current_option % 3 == 0):
        current_row = current_row - 1
    cur.execute("select temp_id,product,quantity,price from temp where session_id = (select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1); ",(phone,))
    data = cur.fetchall()
    print("\n data :",data,"\n",data[0])
    if(current_option % 3 == 1):
        data = data[current_row]
        
        temp_id = data[0]
        prod, opts = check_prod(command,phone)
        if(prod):
            cur.execute("update temp set product = %s where temp_id = %s",(command,temp_id,))
        else:
            cur.execute("update temp set status = %s,product = %s where temp_id = %s",('no',command,temp_id))
            print("\n product edit not matched \n")
        print("\n product updated \n")
    elif(current_option % 3 == 2):
        data = data[current_row]
        print("\n after finding the row : ",data)
        temp_id = data[0]
        cur.execute("update temp set quantity = %s where temp_id = %s",(int(command),temp_id,))
        print("\n quantity updated \n")

    elif(current_option % 3 == 0):
        data = data[current_row]
        temp_id = data[0]
        cur.execute("update temp set price = %s where temp_id = %s",(float(command),temp_id,))
        print("\n price updated \n")
    return 1

def store_in_permanent(data,phone):
    print("\ngoing to store in permanent\n")
    cur.execute("select user_id,manager_id from users where user_phone = %s",(phone,))
    user = cur.fetchone()
    u_id = user[0]
    print("\n\n",u_id)
    cur.execute("select dealer from session where u_id =  %s order by timestamp desc limit 1",(u_id,))
    dealer = cur.fetchone()[0]
    print("\n\n",dealer)
    cur.execute("select c_id from client where lower(c_name) = lower(%s)",(dealer,))
    client = cur.fetchone()[0]
    print("\n2\n",client)
    cur.execute("select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1;",(phone,))
    sess_id = cur.fetchone()[0]
    sales_manager_id = user[1]
    ts = int(datetime.datetime.now().timestamp())
    for i in data:
        cur.execute("select count(*) from quotes")
        q_id = 'qtpl' + str(cur.fetchone()[0])
        print("\n quote id :",q_id,i)
        cur.execute("select org_id from users where user_phone = %s",(phone,))
        user_org_id = cur.fetchone()[0]
        cur.execute("select p_id from product where lower(p_code) = lower(%s)",(i[1],))
        p_id = cur.fetchone()
        if(p_id == None):
            print("\n part  :",i[1])
            cur.execute("select p_id from product where LOWER(p_desc) = LOWER(%s)",(i[1],))
            p_id = cur.fetchone()
        print("\n part id :",p_id)
        cur.execute("insert into quotes(q_id,org_id,user_id,c_id,p_id,qty,unit_price,sales_exec_id,sales_manager_id,chat_conversation,email_conversation,timestamp,thread_id,session_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(q_id,user_org_id,u_id,client,p_id,float(i[2]),float(i[3]),u_id,sales_manager_id,chat_conversation,email_conversation,ts,thread_id,sess_id))
    conn.commit()
    print(" stored into permanent")

def get_data_for_excel(phone):
    
    cur.execute("select session_id from session where u_id = (select user_id from users where user_phone = %s) order by timestamp desc limit 1;",(phone,))
    sess_id = cur.fetchone()[0]
    cur.execute("select c_id,p_id,qty,unit_price from quotes where session_id = %s",(sess_id,))
    data = cur.fetchall()
    full_details = []
    cur.execute("select c_name from client where c_id = %s",(data[0][0],))
    client = cur.fetchone()[0]
    for each_row in data:
        cur.execute("select p_code from product where p_id = %s",(each_row[1],))
        p_code = cur.fetchone()[0]
        full_details.append({'Product': p_code, 'Client': client, 'Quantity': each_row[2], 'Price': each_row[3]})
    return full_details



def get_mail_info(phone):
    cur.execute("select user_email,manager_id from users where user_phone = %s",(phone,))
    user = cur.fetchone()
    sales_mail = user[0]
    cur.execute("select user_email from users where user_id = %s",(user[1],))
    manager = cur.fetchone()[0]
    return sales_mail,manager


def get_user(phone):
    cur.execute("select user_name,org_id from users where user_phone = %s",(phone,))
    try:
        user = cur.fetchone()
        print("\n user : ",user)
        return user[0],user[1]
    except:
        return "new"

def get_user_credentials(phone):
    cur.execute("select user_email,user_password from users where user_phone = %s",(phone,))
    try:
        user_info = cur.fetchone()
        user = user_info[0]
        mail = user_info[1]
        print("\n\n user credens : ",user_info,user,mail)
        return user,mail
    except:
        return 0,0


def sendmail(file_name,path,person_name,phone_number,email_id,cc):
    # importing the requests library 
    import requests 
    import json
    import ast
    import filetype
    import base64
    import os
    here = os.path.dirname(__file__)
    url_appsScript = 'https://script.google.com/macros/s/AKfycbw9Ugx8zLu0F_nlew0vDY4vRvIU66qqbFzqEUCQPbpMFHvrFVMk/exec'



    
    

    mime_type = filetype.guess(path+file_name)

    headers = {'content-type': 'application/json'}

    # r = requests.post(url_appsScript+'?file_name={0}&phone_number={1}&email_id={2}&person_name={3}&mime_type={4}&cc={5}'.format(file_name ,phone_number ,email_id ,person_name ,mime_type,cc),data = base64.urlsafe_b64encode(open('/home/ubuntu/quotationbot/CC_Rosi_Quotation/quotation.xlsx','rb').read()))
    r = requests.post(url_appsScript+'?file_name={0}&phone_number={1}&email_id={2}&person_name={3}&mime_type={4}&cc={5}'.format(file_name ,phone_number ,email_id ,person_name ,mime_type,cc),data = base64.urlsafe_b64encode(open(path + file_name,'rb').read()))

    print(r.text,type(r.text))

    return r.text

def check_number_in_track(phone):
    cur.execute("select state from conversation_track where phone = %s",(phone,))
    res = cur.fetchone()
    if(res == None):
        return 0
    else :
        return 1

def current_state(phone):
    cur.execute("select state,top3 from conversation_track where phone = %s",(phone,))
    res = cur.fetchone()
    return res[0],ast.literal_eval(res[1])

def start_conversation(phone):
    ts = int(datetime.datetime.now().timestamp())
    cur.execute(" INSERT INTO conversation_track (phone,top3,state,timestamp) VALUES (%s,%s,%s,%s)",(phone,'[]',0,ts))
    conn.commit()
    return 1

def change_conversation_state(phone,state):
    ts = int(datetime.datetime.now().timestamp())
    cur.execute("update conversation_track set state = %s where phone = %s",(state,phone,))
    conn.commit()
    print("\n state changed to : ",state)
    return 1

def change_top3(phone,top3_list):
    ts = int(datetime.datetime.now().timestamp())
    cur.execute("update conversation_track set top3 = %s where phone = %s",(top3_list,phone))
    conn.commit()
    print("\n top3_list changed to : ",str(top3_list))
    return 1
    

def get_error_command(error_temp_id):
    cur.execute("select command from temp where temp_id = %s",(error_temp_id,))
    command = cur.fetchone()[0]
    return command

def delete_error_querry(error_temp_id):
    cur.execute("delete from temp where temp_id = %s",(error_temp_id,))
    conn.commit()
    print("\nerror querru deleted : ",error_temp_id)
    return 1
    
    