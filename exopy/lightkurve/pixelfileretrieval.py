"""
Copyright (C) 2025 Ayrik Nabirahni. This file
is apart of the ExoPy project, and licensed under
the GNU AGPL-3.0-or-later. See LICENSE and README for more details.
"""

import time
from lightkurve import search_targetpixelfile
from config.config import *
from utils.saveplot import *
from utils.timer import *
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('qtagg')
def star_pixelfile_retrieval(target_star):
    """
    Retrieves and displays pixelfile of star.
    """
    print(f'Retrieving pixelfile of {target_star}...')
    timer()
    plot_title = f'Pixelfile of {target_star}'
    pixelfile = search_targetpixelfile(target_star).download()

    try:
        pixelfile.plot(title=plot_title)
    except:
        print(f"ERROR: Either no data available for {target_star}, or system doesn't exist.")
        print('\n')
        return 'fail'
    
    timer()
    save_plot(target_star, f'_PIXELFILE.{user_flags['file_saving_format']}')
    plt.show()
    return pixelfile