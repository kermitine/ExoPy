"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the ExoPy project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

from lightkurve import search_lightcurve
from config.config import *
from utils.saveplot import *
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib
from utils.timer import *

matplotlib.use('qtagg')
def star_lightcurve_analysis(target_star):
    """
    Retrieves multiple light curves of star. Automatically graphs and saves light curve, periodogram,
    binned lightcurve and saves values for radius calculations.
    """
    print(f'Retrieving ALL light curves of {target_star}...')
    timer()
    plot_title = f'All light curves of {target_star}'
    search_result = search_lightcurve(target_star, author=user_flags['selected_telescope'], cadence=user_flags['selected_cadence'])
    lightcurve_collection = search_result.download_all()
    try:
        lightcurve_collection.plot(title=plot_title)
    except ValueError:
        print(f"ERROR: Either no data available for {target_star}, or system doesn't exist.")
        return 'fail'

    timer()
    save_plot(target_star, f'_LIGHTCURVECOLLECTION.{user_flags['file_saving_format']}')
    plt.show()
    return lightcurve_collection

def star_lightcurve_analysis_continued(lightcurve_collection, target_star):
    print('Stitching light curve collection...')
    timer()
    lightcurve_stitched = lightcurve_collection.stitch()
    plot_title = f'Stitched lightcurve of {target_star}'
    lightcurve_stitched = lightcurve_stitched.remove_outliers().normalize().flatten()
    timer()
    lightcurve_stitched.plot(title=plot_title)
    
    
    save_plot(target_star, f'_LIGHTCURVECOLLECTIONSTITCHED.{user_flags['file_saving_format']}')
    plt.show()
    alphabet_index = 0
    periodogram_lower_bound_input = input(prompt_periodogram_lower_bound)
    if periodogram_lower_bound_input.strip() == "":
        lower_bound = periodogram_lower_bound_default
    else:
        try:
            lower_bound = round(float(periodogram_lower_bound_input), 2)
        except ValueError:
            lower_bound = periodogram_lower_bound_default
    periodogram_upper_bound_input = input(prompt_periodogram_upper_bound)
    if periodogram_upper_bound_input.strip() == "":
        upper_bound = periodogram_upper_bound_default
    else:
        try:
            upper_bound = round(float(periodogram_upper_bound_input), 2)
        except ValueError:
            upper_bound = periodogram_upper_bound_default

    print('Generating periodogram...')
    timer()
    period = np.linspace(lower_bound, upper_bound, 100000) # Period
    periodogram_bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
    plot_title = f'Periodogram of light curve of {target_star}'
    periodogram_bls.plot(title=plot_title)

    save_plot(target_star, f'_LIGHTCURVEPERIODOGRAM_{alphabet_list[alphabet_index]}.{user_flags['file_saving_format']}')
    timer()
    plt.show()
    # FIRST ONE ABOVE. REST IN LOOP

    while True:
        print('Folding light curve...')
        timer()
        planet_period = periodogram_bls.period_at_max_power
        planet_t0 = periodogram_bls.transit_time_at_max_power
        planet_dur = periodogram_bls.duration_at_max_power
        ax = lightcurve_stitched.fold(period=planet_period, epoch_time=planet_t0).scatter()
        ax.set_xlim(-5, 5)
        ax.plot(title=f'Phasefold of Planet {alphabet_list[alphabet_index]}')

        save_plot(target_star, f'_PHASEFOLD_{alphabet_list[alphabet_index]}.{user_flags['file_saving_format']}')
        timer()
        plt.show()
        
        folded_lc = lightcurve_stitched.fold(period=planet_period, epoch_time=planet_t0)
        flux = folded_lc.flux
        print('Binning...')
        timer()
        binned_phase_fold = folded_lc.bin(bins=user_flags['selected_bins'])
        binned_phase_fold.plot()
        save_plot(target_star, f'_PHASEFOLDBINNED_{alphabet_list[alphabet_index]}.{user_flags['file_saving_format']}')

        min_idx = np.nanargmin(binned_phase_fold.flux)
        min_flux  = binned_phase_fold.flux[min_idx]

        planet_period_float = planet_period.value # convert to float
        print(f"Lowest flux = {min_flux:.6f}. Saved to memory.")
        print(f"Likely period = {planet_period_float} days. Saved to memory.")
        lowest_flux = f"{min_flux:.6f}"
        lowest_flux = float(lowest_flux)
        timer()
        plt.show()
        
        
        while True:
            exit_function = input('Would you like to create another periodogram? (y/n): ')
            if exit_function is None or exit_function.strip() == '' or exit_function.lower().strip() not in ['y', 'n']:
                print(prompt_input_not_recognized)
            else:
                exit_function = exit_function.lower().strip()
                break
        if exit_function == 'n':
            return lowest_flux, planet_period_float


        alphabet_index += 1

        if user_flags['masking_enabled'] is True: # mask signals if true
            planet_mask = periodogram_bls.get_transit_mask(period=planet_period, transit_time=planet_t0, duration=planet_dur)
            lightcurve_stitched = lightcurve_stitched[~planet_mask]
            print('Masking enabled ' + '(' + alphabet_list[alphabet_index] + ')...')

        periodogram_lower_bound_input = input(prompt_periodogram_lower_bound)
        if periodogram_lower_bound_input.strip() == "":
            lower_bound = periodogram_lower_bound_default
        else:
            try:
                lower_bound = round(float(periodogram_lower_bound_input), 2)
            except ValueError:
                lower_bound = periodogram_lower_bound_default

        periodogram_upper_bound_input = input(prompt_periodogram_upper_bound)
        if periodogram_upper_bound_input.strip() == "":
            upper_bound = periodogram_upper_bound_default
        else:
            try:
                upper_bound = round(float(periodogram_upper_bound_input),2)
            except ValueError:
                upper_bound = periodogram_upper_bound_default

        print('Generating periodogram...')
        
        period = np.linspace(lower_bound, upper_bound, 100000) # Period
        periodogram_bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
        plot_title = 'Periodogram of light curve of ' + target_star
        periodogram_bls.plot(title=plot_title)
        save_plot(target_star, f'_LIGHTCURVEPERIODOGRAM_{alphabet_list[alphabet_index]}.{user_flags['file_saving_format']}')
        plt.show()