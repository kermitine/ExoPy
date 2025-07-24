# ExoPy

A Python3 console-based exoplanet detection tool.

## Motivation
This program was made by me during the CSUDH MSEIP, for use on the Physics team. We were tasked with using/manipulating the recorded light curves from stars during planetary transits, as well as determining their radii using the transited star's radius (given) and the dip in the light level, which is automatically calculated by the tool.

## Dependencies
```pip install lightkurve```

## How to Use
run exopy.bat in the root folder. Alternatively, in the root, run ```python -m exopy.exopy```
<br/> <br/>

## Features
### Exoplanet Radius Calculator
Calculate an exoplanets radius using the radius of its star, and the dip in the light emitted during the transit (phase fold, automatically calculated and saved during Lightcurve Retrieval.) Includes uncertanties.

### Star Habitable Zone Calculator

### Star Temperature Calculator

### Orbital Radius Calculator

### Exoplanet Stellar Energy Calculator

### Blackbody Exoplanet Temperature Calculator

### Lightcurve Retrieval/Calculation
Automatically retrieve, plot and graph lightcurves of stars. Automatically generate periodogram and phase folds based on user input, and save for use in radius calculations.

### Pixelfile Retrieval
Automatically retrieve the pixelfile of a star and display it.

### Automated File Saving
Automatically saves all plots to a file type of user's choosing, adjustable in vars. SVG recommended/default.

### Robust Error and Crash Handling


![kermitine](https://github.com/kermitine/kermitine/blob/b523c5954ea8820f70eb6ff786f2dbec7ce08955/images/kermitine.png)
