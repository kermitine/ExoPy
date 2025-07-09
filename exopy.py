from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
import time
from vars import *
from KermLib.KermLib import *
import numpy as np
import os
import math

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

def exoplanet_flux_received(star_luminosity, exoplanet_orbital_radius_astronomicalunits):
    star_luminosity_watts = star_luminosity * 3.827e+26
    exoplanet_orbital_radius_meters = exoplanet_orbital_radius_astronomicalunits * 1.496e+11
    flux_watts = star_luminosity_watts / (4 * math.pi * exoplanet_orbital_radius_meters ** 2)
    print(f'Calculated nominal flux received by exoplanet: {round(flux_watts, rounding_decimal_places)} W/(m^2)')
    print('\n' * 3)
    return flux_watts

def habitable_zone_calculator(star_luminosity):
    inner_nominal_goldilocks_radius = math.sqrt(star_luminosity/1.1)
    outer_nominal_goldilocks_radius = math.sqrt(star_luminosity/0.53)
    print(f'Inner nominal goldilocks radius: {round(inner_nominal_goldilocks_radius, rounding_decimal_places)} AU')
    print(f'Outer nominal goldilocks radius: {round(outer_nominal_goldilocks_radius, rounding_decimal_places)} AU')
    print('\n' * 3)
    return inner_nominal_goldilocks_radius, outer_nominal_goldilocks_radius

def stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity):
    star_radius_meters = star_radius * 6.957e8
    star_luminosity_watts = star_luminosity * 3.828e26
    star_temperature = ((star_luminosity_watts)/(4*math.pi*stefan_boltzmann_constant*(star_radius_meters)**2))**0.25
    print(f'Calculated nominal star temperature: {star_temperature} K')
    print('\n' * 3)
    return star_temperature

def find_exoplanet_radius(star_radius, depth_of_phase_fold, star_radius_uncertainty_positive, star_radius_uncertainty_negative):
    """
    Estimates the radius of a transiting exoplanet using the radius of the transited star (given, solar radii)
    and the dip in the light emitted off the star (measured in flux.) The flux is found and automatically saved
    after retrieving light curve and creating phase fold.
    
    """
    significant_figure_list = [] # iniitalizes significant figure list, which tracks sf of each calculated


    planet_radius_solar_upperlimit_uncertainty = (star_radius + star_radius_uncertainty_positive) * math.sqrt(1-depth_of_phase_fold) # calculates highest possible value
    planet_radius_solar_lowerlimit_uncertainty = (star_radius - star_radius_uncertainty_negative) * math.sqrt(1-depth_of_phase_fold) # calculates lowest possible value
    planet_radius_solar = star_radius * math.sqrt(1-depth_of_phase_fold)
    planet_radius_solar_positive_uncertainty = planet_radius_solar_upperlimit_uncertainty - planet_radius_solar
    planet_radius_solar_negative_uncertainty = planet_radius_solar - planet_radius_solar_lowerlimit_uncertainty


    planet_radius_earth = planet_radius_solar * 109.1223801222 # converts solar radii to earth radii
    planet_radius_earth_positive_uncertainty = planet_radius_solar_positive_uncertainty * 109.1223801222
    planet_radius_earth_negative_uncertainty = planet_radius_solar_negative_uncertainty * 109.1223801222

    print(f'Calculated nominal planet radius: {round(planet_radius_earth, rounding_decimal_places)} R⊕ ({round(planet_radius_earth*6378, rounding_decimal_places)} km) (Uncertainty: +{round(planet_radius_earth_positive_uncertainty, rounding_decimal_places)} -{round(planet_radius_earth_negative_uncertainty, rounding_decimal_places)})')
    print(f'Highest uncertainty: {round(planet_radius_earth + planet_radius_earth_positive_uncertainty, rounding_decimal_places)} R⊕ ({round((planet_radius_earth + planet_radius_earth_positive_uncertainty)*6378, rounding_decimal_places)} km)')
    print(f'Lowest uncertainty: {round(planet_radius_earth - planet_radius_earth_negative_uncertainty, rounding_decimal_places)} R⊕ ({round((planet_radius_earth - planet_radius_earth_negative_uncertainty)*6378, rounding_decimal_places)} km)')

    if 0.5 >= planet_radius_earth:
        print('Predicted planet type: Sub-Earth')
    elif 1.1 >= planet_radius_earth > 0.5:
        print('Predicted planet type: Earth-Like')
    elif 1.75 >= planet_radius_earth > 1.1:
        print('Predicted planet type: Super-Earth')
    elif 3.5 >= planet_radius_earth > 1.75:
        print('Predicted planet type: Sub-Neptune')
    elif 6.1 >= planet_radius_earth > 3.5:
        print('Predicted planet type: Sub-Jupiter')
    elif 14.3 >= planet_radius_earth > 6.1:
        print('Predicted planet type: Jupiter-like')
    elif planet_radius_earth > 14.3:
        print('Predicted planet type: Super-Jupiter')

    print('\n' * 3)
    return planet_radius_earth

def kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass):
    orbital_period_seconds = orbital_period_days * 86400 # convert from days to seconds
    star_mass_kg = star_mass_solarmass * 1.989e+30
    semi_major_axis = ((gravitational_constant*star_mass_kg*(orbital_period_seconds**2))/(4*(math.pi**2)))**(1/3)
    print(f'Calculated nominal semi-major axis: {round(semi_major_axis/1000, rounding_decimal_places)} km')
    print(f'Alternative units: {round(semi_major_axis/1.496e+11, rounding_decimal_places)} AU, {round(semi_major_axis, rounding_decimal_places)} m')
    print('\n' * 3)
    return semi_major_axis

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

def star_lightcurve_retrieval(target_star):
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
lowest_flux = None

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
    print('Parameters')
    target_star = None
    star_radius = None
    depth_of_phase_fold = None
    if user_input == 1: # parameters needed for planet radius calculator   
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

    elif user_input in [2, 3]:
        while True:
            target_star = input('Target star: ')
            if target_star is None or target_star.strip() == '':
                print(prompt_input_not_recognized)
            else:
                target_star = target_star.strip()
                break

    elif user_input == 4:
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

    elif user_input == 5:
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
            star_radius = input("Star's radius (R☉): ")
            if star_radius is None or star_radius.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius = float(star_radius.strip())
                break

    elif user_input == 6:
        print('Unit legend:')
        print('d = Days')
        print('M☉ = Solar Masses')
        print('km = Kilometers')
        print('AU = Astronomical Units')
        while True:
            orbital_period_days = input("Enter planet's orbital period (d): ")
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

    elif user_input == 7:
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
            exoplanet_orbital_radius_astronomicalunits = input("Semi-major axis of exoplanet's orbit (AU): ")
            if exoplanet_orbital_radius_astronomicalunits is None or exoplanet_orbital_radius_astronomicalunits.strip() == '':
                print(prompt_input_not_recognized)
            else:
                exoplanet_orbital_radius_astronomicalunits = float(exoplanet_orbital_radius_astronomicalunits.strip())
                break

    play_sound('sfx/nflsong.wav', True)
    if target_star:
        target_star = target_star.upper()
    print('\n')
    match user_input:
        case 1:
            calculated_planet_radius = find_exoplanet_radius(star_radius, depth_of_phase_fold, star_radius_uncertainty_positive, star_radius_uncertainty_negative)
        case 2:
            pixelfile = star_pixelfile_retrieval(target_star)
        case 3:
            lightcurve_collection = star_lightcurve_retrieval(target_star)
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
                print(f"Lowest flux = {min_flux:.6f}. Saved to memory.")

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
            habitable_zone_calculator(star_luminosity)

        case 5:
            stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity)

        case 6:
            kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass)
        
        case 7:
            exoplanet_flux_received(star_luminosity, exoplanet_orbital_radius_astronomicalunits)

        
                