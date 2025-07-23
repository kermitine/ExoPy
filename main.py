from config.config import *
from utils.KermLib.KermLib import *
from src.getdata.getstardata import *
from utils.initvars import *


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
if selected_cadence.lower() == 'short':
    print('WARNING: short cadence selected. Expect long loading times.')
print(f'Bins: {selected_bins}')


def get_desired_function():
    function_index = 1
    for function in list_of_tools:
        print(function_index, '--', function)
        list_of_functions_index.append(str(function_index))
        function_index += 1
    while True: # PREVENTS CRASHES FROM UNRECOGNIZED INPUTS
        user_input = input('Select desired function: ')
        if user_input not in list_of_functions_index:
            print(prompt_input_not_recognized)
            continue
        else:
            try:
                user_input = int(user_input)
                break
            except ValueError:
                print(prompt_input_not_recognized)
    return list_of_tools[user_input-1]
    
while True: # main program loop
    desired_function = get_desired_function()

    if desired_function == 'Star Pixelfile Retrieval' or desired_function == 'Star Light Curve Analysis':
        target_star = get_target_star(target_star)
        if desired_function == 'Star Pixelfile Retrieval':
            from src.lightkurve.pixelfileretrieval import star_pixelfile_retrieval
            star_pixelfile_retrieval(target_star)
        elif desired_function == 'Star Light Curve Analysis':
            from src.lightkurve.lightcurveanalysis import *
            lightcurve_collection = star_lightcurve_analysis(target_star)
            lowest_flux, planet_period_float = star_lightcurve_analysis_continued(lightcurve_collection, target_star)

    elif desired_function == 'Exoplanet Radius Calculator':
        from src.computation.exoplanetradius import find_exoplanet_radius
        from src.getdata.getstardata import *
        depth_of_phase_fold = get_star_lowest_flux(lowest_flux)
        star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative = get_star_radius()
        print('\n' * 2)
        planet_radius_earth_nominal, planet_radius_earth_upper_diff, planet_radius_earth_lower_diff = find_exoplanet_radius(star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative, depth_of_phase_fold)

    elif desired_function == 'Star Habitable Zone Calculator':
        from src.computation.starhabitablezone import habitable_zone_calculator
        star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative = get_star_luminosity()
        print('\n' * 2)
        inner_goldilocks_radius_nominal, inner_goldilocks_radius_lower_diff, outer_goldilocks_radius_nominal, outer_goldilocks_radius_upper_diff = habitable_zone_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

    elif desired_function == 'Stefan-Boltzmann Star Temperature Calculator':
        from src.computation.startemperature import stefan_boltzmann_star_temperature_calculator
        star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative = get_star_luminosity()
        star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative = get_star_radius()
        print('\n' * 2)
        star_temperature_nominal, star_temperature_upper_diff, star_temperature_lower_diff = stefan_boltzmann_star_temperature_calculator(star_radius, star_luminosity, star_radius_uncertainty_positive, star_radius_uncertainty_negative, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative)

    elif desired_function == 'Kepler Orbital Radius Calculator':
        from src.computation.orbitalSMA import kepler_orbital_radius_calculator
        from src.getdata.getexoplanetdata import *
        orbital_period_days = get_exoplanet_orbital_period(planet_period_float)
        star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative = get_star_mass()
        print('\n' * 2)
        semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU = kepler_orbital_radius_calculator(orbital_period_days, star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative)

    elif desired_function == 'Inverse-Square Exoplanet Stellar Energy Calculator':
        from src.computation.exoplanetstellarenergy import exoplanet_flux_received
        from src.getdata.getexoplanetdata import *
        star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative = get_star_luminosity()
        semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU = get_exoplanet_semimajoraxis()
        print('\n' * 2)
        flux_watts_nominal, flux_watts_upper_diff, flux_watts_lower_diff = exoplanet_flux_received(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU)

    elif desired_function == 'Blackbody Exoplanet Temperature Calculator':
        from src.getdata.getexoplanetdata import *
        from src.computation.exoplanettemperature import blackbody_temperature_calculator
        star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative = get_star_luminosity()
        semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU = get_exoplanet_semimajoraxis()
        print('\n' * 2)
        blackbody_temperature_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative, semi_major_axis_nominal_AU, semi_major_axis_upper_diff_AU, semi_major_axis_lower_diff_AU)

    elif desired_function == 'Generate Full Report':
        from src.computation.generatereport import generate_full_report
        generate_full_report(lowest_flux, planet_period_float)