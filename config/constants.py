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


import scipy.constants

# SCIENTIFIC CONSTANTS
constant_stefan_boltzmann = scipy.constants.Stefan_Boltzmann
constant_gravitational = scipy.constants.gravitational_constant
# CONVERSION CONSTANTS
constant_m_TO_AU = (1/149597870700) # from IAU 2015 Resolution B3
constant_AU_TO_m = 149597870700 # from IAU 2015 Resolution B3
constant_d_TO_s = 86400 # derived from (1day*24hours*60minutes*60seconds)
constant_solarmass_TO_kg = 1988400e24 # from NASA GSFC Sun Fact Sheet
constant_solarluminosity_TO_W = 3.828e26 # from IAU 2015 Resolution B3
constant_solarradii_TO_earthradii = (1/(6371/695700)) # from NASA GSFC Sun Fact Sheet (1earthradii/(6371kmearth/695700kmsun))
constant_solarradii_TO_m = 6.957e8 # from IAU 2015 Resolution B3