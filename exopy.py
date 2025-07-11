from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
import time
from vars import *
from KermLib.KermLib import *
import numpy as np
import os
import math
from datetime import date
import pandas as pd

if sound_enabled is True:
    import winsound

def save_plot(target_star, file_suffix):
    """
    Streamlined way to save matplotlib plots to /saved_data
    """
    if file_saving_enabled is True:
        directory_name = 'saved_data/' + target_star
        file_name = directory_name + '/' + target_star + file_suffix
        os.makedirs(directory_name, exist_ok=True)
        plt.savefig(file_name)
        print(f'Saving {target_star}{file_suffix}...')
        time.sleep(0.8)
        return 'saved'
    else:
        return 'saving is disabled'
    
def play_sound(file_path, loop_enabled):
    if sound_enabled is True:
        if loop_enabled:
            winsound.PlaySound(file_path, winsound.SND_ASYNC | winsound.SND_LOOP | winsound.SND_FILENAME)
        else:
            winsound.PlaySound(file_path, winsound.SND_ASYNC | winsound.SND_FILENAME)
        return 'sound played'
    else:
        return 'sound effects are disabled'

def blackbody_temperature_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative):
    star_luminosity_watts_upper = (star_luminosity+star_luminosity_uncertainty_positive) * constant_solarluminosity_TO_W
    star_luminosity_watts_nominal = star_luminosity * constant_solarluminosity_TO_W
    star_luminosity_watts_lower = (star_luminosity-star_luminosity_uncertainty_negative) * constant_solarluminosity_TO_W

    exoplanet_orbital_radius_m_upper = (exoplanet_orbital_radius_AU + exoplanet_orbital_radius_AU_uncertainty_positive) * constant_AU_TO_m
    exoplanet_orbital_radius_m_nominal = exoplanet_orbital_radius_AU * constant_AU_TO_m
    exoplanet_orbital_radius_m_lower = (exoplanet_orbital_radius_AU-exoplanet_orbital_radius_AU_uncertainty_negative) * constant_AU_TO_m

    exoplanet_temperature_k_upper = ((star_luminosity_watts_upper)/(16*math.pi*((exoplanet_orbital_radius_m_lower)**2)*constant_stefan_boltzmann))**0.25
    exoplanet_temperature_k_nominal = ((star_luminosity_watts_nominal)/(16*math.pi*((exoplanet_orbital_radius_m_nominal)**2)*constant_stefan_boltzmann))**0.25
    exoplanet_temperature_k_lower = ((star_luminosity_watts_lower)/(16*math.pi*((exoplanet_orbital_radius_m_upper)**2)*constant_stefan_boltzmann))**0.25

    exoplanet_temperature_k_upper_diff = exoplanet_temperature_k_upper - exoplanet_temperature_k_nominal
    exoplanet_temperature_k_lower_diff = exoplanet_temperature_k_nominal - exoplanet_temperature_k_lower

    print(f'Calculated nominal exoplanet temperature (assuming blackbody): {round(exoplanet_temperature_k_nominal, rounding_decimal_places)} K (+{round(exoplanet_temperature_k_upper_diff, rounding_decimal_places)} K -{round(exoplanet_temperature_k_lower_diff, rounding_decimal_places)} K)')

    return round(exoplanet_temperature_k_nominal, rounding_decimal_places), round(exoplanet_temperature_k_upper_diff, rounding_decimal_places), round(exoplanet_temperature_k_lower_diff, rounding_decimal_places)

def exoplanet_flux_received(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative):
    star_luminosity_watts_upper = (star_luminosity+star_luminosity_uncertainty_positive) * constant_solarluminosity_TO_W
    star_luminosity_watts_nominal = star_luminosity * constant_solarluminosity_TO_W
    star_luminosity_watts_lower = (star_luminosity-star_luminosity_uncertainty_negative) * constant_solarluminosity_TO_W

    exoplanet_orbital_radius_meters_upper = (exoplanet_orbital_radius_AU+exoplanet_orbital_radius_AU_uncertainty_positive) * constant_AU_TO_m
    exoplanet_orbital_radius_meters_nominal = exoplanet_orbital_radius_AU * constant_AU_TO_m
    exoplanet_orbital_radius_meters_lower = (exoplanet_orbital_radius_AU-exoplanet_orbital_radius_AU_uncertainty_negative) * constant_AU_TO_m

    flux_watts_upper = star_luminosity_watts_upper / (4 * math.pi * exoplanet_orbital_radius_meters_lower ** 2)
    flux_watts_nominal = star_luminosity_watts_nominal / (4 * math.pi * exoplanet_orbital_radius_meters_nominal ** 2)
    flux_watts_lower = star_luminosity_watts_lower / (4 * math.pi * exoplanet_orbital_radius_meters_upper ** 2)

    flux_watts_upper_diff = flux_watts_upper - flux_watts_nominal
    flux_watts_lower_diff = flux_watts_nominal - flux_watts_lower

    print(f"Calculated nominal stellar energy received by exoplanet's atmosphere: {round(flux_watts_nominal, rounding_decimal_places)} W/m^2 (+{round(flux_watts_upper_diff, rounding_decimal_places)} W/m^2 -{round(flux_watts_lower_diff, rounding_decimal_places)} W/m^2)")
    print('\n' * 3)
    return round(flux_watts_nominal, rounding_decimal_places), round(flux_watts_upper_diff, rounding_decimal_places), round(flux_watts_lower_diff, rounding_decimal_places)

