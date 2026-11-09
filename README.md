# ExoPy ![kermitine](https://github.com/kermitine/ExoPy/blob/c14b9972f6f1cc0cb4f2787cab131642d0e844d8/data/icon.ico)

A Python3 console-based exoplanet detection tool.

## Motivation
ExoPy started from a simple frustration. Lightkurve is a powerful library for working with Kepler, K2, and TESS data, but using it for a full transit analysis takes a lot of time and setup. Even routine tasks, like downloading a light curve, flattening it, finding the orbital period, and phase-folding the transit, require writing and running code step by step, usually in a Jupyter notebook. For students and newcomers, that workflow can feel clunky and slow.

We built ExoPy to make that process faster and easier. ExoPy wraps the entire exoplanet detection workflow in a simple, guided console interface, so there’s no notebook and no boilerplate code. It automates light-curve analysis, phase folding, and the key calculations that follow, from planet radius and orbital distance to habitable-zone estimates and equilibrium temperature, all with full uncertainty propagation. The goal is to let anyone go from a star’s name to annotated plots and a complete data report in minutes.

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
Save plots to their own folder based on the star name, in a file format of your choosing. Save full reports of calculated data to .csv file.

## Dependencies
run ```pip install -r requirements.txt``` in project root
## How to Use
After installing all dependencies, the program can be run using launch.bat in the project's root folder. You can also open a CMD window running in the project root, and run the command ```python -m exopy.exopy```. 
Alternatively, you can also use the portable executable in releases—no installation of Python or any other modules necessary.

## Contributors
 - Ayrik Nabirahni (@kermitine)
 - Hana Nabirahni (@hananabirahni-boop)

## License
This repository/project is licensed under the GNU Affero General Public v3.0-or-later. For more information, please consult the LICENSE file (located in the root of the project), or visit https://www.gnu.org/licenses/agpl-3.0.en.html to read the full license.


![kermitine](https://github.com/kermitine/kermitine/blob/b523c5954ea8820f70eb6ff786f2dbec7ce08955/images/kermitine.png)
