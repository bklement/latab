from unittest import TestCase, main
from src.latab.converter import convertUnitToLateX
from astropy import units


class TestColumn(TestCase):

    def test_simpleUnit(self):
        self.assertEqual(convertUnitToLateX(units.kg), "$\mathrm{kg}$")

    def test_compositeUnit(self):
        self.assertEqual(convertUnitToLateX(units.kg * units.m**2 / units.s**2 * units.C**0),
                         "$\mathrm{m^{2}\cdot kg/s^{2}}$")


if __name__ == '__main__':
    main()