def habitable_zone_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative):

    inner_goldilocks_radius_lower = math.sqrt((star_luminosity-star_luminosity_uncertainty_negative)/1.1)
    inner_goldilocks_radius_nominal = math.sqrt(star_luminosity/1.1)

    outer_goldilocks_radius_nominal = math.sqrt(star_luminosity/0.53)
    outer_goldilocks_radius_upper = math.sqrt((star_luminosity+star_luminosity_uncertainty_positive)/0.53)

    inner_goldilocks_radius_lower_diff = inner_goldilocks_radius_nominal-inner_goldilocks_radius_lower
    outer_goldilocks_radius_upper_diff = outer_goldilocks_radius_upper-outer_goldilocks_radius_nominal

    print(f'Calculated nominal inner goldilocks zone radius: {round(inner_goldilocks_radius_nominal, rounding_decimal_places)} AU (-{round(inner_goldilocks_radius_lower_diff, rounding_decimal_places)} AU)')
    print(f'Calculated nominal outer goldilocks zone radius: {round(outer_goldilocks_radius_nominal, rounding_decimal_places)} AU (+{round(outer_goldilocks_radius_upper_diff, rounding_decimal_places)} AU)')
    print('\n' * 3)
    return round(inner_goldilocks_radius_nominal, rounding_decimal_places), round(inner_goldilocks_radius_lower_diff, rounding_decimal_places), round(outer_goldilocks_radius_nominal, rounding_decimal_places), round(outer_goldilocks_radius_upper_diff, rounding_decimal_places)

def stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity, star_radius_uncertainty_positive, star_radius_uncertainty_negative, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative):
    

    star_radius_meters_upper = (star_radius+star_radius_uncertainty_positive) * 6.957e8
    star_luminosity_watts_upper = (star_luminosity+star_luminosity_uncertainty_positive) * 3.828e26

    star_radius_meters_nominal = star_radius * 6.957e8
    star_luminosity_watts_nominal = star_luminosity * 3.828e26

    star_radius_meters_lower = (star_radius-star_radius_uncertainty_negative) * 6.957e8
    star_luminosity_watts_lower = (star_luminosity-star_luminosity_uncertainty_negative) * 3.828e26

    star_temperature_upper = ((star_luminosity_watts_upper)/(4*math.pi*constant_stefan_boltzmann*(star_radius_meters_lower)**2))**0.25
    star_temperature_nominal = ((star_luminosity_watts_nominal)/(4*math.pi*constant_stefan_boltzmann*(star_radius_meters_nominal)**2))**0.25
    star_temperature_lower = ((star_luminosity_watts_lower)/(4*math.pi*constant_stefan_boltzmann*(star_radius_meters_upper)**2))**0.25

    star_temperature_upper_diff = star_temperature_upper-star_temperature_nominal
    star_temperature_lower_diff = star_temperature_nominal-star_temperature_lower

    print(f'Calculated nominal star temperature: {round(star_temperature_nominal, rounding_decimal_places)} K (+{round(star_temperature_upper_diff, rounding_decimal_places)} K -{round(star_temperature_lower_diff, rounding_decimal_places)} K)')
    print('\n' * 3)
    return round(star_temperature_nominal, rounding_decimal_places), round(star_temperature_upper_diff, rounding_decimal_places), round(star_temperature_lower_diff, rounding_decimal_places)

def find_exoplanet_radius(star_radius, depth_of_phase_fold, star_radius_uncertainty_positive, star_radius_uncertainty_negative):
    """
    Estimates the radius of a transiting exoplanet using the radius of the transited star (given, solar radii)
    and the dip in the light emitted off the star (measured in flux.) The flux is found and automatically saved
    after retrieving light curve and creating phase fold.
    
    """


    planet_radius_solar_upperlimit_uncertainty = (star_radius + star_radius_uncertainty_positive) * math.sqrt(1-depth_of_phase_fold) # calculates highest possible value
    planet_radius_solar_lowerlimit_uncertainty = (star_radius - star_radius_uncertainty_negative) * math.sqrt(1-depth_of_phase_fold) # calculates lowest possible value
    planet_radius_solar = star_radius * math.sqrt(1-depth_of_phase_fold)
    planet_radius_solar_positive_uncertainty = planet_radius_solar_upperlimit_uncertainty - planet_radius_solar
    planet_radius_solar_negative_uncertainty = planet_radius_solar - planet_radius_solar_lowerlimit_uncertainty


    planet_radius_earth_nominal = planet_radius_solar * 109.1223801222 # converts solar radii to earth radii
    planet_radius_earth_upper_diff = planet_radius_solar_positive_uncertainty * 109.1223801222
    planet_radius_earth_lower_diff = planet_radius_solar_negative_uncertainty * 109.1223801222

    print(f'Calculated nominal planet radius: {round(planet_radius_earth_nominal, rounding_decimal_places)} R⊕ (+{round(planet_radius_earth_upper_diff, rounding_decimal_places)} R⊕ -{round(planet_radius_earth_lower_diff, rounding_decimal_places)} R⊕)')

    print('\n' * 3)
    return round(planet_radius_earth_nominal, rounding_decimal_places), round(planet_radius_earth_upper_diff, rounding_decimal_places), round(planet_radius_earth_lower_diff, rounding_decimal_places)

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

    print(f'Calculated nominal semi-major axis: {round(semi_major_axis_nominal_AU, rounding_decimal_places)} AU (+{round(semi_major_axis_upper_diff_AU, rounding_decimal_places)} AU -{round(semi_major_axis_lower_diff_AU, rounding_decimal_places)} AU)')
    print('\n' * 3)
    return round(semi_major_axis_nominal_AU, rounding_decimal_places), round(semi_major_axis_upper_diff_AU, rounding_decimal_places), round(semi_major_axis_lower_diff_AU, rounding_decimal_places)

