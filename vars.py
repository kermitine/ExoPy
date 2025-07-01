# USER VARS BELOW
masking_enabled = False # enable/disable cadence masking
sound_enabled = True # enable/disable sound effects
file_saving_enabled = True # enable/disable saving of plots
brain_rot_enabled = False # enables brain rot. WARNING: HEAVILY DEGRADES PERFORMANCE

brain_rot_urls = ['https://www.youtube.com/watch?v=dRpXXgARy_s', 'https://www.youtube.com/watch?v=BqrgpToijV8', 'https://www.youtube.com/watch?v=TDpZl9INc4w', 'https://www.youtube.com/watch?v=u7kdVe8q5zs', 'https://www.youtube.com/watch?v=vTfD20dbxho']
periodogram_lower_bound_default = 1
periodogram_upper_bound_default = 30
file_saving_format = 'svg' # supports png, jpeg, pdf, svg (recommended)
telescope = 'Kepler' # options are Kepler, K2, Tess

# commonly used print statements for easy editing
prompt_periodogram_upper_bound = f'Please input periodogram upper bound (if blank, default {periodogram_upper_bound_default}):'
prompt_periodogram_lower_bound = f'Please input periodogram lower bound (if blank, default {periodogram_lower_bound_default}):'
prompt_input_not_recognized = 'Input not recognized. Please try again.'

# do not edit below
import string
user_flags = ['masking_enabled', masking_enabled, 'sound_enabled', sound_enabled, 'file_saving_enabled', file_saving_enabled, 'brain_rot_enabled', brain_rot_enabled] # add any user vars to this list. First name in str, then variable itself
version = '1.0.0'
list_of_tools = ['Star Image Retrieval', 'Star Light Curve Retrieval', 'Star Light Curve Bulk Retrieval']
alphabet_list = list(string.ascii_uppercase)
list_of_functions_index = []

