from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
from vars import *
from KermLib.KermLib import *


def star_image_retrieval(target_star):
    plot_title = 'Pixelfile of ' + target_star
    pixelfile = search_targetpixelfile(target_star).download()
    pixelfile.plot(title=plot_title)
    plt.show()

def star_lightcurve_retrieval(target_star):
    plot_title = 'Light Curve of ' + target_star
    lightcurve = search_lightcurve(target_star).download()
    lightcurve_corrected = lightcurve.remove_outliers().normalize()
    lightcurve_corrected.plot(title=plot_title)
    plt.show()

print('--Program Loop Start--')

while True:
    function_index = 1
    print('Select desired function:')
    for function in list_of_tools:
        print(function_index, '--', function)
        function_index += 1
    print('\n')
    user_input = int(input())
    print(list_of_tools[user_input-1], 'selected')
    
    print('Select target star')
    target_star = str(input())
    

    match user_input:
        case 1:
            star_image_retrieval(target_star)
        case 2:
            star_lightcurve_retrieval(target_star)