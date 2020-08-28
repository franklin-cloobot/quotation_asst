
import pandas
import difflib
import psycopg2
import calendar;
import time;
import datetime
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
# ts = calendar.timegm(time.gmtime())

conn = psycopg2.connect(database="quotationbot", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
cur = conn.cursor()



############################################## organisation table  ##################################################

# ts = calendar.timegm(time.gmtime())
# cur.execute(" INSERT INTO organisation (org_id,org_name,timestamp) VALUES (%s,%s,%s)",('org101','tplink',ts))

#############################################################################################




########################################################  clients table ############################################

def insert_client(filename,org_id):
    # path = "Assets/client/"
    path = "/var/www/flaskapp_quote_testing/quotation_asst/Assets/client/"
    SHEET = 0
    excel_data_df = pandas.read_excel(path+filename, sheet_name=SHEET)
    print(excel_data_df)
    cur.execute("select count(*) from client where org_id = %s",(org_id,))
    count = cur.fetchone()[0]+1
    for i in range(len(excel_data_df['Client Name'])):
        cid = 'c'+org_id[:3]
        ts = calendar.timegm(time.gmtime())
        cur.execute(" INSERT INTO client (c_id,org_id,c_name,c_phone,c_mail,c_address,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s)",(cid+str(count + i),org_id,excel_data_df['Client Name'][i],excel_data_df['phone'][i],excel_data_df['E-Mail ID'][i],excel_data_df['Location'][i],ts))
    conn.commit()
    return 1
##########################################################################################




################################################## product table #####################################################

def insert_product(filename,org_id):
    # path = "Assets/product/"
    path = "/var/www/flaskapp_quote_testing/quotation_asst/Assets/product/"
    SHEET = 0
    excel_data_df = pandas.read_excel(path+filename, sheet_name=SHEET)
    print(excel_data_df)
    cur.execute("select count(*) from product where org_id = %s",(org_id,))
    count = cur.fetchone()[0]+1
    for i in range(len(excel_data_df['Part_Code'])):
        pid = 'p'+org_id[:3]
        ts = calendar.timegm(time.gmtime())
        
        cur.execute(" INSERT INTO product (p_id,org_id,p_desc,p_category,p_code,timestamp) VALUES (%s,%s,%s,%s,%s,%s)",(pid+str(count + i),org_id,excel_data_df['Product_Description'][i].lower(),excel_data_df['Product_Category'][i].lower(),excel_data_df['Part_Code'][i].lower(),ts))
    
    conn.commit()
    return 1


########################################################################################################################


def insert_user(filename,org_id,user_id):
    # path = "Assets/user/"
    path = "/var/www/flaskapp_quote_testing/quotation_asst/Assets/user/"
    SHEET = 0
    excel_data_df = pandas.read_excel(path+filename, sheet_name=SHEET)
    print(excel_data_df)
    cur.execute("select count(*) from users where org_id = %s",(org_id,))
    count = cur.fetchone()[0]+1
    for i in range(len(excel_data_df['name'])):
        uid = 'u'+org_id[:3]
        ts = calendar.timegm(time.gmtime())
        if('mana' in excel_data_df['designation'][i]):
            auth_level = 4
            manager_id = uid+str(count + i)
        else:
            auth_level = 2
            manager_id = user_id
        
        location_cons = excel_data_df['location_constraints'][i].split(',')
        product_cons = excel_data_df['product_constraints'][i].split(',')
        cur.execute(" INSERT INTO users (user_id,org_id,user_name,user_password,user_phone,user_email,auth_level,manager_id,timestamp,product_constraints,location_constraints) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(uid+str(count + i),org_id,excel_data_df['name'][i],excel_data_df['password'][i],excel_data_df['phone'][i],excel_data_df['mail'][i],auth_level,manager_id,ts,str(product_cons),str(location_cons)))
        
    
    conn.commit()
    return 1





###################################################  user table ######################################################################
# ts = int(datetime.datetime.now().timestamp())
# cur.execute(" INSERT INTO users (user_id,org_id,user_name,user_password,user_phone,user_email,auth_level,manager_id,timestamp,product_constraints,location_constraints) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",('utpl1','org101','franklin','tpl1','9944019577','frank@cloobot.com',4,'manager',ts,'[]','[]'))


###############################################################################################



conn.commit()
print("success")