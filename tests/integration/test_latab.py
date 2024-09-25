from unittest import TestCase, main
import numpy as np
from astropy import units
from src.latab import FloatFormatter, IntFormatter, Table, FixError, RelativeError, AbsoluteError


class TestLatab(TestCase):

    def setUp(self) -> None:
        self.array1 = np.array([13.35000606, 0.76642346, 1.42476496, 9.27577478, 3.83978828, 1.88922311])
        self.array2 = np.array([1.8131508, 5.3586463, 5.6288616, 7.4245393, 8.1266426, 4.5811065]) * units.g / units.cm**3
        self.array3 = np.array([9.47738782e+20, 9.06469621e+20, 2.50771562e+20, 8.85737743e+20,
                                7.04538193e+20, 8.90478371e+20]) * units.kg
        self.array4 = np.arange(0.4, 2.1, 0.1)
        self.array5 = np.array([278, 156, 135, 82, 59, 49, 62, 80, 31, 17, 16, 17, 16, 15, 16, 12, 10])
        self.array6 = np.array([257, 130, 120, 89, 59, 46, 73, 85, 29, 29, 20, 7, 14, 11, 6, 16, 9])
        self.array7 = np.array([0, 0, 0, 0, 0, 0, 6, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.errors = np.array([0.034574, 0.072827, 0.04782, 0.098236, 0.018896, 0.071311]) * units.g / units.cm**3
        self.planets = ["Kepler137b", "Kepler137c", "Kepler137d", "Kepler137e", "Kepler137f", "Kepler137g"]

    def test_example1(self):
        lines = (Table("Nobody expects the Spanish inquisition.")
                 .textColumn("Planet", self.planets)
                 .dataColumn("Semi-major Axis [AU]", self.array1, FixError(0.0005))
                 .dataColumn("$\\varrho$", self.array2, AbsoluteError(self.errors), FloatFormatter(2, 2))
                 .dataColumn("Mass", self.array3, RelativeError(0.05))).lines()

        with open("tests/integration/example1.txt") as file:
            expectedLines = [line.rstrip() for line in file]
        length = len(lines)
        self.assertEqual(length, len(expectedLines))
        for i in range(length):
            self.assertEqual(lines[i], expectedLines[i])

    def test_example2(self):
        lines = (Table("Aprócska kalapocska, benne csacska macska mocska.")
                 .serialColumn("Bolygó", 6)
                 .dataColumn("Félnagytengely [AU]", self.array1, FixError(0.0005))
                 .dataColumn("$\\varrho$", self.array2, AbsoluteError(self.errors), FloatFormatter(2, 2))
                 .dataColumn("Tömeg", self.array3, RelativeError(0.05))).lines(separator=',')

        with open("tests/integration/example2.txt") as file:
            expectedLines = [line.rstrip() for line in file]
        length = len(lines)
        self.assertEqual(length, len(expectedLines))
        for i in range(length):
            self.assertEqual(lines[i], expectedLines[i])

    def test_example3(self):
        lines = (Table("Fotometriai spektrum")
                 .dataColumn("Feszültség [V]", self.array4, formatter=FloatFormatter(1))
                 .dataColumn("1. Detektor [db]", self.array5, formatter=IntFormatter())
                 .dataColumn("2. Detektor [db]", self.array6, formatter=IntFormatter())
                 .dataColumn("Koincidencia [db]", self.array7, formatter=IntFormatter())).lines()
        with open("tests/integration/example3.txt") as file:
            expectedLines = [line.rstrip() for line in file]
        length = len(lines)
        self.assertEqual(length, len(expectedLines))
        for i in range(length):
            self.assertEqual(lines[i], expectedLines[i])


if __name__ == '__main__':
    main()
