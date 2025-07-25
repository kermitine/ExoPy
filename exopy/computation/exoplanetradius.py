from config.constants import *
from config.config import *
import math
def find_exoplanet_radius(star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative, depth_of_phase_fold):
    """
    Estimates the radius of a transiting exoplanet using the radius of the transited star (given, solar radii)
    and the dip in the light emitted off the star (measured in flux.) The flux is found and automatically saved
    after retrieving light curve and creating phase fold.
    
    """
    try:
        planet_radius_solar_upperlimit_uncertainty = (star_radius + star_radius_uncertainty_positive) * math.sqrt(1-depth_of_phase_fold) # calculates highest possible value
        planet_radius_solar_lowerlimit_uncertainty = (star_radius - star_radius_uncertainty_negative) * math.sqrt(1-depth_of_phase_fold) # calculates lowest possible value
        planet_radius_solar = star_radius * math.sqrt(1-depth_of_phase_fold)
    except ValueError:
        print('ERROR: Negative root. Did you enter the correct flux data?')
        return '(Not Generated)', 0, 0 
    planet_radius_solar_positive_uncertainty = planet_radius_solar_upperlimit_uncertainty - planet_radius_solar
    planet_radius_solar_negative_uncertainty = planet_radius_solar - planet_radius_solar_lowerlimit_uncertainty


    planet_radius_earth_nominal = planet_radius_solar * constant_solarradii_TO_earthradii # converts solar radii to earth radii
    planet_radius_earth_upper_diff = planet_radius_solar_positive_uncertainty * constant_solarradii_TO_earthradii
    planet_radius_earth_lower_diff = planet_radius_solar_negative_uncertainty * constant_solarradii_TO_earthradii

    print(f'Calculated nominal planet radius: {round(planet_radius_earth_nominal, rounding_decimal_places)} R⊕ (+{round(planet_radius_earth_upper_diff, rounding_decimal_places)} R⊕ -{round(planet_radius_earth_lower_diff, rounding_decimal_places)} R⊕)')
    return round(planet_radius_earth_nominal, rounding_decimal_places), round(planet_radius_earth_upper_diff, rounding_decimal_places), round(planet_radius_earth_lower_diff, rounding_decimal_places)