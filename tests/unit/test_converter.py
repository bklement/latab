from unittest import TestCase, main
from src.latab.converter import convertUnitToLateX
from astropy import units


class TestColumn(TestCase):

    def test_simpleUnit(self):
        self.assertEqual(convertUnitToLateX(units.kg), "$\mathrm{kg}$")

    def test_WithZeroPowerUnit(self):
        self.assertEqual(convertUnitToLateX(units.kg * units.m**2 / units.s**2 * units.C**0),
                         "$\mathrm{m^{2}\cdot kg/s^{2}}$")

    def test_negativePowerUnit(self):
        self.assertEqual(convertUnitToLateX(units.C**-1), "$\mathrm{1/C}$")

    def test_multipleNegativePowerUnit(self):
        self.assertEqual(convertUnitToLateX(units.C**-1 / units.s**3), "$\mathrm{1/(C\cdot s^{3})}$")

    def test_MultiplePositivePowerUnit(self):
        self.assertEqual(convertUnitToLateX(units.kg * units.m**2), "$\mathrm{m^{2}\cdot kg}$")

    def test_ComplexUnit(self):
        self.assertEqual(convertUnitToLateX(units.kg * units.m**2 * units.cd**4 * units.watt**9 * units.s**-3 * units.C**-1),
                         "$\mathrm{W^{9}\cdot cd^{4}\cdot m^{2}\cdot kg/(C\cdot s^{3})}$")


if __name__ == '__main__':
    main()
