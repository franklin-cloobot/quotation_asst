from .constants import *
from .utils import *
from .anexure_template_int import generate_price_quotation_anex1
import ast
from time import strftime
import pandas as pd
import json
import base64
import re
import requests
import datetime



product_dict={}
price_dict={}
dealer_dict={}
quantity_dict = {}
receiver_email_dict = {}

multi_quote_dict={}

conversation_track = {}
top3_dict = {}
pif_dict = {}
edit_on= 0
HELP_TEXT = """You can use these commands and I'll help you out:\n
- get quote / quotation or : starts the conversation to generate price quotation.\n
- connect with cloobot : displays phone number of a Sales Manager of Cloobot Techlabs
"""

CONTACT_TEXT = """
Aravindh Gunasekaran
aravindh@cloobot.com
+91 8754463981

Vinod Thamilarasan
vinod@cloobot.com
+91 7904521277

Visit us at https://www.cloobot.ai
"""


def check_prod(command):
    products = populate_from_excel(INFO_PRODUCTS, DEF_EXCEL_FILE)
    parts = populate_from_excel(INFO_PART_CODE, DEF_EXCEL_FILE)

    options = []
   
    for j in products:
        
        if(command==j.strip().lower()):
            return j, options

    for j in parts:
        if(command==j.strip().lower()):
            return j, options

    options = get_similar_matches(command, products)
    if len(options) > 0:
        return None, options

    options = get_similar_matches(command, parts)
    if len(options) > 0:
        return None, options

    return None, options

def check_dealers(command):
    dealers = populate_from_excel(INFO_DEALERS, DEF_EXCEL_FILE)
    print(dealers)
    options = []
    for j in dealers:
        if(command==j.strip().lower()):
            return j, options
    
    options = get_similar_matches(command, dealers)
    print('In dealers, ',command, '::', options)
    return None, options

def get_top3_values(info_mode):
    return populate_from_excel(info_mode, DEF_EXCEL_FILE)[:MAX_SEARCH_RESULTS]


def get_price_for_product(product_or_part):
    products = populate_from_excel(INFO_PRODUCTS, DEF_EXCEL_FILE)
    parts = populate_from_excel(INFO_PART_CODE, DEF_EXCEL_FILE)
    price_list = get_price_list_from_excel(DEF_EXCEL_FILE)

    for row in price_list:

        if product_or_part == row[COL_PART_CODE].strip().lower() or product_or_part == row[COL_PRODUCT].strip().lower():
            return float(row[COL_PRICE])
    return None


def check_auth_email(command):
    options = []

    if command == 'me':
        return MY_EMAIL_ID, options
    return command, options


    
def isQty(inputString):
    inputString = inputString.replace('units','').replace('nos','').replace('items','')
    l = inputString.split(' ')
    for i in l:
        if(i.isdigit()):
            return int(i)
    return 0

def isPrice(inputString):
    inputString = inputString.replace('inr','').replace('rs.','').replace('rs','')
    tmp = None
    try:
        tmp = float(inputString)
    except ValueError:
        pass
    return tmp
    
def check_yes_no(inputString):
    if inputString == 'y' or inputString == 'Y' or inputString == 'yes' or inputString == 'Yes':
        return 'y'
    elif inputString == 'n' or inputString == 'N' or inputString == 'no' or inputString == 'No':
        return 'n'
    return None

def check_product_details(command):
    commasep_list = command.split(',')
    if len(commasep_list) != 3:
        return None, None, None, None
    else:
        prod_str = commasep_list[0].strip().lower()
        qty_str = commasep_list[1].strip().lower()
        price_str = commasep_list[2].strip().lower()

        #check numbers
        qty = isQty(qty_str)
        price = isPrice(price_str)
        prod, opts = check_prod(prod_str)
        print('In check prod details::',prod_str,'::',prod,'::',opts)


        return prod, opts, qty, price


def check_product_details_v2(command):
    commasep_list = []
    
    tmp_list = command.split('of')
    commasep_list.append(tmp_list[0])

    tmp_list = tmp_list[1].split('at')
    commasep_list.append(tmp_list[0])
    if len(commasep_list) > 1:
        commasep_list.append(tmp_list[1])

    print('in cpd v2, ',commasep_list)
    if len(commasep_list) != 3:
        return None, None, None, None
    else:
        qty_str = commasep_list[0].strip().lower()
        prod_str = commasep_list[1].strip().lower()
        price_str = commasep_list[2].strip().lower()

        qty = isQty(qty_str)
        price = isPrice(price_str)
        prod, opts = check_prod(prod_str)
        print('In check prod details::',prod_str,'::',prod,'::',opts)
        
        return prod, opts, qty, price






