


########################## This file is for check the token that belongs to the any valid user or not #####################
import psycopg2
conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="quotationbot", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")

cust_id = {"id":''}
import jwt
import ast
cur = conn.cursor()

def valid_user(token):
    #below is token validation fetch user details one by one from user table and try to decode the token
    cur.execute("select user_email,user_password,auth_level,product_constraints,location_constraints,user_id from users")
    user_info = cur.fetchall()
    for each_user in user_info:
        try:
            print("\n\n\n each user",each_user,"\n\n\n")
            decode = jwt.decode(token,each_user[1], algorithm='HS256')
            print("\n\n\n decode",decode,"\n\n\n")
            if decode['user_id'] == each_user[0]:
                print("\n\n valid token \n\n")
                return {"data":'True',"auth_level":each_user[2],"prod_cons":each_user[3],"location_cons":each_user[4],"user_id":each_user[5]}
            
        except:
            print("\n\n\nerror in jwt\n\n\n")
            continue
    return {"data":'False'}

# update users set product_constraints = "['tl-sg1005p','tl-sf1024d','tl-sg1005d','tl-sf1008p']",location_constraints = "['chennai','coimbatore','bangalore','mumbai']";


