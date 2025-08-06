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


from config.constants import *
from config.config import *
import math
def kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative):
    orbital_period_seconds = orbital_period_days * constant_d_TO_s 

    star_mass_kg_upper = (star_mass_solarmass + star_mass_solarmass_uncertainty_positive) * constant_solarmass_TO_kg 
    star_mass_kg_nominal = star_mass_solarmass * constant_solarmass_TO_kg 
    star_mass_kg_lower = (star_mass_solarmass - star_mass_solarmass_uncertainty_negative) * constant_solarmass_TO_kg 
    
    semi_major_axis_upper = ((constant_gravitational*star_mass_kg_upper*(orbital_period_seconds**2))/(4*(math.pi**2)))**(1/3)
    semi_major_axis_nominal = ((constant_gravitational*star_mass_kg_nominal*(orbital_period_seconds**2))/(4*(math.pi**2)))**(1/3)
    semi_major_axis_lower = ((constant_gravitational*star_mass_kg_lower*(orbital_period_seconds**2))/(4*(math.pi**2)))**(1/3)

    semi_major_axis_nominal_AU = semi_major_axis_nominal * constant_m_TO_AU
    semi_major_axis_upper_diff_AU = (semi_major_axis_upper-semi_major_axis_nominal)*constant_m_TO_AU
    semi_major_axis_lower_diff_AU = (semi_major_axis_nominal-semi_major_axis_lower)*constant_m_TO_AU

    try:
        print(f'Calculated nominal semi-major axis: {round(semi_major_axis_nominal_AU, rounding_decimal_places)} AU (+{round(semi_major_axis_upper_diff_AU, rounding_decimal_places)} AU -{round(semi_major_axis_lower_diff_AU, rounding_decimal_places)} AU)')
        return round(semi_major_axis_nominal_AU, rounding_decimal_places), round(semi_major_axis_upper_diff_AU, rounding_decimal_places), round(semi_major_axis_lower_diff_AU, rounding_decimal_places)
    except TypeError:
        print('ERROR: Complex number. Are you sure you entered the correct data?')
        return '(Not Generated)', 0, 0