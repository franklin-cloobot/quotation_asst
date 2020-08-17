
import pandas
import difflib
import psycopg2
import calendar;
import time;
import datetime
# ts = calendar.timegm(time.gmtime())

conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
cur = conn.cursor()



############################################## organisation table  ##################################################

# ts = calendar.timegm(time.gmtime())
# cur.execute(" INSERT INTO organisation (org_id,org_name,timestamp) VALUES (%s,%s,%s)",('org101','tplink',ts))

#############################################################################################




########################################################  clients table ############################################
# DEF_EXCEL_FILE = "Assets/Quotation Chatbot Details.xlsx"
# COL_PART_CODE = 0
# excel_data_df = pandas.read_excel(DEF_EXCEL_FILE, sheet_name=COL_PART_CODE)
# print(excel_data_df)

# for i in range(len(excel_data_df['Company Name'])):
#     cid = 'c'+'tpl'
#     ts = calendar.timegm(time.gmtime())
#     cur.execute(" INSERT INTO client (c_id,org_id,c_name,c_phone,c_mail,c_address,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s)",(cid+str(i),'org101',excel_data_df['Company Name'][i],'9944556677',excel_data_df['E-Mail ID'][i],excel_data_df['Location'][i],ts))

##########################################################################################




################################################## product table #####################################################


# DEF_EXCEL_FILE = "Assets/Quotation Chatbot Details.xlsx"
# COL_PART_CODE = 1
# excel_data_df = pandas.read_excel(DEF_EXCEL_FILE, sheet_name=COL_PART_CODE)
# print(excel_data_df)

# for i in range(len(excel_data_df['Part Code'])):
#     pid = 'p'+'tpl'
#     ts = calendar.timegm(time.gmtime())
#     cur.execute(" INSERT INTO product (p_id,org_id,p_desc,p_category,p_code,timestamp) VALUES (%s,%s,%s,%s,%s,%s)",(pid+str(i),'org101',excel_data_df['Product Description'][i],' ',excel_data_df['Part Code'][i],ts))


########################################################################################################################








###################################################  user table ######################################################################
# ts = int(datetime.datetime.now().timestamp())
# cur.execute(" INSERT INTO users (user_id,org_id,user_name,user_password,user_phone,user_email,auth_level,manager_id,timestamp,product_constraints,location_constraints) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",('utpl1','org101','franklin','tpl1','9944019577','frank@cloobot.com',4,'manager',ts,'[]','[]'))


###############################################################################################



conn.commit()
print("success")