def star_pixelfile_retrieval(target_star):
    """
    Retrieves and displays pixelfile of star.
    """
    print(f'Retrieving pixelfile of {target_star}...')
    start_time = time.time() # measure time 
    plot_title = f'Pixelfile of {target_star}'
    pixelfile = search_targetpixelfile(target_star).download()

    try:
        pixelfile.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star}, or system doesn't exist.")
        print('\n')
        return 'fail'
    
    end_time = time.time() # measure time
    print(f'took {round((end_time - start_time), 1)} seconds to retrieve')
    save_plot(target_star, f'_PIXELFILE.{file_saving_format}')
    plt.show()
    print('\n' * 3)
    return pixelfile

def star_lightcurve_analysis(target_star):
    """
    Retrieves multiple light curves of star. Automatically graphs and saves light curve, periodogram,
    binned lightcurve and saves values for radius calculations.
    """
    print(f'Retrieving ALL light curves of {target_star}...')
    start_time = time.time() # measure time
    plot_title = f'All light curves of {target_star}'
    search_result = search_lightcurve(target_star, author=selected_telescope, cadence=selected_cadence)
    lightcurve_collection = search_result.download_all()
    try:
        lightcurve_collection.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star}, or system doesn't exist.")
        print('\n')
        return 'fail'

    end_time = time.time() # measure time
    print(f'took {round((end_time - start_time), 1)} seconds to retrieve')
    save_plot(target_star, f'_LIGHTCURVECOLLECTION.{file_saving_format}')
    plt.show()
    print('\n' * 3)
    return lightcurve_collection


KermLib.ascii_run()
print(f'ExoPy V{version} initialized')
print('Created by Ayrik Nabirahni')
print('\n')

