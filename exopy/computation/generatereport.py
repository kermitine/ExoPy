import pandas as pd
from config.config import *
from datetime import date
import os
from exopy.getdata.getexoplanetdata import *
from exopy.getdata.getstardata import *

initialize_vars = False
def generate_full_report(lowest_flux, planet_period_float, target_star):
    global initialize_vars
    if initialize_vars is False:
        flux_watts_nominal = '(Not Generated)'
        semi_major_axis_nominal_AU = '(Not Generated)'
        star_temperature_nominal = '(Not Generated)'
        inner_goldilocks_radius_nominal = outer_goldilocks_radius_nominal = '(Not Generated)'
        star_luminosity = '(Data Not Available)'
        star_radius = '(Data Not Available)'
        star_mass_solarmass = '(Data Not Available)'
        planet_radius_earth_nominal = '(Not Generated)'
        exoplanet_k_temperature_nominal = '(Not Generated)'
        orbital_period_days = 0
        planet_radius_earth_upper_diff = planet_radius_earth_lower_diff = '0.0'
        flux_watts_upper_diff = flux_watts_lower_diff = '0.0'
        semi_major_axis_upper_diff_AU = semi_major_axis_lower_diff_AU = '0.0'
        star_temperature_upper_diff = star_temperature_lower_diff = '0.0'
        inner_goldilocks_radius_lower_diff  = outer_goldilocks_radius_upper_diff = '0.0'
        star_luminosity_uncertainty_positive = star_luminosity_uncertainty_negative = '0.0'
        star_radius_uncertainty_positive = star_radius_uncertainty_negative = '0.0'
        star_mass_solarmass_uncertainty_positive = star_mass_solarmass_uncertainty_negative = '0.0'
        exoplanet_k_temperature_upper_diff = exoplanet_k_temperature_lower_diff = '0.0'
        initialize_vars = True

    while True:
        print('Current Report Status')
        current_date = str(date.today())
        print(f'Date: {current_date}')
        data_star = {'Star Data': ['Radius:', 'Temperature:', 'Goldilocks Zone Inner Radius:', 'Goldilocks Zone Outer Radius:', 'Luminosity:', 'Mass:'],'Value': [f'{star_radius} R☉ (+{star_radius_uncertainty_positive} R☉ -{star_radius_uncertainty_negative} R☉)', f'{star_temperature_nominal} K (+{star_temperature_upper_diff} K -{star_temperature_lower_diff} K)', f'{inner_goldilocks_radius_nominal} AU (-{inner_goldilocks_radius_lower_diff} AU)', f'{outer_goldilocks_radius_nominal} AU (+{outer_goldilocks_radius_upper_diff} AU)', f'{star_luminosity} L☉ (+{star_luminosity_uncertainty_positive} L☉ -{star_luminosity_uncertainty_negative} L☉)', f'{star_mass_solarmass} M☉ (+{star_mass_solarmass_uncertainty_positive} M☉ -{star_mass_solarmass_uncertainty_negative} M☉)']}
        table_star = pd.DataFrame(data_star) # HERE IS TABLE FOR STARS
        print(table_star)
        print('\n')

        if semi_major_axis_nominal_AU != '(Not Generated)' and inner_goldilocks_radius_nominal != '(Not Generated)':
            if outer_goldilocks_radius_nominal > semi_major_axis_nominal_AU > inner_goldilocks_radius_nominal:
                in_habitable_zone = 'Yes (Nominal)'
            elif (outer_goldilocks_radius_nominal+outer_goldilocks_radius_upper_diff) > (semi_major_axis_nominal_AU+semi_major_axis_upper_diff_AU) > (inner_goldilocks_radius_nominal-inner_goldilocks_radius_lower_diff) or (outer_goldilocks_radius_nominal+outer_goldilocks_radius_upper_diff) > (semi_major_axis_nominal_AU-semi_major_axis_lower_diff_AU) > (inner_goldilocks_radius_nominal-inner_goldilocks_radius_lower_diff) or (outer_goldilocks_radius_nominal+outer_goldilocks_radius_upper_diff) > semi_major_axis_nominal_AU > (inner_goldilocks_radius_nominal-inner_goldilocks_radius_lower_diff):
                in_habitable_zone = 'Possible'
            else:
                in_habitable_zone = 'No'
        else:
            in_habitable_zone = '(Not Generated)'

        if planet_radius_earth_nominal != '(Not Generated)' and exoplanet_k_temperature_nominal != '(Not Generated)':
            if exoplanet_k_temperature_nominal >= 1000:
                exoplanet_temperature_prefix = 'Hot '
            elif 1000 > exoplanet_k_temperature_nominal > 300:
                exoplanet_temperature_prefix = 'Warm '
            else:
                exoplanet_temperature_prefix = 'Cold '

            if planet_radius_earth_nominal >= 7:
                exoplanet_size_suffix = 'Jupiter-like'
            elif 7 > planet_radius_earth_nominal >= 3.8:
                exoplanet_size_suffix = 'Neptune-like'
            elif 3.8 > planet_radius_earth_nominal >= 2.2:
                exoplanet_size_suffix = 'Mini-Neptune'
            elif 2.2 > planet_radius_earth_nominal >= 1.5:
                exoplanet_size_suffix = 'Super-Earth'
            else:
                exoplanet_size_suffix = 'Earth-Like'
        else:
            exoplanet_temperature_prefix = ''
            exoplanet_size_suffix = '(Not Generated)'



        data_exoplanet = {'Exoplanet Data': ['Radius:', 'Orbital Period:', 'Blackbody Temperature:', 'Semi-major axis of orbit:', 'Stellar Flux Received:', 'In Goldilocks Zone?', 'Planet Classification:'],'Value': [f'{planet_radius_earth_nominal} R⊕ (+{planet_radius_earth_upper_diff} R⊕ -{planet_radius_earth_lower_diff} R⊕)', f'{round(orbital_period_days, rounding_decimal_places)} d',f'{exoplanet_k_temperature_nominal} K (+{exoplanet_k_temperature_upper_diff} K -{exoplanet_k_temperature_lower_diff} K)', f'{semi_major_axis_nominal_AU} AU (+{semi_major_axis_upper_diff_AU} AU -{semi_major_axis_lower_diff_AU} AU)', f'{flux_watts_nominal} W/m^2 (+{flux_watts_upper_diff} W/m^2 -{flux_watts_lower_diff} W/m^2)', f'{in_habitable_zone}', f'{exoplanet_temperature_prefix}{exoplanet_size_suffix}']}
        table_exoplanet = pd.DataFrame(data_exoplanet) # HERE IS TABLE FOR EXOPLANET
        print(table_exoplanet)

        print('\n')

        has_not_generated_star = table_star.map(lambda x: "(Not Generated)" in str(x)).any().any() # CHECK IF ANY DATA NOT GENERATED
        has_not_generated_exoplanet = table_exoplanet.map(lambda x: "(Not Generated)" in str(x)).any().any() # CHECK IF ANY DATA NOT GENERATED

        if has_not_generated_star or has_not_generated_exoplanet:
            while True:
                user_decision = input('WARNING: Missing table data. Would you like to bulk calculate ALL values? (y/n): ')
                if user_decision.lower().strip() in ['y', 'n']:
                    break
                else:
                    print(prompt_input_not_recognized)

            if user_decision == 'y': # TAKE ALL VALUES AND CALCULATE AT ONCE
                star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative = get_star_radius()
                star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative = get_star_luminosity()
                star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative = get_star_mass()
                depth_of_phase_fold = get_star_lowest_flux(lowest_flux)
                orbital_period_days = get_exoplanet_orbital_period(planet_period_float)
                from exopy.computation.orbitalSMA import kepler_orbital_radius_calculator
                from exopy.computation.exoplanetradius import find_exoplanet_radius
                from exopy.computation.starhabitablezone import habitable_zone_calculator
                from exopy.computation.startemperature import stefan_boltzmann_star_temperature_calculator
                from exopy.computation.exoplanetstellarenergy import exoplanet_flux_received
                from exopy.computation.exoplanettemperature import blackbody_temperature_calculator

                print('\n' * 2)

                semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU = kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative)

                planet_radius_earth_nominal, planet_radius_earth_upper_diff, planet_radius_earth_lower_diff = find_exoplanet_radius(star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative, depth_of_phase_fold)

                inner_goldilocks_radius_nominal, inner_goldilocks_radius_lower_diff, outer_goldilocks_radius_nominal, outer_goldilocks_radius_upper_diff = habitable_zone_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

                star_temperature_nominal, star_temperature_upper_diff, star_temperature_lower_diff = stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity, star_radius_uncertainty_positive, star_radius_uncertainty_negative, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

                flux_watts_nominal, flux_watts_upper_diff, flux_watts_lower_diff = exoplanet_flux_received(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU)

                exoplanet_k_temperature_nominal, exoplanet_k_temperature_upper_diff, exoplanet_k_temperature_lower_diff = blackbody_temperature_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU)

                print('\n' * 2)

                continue

        while True:
            user_decision = input('Would you like to proceed in exporting current report? (y/n): ')
            if user_decision.lower().strip() in ['y', 'n']:
                break
            else:
                print(prompt_input_not_recognized)
        
        if user_decision == 'y':
            while True:
                target_star = input(f'Enter system/star name (Last used: {target_star}): ')
                target_star = target_star.strip().upper()
                if target_star == '' or target_star is None:
                    print(prompt_input_not_recognized)
                else:
                    break
            file_path = f'saved/saved_data/{target_star}/{current_date}'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            table_exoplanet.to_csv(f'{file_path}-EXOPLANET_REPORT.csv', sep ='\t')
            table_star.to_csv(f'{file_path}-STAR_REPORT.csv', sep ='\t')
            print(f'Dataframe sucessfully exported to {file_path}-EXOPLANET_REPORT as csv')
            print(f'Dataframe sucessfully exported to {file_path}-STAR_REPORT as csv')
            print('\n' * 2)
            break
        else:
            print('\n' * 2)
            break