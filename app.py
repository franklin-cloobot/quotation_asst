from Monolithic.main import start_conversation
from Monolithic.server import start_whatsapp_conversation_server

try:
    start_whatsapp_conversation_server()
    # start_conversation()
except Exception as e:
    print(e)