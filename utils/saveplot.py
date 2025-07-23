from config.config import *
import os
import time
import matplotlib.pyplot as plt

def save_plot(target_star, file_suffix):
    """
    Streamlined way to save matplotlib plots to /saved_data
    """
    if file_saving_enabled is True:
        directory_name = 'exopy/saved/saved_data/' + target_star
        file_name = directory_name + '/' + target_star + file_suffix
        os.makedirs(directory_name, exist_ok=True)
        plt.savefig(file_name)
        print(f'Saving {target_star}{file_suffix}...')
        time.sleep(0.8)
        return 'saved'
    else:
        return 'saving is disabled'