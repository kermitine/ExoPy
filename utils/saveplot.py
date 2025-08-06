# Copyright (C) 2025 Ayrik Nabirahni
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see https://www.gnu.org/licenses.


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