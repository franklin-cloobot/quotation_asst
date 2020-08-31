from .constants import *
from .utils import *
from .templates.cloobot import generate_price_quotation_anex1
import ast
from time import strftime
import pandas as pd
import json
import base64
import re
import requests
import datetime
import urllib





conversation_track = 0
top3_dict = []

HELP_TEXT = """You can use these commands and I'll help you out:\n
- get quote / quotation or : starts the conversation to generate price quotation.\n
- connect with cloobot : displays phone number of a Sales Manager of Cloobot Techlabs
"""

CONTACT_TEXT = """
Vinod Thamilarasan
vinod@cloobot.com
+91 7904521277

Visit us at https://www.cloobot.ai
"""


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

def check_dealers(command,phone):
    dealers = populate_from_excel(INFO_DEALERS, DEF_EXCEL_FILE,phone)
    print(dealers)
    options = []
    for j in dealers:
        if(command==j.strip().lower()):
            return j, options
    
    options = get_similar_matches(command, dealers,phone)
    print('In dealers, ',command, '::', options)
    return None, options

def get_top3_values(info_mode,phone):
    return populate_from_excel(info_mode, DEF_EXCEL_FILE,phone)[:MAX_SEARCH_RESULTS]


def get_price_for_product(product_or_part,phone):
    products = populate_from_excel(INFO_PRODUCTS, DEF_EXCEL_FILE,phone)
    parts = populate_from_excel(INFO_PART_CODE, DEF_EXCEL_FILE,phone)
    price_list = get_price_list_from_excel(DEF_EXCEL_FILE,phone)

    for row in price_list:

        if product_or_part == row[COL_PART_CODE].strip().lower() or product_or_part == row[COL_PRODUCT].strip().lower():
            return float(row[COL_PRICE])
    return None


def check_auth_email(command,phone):
    options = []

    if command == 'me':
        return MY_EMAIL_ID, options
    return command, options


    
def isQty(inputString,phone):
    inputString = inputString.replace('units','').replace('nos','').replace('items','')
    l = inputString.split(' ')
    for i in l:
        if(i.isdigit()):
            return int(i)
    return 0

def isPrice(inputString,phone):
    inputString = inputString.replace('inr','').replace('rs.','').replace('rs','')
    tmp = None
    try:
        tmp = float(inputString)
    except ValueError:
        pass
    return tmp
    
def check_yes_no(inputString,phone):
    if inputString == 'y' or inputString == 'Y' or inputString == 'yes' or inputString == 'Yes':
        return 'y'
    elif inputString == 'n' or inputString == 'N' or inputString == 'no' or inputString == 'No':
        return 'n'
    return None

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
        prod, opts = check_prod(prod_str,phone,phone)
        print('In check prod details::',prod_str,'::',prod,'::',opts)


        return prod, opts, qty, price


def check_product_details_v2(command,phone):
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

        qty = isQty(qty_str,phone)
        price = isPrice(price_str,phone)
        prod, opts = check_prod(prod_str,phone,phone)
        print('In check prod details::',prod_str,'::',prod,'::',opts)
        
        return prod, opts, qty, price






