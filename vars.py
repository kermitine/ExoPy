# USER VARS BELOW
masking_enabled = False # enable/disable cadence masking
sound_enabled = False # enable/disable sound effects
significant_figure_rounding = False # if disabled, rounds to 4 decimal places
file_saving_enabled = True # enable/disable saving of plots

periodogram_lower_bound_default = 0.5
periodogram_upper_bound_default = 30
file_saving_format = 'svg' # supports png, jpeg, pdf, svg (recommended)
rounding_decimal_places = 4 # fallback decimal places to round to if significant_figure_rounding = False
selected_telescope = 'Kepler' # options are Kepler, K2, Tess
selected_cadence = 'long' # long or short
selected_bins = 700 # default: 700
# commonly used print statements for easy editing
prompt_periodogram_upper_bound = f'Please input periodogram upper bound (if blank, default {periodogram_upper_bound_default}):'
prompt_periodogram_lower_bound = f'Please input periodogram lower bound (if blank, default {periodogram_lower_bound_default}):'
prompt_input_not_recognized = 'Input not recognized. Please try again.'
# do not edit below
import string
user_flags = ['masking_enabled', masking_enabled, 'sound_enabled', sound_enabled, 'significant_figure_rounding', significant_figure_rounding, 'file_saving_enabled', file_saving_enabled] # add any user vars to this list. First name in str, then variable itself
version = '1.1.8'
list_of_tools = ['Exoplanet Radius Calculator','Star Pixelfile Retrieval', 'Star Light Curve Retrieval']
alphabet_list = list(string.ascii_uppercase) # list of every individual letter from the alphabet, uppercase
list_of_functions_index = []

