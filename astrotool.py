from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
import time
from vars import *
from KermLib.KermLib import *
import numpy as np
import os
import winsound

def save_plot(target_star, file_suffix):
    directory_name = 'saved_data/' + target_star
    file_name = directory_name + '/' + target_star + file_suffix
    os.makedirs(directory_name, exist_ok=True)
    plt.savefig(file_name)
    return None
    


def star_image_retrieval(target_star):
    print('Retrieving pixelfile of', target_star + '...')
    start_time = time.time() # measure load time
    plot_title = 'Pixelfile of ' + target_star
    pixelfile = search_targetpixelfile(target_star).download()

    try:
        pixelfile.plot(title=plot_title)
    except:
        print('ERROR: Either no data available of', target_star + ", or system doesn't exist.")
        print('\n')
        return 'fail'
    
    save_plot(target_star, '_PIXELFILE.svg')
    
    end_time = time.time() # measure load time
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()
    return pixelfile

def star_lightcurve_retrieval(target_star):
    print('Retrieving light curve of', target_star + '...')
    start_time = time.time()
    plot_title = 'Light curve of ' + target_star
    lightcurve = search_lightcurve(target_star, author='Kepler', cadence='long').download()
    lightcurve_corrected = lightcurve.remove_outliers().normalize().flatten()
    try:
        lightcurve_corrected.plot(title=plot_title)
    except:
        print('ERROR: Either no data available of', target_star + ", or system doesn't exist.")
        print('\n')
        return 'fail'

    save_plot(target_star, '_LIGHTCURVE.svg')

    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()
    return lightcurve_corrected

def star_lightcurve_bulk_retrieval(target_star):
    print('Retrieving ALL light curves of', target_star + '...')
    start_time = time.time()
    plot_title = 'All light curves of ' + target_star
    search_result = search_lightcurve(target_star, author='Kepler', cadence='long')
    lightcurve_collection = search_result.download_all()
    try:
        lightcurve_collection.plot(title=plot_title)
    except:
        print('ERROR: Either no data available of', target_star + ", or system doesn't exist.")
        print('\n')
        return 'fail'

    save_plot(target_star, '_LIGHTCURVECOLLECTION.svg')

    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()
    return lightcurve_collection

KermLib.ascii_run()
print('Astrotool V' + str(version), 'initialized')

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
            print('Input not recognized. Please try again.')
            user_input = input()
        else:
            user_input = int(user_input)
            break

    print('Enter parameters:')
    while True:
        target_star = input('Target star: ')
        if target_star is None or target_star.strip() == '':
            print('Input not recognized. Please try again.')
        else:
            target_star = target_star.strip()
            break

    target_star = target_star.upper()
    match user_input:
        case 1:
            pixelfile = star_image_retrieval(target_star)
        case 2:
            lightcurve = star_lightcurve_retrieval(target_star)
        case 3:
            lightcurve_collection = star_lightcurve_bulk_retrieval(target_star)
            if lightcurve_collection == 'fail':
                continue
            print('Stitching light curve collection...')
            lightcurve_stitched = lightcurve_collection.stitch()
            plot_title = 'Stitched lightcurve of ' + target_star
            lightcurve_stitched = lightcurve_stitched.remove_outliers().normalize().flatten()
            lightcurve_stitched.plot(title=plot_title)
            
            save_plot(target_star, '_LIGHTCURVECOLLECTIONSTITCHED.svg')

            plt.show()

            alphabet_index = 0
            
            print('Please input periodogram lower bound (if blank, default 1):')
            lower_bound_input = input()
            if lower_bound_input.strip() == "":
                lower_bound = 1
            else:
                try:
                    lower_bound = int(lower_bound_input)
                except ValueError:
                    lower_bound = 1
            print('Please input periodogram upper bound (if blank, default 20):')
            upper_bound_input = input()
            if upper_bound_input.strip() == "":
                upper_bound = 20
            else:
                try:
                    upper_bound = int(upper_bound_input)
                except ValueError:
                    upper_bound = 20

            winsound.PlaySound("sfx/microwave_sound_effect.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
            time.sleep(3)
            print('Generating periodogram...')
            
            period = np.linspace(lower_bound, upper_bound, 100000) # Period
            periodogram_bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
            plot_title = 'Periodogram of light curve of ' + target_star
            periodogram_bls.plot(title=plot_title)
            
            save_plot(target_star, '_LIGHTCURVEPERIODOGRAM_' + alphabet_list[alphabet_index] + '.svg')

            winsound.PlaySound("sfx/ovending.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
            time.sleep(2)
            plt.show()
            # FIRST ONE ABOVE. REST IN LOOP

            while True:

                planet_period = periodogram_bls.period_at_max_power
                planet_t0 = periodogram_bls.transit_time_at_max_power
                planet_dur = periodogram_bls.duration_at_max_power

                ax = lightcurve_stitched.fold(period=planet_period, epoch_time=planet_period).scatter()
                ax.set_xlim(-5, 5)
                ax.plot(title='Phasefold of Planet ' + alphabet_list[alphabet_index])

                save_plot(target_star, '_PHASEFOLD_' + alphabet_list[alphabet_index] + '.svg')
                
                plt.show()
                
                alphabet_index += 1

                if use_masking is True: # mask signals if true
                    planet_mask = periodogram_bls.get_transit_mask(period=planet_period, transit_time=planet_t0, duration=planet_dur)
                    lightcurve_stitched = lightcurve_stitched[~planet_mask]
                    print('Masking enabled ' + '(' + alphabet_list[alphabet_index] + ')...')

                print('Please input periodogram lower bound (if blank, default 1):')
                lower_bound_input = input()
                if lower_bound_input.strip() == "":
                    lower_bound = 1
                else:
                    try:
                        lower_bound = int(lower_bound_input)
                    except ValueError:
                        lower_bound = 1
                print('Please input periodogram upper bound (if blank, default 20):')
                upper_bound_input = input()
                if upper_bound_input.strip() == "":
                    upper_bound = 20
                else:
                    try:
                        upper_bound = int(upper_bound_input)
                    except ValueError:
                        upper_bound = 20

                winsound.PlaySound("sfx/microwave_sound_effect.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
                time.sleep(3)
                print('Generating periodogram...')
                
                period = np.linspace(lower_bound, upper_bound, 100000) # Period
                periodogram_bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
                plot_title = 'Periodogram of light curve of ' + target_star
                periodogram_bls.plot(title=plot_title)
                winsound.PlaySound("sfx/ovending.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
                time.sleep(2)

                save_plot(target_star, '_LIGHTCURVEPERIODOGRAM_' + alphabet_list[alphabet_index] + '.svg')

                plt.show()