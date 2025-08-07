"""
Copyright (C) 2025 Ayrik Nabirahni. This file is licensed under
the AGPLv3 license, and is apart of the ExoPy project.
See LICENSE and README for more details.
"""

from config.config import *
import os
import matplotlib.pyplot as plt

if user_flags['file_saving_enabled'] == True:
    try:
        os.makedirs('saved', exist_ok=True)
    except PermissionError:
        print('ERROR: Insufficient permissions, file saving disabled. Please run as adminstrator.')
        user_flags['file_saving_enabled'] = False

def save_plot(target_star, file_suffix):
    """
    Streamlined way to save matplotlib plots to /saved_data
    """
    if user_flags['file_saving_enabled'] == True:
        directory_name = 'saved/saved_data/' + target_star
        file_name = directory_name + '/' + target_star + file_suffix
        os.makedirs(directory_name, exist_ok=True)
        plt.savefig(file_name)
        print(f'Saving {target_star}{file_suffix}...')
        return 'saved'
    else:
        return 'saving is disabled'