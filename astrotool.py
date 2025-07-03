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

if brain_rot_enabled is True:
    import webbrowser
    import random

def save_plot(target_star, file_suffix):
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
        return 'sound_played'
    else:
        return 'sound effects are disabled'


def find_planet_radius(star_radius, depth_of_phase_fold):
    planet_radius_solar = star_radius * math.sqrt(1-depth_of_phase_fold)
    planet_radius_earth = planet_radius_solar * 109.1223801222
    print(f'Calculated planet radius: {planet_radius_earth} earth radii')
    print('\n' * 3)
    return planet_radius_earth

def star_image_retrieval(target_star):
    print(f'Retrieving pixelfile of {target_star}...')
    start_time = time.time() # measure time
    plot_title = f'Pixelfile of {target_star}'
    pixelfile = search_targetpixelfile(target_star).download()

    try:
        pixelfile.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star} system doesn't exist.")
        print('\n')
        return 'fail'
    
    end_time = time.time() # measure load time
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    save_plot(target_star, f'_PIXELFILE.{file_saving_format}')
    plt.show()
    return pixelfile

def star_lightcurve_retrieval(target_star):
    print(f'Retrieving light curve of {target_star}...')
    start_time = time.time()
    plot_title = f'Light curve of {target_star}'
    lightcurve = search_lightcurve(target_star, author=selected_telescope, cadence=selected_cadence).download()
    lightcurve_corrected = lightcurve.remove_outliers().normalize().flatten()
    try:
        lightcurve_corrected.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star} system doesn't exist.")
        print('\n')
        return 'fail'

    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    save_plot(target_star, f'_LIGHTCURVE.{file_saving_format}')
    plt.show()
    return lightcurve_corrected

def star_lightcurve_bulk_retrieval(target_star):
    print(f'Retrieving ALL light curves of {target_star}...')
    start_time = time.time()
    plot_title = f'All light curves of {target_star}'
    search_result = search_lightcurve(target_star, author=selected_telescope, cadence=selected_cadence)
    lightcurve_collection = search_result.download_all()
    try:
        lightcurve_collection.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star} system doesn't exist.")
        print('\n')
        return 'fail'

    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')

    if brain_rot_enabled is True:
        brain_rot_urls_selected = random.sample(brain_rot_urls, 5)
        webbrowser.open_new(brain_rot_urls_selected[0])
        time.sleep(0.2)
        webbrowser.open_new(brain_rot_urls_selected[1])
        time.sleep(0.3)
        webbrowser.open_new(brain_rot_urls_selected[2])
        time.sleep(0.1)
        webbrowser.open_new(brain_rot_urls_selected[3])
        time.sleep(0.2)
        webbrowser.open_new(brain_rot_urls_selected[4])

    save_plot(target_star, f'_LIGHTCURVECOLLECTION.{file_saving_format}')
    plt.show()
    return lightcurve_collection

play_sound('sfx/subwaysurfers.wav', False)

KermLib.ascii_run()
print(f'Astrotool V{version} initialized')
print('Created by Ayrik Nabirahni')
print('\n')

print('Flags:')
flag_index = 0
for x in range(len(user_flags)//2):
    print(user_flags[flag_index] + ' = ' + str(user_flags[flag_index+1]))
    flag_index += 2
print(f'Telescope selected: {selected_telescope}')
print(f'Cadence selected: {selected_cadence}')
if file_saving_enabled is True:
    print(f'File saving format: {file_saving_format}')

print('\n')

while True:
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
    if user_input in [2, 3, 4]:
        while True:
            target_star = input('Target star: ')
            if target_star is None or target_star.strip() == '':
                print(prompt_input_not_recognized)
            else:
                target_star = target_star.strip()
                break

    if user_input == 1:
        while True:
            star_radius = input("Transited star's radius (in solar radii): ")
            if star_radius is None or star_radius.strip() == '':
                print(prompt_input_not_recognized)
            else:
                star_radius = float(star_radius.strip())
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
                use_last_value = input(f'Would you like to use last stored value ({lowest_flux})? (y/n): ')
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
    
    play_sound('sfx/nflsong.wav', True)
    if target_star:
        target_star = target_star.upper()
    print('\n')
    match user_input:
        case 1:
            calculated_planet_radius = find_planet_radius(star_radius, depth_of_phase_fold)
        case 2:
            pixelfile = star_image_retrieval(target_star)
        case 3:
            lightcurve = star_lightcurve_retrieval(target_star)
        case 4:
            lightcurve_collection = star_lightcurve_bulk_retrieval(target_star)
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

                binned_phase_fold = folded_lc.bin(bins=100)
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
                