def assistant(command, phone, mode):
    global product_dict, dealer_dict, quantity_dict, receiver_email_dict, conversation_track, multi_quote_dict
    
    if phone not in product_dict:
        product_dict[phone] = ''

    if phone not in dealer_dict:
        dealer_dict[phone] = ''
    
    if phone not in quantity_dict:
        quantity_dict[phone] = 0   
    
    if phone not in receiver_email_dict:
        receiver_email_dict[phone] = ''  

    if phone not in conversation_track:
        conversation_track[phone] = CS_QUOTE_START

    if phone not in top3_dict:
        top3_dict[phone] = []

    if phone not in pif_dict:
        pif_dict[phone] = []
    
    print('Convo:',conversation_track[phone])
    response_text = ""
    return_status = True
    take_next_step_convo = True
    options_found_flag = False
    add_more_product_flag = False

   
    pif_options = []
    pif_review_option = ''
   

    
    command = str(command).strip().lower()

    if 'shutdown' in command or command == "bye":
        response_text = 'Bye bye Sir. Have a nice day'
        return_status = False
       
    elif 'hello' == command or 'hi' == command:
        name = ''
        name = get_user(phone)
        if(name == 'new'):
            response_text = "Sorry I didn't know you.Your numbers is not in my registry.Please contact your manager for more details.Thankyou see you soon :)"
        else:
            response_text = 'Hello '+ name+'\n\n'+HELP_TEXT


    elif 'help me' in command:
        response_text = HELP_TEXT

    elif 'connect with cloobot' in command:
        response_text = CONTACT_TEXT


    #ask me anything
    elif 'quotation' in command or 'quote' in command or (phone in conversation_track and conversation_track[phone] == CS_QUOTE_START):
        print('c1')
        
        #initialising
        dealer_dict[phone]=''
        receiver_email_dict[phone] = None
        conversation_track[phone] = CS_QUOTE_START
        create_new_session(phone)
       
        

        try:
           

            resp = '''. What's the name of the client. Here are a list of common clients or give the client name you want\n'''
            
            resp += 'Please enter a choice 1-10:\n'            
            top3_dict[phone] = get_top3_values(INFO_DEALERS)
            for i,t in enumerate(top3_dict[phone]):
                resp += str(i+1) + '. ' + t + '\n'
            response_text = resp
            
            conversation_track[phone] = CS_QUOTE_CLIENT

        except Exception as e:
            print(e)
            response_text = e
    
    
    elif conversation_track[phone] == CS_QUOTE_CLIENT:
        print('c3')

        tmp_command = None
        try:
            tmp_command = int(command)
        except ValueError:
            pass

       
        if tmp_command and tmp_command >= 1 and tmp_command <= MAX_SEARCH_RESULTS:
            command = top3_dict[phone][int(command)-1]
            command = str(command).strip().lower()


        tmp, options = check_dealers(command)
        if tmp:
            dealer_dict[phone] = tmp
            # new session is started
            store_dealers_in_session(phone,tmp)
            resp = "Got it. "+dealer_dict[phone]+". Please enter product in  the format [name],[quantity],[price].If you want more than one product give each of them in new line using the correct format as said before."
            response_text = resp
            conversation_track[phone] = CS_QUOTE_PRODUCT_DETAILS
        else:
            if len(options) > 0:
                top3_dict[phone] = options
                response_text = "Found these options, please select an option: \n"
                for i,t in enumerate(top3_dict[phone]):
                    response_text += str(i+1) + '. ' + t + '\n'
               

    elif conversation_track[phone] == CS_QUOTE_PRODUCT_DETAILS:
        print('c2')

        product_dict[phone]=''
        price_dict[phone]=0  
        quantity_dict[phone] = 0
        top3_dict[phone] = []
        pif_dict[phone] = False

       
        command = str(command).strip().lower()

        print('command::',command)

        prod = None
        options = None
        qty = None
        price = None
        # if the prod,qty,price get and not confirmed comes in pendinglist
        pending_list = get_unstored_from_temp(phone)
        print("\n\n pending list : ",pending_list)
        #if any edit options given that comes here
        current_option = get_current_option(phone)
        print("\n current option \n",current_option)
        if(len(command) <= 2 and pending_list != []):
            pending = get_unstored_from_temp(phone)
            print("\n\ndata from temp : ",pending)
            option_list =  ast.literal_eval(pending[0][1])
            print("\n\n options list : ",option_list)
            store_confirmed_product(pending[0],option_list[int(command)-1])

       

            

        else:
            # store the correct product with correct nname and change status as 'Yes'
            store_in_temp(command,phone)
        
        # this get all from temp with status 'no'
        pending_list = get_unstored_from_temp(phone)
        print("\n\n pending list : ",pending_list)
        if(pending_list == [] and current_option == 0 ):
            resp = ''
            from_temp = get_for_check(phone)
            option_length = len(from_temp)*3
            resp = "All correct? Please enter a choice 1-"+str(option_length)+" to change:" 
            sno = 1
            for i in range(len(from_temp)):
                print(type(from_temp[i][1]),type(from_temp[i][2]),type(from_temp[i][3]))
                resp = resp + "\n product : "+str(i) + '\n'
                resp = resp + str(sno) + " . Product is "+ from_temp[i][1]  + '\n'
                sno = sno + 1
                resp = resp + str(sno) +" . Quantity is " + from_temp[i][2] + " nos" + '\n'
                sno = sno + 1
                resp = resp + str(sno) +" . Price is Rs." + from_temp[i][3] + "\n"
                sno = sno + 1
            resp = resp + "\n\nDo you want to add one more product? (Yes / No).If 'no' means Im going to send the quotation details to you via mail."
            response_text = resp
            conversation_track[phone] = CS_QUOTE_REVIEW
        else:
            # if product i mismatched this part ask for correct option
            sno = 1
            resp = 'Select one of these option related to your query\n'
            option_list = ast.literal_eval(pending_list[0][1])
            print("\n option list : ",option_list)
            for i in option_list:
                resp =  resp + str(sno) +" , " + i + '\n'
                sno = sno + 1
            response_text = resp

      

    elif conversation_track[phone] == CS_QUOTE_PRODUCT:
        print('c2')

        tmp_command = None
        try:
            tmp_command = int(command)
        except ValueError:
            pass

        if tmp_command and tmp_command >= 1 and tmp_command <= MAX_SEARCH_RESULTS:
            print('found choice::',top3_dict[phone],'::',top3_dict[phone][int(command)-1])
            command = top3_dict[phone][int(command)-1]
            command = str(command).strip().lower()

        print('command::',command)

        tmp, options = check_prod(command)
        
        if tmp:
            print('r1')
            product_dict[phone] = tmp

        

        else:
          
            if len(options) > 0:
                pif_options = options
              

    elif conversation_track[phone] == CS_QUOTE_QUANTITY:
        print('c4')

        tmp = isQty(command)
        if tmp:
            quantity_dict[phone] = tmp
        else:
            pass
           

    elif conversation_track[phone] == CS_QUOTE_PRICE:
        print('c41')

        tmp = isPrice(command)
        if tmp:
            price_dict[phone] = tmp
           
        else:
            pass
            
    elif conversation_track[phone] == CS_QUOTE_REVIEW:
        resp = ''
        pending_list = get_unstored_from_temp(phone)
        print("\n\n pending list : ",pending_list)
        current_option = get_current_option(phone)
        print("\n cuurent option : ",current_option)

        #if choose move to add or mail
        if(command in ['yes','Yes','Y','y','No','no','n','N']):
            print("\n Yes or No\n")
            
            if(command in ['yes','Yes','Y','y']):
                resp = "Sure. Please enter next product [name], [quantity], [price]."
                response_text = resp
                conversation_track[phone] = CS_QUOTE_PRODUCT_DETAILS
            else:
                # get detaisls of this session
                from_temp = get_for_check(phone)
                #store this sesion in quotes table
                store_in_permanent(from_temp,phone)
                # resp = "Im going to send the mail to you."
                # response_text =  resp
                conversation_track[phone] = CS_QUOTE_MAILID
                
        elif(current_option == 0):
            #ask for the options
            store_current_option(phone,int(command))
            which_detail_edit = int(command)%3
            if(which_detail_edit == 1):
                resp = "what is the product."
            elif(which_detail_edit == 2):
                resp = "what is the quantity."
            else:
                resp = "what is the price."
            response_text = resp

        elif(current_option > 0):
            #get the changed value and update them in tenp
            print("\n goint to change")
            change_the_details(command,phone)
            print("\n changed succesfully")
            if(pending_list == []):
                resp = ''
                from_temp = get_for_check(phone)
                option_length = len(from_temp)*3
                resp = "All correct? Please enter a choice 1-"+str(option_length)+" to change:" 
                sno = 1
                for i in range(len(from_temp)):
                    resp = resp + "\n product : "+str(i) + '\n'
                    resp = resp + str(sno) + " . Product is "+ from_temp[i][1]  + '\n'
                    sno = sno + 1
                    resp = resp + str(sno) +" . Quantity is " + from_temp[i][2] + " nos" + '\n'
                    sno = sno + 1
                    resp = resp + str(sno) +" . Price is Rs." + from_temp[i][3] + "\n"
                    sno = sno + 1
                resp = resp + "\n\nDo you want to add one more product? (Yes / No).If 'no' means Im going to send the quotation details to you via mail."
                response_text = resp
            store_current_option(phone,int(0))
            print("\n option set to 0\n")
            


  
    elif 'quit' in command:
        try:
            response_text = "bye, have a good day"
        except Exception as e:
            print(e)
            response_text = e
        
        return_status = False
        
    else:
        response_text = "Sorry, I don't understand that.\n" + HELP_TEXT
    

    if conversation_track[phone] == CS_QUOTE_MAILID:
        print('c6')
        #Add all 
        table  = get_data_for_excel(phone)
        print("\n table is :",table)
        name = get_user(phone)
        user_mail,user_password = get_user_credentials(phone)
        print("\n Username,password : ",user_mail,user_password)
        to,manager = get_mail_info(phone)
        qfilename = "quotation.xlsx"
        generate_price_quotation_anex1(qfilename, table)
        response_status = sendmail('quotation.xlsx',name,phone,to,manager)


      
        
    
        print("\n\n\n response text : ",response_status,"\n\n\n")

        if response_status == '''"ok"''':
            print("\n Mail has been sent \n")
            
            if(user_mail):
                print("\n\n Yes in \n\n")
                resp = 'Mail has been sent to '+ to + '. ' + HELP_TEXT 
                response_text = resp
                print(" \n response is : ",type(resp),resp)
                # response_text = 'Mail has been sent'
                conversation_track[phone] = CS_QUOTE_START

            else:
                response_text = 'Error while fetch your credentials'
            
        else:
            print("\n\n\n\nError While Sending the Mail\n\n\n\n")
        

    if pif_dict[phone]:
        print('Inside pif')
        if not product_dict[phone] or pif_review_option == '1':
            print('Inside pif prod')
            product_dict[phone] = ''
            conversation_track[phone] = CS_QUOTE_PRODUCT            
            resp = '''Which product? Your most popular products are listed below:\n'''
            
            if pif_options:
                top3_dict[phone] = pif_options    
            else:
                top3_dict[phone] = get_top3_values(INFO_PRODUCTS)
            
            for i,t in enumerate(top3_dict[phone]):
                resp += str(i+1) + '. ' + t + '\n'
            response_text = resp


        elif not quantity_dict[phone] or pif_review_option == '2':
            print('Inside pif quant')

            conversation_track[phone] = CS_QUOTE_QUANTITY
            resp = "What is the quantity in nos?"
            response_text = resp

        elif not price_dict[phone] or pif_review_option == '3':
            print('Inside pif price')

            conversation_track[phone] = CS_QUOTE_PRICE
            resp = "What is the price in INR?"
            response_text = resp
        else:
            conversation_track[phone] = CS_QUOTE_REVIEW
            resp = "All correct? Please enter a choice 1-3 to change:" + \
                "\n1. Product is "+ product_dict[phone] + \
                "\n2. Quantity is " + str(quantity_dict[phone]) +  " nos" + \
                "\n3. Price is Rs." + str(price_dict[phone]) + \
                "\n\nDo you want to add one more product? (Yes / No)"
            pif_dict[phone] = False
            response_text = resp

    

    return return_status, response_text 


