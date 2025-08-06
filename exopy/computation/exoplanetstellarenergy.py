# Copyright (C) 2025 Ayrik Nabirahni
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see https://www.gnu.org/licenses.


from config.config import *
from config.constants import *
import math
def exoplanet_flux_received(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative):
    star_luminosity_watts_upper = (star_luminosity+star_luminosity_uncertainty_positive) * constant_solarluminosity_TO_W
    star_luminosity_watts_nominal = star_luminosity * constant_solarluminosity_TO_W
    star_luminosity_watts_lower = (star_luminosity-star_luminosity_uncertainty_negative) * constant_solarluminosity_TO_W

    exoplanet_orbital_radius_meters_upper = (exoplanet_orbital_radius_AU+exoplanet_orbital_radius_AU_uncertainty_positive) * constant_AU_TO_m
    exoplanet_orbital_radius_meters_nominal = exoplanet_orbital_radius_AU * constant_AU_TO_m
    exoplanet_orbital_radius_meters_lower = (exoplanet_orbital_radius_AU-exoplanet_orbital_radius_AU_uncertainty_negative) * constant_AU_TO_m

    try:
        flux_watts_upper = star_luminosity_watts_upper / (4 * math.pi * exoplanet_orbital_radius_meters_lower ** 2)
        flux_watts_nominal = star_luminosity_watts_nominal / (4 * math.pi * exoplanet_orbital_radius_meters_nominal ** 2)
        flux_watts_lower = star_luminosity_watts_lower / (4 * math.pi * exoplanet_orbital_radius_meters_upper ** 2)
    except ZeroDivisionError:
        print("ERROR: Divison by Zero. Did you enter the correct semi-major axis data of the exoplanet's orbit?")
        return '(Not Generated)', 0, 0

    flux_watts_upper_diff = flux_watts_upper - flux_watts_nominal
    flux_watts_lower_diff = flux_watts_nominal - flux_watts_lower

    print(f"Calculated nominal stellar energy received by exoplanet's atmosphere: {round(flux_watts_nominal, rounding_decimal_places)} W/m^2 (+{round(flux_watts_upper_diff, rounding_decimal_places)} W/m^2 -{round(flux_watts_lower_diff, rounding_decimal_places)} W/m^2)")
    return round(flux_watts_nominal, rounding_decimal_places), round(flux_watts_upper_diff, rounding_decimal_places), round(flux_watts_lower_diff, rounding_decimal_places)