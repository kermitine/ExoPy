"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the ExoPy project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

from config.config import *
def get_star_luminosity():
    while True:
        star_luminosity = input("Star's luminosity (L☉): ")
        if star_luminosity is None or star_luminosity.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_luminosity = float(star_luminosity.strip())
                break
            except ValueError:
                print(prompt_input_not_recognized)
            
    while True:
        star_luminosity_uncertainty_positive = input("The 'greather than' uncertainty of transited star's luminosity (L☉): ")
        if star_luminosity_uncertainty_positive is None or star_luminosity_uncertainty_positive.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_luminosity_uncertainty_positive = abs(float(star_luminosity_uncertainty_positive.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)

    while True:
        star_luminosity_uncertainty_negative = input("The 'less than' uncertainty of transited star's luminosity (L☉): ")
        if star_luminosity_uncertainty_negative is None or star_luminosity_uncertainty_negative.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_luminosity_uncertainty_negative = abs(float(star_luminosity_uncertainty_negative.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)
    return star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative

def get_star_mass():
    while True:
        star_mass_solarmass = input("Enter star's mass (M☉): ")
        if star_mass_solarmass is None or star_mass_solarmass.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_mass_solarmass = float(star_mass_solarmass.strip())
                break
            except ValueError:
                print(prompt_input_not_recognized)
        
    while True:
        star_mass_solarmass_uncertainty_positive = input("The 'greather than' uncertainty of transited star's mass (M☉): ")
        if star_mass_solarmass_uncertainty_positive is None or star_mass_solarmass_uncertainty_positive.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_mass_solarmass_uncertainty_positive = abs(float(star_mass_solarmass_uncertainty_positive.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)

    while True:
        star_mass_solarmass_uncertainty_negative = input("The 'less than' uncertainty of transited star's mass (M☉): ")
        if star_mass_solarmass_uncertainty_negative is None or star_mass_solarmass_uncertainty_negative.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_mass_solarmass_uncertainty_negative = abs(float(star_mass_solarmass_uncertainty_negative.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)
    return star_mass_solarmass, star_mass_solarmass_uncertainty_positive, star_mass_solarmass_uncertainty_negative

def get_star_radius():
    while True:
        star_radius = input("Star's radius (R☉): ")
        if star_radius is None or star_radius.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_radius = float(star_radius.strip())
                break
            except ValueError:
                print(prompt_input_not_recognized)
    while True:
        star_radius_uncertainty_positive = input("The 'greather than' uncertainty of transited star's radius (R☉): ")
        if star_radius_uncertainty_positive is None or star_radius_uncertainty_positive.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_radius_uncertainty_positive = abs(float(star_radius_uncertainty_positive.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)

    while True:
        star_radius_uncertainty_negative = input("The 'less than' uncertainty of transited star's radius (R☉): ")
        if star_radius_uncertainty_negative is None or star_radius_uncertainty_negative.strip() == '':
            print(prompt_input_not_recognized)
        else:
            try:
                star_radius_uncertainty_negative = abs(float(star_radius_uncertainty_negative.strip()))
                break
            except ValueError:
                print(prompt_input_not_recognized)
    return star_radius, star_radius_uncertainty_positive, star_radius_uncertainty_negative

def get_target_star(target_star):
    while True:
        target_star = input(f'Enter system/star name (Last used: {target_star}): ')
        if target_star is None or target_star.strip() == '':
            print(prompt_input_not_recognized)
        else:
            target_star = target_star.strip().upper()
            break
    return target_star

def get_star_lowest_flux(lowest_flux):
    while True:
        if lowest_flux is None:
            depth_of_phase_fold = input('Minimum flux value during transit: ')
            if depth_of_phase_fold is None or depth_of_phase_fold.strip() == '':
                    print(prompt_input_not_recognized)
            else:
                try:
                    depth_of_phase_fold = float(depth_of_phase_fold.strip())
                    return depth_of_phase_fold
                except ValueError:
                    print(prompt_input_not_recognized)
                    continue
        else:
            use_last_value = input(f'Would you like to use the last stored lowest flux value ({lowest_flux})? (y/n): ')
            if use_last_value.lower().strip() == 'y':
                depth_of_phase_fold = lowest_flux
                return depth_of_phase_fold
            else:
                depth_of_phase_fold = input('Minimum flux value during transit: ')
                if depth_of_phase_fold is None or depth_of_phase_fold.strip() == '':
                    print(prompt_input_not_recognized)
                else:
                    try:
                        depth_of_phase_fold = float(depth_of_phase_fold.strip())
                        return depth_of_phase_fold
                    except ValueError:
                        print(prompt_input_not_recognized)
                        continue