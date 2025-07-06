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

def round_sig_fig(x, sig):
    """
    Round x to sig significant figures. (COPIED FROM CHATGPT)
    """
    if x == 0:
        return 0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def find_significant_figures(float, integer):
    """
    calculate the sig figs of a number.
    """
    significant_figures = 0
    leading_zero = True
    if round(float) == 0: # disregard sig figs if 0
        return 100
    if float: # convert to string
        string_float = str(float)
    if integer:
        string_integer = str(integer)

    if float:
        for char in string_float:
            if char == '0' and leading_zero is True: # dont count leading zeros toward sig figs
                continue
            elif char == '.': # dont count decimal place as sig figs
                continue
            if char != '0' and char != '.' and leading_zero is True: 
                leading_zero = False
                significant_figures += 1
            else:
                significant_figures += 1
    return significant_figures

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

    # SIGNIFICANT FIGURE ROUNDING HERE
    significant_figure_list.append(find_significant_figures(star_radius, None))
    significant_figure_list.append(find_significant_figures(depth_of_phase_fold, None))
    significant_figure_list.append(find_significant_figures(star_radius_uncertainty_negative, None))
    significant_figure_list.append(find_significant_figures(star_radius_uncertainty_positive, None))
    lowest_sig_fig = min(significant_figure_list)

    if significant_figure_rounding is True:
        print(f'Calculated nominal planet radius: {round_sig_fig(planet_radius_earth, lowest_sig_fig)} earth radii (Uncertainty: +{round_sig_fig(planet_radius_earth_positive_uncertainty, lowest_sig_fig)} -{round_sig_fig(planet_radius_earth_negative_uncertainty, lowest_sig_fig)}) (Rounded to {lowest_sig_fig} sig figs)')
        print(f'Highest uncertainty: {round_sig_fig(planet_radius_earth + planet_radius_earth_positive_uncertainty, lowest_sig_fig)} earth radii')
        print(f'Lowest uncertainty: {round_sig_fig(planet_radius_earth - planet_radius_earth_negative_uncertainty, lowest_sig_fig)} earth radii')
    else:
        print(f'Calculated nominal planet radius: {round(planet_radius_earth, rounding_decimal_places)} earth radii (Uncertainty: +{round(planet_radius_earth_positive_uncertainty, rounding_decimal_places)} -{round(planet_radius_earth_negative_uncertainty, rounding_decimal_places)}) (Rounded to {rounding_decimal_places} decimal places)')
        print(f'Highest uncertainty: {round(planet_radius_earth + planet_radius_earth_positive_uncertainty, rounding_decimal_places)} earth radii')
        print(f'Lowest uncertainty: {round(planet_radius_earth - planet_radius_earth_negative_uncertainty, rounding_decimal_places)} earth radii')

    print('\n' * 3)
    return planet_radius_earth

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
    return lightcurve_collection


KermLib.ascii_run()
print(f'Astrotool V{version} initialized')
print('Created by Ayrik Nabirahni')
print('\n')

print('Flags:')
flag_index = 0
for x in range(len(user_flags)//2):
    print(user_flags[flag_index] + ' = ' + str(user_flags[flag_index+1]))
    flag_index += 2
if file_saving_enabled is True:
    print(f'File saving format: {file_saving_format}')
if significant_figure_rounding is False:
    print(f'Decimals to round to: {rounding_decimal_places}')
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
        while True:
            star_radius = input("Transited star's radius (in solar radii): ")
            if star_radius is None or star_radius.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius = float(star_radius.strip())
                break

        while True:
            star_radius_uncertainty_positive = input("The 'greather than' uncertainty of transited star's radius (in solar radii): ")
            if star_radius_uncertainty_positive is None or star_radius_uncertainty_positive.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius_uncertainty_positive = abs(float(star_radius_uncertainty_positive.strip()))
                break

        while True:
            star_radius_uncertainty_negative = input("The 'less than' uncertainty of transited star's radius (in solar radii): ")
            if star_radius_uncertainty_negative is None or star_radius_uncertainty_negative.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius_uncertainty_negative = abs(float(star_radius_uncertainty_negative.strip()))
                break


        while True:
            if lowest_flux is None:
                depth_of_phase_fold = input('Depth of Phase Fold: ')
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
                    depth_of_phase_fold = input('Depth of Phase Fold: ')
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
                    lower_bound = int(periodogram_lower_bound_input)
                except ValueError:
                    lower_bound = periodogram_lower_bound_default
            print(prompt_periodogram_upper_bound)
            periodogram_upper_bound_input = input()
            if periodogram_upper_bound_input.strip() == "":
                upper_bound = periodogram_upper_bound_default
            else:
                try:
                    upper_bound = int(periodogram_upper_bound_input)
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
                        lower_bound = int(periodogram_lower_bound_input)
                    except ValueError:
                        lower_bound = periodogram_lower_bound_default

                print(prompt_periodogram_upper_bound) # input upper bound
                periodogram_upper_bound_input = input()
                if periodogram_upper_bound_input.strip() == "":
                    upper_bound = periodogram_upper_bound_default
                else:
                    try:
                        upper_bound = int(periodogram_upper_bound_input)
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
                