
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
conn = psycopg2.connect(database="allotment", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="allotment", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
cur = conn.cursor()



############################################## organisation table  ##################################################

ts = calendar.timegm(time.gmtime())
cur.execute(" INSERT INTO customer (cust_name,cust_password,cust_phone,cust_email,timestamp) VALUES (%s,%s,%s,%s,%s)",('admin','admin','9944019577','admin@cloobot.com',ts))

def insert_data():
    ########################################################  clients table ############################################
    DEF_EXCEL_FILE = "Assets/master.xlsx"
    COL_PART_CODE = 0
    types_table = pandas.read_excel(DEF_EXCEL_FILE, sheet_name=COL_PART_CODE)
    print(types_table)



    DEF_EXCEL_FILE = "Assets/master.xlsx"
    COL_PART_CODE = 2
    excel_data_df = pandas.read_excel(DEF_EXCEL_FILE, sheet_name=COL_PART_CODE)
    print(excel_data_df)
    for i in range(len(excel_data_df['Name'])):
        types = []
        for j in types_table['Project_Type_Name']:
            if(excel_data_df[j][i] == 1):
                types.append(j)
        types_str = ','.join(types)
        ts = calendar.timegm(time.gmtime())
        # print(excel_data_df['Name'][i],"123",excel_data_df['Whatsapp_phone_number'][i],excel_data_df['Email_ID'][i],4,excel_data_df['Role'][i],excel_data_df['TL'][i],excel_data_df['project_type'][i],ts)
        cur.execute(" INSERT INTO USERS (USER_NAME,USER_PASSWORD,USER_PHONE,USER_EMAIL,USER_AUTH_LEVEL,USER_ROLE,USER_TL,USER_PROJ_TYPE,TIMESTAMP) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(excel_data_df['Name'][i],"123",excel_data_df['Whatsapp_phone_number'][i],excel_data_df['Email_ID'][i],4,excel_data_df['Role'][i],excel_data_df['TL'][i],types_str,ts))    

    ##########################################################################################



    DEF_EXCEL_FILE = "Assets/master.xlsx"
    COL_PART_CODE = 1
    excel_data_df = pandas.read_excel(DEF_EXCEL_FILE, sheet_name=COL_PART_CODE)
    print(excel_data_df)
    for i in range(len(excel_data_df['Project_Name'])):
        ts = calendar.timegm(time.gmtime())
        cur.execute(" INSERT INTO project (P_NAME,P_DETAIL,P_DOCS,P_MANUAL_OVERRIDE,P_TYPE,P_TL,P_CHECK,P_ESTIMATE,P_CE,P_ALOT_TIME,P_DONE_TIME,P_LAST_REM,P_TOTAL_REM,P_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(excel_data_df['Project_Name'][i],excel_data_df['Project_Detail'][i],excel_data_df['Document_and_folder_links'][i],excel_data_df['Manual_Override'][i],excel_data_df['Project_Type'][i],excel_data_df['TL'][i],excel_data_df['Checked_Alloted'][i],excel_data_df['Estimated_hours_to_complete'][i],'',0,0,0,0,0))


    ########################################################################################################################








    conn.commit()
conn.commit()
# insert_data()
print("success")