"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the ExoPy project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

def convert_dict_to_float(wikipull_dict):
    string_nominal = wikipull_dict['nominal']
    string_lower_uncertainty = wikipull_dict['lower_uncertainty']
    string_higher_uncertainty = wikipull_dict['higher_uncertainty']

    float_nominal = float(string_nominal)
    float_lower_uncerainty = float(string_lower_uncertainty)
    float_higher_uncerainty = float(string_higher_uncertainty)
    return float_nominal, float_higher_uncerainty, float_lower_uncerainty
