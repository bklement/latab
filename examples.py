import numpy as np
from astropy import units
from src.latab import Table, FloatFormatter, FixError, AbsoluteError, RelativeError


array1 = np.array([13.35000606, 0.76642346, 1.42476496, 9.27577478, 3.83978828, 1.88922311])
array2 = np.array([1.8131508, 5.3586463, 5.6288616, 7.4245393, 8.1266426, 4.5811065]) * units.g / units.cm**3
array3 = np.array([9.47738782e+20, 9.06469621e+20, 2.50771562e+20, 8.85737743e+20, 7.04538193e+20,
                   8.90478371e+20]) * units.kg
errors = np.array([0.034574, 0.072827, 0.04782, 0.098236, 0.018896, 0.071311]) * units.g / units.cm**3
planets = ["Kepler137b", "Kepler137c", "Kepler137d", "Kepler137e", "Kepler137f", "Kepler137g"]


(Table("Nobody expects the Spanish inquisition.")
 .serialColumn("Planet", 6)
 .dataColumn("Semi-major Axis [AU]", array1, FixError(0.005), FloatFormatter(3, 3))
 .dataColumn("$\\varrho$", array2, AbsoluteError(errors), FloatFormatter(2, 2))
 .dataColumn("Mass", array3, RelativeError(0.05))).print()


(Table("Aprócska kalapocska, benne csacska macska mocska.")
 .textColumn("Bolygó", planets)
 .dataColumn("Félnagytengely [AU]", array1, FixError(0.005), FloatFormatter(3, 3))
 .dataColumn("$\\varrho$", array2, AbsoluteError(errors), FloatFormatter(2, 2))
 .dataColumn("Tömeg", array3, RelativeError(0.05))).print(separator=',')
