from unittest import TestCase, main
import numpy as np
from astropy import units
from src.latab import SerialNumberColumn, EmptyColumn, DataColumn, FloatFormatter, Table


class TestLatab(TestCase):

    def setUp(self) -> None:
        self.array1 = np.array([13.35000606, 0.76642346, 1.42476496, 9.27577478, 3.83978828, 1.88922311, 8.46868664, 3.6269277, 2.86984472, 4.13375383]) # noqa
        self.array2 = np.array([1.8131508, 5.3586463, 5.6288616, 7.4245393, 8.1266426, 4.5811065, 8.7617888, 9.972409, 9.2422739, 4.1967336]) * units.g / units.cm**3 # noqa
        self.array3 = np.array([9.47738782e+20, 9.06469621e+20, 2.50771562e+20, 8.85737743e+20, 7.04538193e+20, 8.90478371e+20, 3.58848823e+18, 6.37444615e+20, 2.72502714e+19, 8.95868100e+20]) * units.kg # noqa
        self.errors = np.array([0.034574, 0.072827, 0.04782, 0.098236, 0.018896, 0.071311, 0.065703, 0.080372, 0.078894, 0.072819]) * units.g / units.cm**3 # noqa

    def test_example1(self):
        col1 = SerialNumberColumn("Planet", 10)
        col2 = DataColumn("Semi-major Axis", self.array1).fixError(0.005, 3).unit("AU")
        col3 = DataColumn("$\\varrho$", self.array2, formatter=FloatFormatter(2, 0)).absoluteError(self.errors)
        col4 = DataColumn("Mass", self.array3).relativeError(0.05)
        col5 = EmptyColumn("Note", 10)

        table = Table([col1, col2, col3, col4, col5], "Nobody expects the Spanish inquisition.")
        lines = table.lines()

        with open("tests/integration/example1.txt") as file:
            expectedLines = [line.rstrip() for line in file]
        length = len(lines)
        self.assertEqual(length, len(expectedLines))
        for i in range(length):
            self.assertEqual(lines[i], expectedLines[i])

    def test_example2(self):
        col1 = SerialNumberColumn("Bolygó", 10)
        col2 = DataColumn("Félnagytengely", self.array1).fixError(0.005, 3).unit("AU")
        col3 = DataColumn("$\\varrho$", self.array2, formatter=FloatFormatter(2, 0)).absoluteError(self.errors)
        col4 = DataColumn("Tömeg", self.array3).relativeError(0.05)
        col5 = EmptyColumn("Megjegyzés", 10)

        table = Table([col1, col2, col3, col4, col5], "Aprócska kalapocska, benne csacska macska mocska.")
        lines = table.lines(separator=',')

        with open("tests/integration/example2.txt") as file:
            expectedLines = [line.rstrip() for line in file]
        length = len(lines)
        self.assertEqual(length, len(expectedLines))
        for i in range(length):
            self.assertEqual(lines[i], expectedLines[i])

    def test_example3(self):
        lines = Table.fromDictionary({
            "Semi-major Axis [AU]": self.array1,
            "$\\varrho$": self.array2,
            "Mass": self.array3,
        }, "Tis but a scratch!").lines()

        with open("tests/integration/example3.txt") as file:
            expectedLines = [line.rstrip() for line in file]
        length = len(lines)
        self.assertEqual(length, len(expectedLines))
        for i in range(length):
            self.assertEqual(lines[i], expectedLines[i])


if __name__ == '__main__':
    main()
