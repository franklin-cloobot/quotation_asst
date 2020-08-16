
#Single quote assistant
# from .quote_assistant import assistant
# from .constants import *

#Multiple products, one at a time
# from .assist_multi_1_at_a_time.quote_assistant import assistant
# from .assist_multi_1_at_a_time.constants import *

#Dump, Review, Change
from .assist_multi_drc.quote_assistant import assistant
from .assist_multi_drc.constants import *


is_loop_running = True
received_input = None

def wait_till_input_received(mode):
    input_data = ''
    if mode == MODE_MANUAL:
        input_data = input('Waiting for your input...')
    
    flag, resp = assistant(input_data, '9944019544', mode)
    print("Received input... ",resp)
    return flag

#loop to continue executing multiple commands
def start_conversation():
    while True:    
        if not wait_till_input_received(MODE_MANUAL):
            break
        
