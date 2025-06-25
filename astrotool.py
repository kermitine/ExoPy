from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
import time
from vars import *
from KermLib.KermLib import *

def star_image_retrieval(target_star):
    print('Retrieving pixelfile of', target_star + '...')
    start_time = time.time()
    plot_title = 'Pixelfile of ' + target_star
    pixelfile = search_targetpixelfile(target_star).download()
    pixelfile.plot(title=plot_title)
    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()

def star_lightcurve_retrieval(target_star):
    print('Retrieving light curve of', target_star + '...')
    start_time = time.time()
    plot_title = 'Light curve of ' + target_star
    lightcurve = search_lightcurve(target_star).download()
    lightcurve_corrected = lightcurve.remove_outliers().normalize()
    lightcurve_corrected.plot(title=plot_title)
    end_time = time.time()
    print('took', round((end_time - start_time), 1), 'seconds to retrieve')
    plt.show()


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
    # mission = str(input('Mission (Kepler, K2, Tess): '))
    # quarter = str(input('Quarter (Recommend 16): '))
    match user_input:
        case 1:
            star_image_retrieval(target_star)
        case 2:
            star_lightcurve_retrieval(target_star)
    print('\n')