print('Flags:')
flag_index = 0
for x in range(len(user_flags)//2):
    print(user_flags[flag_index] + ' = ' + str(user_flags[flag_index+1]))
    flag_index += 2
if file_saving_enabled is True:
    print(f'File saving format: {file_saving_format}')
print(f'Telescope selected: {selected_telescope}')
print(f'Cadence selected: {selected_cadence}')
print(f'Bins: {selected_bins}')

#INITIALIZE VALUES FOR THE FIRST TIME HERE
lowest_flux = None
flux_watts_nominal = '(Not Generated)'
semi_major_axis_nominal_AU = '(Not Generated)'
star_temperature_nominal = '(Not Generated)'
inner_goldilocks_radius_nominal = outer_goldilocks_radius_nominal = '(Not Generated)'
star_luminosity = '(Not Generated)'
star_radius = '(Not Generated)'
star_mass_solarmass = '(Not Generated)'
planet_radius_earth_nominal = '(Not Generated)'
exoplanet_k_temperature_nominal = '(Not Generated)'
target_star = None
planet_period_float = None
planet_radius_earth_upper_diff = planet_radius_earth_lower_diff = '0.0'
flux_watts_upper_diff = flux_watts_lower_diff = '0.0'
semi_major_axis_upper_diff_AU = semi_major_axis_lower_diff_AU = '0.0'
star_temperature_upper_diff = star_temperature_lower_diff = '0.0'
inner_goldilocks_radius_lower_diff  = outer_goldilocks_radius_upper_diff = '0.0'
star_luminosity_uncertainty_positive = star_luminosity_uncertainty_negative = '0.0'
star_radius_uncertainty_positive = star_radius_uncertainty_negative = '0.0'
star_mass_solarmass_uncertainty_positive = star_mass_solarmass_uncertainty_negative = '0.0'
exoplanet_k_temperature_upper_diff = exoplanet_k_temperature_lower_diff = '0.0'
# INITIALIZE VALUES FOR THE FIRST TIME HERE

print('\n')

while True:
    play_sound('sfx/subwaysurfers.wav', False)
    function_index = 1
    print('Select desired function:')
    for function in list_of_tools:
        print(function_index, '--', function)
        list_of_functions_index.append(str(function_index))
        function_index += 1

    user_input = input()

    while True: # PREVENTS CRASHES FROM UNRECOGNIZED INPUTS
        if user_input not in list_of_functions_index:
            print(prompt_input_not_recognized)
            user_input = input()
        else:
            user_input = int(user_input)
            break
    print('\n')
    depth_of_phase_fold = None
    if user_input == 3: # parameters needed for planet radius calculator  
        print('Parameters') 
        print('Unit legend:')
        print('R☉ = Solar Radius')
        print('R⊕ = Earth Radius')
        print('\n')
        while True:
            star_radius = input("Transited star's radius (R☉): ")
            if star_radius is None or star_radius.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius = float(star_radius.strip())
                break

        while True:
            star_radius_uncertainty_positive = input("The 'greather than' uncertainty of transited star's radius (R☉): ")
            if star_radius_uncertainty_positive is None or star_radius_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius_uncertainty_positive = abs(float(star_radius_uncertainty_positive.strip()))
                break

        while True:
            star_radius_uncertainty_negative = input("The 'less than' uncertainty of transited star's radius (R☉): ")
            if star_radius_uncertainty_negative is None or star_radius_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius_uncertainty_negative = abs(float(star_radius_uncertainty_negative.strip()))
                break

        while True:
            if lowest_flux is None:
                depth_of_phase_fold = input('Minimum flux value during transit: ')
                if depth_of_phase_fold is None or depth_of_phase_fold.strip() == '':
                        print(prompt_input_not_recognized)
                else:
                    depth_of_phase_fold = float(depth_of_phase_fold.strip())
                    break
            else:
                use_last_value = input(f'Would you like to use the last stored lowest flux value ({lowest_flux})? (y/n): ')
                if use_last_value.lower().strip() == 'y':
                    depth_of_phase_fold = lowest_flux
                    break
                else:
                    depth_of_phase_fold = input('Minimum flux value during transit: ')
                    if depth_of_phase_fold is None or depth_of_phase_fold.strip() == '':
                        print(prompt_input_not_recognized)
                    else:
                        depth_of_phase_fold = float(depth_of_phase_fold.strip())
                        break

    elif user_input in [1, 2]:
        print('Parameters') 
        while True:
            target_star = input('Target star: ')
            if target_star is None or target_star.strip() == '':
                print(prompt_input_not_recognized)
            else:
                target_star = target_star.strip()
                break

    elif user_input == 4:
        print('Parameters') 
        print('Unit legend:')
        print('L☉ = Solar Luminosity')
        print('AU = Astronomical Units')
        print('\n')
        while True:
            star_luminosity = input("Star's luminosity (L☉): ")
            if star_luminosity is None or star_luminosity.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity = float(star_luminosity.strip())
                break
        while True:
            star_luminosity_uncertainty_positive = input("The 'greather than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_positive is None or star_luminosity_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_positive = abs(float(star_luminosity_uncertainty_positive.strip()))
                break

        while True:
            star_luminosity_uncertainty_negative = input("The 'less than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_negative is None or star_luminosity_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_negative = abs(float(star_luminosity_uncertainty_negative.strip()))
                break

    elif user_input == 5:
        print('Parameters') 
        print('Unit legend:')
        print('L☉ = Solar Luminosity')
        print('R☉ = Solar Radius')
        print('K = Kelvin')
        print('\n')
        while True:
            star_luminosity = input("Star's luminosity (L☉): ")
            if star_luminosity is None or star_luminosity.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity = float(star_luminosity.strip())
                break
        while True:
            star_luminosity_uncertainty_positive = input("The 'greather than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_positive is None or star_luminosity_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_positive = abs(float(star_luminosity_uncertainty_positive.strip()))
                break

        while True:
            star_luminosity_uncertainty_negative = input("The 'less than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_negative is None or star_luminosity_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_negative = abs(float(star_luminosity_uncertainty_negative.strip()))
                break
        while True:
            star_radius = input("Star's radius (R☉): ")
            if star_radius is None or star_radius.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius = float(star_radius.strip())
                break
        while True:
            star_radius_uncertainty_positive = input("The 'greather than' uncertainty of transited star's radius (R☉): ")
            if star_radius_uncertainty_positive is None or star_radius_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius_uncertainty_positive = abs(float(star_radius_uncertainty_positive.strip()))
                break

        while True:
            star_radius_uncertainty_negative = input("The 'less than' uncertainty of transited star's radius (R☉): ")
            if star_radius_uncertainty_negative is None or star_radius_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius_uncertainty_negative = abs(float(star_radius_uncertainty_negative.strip()))
                break

    elif user_input == 6:
        print('Parameters') 
        print('Unit legend:')
        print('d = Days')
        print('M☉ = Solar Masses')
        print('km = Kilometers')
        print('AU = Astronomical Units')
        while True:
            if planet_period_float is None:
                orbital_period_days = input("Enter planet's orbital period (d): ")
                if orbital_period_days is None or orbital_period_days.strip() == '':
                        print(prompt_input_not_recognized)
                else:
                    orbital_period_days = float(orbital_period_days.strip())
                    break
            else:
                use_last_value = input(f'Would you like to use the last stored orbital period ({planet_period_float} d)? (y/n): ')
                if use_last_value.lower().strip() == 'y':
                    orbital_period_days = planet_period_float
                    break
                else:
                    orbital_period_days = input('Minimum flux value during transit: ')
                    if orbital_period_days is None or orbital_period_days.strip() == '':
                        print(prompt_input_not_recognized)
                    else:
                        orbital_period_days = float(orbital_period_days.strip())
                        break
        
        while True:
            star_mass_solarmass = input("Enter star's mass (M☉): ")
            if star_mass_solarmass is None or star_mass_solarmass.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_mass_solarmass = float(star_mass_solarmass.strip())

                break
            
        while True:
            star_mass_solarmass_uncertainty_positive = input("The 'greather than' uncertainty of transited star's mass (M☉): ")
            if star_mass_solarmass_uncertainty_positive is None or star_mass_solarmass_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_mass_solarmass_uncertainty_positive = abs(float(star_mass_solarmass_uncertainty_positive.strip()))
                break

        while True:
            star_mass_solarmass_uncertainty_negative = input("The 'less than' uncertainty of transited star's mass (M☉): ")
            if star_mass_solarmass_uncertainty_negative is None or star_mass_solarmass_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_mass_solarmass_uncertainty_negative = abs(float(star_mass_solarmass_uncertainty_negative.strip()))
                break

    elif user_input == 7:
        print('Parameters') 
        print('Unit legend:')
        print('L☉ = Solar Luminosity')
        print('AU = Astronomical Units')
        print('W = Watts')
        print('m = Meters')
        print('\n')
        while True:
            star_luminosity = input("Star's luminosity (L☉): ")
            if star_luminosity is None or star_luminosity.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity = float(star_luminosity.strip())
                break
        while True:
            star_luminosity_uncertainty_positive = input("The 'greather than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_positive is None or star_luminosity_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_positive = abs(float(star_luminosity_uncertainty_positive.strip()))
                break

        while True:
            star_luminosity_uncertainty_negative = input("The 'less than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_negative is None or star_luminosity_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_negative = abs(float(star_luminosity_uncertainty_negative.strip()))
                break
        while True:
            exoplanet_orbital_radius_AU = input("Semi-major axis of exoplanet's orbit (AU): ")
            if exoplanet_orbital_radius_AU is None or exoplanet_orbital_radius_AU.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_AU = float(exoplanet_orbital_radius_AU.strip())
                break
        while True:
            exoplanet_orbital_radius_AU_uncertainty_positive = input("The 'greather than' uncertainty of the exoplanet's semi-major axis (AU): ")
            if exoplanet_orbital_radius_AU_uncertainty_positive is None or exoplanet_orbital_radius_AU_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_AU_uncertainty_positive = abs(float(exoplanet_orbital_radius_AU_uncertainty_positive.strip()))
                break

        while True:
            exoplanet_orbital_radius_AU_uncertainty_negative = input("The 'less than' uncertainty of the exoplanet's semi-major axis (AU): ")
            if exoplanet_orbital_radius_AU_uncertainty_negative is None or exoplanet_orbital_radius_AU_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_AU_uncertainty_negative = abs(float(exoplanet_orbital_radius_AU_uncertainty_negative.strip()))
                break

    elif user_input == 8:
        print('Parameters') 
        print('Unit legend:')
        print('L☉ = Solar Luminosity')
        print('AU = Astronomical Units')
        print('K = Kelvin')
        print('\n')
        while True:
            star_luminosity = input("Star's luminosity (L☉): ")
            if star_luminosity is None or star_luminosity.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity = float(star_luminosity.strip())
                break
        while True:
            star_luminosity_uncertainty_positive = input("The 'greather than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_positive is None or star_luminosity_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_positive = abs(float(star_luminosity_uncertainty_positive.strip()))
                break

        while True:
            star_luminosity_uncertainty_negative = input("The 'less than' uncertainty of transited star's luminosity (L☉): ")
            if star_luminosity_uncertainty_negative is None or star_luminosity_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_luminosity_uncertainty_negative = abs(float(star_luminosity_uncertainty_negative.strip()))
                break
        while True:
            exoplanet_orbital_radius_AU = input("Semi-major axis of exoplanet's orbit (AU): ")
            if exoplanet_orbital_radius_AU is None or exoplanet_orbital_radius_AU.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_AU = float(exoplanet_orbital_radius_AU.strip())
                break
        while True:
            exoplanet_orbital_radius_AU_uncertainty_positive = input("The 'greather than' uncertainty of the exoplanet's semi-major axis (AU): ")
            if exoplanet_orbital_radius_AU_uncertainty_positive is None or exoplanet_orbital_radius_AU_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_AU_uncertainty_positive = abs(float(exoplanet_orbital_radius_AU_uncertainty_positive.strip()))
                break

        while True:
            exoplanet_orbital_radius_AU_uncertainty_negative = input("The 'less than' uncertainty of the exoplanet's semi-major axis (AU): ")
            if exoplanet_orbital_radius_AU_uncertainty_negative is None or exoplanet_orbital_radius_AU_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_AU_uncertainty_negative = abs(float(exoplanet_orbital_radius_AU_uncertainty_negative.strip()))
                break


    play_sound('sfx/nflsong.wav', True)
    if target_star:
        target_star = target_star.upper()
    print('\n')
    match user_input:
        case 3:
            planet_radius_earth_nominal, planet_radius_earth_upper_diff, planet_radius_earth_lower_diff = find_exoplanet_radius(star_radius, depth_of_phase_fold, star_radius_uncertainty_positive, star_radius_uncertainty_negative)
        case 1:
            star_pixelfile_retrieval(target_star)
        case 2:
            lightcurve_collection = star_lightcurve_analysis(target_star)
            if lightcurve_collection == 'fail':
                continue
            print('Stitching light curve collection...')
            lightcurve_stitched = lightcurve_collection.stitch()
            plot_title = f'Stitched lightcurve of {target_star}'
            lightcurve_stitched = lightcurve_stitched.remove_outliers().normalize().flatten()
            lightcurve_stitched.plot(title=plot_title)
            
            
            save_plot(target_star, f'_LIGHTCURVECOLLECTIONSTITCHED.{file_saving_format}')
            plt.show()
            alphabet_index = 0
            
            print(prompt_periodogram_lower_bound)
            periodogram_lower_bound_input = input()
            if periodogram_lower_bound_input.strip() == "":
                lower_bound = periodogram_lower_bound_default
            else:
                try:
                    lower_bound = round(float(periodogram_lower_bound_input), 2)
                except ValueError:
                    lower_bound = periodogram_lower_bound_default
            print(prompt_periodogram_upper_bound)
            periodogram_upper_bound_input = input()
            if periodogram_upper_bound_input.strip() == "":
                upper_bound = periodogram_upper_bound_default
            else:
                try:
                    upper_bound = round(float(periodogram_upper_bound_input), 2)
                except ValueError:
                    upper_bound = periodogram_upper_bound_default

            play_sound("sfx/microwave_sound_effect.wav", True)
            time.sleep(3)
            print('Generating periodogram...')
            
            period = np.linspace(lower_bound, upper_bound, 100000) # Period
            periodogram_bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
            plot_title = f'Periodogram of light curve of {target_star}'
            periodogram_bls.plot(title=plot_title)

            play_sound("sfx/ovending.wav", False)

            time.sleep(2)
            save_plot(target_star, f'_LIGHTCURVEPERIODOGRAM_{alphabet_list[alphabet_index]}.{file_saving_format}')
            plt.show()
            # FIRST ONE ABOVE. REST IN LOOP
            time.sleep(1)

            while True:
                play_sound('sfx/subwaysurfers.wav', True)
                print('Folding light curve...')
                planet_period = periodogram_bls.period_at_max_power
                planet_t0 = periodogram_bls.transit_time_at_max_power
                planet_dur = periodogram_bls.duration_at_max_power
                ax = lightcurve_stitched.fold(period=planet_period, epoch_time=planet_t0).scatter()
                ax.set_xlim(-5, 5)
                ax.plot(title=f'Phasefold of Planet {alphabet_list[alphabet_index]}')

                save_plot(target_star, f'_PHASEFOLD_{alphabet_list[alphabet_index]}.{file_saving_format}')

                plt.show()
                
                folded_lc = lightcurve_stitched.fold(period=planet_period, epoch_time=planet_t0)
                flux = folded_lc.flux
                print('Binning...')
                binned_phase_fold = folded_lc.bin(bins=selected_bins)
                binned_phase_fold.plot()
                save_plot(target_star, f'_PHASEFOLDBINNED_{alphabet_list[alphabet_index]}.{file_saving_format}')

                min_idx = np.nanargmin(binned_phase_fold.flux)
                min_flux  = binned_phase_fold.flux[min_idx]

                planet_period_float = planet_period.value # convert to float
                print(f"Lowest flux = {min_flux:.6f}. Saved to memory.")
                print(f"Likely Period = {planet_period_float} days. Saved to memory.")
                lowest_flux = f"{min_flux:.6f}"
                lowest_flux = float(lowest_flux)
                plt.show()
                
                print('\n')
                print('Would you like to create another periodogram? (y/n)')
                while True:
                    exit_function = input()
                    if exit_function is None or exit_function.strip() == '' or exit_function.lower().strip() not in ['y', 'n']:
                        print(prompt_input_not_recognized)
                    else:
                        exit_function = exit_function.lower().strip()
                        break
                print('\n')
                if exit_function == 'n':
                    break


                alphabet_index += 1

                if masking_enabled is True: # mask signals if true
                    planet_mask = periodogram_bls.get_transit_mask(period=planet_period, transit_time=planet_t0, duration=planet_dur)
                    lightcurve_stitched = lightcurve_stitched[~planet_mask]
                    print('Masking enabled ' + '(' + alphabet_list[alphabet_index] + ')...')

                print(prompt_periodogram_lower_bound) # input lower bound
                periodogram_lower_bound_input = input()
                if periodogram_lower_bound_input.strip() == "":
                    lower_bound = periodogram_lower_bound_default
                else:
                    try:
                        lower_bound = round(float(periodogram_lower_bound_input), 2)
                    except ValueError:
                        lower_bound = periodogram_lower_bound_default

                print(prompt_periodogram_upper_bound) # input upper bound
                periodogram_upper_bound_input = input()
                if periodogram_upper_bound_input.strip() == "":
                    upper_bound = periodogram_upper_bound_default
                else:
                    try:
                        upper_bound = round(float(periodogram_upper_bound_input),2)
                    except ValueError:
                        upper_bound = periodogram_upper_bound_default

                play_sound("sfx/microwave_sound_effect.wav", True)
                time.sleep(3)
                print('Generating periodogram...')
                
                period = np.linspace(lower_bound, upper_bound, 100000) # Period
                periodogram_bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
                plot_title = 'Periodogram of light curve of ' + target_star
                periodogram_bls.plot(title=plot_title)
                play_sound("sfx/ovending.wav", False)
                time.sleep(2)
                save_plot(target_star, f'_LIGHTCURVEPERIODOGRAM_{alphabet_list[alphabet_index]}.{file_saving_format}')
                plt.show()           
        case 4:
            inner_goldilocks_radius_nominal, inner_goldilocks_radius_lower_diff, outer_goldilocks_radius_nominal, outer_goldilocks_radius_upper_diff = habitable_zone_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

        case 5:
            star_temperature_nominal, star_temperature_upper_diff, star_temperature_lower_diff = stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity, star_radius_uncertainty_positive, star_radius_uncertainty_negative, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

        case 6:
            semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU = kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative)
        
        case 7:
            flux_watts_nominal, flux_watts_upper_diff, flux_watts_lower_diff = exoplanet_flux_received(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative)

        case 8:
            exoplanet_k_temperature_nominal, exoplanet_k_temperature_upper_diff, exoplanet_k_temperature_lower_diff = blackbody_temperature_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, exoplanet_orbital_radius_AU, exoplanet_orbital_radius_AU_uncertainty_positive, exoplanet_orbital_radius_AU_uncertainty_negative)
        case 9:
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
                    in_habitable_zone = '(Data Not Available)'

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
                    exoplanet_size_suffix = '(Data Not Available)'



                data_exoplanet = {'Exoplanet Data': ['Radius:', 'Blackbody Temperature:', 'Semi-major axis of orbit:', 'Stellar Flux Received:', 'In Goldilocks Zone?', 'Planet Classification:'],'Value': [f'{planet_radius_earth_nominal} R⊕ (+{planet_radius_earth_upper_diff} R⊕ -{planet_radius_earth_lower_diff} R⊕)', f'{exoplanet_k_temperature_nominal} K (+{exoplanet_k_temperature_upper_diff} K -{exoplanet_k_temperature_lower_diff} K)', f'{semi_major_axis_nominal_AU} AU (+{semi_major_axis_upper_diff_AU} AU -{semi_major_axis_lower_diff_AU} AU)', f'{flux_watts_nominal} W/m^2 (+{flux_watts_upper_diff} W/m^2 -{flux_watts_lower_diff} W/m^2)', f'{in_habitable_zone}', f'{exoplanet_temperature_prefix}{exoplanet_size_suffix}']}
                table_exoplanet = pd.DataFrame(data_exoplanet) # HERE IS TABLE FOR STARS
                print(table_exoplanet)

                print('\n')

                has_not_generated_star = table_star.map(lambda x: "(Not Generated)" in str(x)).any().any() # CHECK IF ANY DATA NOT GENERATED
                has_not_generated_exoplanet = table_exoplanet.map(lambda x: "(Not Generated)" in str(x)).any().any() # CHECK IF ANY DATA NOT GENERATED

                if has_not_generated_star or has_not_generated_exoplanet:
                    while True:
                        user_decision = input('WARNING: Missing table data. Would you like to bulk calculate ALL values? (y/n) ')
                        if user_decision.lower().strip() in ['y', 'n']:
                            break
                        else:
                            print(prompt_input_not_recognized)

                    if user_decision == 'y': # TAKE ALL VALUES AND CALCULATE AT ONCE
                        print('Unit legend:')
                        print('R☉ = Solar Radius')
                        print('R⊕ = Earth Radius')
                        print('L☉ = Solar Luminosity')
                        print('M☉ = Solar Masses')
                        print('AU = Astronomical Units')
                        print('K = Kelvin')
                        print('d = Days')
                        print('W = Watts')
                        print('km = Kilometers')
                        print('m = Meters')
                        while True:
                            star_radius = input("Transited star's radius (R☉): ")
                            if star_radius is None or star_radius.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_radius = float(star_radius.strip())
                                break

                        while True:
                            star_radius_uncertainty_positive = input("The 'greather than' uncertainty of transited star's radius (R☉): ")
                            if star_radius_uncertainty_positive is None or star_radius_uncertainty_positive.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_radius_uncertainty_positive = abs(float(star_radius_uncertainty_positive.strip()))
                                break

                        while True:
                            star_radius_uncertainty_negative = input("The 'less than' uncertainty of transited star's radius (R☉): ")
                            if star_radius_uncertainty_negative is None or star_radius_uncertainty_negative.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_radius_uncertainty_negative = abs(float(star_radius_uncertainty_negative.strip()))
                                break

                        while True:
                            if lowest_flux is None:
                                depth_of_phase_fold = input('Minimum flux value during transit: ')
                                if depth_of_phase_fold is None or depth_of_phase_fold.strip() == '':
                                        print(prompt_input_not_recognized)
                                else:
                                    depth_of_phase_fold = float(depth_of_phase_fold.strip())
                                    break
                            else:
                                use_last_value = input(f'Would you like to use the last stored lowest flux value ({lowest_flux})? (y/n): ')
                                if use_last_value.lower().strip() == 'y':
                                    depth_of_phase_fold = lowest_flux
                                    break
                                else:
                                    depth_of_phase_fold = input('Minimum flux value during transit: ')
                                    if depth_of_phase_fold is None or depth_of_phase_fold.strip() == '':
                                        print(prompt_input_not_recognized)
                                    else:
                                        depth_of_phase_fold = float(depth_of_phase_fold.strip())
                                        break
                        
                        while True:
                            star_luminosity = input("Star's luminosity (L☉): ")
                            if star_luminosity is None or star_luminosity.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_luminosity = float(star_luminosity.strip())
                                break
                        while True:
                            star_luminosity_uncertainty_positive = input("The 'greather than' uncertainty of transited star's luminosity (L☉): ")
                            if star_luminosity_uncertainty_positive is None or star_luminosity_uncertainty_positive.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_luminosity_uncertainty_positive = abs(float(star_luminosity_uncertainty_positive.strip()))
                                break

                        while True:
                            star_luminosity_uncertainty_negative = input("The 'less than' uncertainty of transited star's luminosity (L☉): ")
                            if star_luminosity_uncertainty_negative is None or star_luminosity_uncertainty_negative.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_luminosity_uncertainty_negative = abs(float(star_luminosity_uncertainty_negative.strip()))
                                break

                        while True:
                            if planet_period_float is None:
                                orbital_period_days = input("Enter planet's orbital period (d): ")
                                if orbital_period_days is None or orbital_period_days.strip() == '':
                                        print(prompt_input_not_recognized)
                                else:
                                    orbital_period_days = float(orbital_period_days.strip())
                                    break
                            else:
                                use_last_value = input(f'Would you like to use the last stored orbital period ({planet_period_float} d)? (y/n): ')
                                if use_last_value.lower().strip() == 'y':
                                    orbital_period_days = planet_period_float
                                    break
                                else:
                                    orbital_period_days = input('Minimum flux value during transit: ')
                                    if orbital_period_days is None or orbital_period_days.strip() == '':
                                        print(prompt_input_not_recognized)
                                    else:
                                        orbital_period_days = float(orbital_period_days.strip())
                                        break
                        
                        while True:
                            star_mass_solarmass = input("Enter star's mass (M☉): ")
                            if star_mass_solarmass is None or star_mass_solarmass.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_mass_solarmass = float(star_mass_solarmass.strip())

                                break
                            
                        while True:
                            star_mass_solarmass_uncertainty_positive = input("The 'greather than' uncertainty of transited star's mass (M☉): ")
                            if star_mass_solarmass_uncertainty_positive is None or star_mass_solarmass_uncertainty_positive.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_mass_solarmass_uncertainty_positive = abs(float(star_mass_solarmass_uncertainty_positive.strip()))
                                break

                        while True:
                            star_mass_solarmass_uncertainty_negative = input("The 'less than' uncertainty of transited star's mass (M☉): ")
                            if star_mass_solarmass_uncertainty_negative is None or star_mass_solarmass_uncertainty_negative.strip() == '':
                                print(prompt_input_not_recognized)
                            else:
                                star_mass_solarmass_uncertainty_negative = abs(float(star_mass_solarmass_uncertainty_negative.strip()))
                                break
                        
                        print('\n' * 3)

                        semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU = kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative)

                        planet_radius_earth_nominal, planet_radius_earth_upper_diff, planet_radius_earth_lower_diff = find_exoplanet_radius(star_radius, depth_of_phase_fold, star_radius_uncertainty_positive, star_radius_uncertainty_negative)

                        inner_goldilocks_radius_nominal, inner_goldilocks_radius_lower_diff, outer_goldilocks_radius_nominal, outer_goldilocks_radius_upper_diff = habitable_zone_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

                        star_temperature_nominal, star_temperature_upper_diff, star_temperature_lower_diff = stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity, star_radius_uncertainty_positive, star_radius_uncertainty_negative, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

                        flux_watts_nominal, flux_watts_upper_diff, flux_watts_lower_diff = exoplanet_flux_received(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU)

                        exoplanet_k_temperature_nominal, exoplanet_k_temperature_upper_diff, exoplanet_k_temperature_lower_diff = blackbody_temperature_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU)

                        continue

                while True:
                    user_decision = input('Would you like to proceed in exporting current report (y/n)? ')
                    if user_decision.lower().strip() in ['y', 'n']:
                        break
                    else:
                        print(prompt_input_not_recognized)
                
                if user_decision == 'y':
                    while True:
                        target_star = input('Enter system/star name: ')
                        target_star = target_star.strip().upper()
                        if target_star == '' or target_star is None:
                            print(prompt_input_not_recognized)
                        else:
                            break
                    file_path = f'saved_data/{target_star}/{current_date}'
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    table_exoplanet.to_csv(f'{file_path}-EXOPLANET_REPORT.csv', sep ='\t')
                    table_star.to_csv(f'{file_path}-STAR_REPORT.csv', sep ='\t')
                    print(f'Dataframe sucessfully exported to {file_path}-EXOPLANET_REPORT as csv')
                    print(f'Dataframe sucessfully exported to {file_path}-STAR_REPORT as csv')
                    print('\n' * 3)
                    break
                else:
                    print('\n' * 3)
                    break