def assistant(command, phone, mode):
    top3_dict = []
    if(check_number_in_track(phone)):
        conversation_track,top3_dict = current_state(phone)
        if top3_dict == '[]':
            top3_dict = []
        else:
            top3_dict = top3_dict
            print("\n top3 : ",top3_dict,type(top3_dict))
    else:
        start_conversation(phone)
        conversation_track = 0
    
    print("\n\ncommand : ",command,"   Conversation phone track : ",conversation_track,"  Top3 dict : ",top3_dict,"command length : ",len(command))
    

    

    
    
    print('Convo:',conversation_track)
    response_text = ""
    return_status = True
   

   

    
    command = str(command).strip().lower()

    if 'shutdown' in command or command == "bye":
        response_text = 'Bye bye Sir. Have a nice day'
        return_status = False
       
    elif 'hello' in command or 'hi' in command:
        name = ''
        name,org = get_user(phone)
        if(name == 'new'):
            response_text = "Sorry I didn't know you.Your numbers is not in my registry.Please contact your manager for more details.Thankyou see you soon :)"
        else:
            response_text = 'Hello '+ name+'\n\n'+HELP_TEXT
        


    elif 'help me' in command:
        response_text = HELP_TEXT

    elif 'connect with cloobot' in command:
        response_text = CONTACT_TEXT


    #ask me anything
    elif 'quotation' in command or 'quote' in command or (conversation_track == CS_QUOTE_START):
        print('c1')
        
        #initialising
        
        change_conversation_state(phone,CS_QUOTE_START)
        conversation_track,top3_dict = current_state(phone) 
        # conversation_track[phone] = CS_QUOTE_START
        create_new_session(phone)
       
        

        try:
           

            resp = '''What's the name of the client. Here are a list of common clients or give the client name you want\n'''
            
            resp += 'Please enter a choice 1-10:\n'            
            # top3_dict[phone] = get_top3_values(INFO_DEALERS,phone)
            print("top3_dict : ",get_top3_values(INFO_DEALERS,phone),type(get_top3_values(INFO_DEALERS,phone)))
            change_top3(phone,str(get_top3_values(INFO_DEALERS,phone)))
            conversation_track,top3_dict = current_state(phone)
            for i,t in enumerate(top3_dict):
                resp += str(i+1) + '. ' + t + '\n'
            response_text = resp
            
            # conversation_track[phone] = CS_QUOTE_CLIENT
            change_conversation_state(phone,CS_QUOTE_CLIENT)
            conversation_track,top3_dict = current_state(phone)
            print("\n conversation track : ",conversation_track)

        except Exception as e:
            print(e)
            response_text = "Sorry, there is a problem.\n" + HELP_TEXT
    
    
    elif conversation_track == CS_QUOTE_CLIENT:
        try:
            print('c2')
            conversation_track,top3_dict = current_state(phone)
            tmp_command = None
            try:
                tmp_command = int(command)
            except ValueError:
                pass

        
            if tmp_command and tmp_command >= 1 and tmp_command <= MAX_SEARCH_RESULTS:
                command = top3_dict[int(command)-1]
                command = str(command).strip().lower()


            tmp, options = check_dealers(command,phone)
            if tmp:
                
                # new session is started
                store_dealers_in_session(phone,tmp)
                args = {"phone": phone}
                #url = "localhost:8001/product_list?{}".format(urllib.parse.urlencode(args))
                url = "quote.cloobot.ai/quote_testing_api/product_list?{}".format(urllib.parse.urlencode(args))
                resp = "Got it "+tmp+". Please enter product in the format [name],[quantity],[price].If you want more than one product give each of them in new line using the correct format as said before.If u not sure about the product see the list of products\n here : " + url
                response_text = resp
                # conversation_track[phone] = CS_QUOTE_PRODUCT_DETAILS
                change_conversation_state(phone,CS_QUOTE_PRODUCT_DETAILS)
                conversation_track,top3_dict = current_state(phone)
                print("\n conversation track : ",conversation_track)

            else:
                if len(options) > 0:
                    # top3_dict[phone] = options
                    change_top3(phone,str(options))
                    change_conversation_state(phone,CS_QUOTE_CLIENT)
                    conversation_track,top3_dict = current_state(phone)
                    print("\n conversation track : ",conversation_track)
                    response_text = "Found these options, please select an option: \n"
                    for i,t in enumerate(top3_dict):
                        response_text += str(i+1) + '. ' + t + '\n'
                else:
                    response_text = "There is no any clients related to your querry.Please re enter.\n" + HELP_TEXT
        except:
            response_text = "Sorry, there is a problem.\n" + HELP_TEXT
               

    elif conversation_track == CS_QUOTE_PRODUCT_DETAILS:
        print('c3')

        
         
        # try:
        # top3_dict[phone] = []
        change_top3(phone,'[]')
    

    
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
            try:
                store_in_temp(command,phone)
            except :
                print("\n\n error in storing")
        
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
            # conversation_track[phone] = CS_QUOTE_REVIEW
            change_conversation_state(phone,CS_QUOTE_REVIEW)
            conversation_track,top3_dict = current_state(phone)
            print("\n conversation track : ",conversation_track)
        else:
            # if product i mismatched this part ask for correct option
            sno = 1
            resp = 'Select one of these option related to your query :\n'
            option_list = ast.literal_eval(pending_list[0][1])
            try:
                if(option_list == [] or option_list == None):
                    error_querry = get_error_command(pending_list[0][0])
                    print("\n\nerror querry : ",error_querry)
                    delete_error_querry(pending_list[0][0])
                    args = {"phone": phone}
                    url = "quote.cloobot.ai/quote_testing_api/product_list?{}".format(urllib.parse.urlencode(args))
                    # url = "localhost:8001/product_list?{}".format(urllib.parse.urlencode(args))
                    change_conversation_state(phone,CS_QUOTE_PRODUCT_DETAILS)
                    conversation_track,top3_dict = current_state(phone)
                    print("\n conversation track : ",conversation_track)
                    # url = "quote.cloobot.ai/quote_testing_api/product_list?{}".format(urllib.parse.urlencode(args))
                    response_text = "There is no any product related to your query or the inpuformat is wrong for command '" + error_querry + "' ,please re enter in correct format" + "\nPlease enter product in the format [name],[quantity],[price].If you want more than one product give each of them in new line using the correct format as said before.If u not sure about the product see the list of products\n here : " + url
                    
                else:
                    print("\n option list : ",option_list)
                    for i in option_list:
                        resp =  resp + str(sno) +" , " + i + '\n'
                        sno = sno + 1
                    response_text = resp
            except:
                response_text = "Sorry, there is a problem.\n" + HELP_TEXT
        # except:
        #     response_text = "Sorry, there is a problem.\n" + HELP_TEXT

      

   
            
    elif conversation_track == CS_QUOTE_REVIEW:
        
        resp = ''
        pending_list = get_unstored_from_temp(phone)
        print("\n\n pending list : ",pending_list)
        current_option = get_current_option(phone)
        print("\n cuurent option : ",current_option)

        #if choose move to add or mail
        if(command in ['yes','Yes','Y','y','No','no','n','N']):
            print("\n Yes or No\n")
            
            if(command in ['yes','Yes','Y','y']):
                print("\n\n Yes")
                args = {"phone": phone}
                url = "quote.cloobot.ai/quote_testing_api/product_list?{}".format(urllib.parse.urlencode(args))
                # url = "localhost:8001/product_list?{}".format(urllib.parse.urlencode(args))
                resp = "Sure. Please enter next product [name],[quantity],[price].\nUse this link for your product code reference : " + url
                response_text = resp
                # conversation_track[phone] = CS_QUOTE_PRODUCT_DETAILS
                change_conversation_state(phone,CS_QUOTE_PRODUCT_DETAILS)
                conversation_track,top3_dict = current_state(phone)
                print("\n conversation track : ",conversation_track)

            else:
                print("go to mail")
                # get detaisls of this session
                from_temp = get_for_check(phone)
                #store this sesion in quotes table
                store_in_permanent(from_temp,phone)
                change_conversation_state(phone,CS_QUOTE_MAILID)
                conversation_track,top3_dict = current_state(phone)
                print("\n conversation track : ",conversation_track)
                
        elif(current_option == 0):
            #ask for the options
            store_current_option(phone,int(command))
            which_detail_edit = int(command)%3
            if(which_detail_edit == 1):
                args = {"phone": phone}
                url = "quote.cloobot.ai/quote_testing_api/product_list?{}".format(urllib.parse.urlencode(args))
                # url = "localhost:8001/product_list?{}".format(urllib.parse.urlencode(args))
                resp = "what is the product." + "\nUse this link for your product code reference : " + url
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
                    resp = resp + "\n product : "+str(i+1) + '\n'
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
        # except:
        # response_text = "Sorry, there is a problem.\n" + HELP_TEXT

            


  
    elif 'quit' in command:
        try:
            response_text = "bye, have a good day"
        except Exception as e:
            print(e)
            response_text = e
        
        return_status = False
        
    else:
        response_text = "Sorry, I don't understand that.\n" + HELP_TEXT
    

    if conversation_track == CS_QUOTE_MAILID:
        try:
            print('c6')
            #Add all 
            table  = get_data_for_excel(phone)
            print("\n table is :",table)
            name,org = get_user(phone)
            to,manager = get_mail_info(phone)
            ts = datetime.datetime.now().strftime("_%H_%M_%S_%f")
            qfilename =org+ts+".xlsx"
            
            path = "/var/www/flaskapp_quote_testing/quotation_asst/Monolithic/assist_multi_drc/quotes/"
            # path = "D:/devops/backend/qoutation-asst/Monolithic/assist_multi_drc/quotes/"
            generate_price_quotation_anex1(qfilename,path, table)
            response_status = sendmail(qfilename,path,name,phone,to,manager)
            change_conversation_state(phone,0)
            conversation_track,top3_dict = current_state(phone)
            print("\n conversation track : ",conversation_track)

        
            
        
            print("\n\n\n response text : ",response_status,"\n\n\n")

            if response_status == '''"ok"''':
                print("\n Mail has been sent \n")
                
                
                print("\n\n Yes in \n\n")
                resp = 'Mail has been sent to '+ to + '. ' + HELP_TEXT 
                response_text = resp
                print(" \n response is : ",type(resp),resp)
                # conversation_track[phone] = CS_QUOTE_START
                change_conversation_state(phone,0)
                conversation_track,top3_dict = current_state(phone)
                print("\n conversation track : ",conversation_track)

                
                
            else:
                print("\n\n\n\nError While Sending the Mail\n\n\n\n")
        except:
            response_text = "Sorry, there is a problem.\n" + HELP_TEXT
        

   

    

    return return_status, response_text 


