"""
Copyright (C) 2025 Ayrik Nabirahni. This file is licensed under
the AGPLv3 license, and is apart of the ExoPy project.
See LICENSE and README for more details.
"""

from config.config import *
from config.constants import *
import math
def stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity, star_radius_uncertainty_positive, star_radius_uncertainty_negative, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative):
    

    star_radius_meters_upper = (star_radius+star_radius_uncertainty_positive) * constant_solarradii_TO_m
    star_luminosity_watts_upper = (star_luminosity+star_luminosity_uncertainty_positive) * constant_solarluminosity_TO_W

    star_radius_meters_nominal = star_radius * constant_solarradii_TO_m
    star_luminosity_watts_nominal = star_luminosity * constant_solarluminosity_TO_W

    star_radius_meters_lower = (star_radius-star_radius_uncertainty_negative) * constant_solarradii_TO_m
    star_luminosity_watts_lower = (star_luminosity-star_luminosity_uncertainty_negative) * constant_solarluminosity_TO_W

    try:
        star_temperature_upper = ((star_luminosity_watts_upper)/(4*math.pi*constant_stefan_boltzmann*(star_radius_meters_lower)**2))**0.25
        star_temperature_nominal = ((star_luminosity_watts_nominal)/(4*math.pi*constant_stefan_boltzmann*(star_radius_meters_nominal)**2))**0.25
        star_temperature_lower = ((star_luminosity_watts_lower)/(4*math.pi*constant_stefan_boltzmann*(star_radius_meters_upper)**2))**0.25
    except ZeroDivisionError:
        print('ERROR: Division by zero. Did you enter the correct star radius data?')
        return '(Not Generated)', 0, 0

    star_temperature_upper_diff = star_temperature_upper-star_temperature_nominal
    star_temperature_lower_diff = star_temperature_nominal-star_temperature_lower

    try:
        print(f'Calculated nominal star temperature: {round(star_temperature_nominal, rounding_decimal_places)} K (+{round(star_temperature_upper_diff, rounding_decimal_places)} K -{round(star_temperature_lower_diff, rounding_decimal_places)} K)')
        return round(star_temperature_nominal, rounding_decimal_places), round(star_temperature_upper_diff, rounding_decimal_places), round(star_temperature_lower_diff, rounding_decimal_places)
    except TypeError:
        print('ERROR: Complex number. Are you sure you entered the correct data?')
        return '(Not Generated)', 0, 0