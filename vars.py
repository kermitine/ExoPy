import scipy.constants

version = '1.8.10'
# ENABLE/DISABLE FUNCTIONALITY BELOW
masking_enabled = False # enable/disable cadence masking
sound_enabled = False # enable/disable sound effects
file_saving_enabled = True # recommended enabled (saves plots to saved_data/{starsystem})
# DEFAULTS
periodogram_lower_bound_default = 0.5
periodogram_upper_bound_default = 30
selected_bins = 700 # default: 700
rounding_decimal_places = 4 # decimal places to round to
file_saving_format = 'svg' # supports png, jpeg, pdf, svg (recommended)
# TELESCOPE DATA
selected_telescope = 'Kepler' # options are Kepler, K2, Tess (recommend Kepler)
selected_cadence = 'long' # long or short
# commonly used print statements for easy editing
prompt_periodogram_upper_bound = f'Please input periodogram upper bound (if blank, default {periodogram_upper_bound_default}): '
prompt_periodogram_lower_bound = f'Please input periodogram lower bound (if blank, default {periodogram_lower_bound_default}): '
prompt_input_not_recognized = 'Input not recognized. Please try again.'
# do not edit below
import string
user_flags = ['masking_enabled', masking_enabled, 'sound_enabled', sound_enabled, 'file_saving_enabled', file_saving_enabled] # add any user vars to this list. First name in str, then variable itself
list_of_tools = ['Star Pixelfile Retrieval', 'Star Light Curve Analysis', 'Exoplanet Radius Calculator', 'Star Habitable Zone Calculator', 'Stefan-Boltzmann Star Temperature Calculator', 'Kepler Orbital Radius Calculator', 'Inverse-Square Exoplanet Stellar Energy Calculator', 'Blackbody Exoplanet Temperature Calculator', 'Generate Full Report']
alphabet_list = list(string.ascii_uppercase) # list of every individual letter from the alphabet, uppercase
list_of_functions_index = []


# SCIENTIFIC CONSTANTS
constant_stefan_boltzmann = scipy.constants.Stefan_Boltzmann
constant_gravitational = scipy.constants.gravitational_constant
# CONVERSION CONSTANTS
constant_m_TO_AU = (1/149597870700) # from IAU 2015 Resolution B3
constant_AU_TO_m = 149597870700 # from IAU 2015 Resolution B3
constant_d_TO_s = 86400 # derived from (1day*24hours*60minutes*60seconds)
constant_solarmass_TO_kg = 1988400e24 # from NASA GSFC Sun Fact Sheet
constant_solarluminosity_TO_W = 3.828e26 # from IAU 2015 Resolution B3
constant_solarradii_TO_earthradii = (1/(6371/695700)) # from NASA GSFC Sun Fact Sheet (1earthradii/(6371kmearth/695700kmsun))
constant_solarradii_TO_m = 6.957e8 # from IAU 2015 Resolution B3
