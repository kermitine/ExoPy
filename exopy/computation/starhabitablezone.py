from config.config import *
import math
def habitable_zone_calculator(star_luminosity, star_luminosity_uncertainty_positive, star_luminosity_uncertainty_negative):
    try:
        inner_goldilocks_radius_lower = math.sqrt((star_luminosity-star_luminosity_uncertainty_negative)/1.1)
        inner_goldilocks_radius_nominal = math.sqrt(star_luminosity/1.1)

        outer_goldilocks_radius_nominal = math.sqrt(star_luminosity/0.53)
        outer_goldilocks_radius_upper = math.sqrt((star_luminosity+star_luminosity_uncertainty_positive)/0.53)
    except ValueError:
        print('ERROR: Negative root. Did you enter the correct luminosity incertanties?')
        print('\n' * 3)
        return '(Not Generated)', 0, '(Not Generated)', 0

    inner_goldilocks_radius_lower_diff = inner_goldilocks_radius_nominal-inner_goldilocks_radius_lower
    outer_goldilocks_radius_upper_diff = outer_goldilocks_radius_upper-outer_goldilocks_radius_nominal

    print(f'Calculated nominal inner goldilocks zone radius: {round(inner_goldilocks_radius_nominal, rounding_decimal_places)} AU (-{round(inner_goldilocks_radius_lower_diff, rounding_decimal_places)} AU)')
    print(f'Calculated nominal outer goldilocks zone radius: {round(outer_goldilocks_radius_nominal, rounding_decimal_places)} AU (+{round(outer_goldilocks_radius_upper_diff, rounding_decimal_places)} AU)')
    print('\n' * 3)
    return round(inner_goldilocks_radius_nominal, rounding_decimal_places), round(inner_goldilocks_radius_lower_diff, rounding_decimal_places), round(outer_goldilocks_radius_nominal, rounding_decimal_places), round(outer_goldilocks_radius_upper_diff, rounding_decimal_places)