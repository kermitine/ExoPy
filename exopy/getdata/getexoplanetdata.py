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
def get_exoplanet_semimajoraxis():
    while True:
        exoplanet_orbital_radius_AU = input("Semi-major axis of exoplanet's orbit (AU): ")
        if exoplanet_orbital_radius_AU is None or exoplanet_orbital_radius_AU.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                exoplanet_orbital_radius_AU = float(exoplanet_orbital_radius_AU.strip())
                break
            except ValueError:
                print(prompt_input_not_recognized)

    while True:
        exoplanet_orbital_radius_AU_uncertainty_positive = input("The 'greather than' uncertainty of the exoplanet's semi-major axis (AU): ")
        if exoplanet_orbital_radius_AU_uncertainty_positive is None or exoplanet_orbital_radius_AU_uncertainty_positive.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                exoplanet_orbital_radius_AU_uncertainty_positive = abs(float(exoplanet_orbital_radius_AU_uncertainty_positive.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)

    while True:
        exoplanet_orbital_radius_AU_uncertainty_negative = input("The 'less than' uncertainty of the exoplanet's semi-major axis (AU): ")
        if exoplanet_orbital_radius_AU_uncertainty_negative is None or exoplanet_orbital_radius_AU_uncertainty_negative.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                exoplanet_orbital_radius_AU_uncertainty_negative = abs(float(exoplanet_orbital_radius_AU_uncertainty_negative.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)
    return exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative

def get_exoplanet_orbital_period(planet_period_float):
    while True:
        if planet_period_float is None:
            orbital_period_days = input("Enter planet's orbital period (d): ")
            if orbital_period_days is None or orbital_period_days.strip() == '':
                    print(prompt_input_not_recognized)
            else:
                try:
                    orbital_period_days = float(orbital_period_days.strip())
                    return orbital_period_days
                except ValueError:
                    print(prompt_input_not_recognized)
                    continue
        else:
            use_last_value = input(f'Would you like to use the last stored orbital period ({planet_period_float} d)? (y/n): ')
            if use_last_value.lower().strip() == 'y':
                orbital_period_days = planet_period_float
                return orbital_period_days
            else:
                orbital_period_days = input('Minimum flux value during transit: ')
                if orbital_period_days is None or orbital_period_days.strip() == '':
                    print(prompt_input_not_recognized)
                else:
                    try:
                        orbital_period_days = float(orbital_period_days.strip())
                        return orbital_period_days
                    except ValueError:
                        print(prompt_input_not_recognized)
                        continue