# ExoPy

A Python3 console-based exoplanet detection tool.

## Motivation
This program was made by me during the CSUDH MSEIP, for use on the Physics team. We were tasked with using/manipulating the recorded light curves from stars during planetary transits, as well as determining their radii using the transited star's radius (given) and the dip in the light level, which is automatically calculated by the tool.

## Dependencies
pip install lightkurve

## How to Use
The program is launched using exopy.py, located in the main directory.
There are many variables and "flags" which can be adjusted, enabled, and disabled in vars.py. This includes enabling/disabling sound effects, file saving, cadence masking, desired telescope, desired cadence, periodogram default bounds, and more.
<br/> <br/>

## Features
### Exoplanet Radius Calculator
Calculate an exoplanets radius using the radius of its star, and the dip in the light emitted during the transit (phase fold, automatically calculated and saved during Lightcurve Retrieval.) Includes uncertanties.

### Lightcurve Retrieval/Calculation
Automatically retrieve, plot and graph lightcurves of stars. Automatically generate periodogram and phase folds based on user input, and save for use in radius calculations.

### Pixelfile Retrieval
Automatically retrieve the pixelfile of a star and display it.

### Automated File Saving
Automatically saves all plots to a file type of user's choosing, adjustable in vars. SVG recommended/default.

### Significant Figure Rounding
Toggleable via vars.py.


![kermitine](https://github.com/kermitine/kermitine/blob/b523c5954ea8820f70eb6ff786f2dbec7ce08955/images/kermitine.png)
