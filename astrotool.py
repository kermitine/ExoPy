from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
import time
from vars import *
from KermLib.KermLib import *
import numpy as np






def star_image_retrieval(target_star):
    print('Retrieving pixelfile of', target_star + '...')
    start_time = time.time()
    plot_title = 'Pixelfile of ' + target_star
    pixelfile = search_targetpixelfile(target_star).download()
    pixelfile.plot(title=plot_title)
    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()
    return pixelfile

def star_lightcurve_retrieval(target_star):
    print('Retrieving light curve of', target_star + '...')
    start_time = time.time()
    plot_title = 'Light curve of ' + target_star
    lightcurve = search_lightcurve(target_star, author='Kepler', cadence='long').download()
    lightcurve_corrected = lightcurve.remove_outliers().normalize()
    lightcurve_corrected.plot(title=plot_title)
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
    lightcurve_collection.plot(title=plot_title)
    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()
    return lightcurve_collection

KermLib.ascii_run()
print('Astrotool', version, 'initialized')

print('\n')
print('--Loop Start--')

while True:
    function_index = 1
    print('Select desired function:')
    for function in list_of_tools:
        print(function_index, '--', function)
        function_index += 1
    user_input = int(input())
    print(list_of_tools[user_input-1], 'selected')
    

    print('Enter parameters:')
    target_star = str(input('Target star: '))
    match user_input:
        case 1:
            pixelfile = star_image_retrieval(target_star)
        case 2:
            lightcurve = star_lightcurve_retrieval(target_star)
        case 3:
            lightcurve_collection = star_lightcurve_bulk_retrieval(target_star)
            print('Stitching light curve collection...')
            lightcurve_stitched = lightcurve_collection.stitch()
            lightcurve_stitched.plot(title=target_star)
            plt.show()


            print('Generating periodogram...')
            period = np.linspace(1, 20, 10000) #Period
            bls = lightcurve_stitched.to_periodogram(method='bls', period=period, frequency_factor=500)
            bls.plot()
            plt.show()
    
    print('\n')