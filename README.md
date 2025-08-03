# ExoPy

A Python3 console-based exoplanet detection tool, leveraging LightKurve

## Motivation
This program was made by me during the CSUDH MSEIP-STALP, for use on the Physics team. Our core project was to analyze Kepler light curve data, and create annotated graphs of the transit event, as well as ascertain the radius of the transiting exoplanet. However, the scope of our project increased, and as such, ExoPy contains many more features to help streamline the entire exoplanet detection process.

## Features
### Light Curve Analysis
Analyze Kepler, K2, or TESS light curves using an easy, simple-to-use wizard. Automatically generate phase folds and save key data, such as likely orbital period length and fold depth for use in Exoplanet radius calculations.

### Star Habitable Zone Calculator
Estimate a star's habitable zone's radius using its luminosity.

### Star Temperature Calculator
Estimate a star's temperature using its luminosity and radius.

### Orbital Radius Calculator
Estimate a planet's orbital radius using its orbital period.

### Exoplanet Stellar Energy Calculator
Estimate the amount of energy absorbed by a planet from its star using the star's luminosity and the exoplanet's orbital radius.

### Blackbody Exoplanet Temperature Calculator
Estimate the temperature of an exoplanet (assuming a blackbody) using the star's luminosity and the exoplanet's orbital radius.  

### Pixelfile Retrieval
Quickly pull Kepler, K2, or TESS pixelfiles of stars.

### Automatic Wikipedia Stellar Data Retrieval
Automatically attempt to pull a star's data, such as radius, mass, and luminosity (along with all uncertantities) using Pandas read_html() method, and a custom-made data parser.

### Uncertainty Calculations
All inputs and outputs of ExoPy feature the capability of accepting the uncertanties of measurements.

### Error and Crash Handling
All inputs are filtered to prevent any crashes. Please open an issue ticket if you run into one.

### File saving
Save .svg files of all plots to their own folder based on the star name. Save full reports of calculated data to .csv file.

## Dependencies
```pip install lightkurve```

```pip install scipy```

## How to Use
After installing all dependencies, the program can be run using exopy.bat in the project's root folder. Alternatively, with a CMD window running in the project root, run the command ```python -m exopy.exopy```. 

Alternatively, you can also use the portable executable in releases—no installation of Python or any other modules necessary.




![kermitine](https://github.com/kermitine/kermitine/blob/b523c5954ea8820f70eb6ff786f2dbec7ce08955/images/kermitine.png)
