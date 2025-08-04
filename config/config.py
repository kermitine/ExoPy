version = '2.2.2'
# USER VARS BELOW
user_flags = {
"masking_enabled": False,
"sound_enabled": False,
"file_saving_enabled": True,
"attempt_wikipedia_pull": True,
"selected_bins": 700,
"file_saving_format": 'svg',
"selected_telescope": 'Kepler',
"selected_cadence": "long"
}
# DEFAULTS
periodogram_lower_bound_default = 0.5
periodogram_upper_bound_default = 30
rounding_decimal_places = 4 # decimal places to round to
# commonly used print statements for easy editing
prompt_periodogram_upper_bound = f'Please input periodogram upper bound (if blank, default {periodogram_upper_bound_default}): '
prompt_periodogram_lower_bound = f'Please input periodogram lower bound (if blank, default {periodogram_lower_bound_default}): '
prompt_input_not_recognized = 'Input not recognized. Please try again.'
# do not edit below
import string
list_of_tools = ['Star Pixelfile Retrieval', 'Star Light Curve Analysis', 'Exoplanet Radius Calculator', 'Star Habitable Zone Calculator', 'Stefan-Boltzmann Star Temperature Calculator', 'Kepler Orbital Radius Calculator', 'Inverse-Square Exoplanet Stellar Energy Calculator', 'Blackbody Exoplanet Temperature Calculator', 'Generate Full Report', 'Edit Settings']
alphabet_list = list(string.ascii_uppercase) # list of every individual letter from the alphabet, uppercase
list_of_functions_index = []
