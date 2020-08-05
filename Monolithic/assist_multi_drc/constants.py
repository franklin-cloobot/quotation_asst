MODE_MANUAL = 0
MODE_WHATSAPP = 1
MODE_VOICE = 2

# MY_EMAIL_ID = "stejasvin@cloobot.com"
ORG_ID = 'org_101'
# AUTHORIZED_RECEIVER_EMAILS = [MY_EMAIL_ID, "vinod@cloobot.com", "aravindh@cloobot.com"]
MY_EMAIL_ID = "franklin@cloobot.com"

AUTHORIZED_RECEIVER_EMAILS = [MY_EMAIL_ID, "vinod@cloobot.com", "aravindh@cloobot.com"]
# sales_manager_id = "mtpl2"
chat_conversation = "not stored"
email_conversation = "not stored"
thread_id = "not stored"
API_ROOT = "rpm.cloobot.ai"
WHATSAPP_SERVER_PORT = 8203

OUTLOOK_ROOT = API_ROOT
OUTLOOK_PORT = 8204

MAX_SEARCH_RESULTS = 10

INFO_DEALERS = 0
INFO_PRODUCTS = 1
INFO_PRICE = 2
INFO_PART_CODE = 3
INFO_QUANTITY = 4

HEADER_DEALERS      = "Client"
HEADER_PRODUCTS     = "Product"
HEADER_PRICE        = "Price"
HEADER_PART_CODE    = "Part code"
HEADER_QUANTITY     = "Quantity"

DEF_EXCEL_FILE = "Assets/Quotation Chatbot Details.xlsx"

#Sheet Product and Price list
COL_PART_CODE = 'Part Code'
COL_PRICE = 'Unit Price'
COL_PRODUCT = 'Product Description'



CS_QUOTE_START              = 0
CS_QUOTE_CLIENT             = 1
CS_QUOTE_PRODUCT_DETAILS    = 2
CS_QUOTE_COLLECT_REM        = 3
CS_QUOTE_REVIEW             = 4
CS_QUOTE_ADDMORE            = 5
CS_QUOTE_MAILID             = 6
CS_QUOTE_END                = 7

CS_QUOTE_PRODUCT    = 10
CS_QUOTE_QUANTITY   = 11
CS_QUOTE_PRICE      = 12


CONVERSATION_STEP_LIST = [
    CS_QUOTE_START,
    CS_QUOTE_CLIENT,
    CS_QUOTE_PRODUCT_DETAILS,
    CS_QUOTE_REVIEW,
    CS_QUOTE_ADDMORE,
    CS_QUOTE_MAILID,
    CS_QUOTE_END
]