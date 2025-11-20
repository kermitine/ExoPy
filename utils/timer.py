

timer_data = {
    'timer_active': False,
    'start_time': 0,
    'end_time': 0
}

import time

def timer():
    if timer_data['timer_active'] == False: # start timer
        timer_data['start_time'] = time.time()
        timer_data['timer_active'] = True
        return None
    
    elif timer_data['timer_active'] == True:
        timer_data['end_time'] = time.time()
        elapsed_time = round((timer_data['end_time'] - timer_data['start_time']), 1)

        timer_data['timer_active'] = False
        
        print(f'took {elapsed_time} seconds')
        return elapsed_time