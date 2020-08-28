
from .allotment_bot import *
from .constants import *
# from .constants import *
is_loop_running = True
received_input = None

def wait_till_input_received(mode):
    input_data = ''
    if mode == MODE_MANUAL:
        input_data = input('Waiting for your input...')
    
    flag, resp = assistant_act3(input_data, '7868819576', mode)
    print("Received input... ",resp)
    return flag

#loop to continue executing multiple commands
def start():
    while True:    
        if not wait_till_input_received(MODE_MANUAL):
            break
        
