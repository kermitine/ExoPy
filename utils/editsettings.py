from config.config import *
from exopy.getdata.getsetting import *
def show_flags():
    for key in user_flags:
        print(f'{key} = {user_flags[key]}')
    print('\n' * 2)

def edit_settings():
    show_flags()
    user_input = get_setting()
    new_setting = get_new_setting(user_flags[user_input])
    user_flags[user_input] = new_setting