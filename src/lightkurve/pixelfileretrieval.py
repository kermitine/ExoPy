import time
from lightkurve import search_targetpixelfile
from config.config import *
from utils.saveplot import *
import matplotlib.pyplot as plt
def star_pixelfile_retrieval(target_star):
    """
    Retrieves and displays pixelfile of star.
    """
    print(f'Retrieving pixelfile of {target_star}...')
    start_time = time.time() # measure time 
    plot_title = f'Pixelfile of {target_star}'
    pixelfile = search_targetpixelfile(target_star).download()

    try:
        pixelfile.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star}, or system doesn't exist.")
        print('\n')
        return 'fail'
    
    end_time = time.time() # measure time
    print(f'took {round((end_time - start_time), 1)} seconds to retrieve')
    save_plot(target_star, f'_PIXELFILE.{file_saving_format}')
    plt.show()
    print('\n' * 3)
    return pixelfile