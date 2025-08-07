"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the ExoPy project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

import math
from config.constants import *
from config.config import *
def blackbody_temperature_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative):
    star_luminosity_watts_upper = (star_luminosity+star_luminosity_uncertainty_positive) * constant_solarluminosity_TO_W
    star_luminosity_watts_nominal = star_luminosity * constant_solarluminosity_TO_W
    star_luminosity_watts_lower = (star_luminosity-star_luminosity_uncertainty_negative) * constant_solarluminosity_TO_W

    exoplanet_orbital_radius_m_upper = (exoplanet_orbital_radius_AU + exoplanet_orbital_radius_AU_uncertainty_positive) * constant_AU_TO_m
    exoplanet_orbital_radius_m_nominal = exoplanet_orbital_radius_AU * constant_AU_TO_m
    exoplanet_orbital_radius_m_lower = (exoplanet_orbital_radius_AU-exoplanet_orbital_radius_AU_uncertainty_negative) * constant_AU_TO_m

    try:
        exoplanet_temperature_k_upper = ((star_luminosity_watts_upper)/(16*math.pi*((exoplanet_orbital_radius_m_lower)**2)*constant_stefan_boltzmann))**0.25
        exoplanet_temperature_k_nominal = ((star_luminosity_watts_nominal)/(16*math.pi*((exoplanet_orbital_radius_m_nominal)**2)*constant_stefan_boltzmann))**0.25
        exoplanet_temperature_k_lower = ((star_luminosity_watts_lower)/(16*math.pi*((exoplanet_orbital_radius_m_upper)**2)*constant_stefan_boltzmann))**0.25

    except ZeroDivisionError:
        print('ERROR: Divison by zero. Did you enter the correct exoplanet radius data?')
        return 'Not Generated', 0, 0
    
    exoplanet_temperature_k_upper_diff = exoplanet_temperature_k_upper - exoplanet_temperature_k_nominal
    exoplanet_temperature_k_lower_diff = exoplanet_temperature_k_nominal - exoplanet_temperature_k_lower

    try:
        print(f'Calculated nominal exoplanet temperature (assuming blackbody): {round(exoplanet_temperature_k_nominal, rounding_decimal_places)} K (+{round(exoplanet_temperature_k_upper_diff, rounding_decimal_places)} K -{round(exoplanet_temperature_k_lower_diff, rounding_decimal_places)} K)')
        return round(exoplanet_temperature_k_nominal, rounding_decimal_places), round(exoplanet_temperature_k_upper_diff, rounding_decimal_places), round(exoplanet_temperature_k_lower_diff, rounding_decimal_places)

    except TypeError:
        print('ERROR: Complex number. Are you sure you entered the correct data?')
        return '(Not Generated)', 0, 0