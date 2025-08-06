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


import time
from lightkurve import search_targetpixelfile
from config.config import *
from utils.saveplot import *
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('qtagg')
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
    save_plot(target_star, f'_PIXELFILE.{user_flags['file_saving_format']}')
    plt.show()
    return pixelfile