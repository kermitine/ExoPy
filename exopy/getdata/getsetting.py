from config.config import *
def get_setting():
    while True: # PREVENTS CRASHES FROM UNRECOGNIZED INPUTS
        user_input = input('Select the setting you want to change: ')
        if user_input.lower().strip() not in user_flags:
            print(prompt_input_not_recognized)
            continue
        else:
            try:
                user_input = str(user_input).lower().strip()
                break
            except ValueError:
                print(prompt_input_not_recognized)
    return user_input
    
def get_new_setting(old_setting_value):
    if str(type(old_setting_value)) == "<class 'bool'>":
        old_setting_type = 'True/False'
        new_setting_allowed_values = ['True', 'False']
    if str(type(old_setting_value)) == "<class 'str'>":
        old_setting_type = 'String'
        if old_setting_value.lower().strip() in ['k2', 'kepler', 'tess']:
            new_setting_allowed_values = ['k2', 'kepler', 'tess']
        elif old_setting_value.lower().strip() in ['long', 'short']:
            new_setting_allowed_values = ['long', 'short']
        else:
            new_setting_allowed_values = ['svg', 'png', 'jpeg', 'jpg', 'tiff', 'tif', 'pdf', 'webp']
    if str(type(old_setting_value)) == "<class 'int'>":
        old_setting_type = 'Integer'
        new_setting_allowed_values = ['Integer']


    while True: # PREVENTS CRASHES FROM UNRECOGNIZED INPUTS
        user_input = input(f'Enter new value for setting ({', '.join(new_setting_allowed_values)}): ')


        # BOOLS 
        if old_setting_type == 'True/False':
            try:
                user_input.strip().capitalize()
            except:
                print(prompt_input_not_recognized)
                continue
            if user_input == 'True':
                return True
            elif user_input == 'False':
                return False
            else:
                print(prompt_input_not_recognized)
                continue

        # STR
        if old_setting_type == 'String':
            if user_input.strip().lower() in new_setting_allowed_values:
                try:
                    user_input = str(user_input)
                except:
                    print(prompt_input_not_recognized)
                    continue
                return user_input
            else:
                print(prompt_input_not_recognized)
                continue
        
        # INT
        if old_setting_type == 'Integer':
            try:
                user_input = int(user_input)
            except:
                print(prompt_input_not_recognized)
                continue
            return user_input
                
            








