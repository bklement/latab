# LaTab

Utility to help convert numpy arrays to a LateX table. The main goal is to provide a code snippet with proper number and unit formatting, with a basic table layout. Formatting of the table itself is expected to be done manually by the user in the LateX document, but simpler features might be added in later versions if the need arises.

## Examples

### Imports and sample data

```
import numpy as np
from astropy import units
from latab import DataColumn, Table, SerialNumberColumn, EmptyColumn, FloatFormatter

array1 = np.array([13.35000606, 0.76642346, 1.42476496, 9.27577478, 3.83978828,
                   1.88922311, 8.46868664, 3.6269277, 2.86984472, 4.13375383])
array2 = np.array([1.8131508, 5.3586463, 5.6288616, 7.4245393, 8.1266426, 4.5811065,
                   8.7617888, 9.972409, 9.2422739, 4.1967336]) * units.g / units.cm**3
array3 = np.array([9.47738782e+20, 9.06469621e+20, 2.50771562e+20, 8.85737743e+20, 7.04538193e+20,
                   8.90478371e+20, 3.58848823e+18, 6.37444615e+20, 2.72502714e+19, 8.95868100e+20]) * units.kg
errors = np.array([0.034574, 0.072827, 0.04782, 0.098236, 0.018896, 0.071311, 0.065703, 0.080372,
                   0.078894, 0.072819]) * units.g / units.cm**3
```

### Example using explicit definition

```
col1 = SerialNumberColumn("Planet", 10)
col2 = DataColumn("Semi-major Axis", array1).fixError(0.005, 3).unit("AU")
col3 = DataColumn("$\\varrho$", array2, formatter=FloatFormatter(2, 0)).absoluteError(errors)
col4 = DataColumn("Mass", array3).relativeError(0.05)
col5 = EmptyColumn("Note", 10)

table = Table([col1, col2, col3, col4, col5], "Nobody expects the Spanish inquisition.")
table.print()
```

```
\begin{table}
    \centering
    \begin{tabular}{|c|c|c|c|c|} \hline
        Planet & Semi-major Axis [AU] & $\varrho$ [$\mathrm{g/cm^{3}}$] & Mass [$\mathrm{kg}$] & Note \\ \hline
        1. & $13.350 \pm 0.005$  & $1.81 \pm 0.03$  & $(9.477 \pm 0.4739)\cdot 10^{20}$  &  \\ \hline
        2. & $0.766 \pm 0.005$  & $5.36 \pm 0.07$  & $(9.065 \pm 0.4532)\cdot 10^{20}$  &  \\ \hline
        3. & $1.425 \pm 0.005$  & $5.63 \pm 0.05$  & $(2.508 \pm 0.1254)\cdot 10^{20}$  &  \\ \hline
        4. & $9.276 \pm 0.005$  & $7.42 \pm 0.10$  & $(8.857 \pm 0.4429)\cdot 10^{20}$  &  \\ \hline
        5. & $3.840 \pm 0.005$  & $8.13 \pm 0.02$  & $(7.045 \pm 0.3523)\cdot 10^{20}$  &  \\ \hline
        6. & $1.889 \pm 0.005$  & $4.58 \pm 0.07$  & $(8.905 \pm 0.4452)\cdot 10^{20}$  &  \\ \hline
        7. & $8.469 \pm 0.005$  & $8.76 \pm 0.07$  & $(3.588 \pm 0.1794)\cdot 10^{18}$  &  \\ \hline
        8. & $3.627 \pm 0.005$  & $9.97 \pm 0.08$  & $(6.374 \pm 0.3187)\cdot 10^{20}$  &  \\ \hline
        9. & $2.870 \pm 0.005$  & $9.24 \pm 0.08$  & $(2.725 \pm 0.1363)\cdot 10^{19}$  &  \\ \hline
        10. & $4.134 \pm 0.005$  & $4.20 \pm 0.07$  & $(8.959 \pm 0.4479)\cdot 10^{20}$  &  \\ \hline
    \end{tabular}
    \caption{Nobody expects the Spanish inquisition.}
\end{table}
```

