"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the ExoPy project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

import pandas as pd
import requests

def wikipull(wiki_id, target_data): # rolls it all up into one function
    pulled_wiki = get_wiki_data(wiki_id, target_data)
    nominal, upper_diff, lower_diff = parse_wiki_data(pulled_wiki)
    return nominal, upper_diff, lower_diff

def get_wiki_data(wiki_id, target_data):
    wikipedia_url = 'https://en.wikipedia.org/wiki/' + wiki_id.lower()
    wikipedia_html = requests.get(wikipedia_url, headers={'User-Agent': 'Mozilla/5.0'})
    star_table = pd.read_html(wikipedia_html.content)[0]
    
    first_column = star_table.columns[0]
    pulled_row = star_table.loc[star_table[first_column] == target_data]
    pulled_value = pulled_row.iloc[0, 1]
    return pulled_value
    
def parse_wiki_data(infotable_string):
    list_of_accepted_nums_filter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    list_of_accepted_symbols_filter =  ['+', '−', '-', '±']
    plus_minus_combined = False
    infotable_string_list = []
    nominal_value_list = []
    nominal_done = False
    upper_diff_value_list = []
    upper_diff_done = False
    lower_diff_value_list = []
    infotable_string = infotable_string.replace(' ', '') # strips all spaces from text

    for char in infotable_string: # further processing to remove all units
        if char == '[': # STOP ONCE REFERENCE REACHED
            break
        elif char in list_of_accepted_nums_filter + list_of_accepted_symbols_filter:
            infotable_string_list.append(char)


    infotable_string_filtered = ''.join(infotable_string_list)
    for char in infotable_string_filtered:
        if char not in list_of_accepted_symbols_filter and nominal_done == False and upper_diff_done == False:
            nominal_value_list.append(char)
        elif char == '+':
            nominal_done = True
            continue
        elif char == '±':
            nominal_done = True
            plus_minus_combined = True
            continue
        elif char not in list_of_accepted_symbols_filter and nominal_done == True and upper_diff_done == False and plus_minus_combined == True:
            upper_diff_value_list.append(char)
            lower_diff_value_list.append(char)
        elif char not in list_of_accepted_symbols_filter and nominal_done == True and upper_diff_done == False and plus_minus_combined == False:
            upper_diff_value_list.append(char)
        elif char == '−' or char == '-':
            upper_diff_done = True
            continue
        elif char not in list_of_accepted_symbols_filter and nominal_done == True and upper_diff_done == True:
            lower_diff_value_list.append(char)

    joined_nominal = ''.join(nominal_value_list)
    joined_upper_diff = ''.join(upper_diff_value_list)
    joined_lower_diff = ''.join(lower_diff_value_list)

    if joined_nominal == '' or joined_nominal == None:
        joined_nominal = 0
    if joined_upper_diff == '' or joined_upper_diff == None:
        joined_upper_diff = 0
    if joined_lower_diff == '' or joined_lower_diff == None:
        joined_lower_diff = 0


    return float(joined_nominal), float(joined_upper_diff), float(joined_lower_diff)
