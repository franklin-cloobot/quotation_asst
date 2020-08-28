from .constants import *
from .utils import *
import dateutil.relativedelta
from time import strftime
import pandas as pd
import json
import base64
import re
import requests
# import datetime
from datetime import datetime
import pytz




conversation_track = {}


HELP_TEXT = """You can use these commands and I'll help you out:\n
- "Give me a project" to starts the conversation to generate price quotation.\n
- connect with cloobot : displays phone number of a Sales Manager of Cloobot Techlabs
"""

CONTACT_TEXT = """
Vinod Thamilarasan
vinod@cloobot.com
+91 7904521277

Visit us at https://www.cloobot.ai
"""



def assistant_act1(command, phone, mode):
    print(command)
    return_status = True
    if phone not in conversation_track:
        conversation_track[phone] = HI
    
   

    
    response_text = ""
   

   

    # "if statements for executing commands"  
    command = str(command).strip().lower()

    if 'shutdown' in command or command == "bye":
        response_text = 'Bye bye Sir. Have a nice day'
        return_status = False
       
    
    #greetings
    elif 'hello' in command or 'hi' in command and conversation_track[phone] == 0:
        response_text = """Hi Franklin,
What's on your mind?
1. Register a visit

Leads:
2. See leads alloted to you

3. Receive for a new lead

4. Add a new Lead

Quotes:
5. Generate new quote

6. See previous quotes"""
        
        conversation_track[phone] = NEW_LEAD
    
    elif  conversation_track[phone] == NEW_LEAD:
        response_text = "Is this a new customer? (Y/N)" 
        conversation_track[phone] = LEAD_DETAILS 

    elif  conversation_track[phone] == LEAD_DETAILS:
        response_text = """Please enter the following details in this order:

Company Name, 
Contact person name,
Phone, 
Email"""
        conversation_track[phone] = ENQUIRY

    elif  conversation_track[phone] == ENQUIRY:
        response_text = """What is the enquiry? You may paste the enquiry content here."""
        conversation_track[phone] = AFTER_ENQUIRY

    elif  conversation_track[phone] == AFTER_ENQUIRY:
        response_text = """In order to send a First Contact Welcome email with product collaterals, please select the product list.
http://quote.cloobot.ai/productlist?p=98989898989

Or Send "No" to skip"""
        conversation_track[phone] = PRODUCT_DETAILS

    elif  conversation_track[phone] == PRODUCT_DETAILS:
        response_text = """Got it! I have sent an email to the client ccing you and sales manager."""
        conversation_track[phone] = AFTER_ENQUIRY

    return 1,response_text