![Example 1](https://astro.bklement.com/latab/img1.png)

### Localized example with different decimal separator

```
col1 = SerialNumberColumn("Bolygó", 10)
col2 = DataColumn("Félnagytengely", array1).fixError(0.005, 3).unit("AU")
col3 = DataColumn("$\\varrho$", array2, formatter=FloatFormatter(2, 0)).absoluteError(errors)
col4 = DataColumn("Tömeg", array3).relativeError(0.05)
col5 = EmptyColumn("Megjegyzés", 10)

table = Table([col1, col2, col3, col4, col5], "Aprócska kalapocska, benne csacska macska mocska.")
table.print(separator=',')
```

```
\begin{table}
    \centering
    \begin{tabular}{|c|c|c|c|c|} \hline
        Bolygó & Félnagytengely [AU] & $\varrho$ [$\mathrm{g/cm^{3}}$] & Tömeg [$\mathrm{kg}$] & Megjegyzés \\ \hline
        1. & $13,350 \pm 0,005$  & $1,81 \pm 0,03$  & $(9,477 \pm 0,4739)\cdot 10^{20}$  &  \\ \hline
        2. & $0,766 \pm 0,005$  & $5,36 \pm 0,07$  & $(9,065 \pm 0,4532)\cdot 10^{20}$  &  \\ \hline
        3. & $1,425 \pm 0,005$  & $5,63 \pm 0,05$  & $(2,508 \pm 0,1254)\cdot 10^{20}$  &  \\ \hline
        4. & $9,276 \pm 0,005$  & $7,42 \pm 0,10$  & $(8,857 \pm 0,4429)\cdot 10^{20}$  &  \\ \hline
        5. & $3,840 \pm 0,005$  & $8,13 \pm 0,02$  & $(7,045 \pm 0,3523)\cdot 10^{20}$  &  \\ \hline
        6. & $1,889 \pm 0,005$  & $4,58 \pm 0,07$  & $(8,905 \pm 0,4452)\cdot 10^{20}$  &  \\ \hline
        7. & $8,469 \pm 0,005$  & $8,76 \pm 0,07$  & $(3,588 \pm 0,1794)\cdot 10^{18}$  &  \\ \hline
        8. & $3,627 \pm 0,005$  & $9,97 \pm 0,08$  & $(6,374 \pm 0,3187)\cdot 10^{20}$  &  \\ \hline
        9. & $2,870 \pm 0,005$  & $9,24 \pm 0,08$  & $(2,725 \pm 0,1363)\cdot 10^{19}$  &  \\ \hline
        10. & $4,134 \pm 0,005$  & $4,20 \pm 0,07$  & $(8,959 \pm 0,4479)\cdot 10^{20}$  &  \\ \hline
    \end{tabular}
    \caption{Aprócska kalapocska, benne csacska macska mocska.}
\end{table}
```

![Example 2](https://astro.bklement.com/latab/img2.png)

### Example using the simple dictionary interface

There is a simple interface to create a table, but you are limited to the default Formatter with precision 3 and without errors:

```
Table.fromDictionary({
    "Semi-major Axis [AU]": array1,
    "$\\varrho$": array2,
    "Mass": array3,
}, "Tis but a scratch!").print()
```

```
\begin{table}
    \centering
    \begin{tabular}{|c|c|c|} \hline
        Semi-major Axis [AU] & $\varrho$ [$\mathrm{g/cm^{3}}$] & Mass [$\mathrm{kg}$] \\ \hline
        13.350  & 1.813  & $9.477 \cdot 10^{20}$  \\ \hline
        0.766  & 5.359  & $9.065 \cdot 10^{20}$  \\ \hline
        1.425  & 5.629  & $2.508 \cdot 10^{20}$  \\ \hline
        9.276  & 7.425  & $8.857 \cdot 10^{20}$  \\ \hline
        3.840  & 8.127  & $7.045 \cdot 10^{20}$  \\ \hline
        1.889  & 4.581  & $8.905 \cdot 10^{20}$  \\ \hline
        8.469  & 8.762  & $3.588 \cdot 10^{18}$  \\ \hline
        3.627  & 9.972  & $6.374 \cdot 10^{20}$  \\ \hline
        2.870  & 9.242  & $2.725 \cdot 10^{19}$  \\ \hline
        4.134  & 4.197  & $8.959 \cdot 10^{20}$  \\ \hline
    \end{tabular}
    \caption{Tis but a scratch!}
\end{table}
```

![Example 3](https://astro.bklement.com/latab/img3.png)
