from unittest import TestCase, main
from src.latab import FloatFormatter, ExponentialFormatter
from src.latab.formatters import Formatter

ABSTRACT_CLASS_ERROR_MESSAGE = "^Can't instantiate abstract class Formatter with abstract method format$"


class TestFloatFormatter(TestCase):

    def test_FormatterIsAbstract(self):
        with self.assertRaisesRegex(TypeError, ABSTRACT_CLASS_ERROR_MESSAGE):
            Formatter()

    def test_format(self):
        underTest = FloatFormatter()
        self.assertEqual(underTest.format(1.0046), "1.005 ")
        self.assertEqual(underTest.format(1.0045), "1.004 ")

        underTest = FloatFormatter(precision=2)
        self.assertEqual(underTest.format(1.046), "1.05 ")
        self.assertEqual(underTest.format(1.045), "1.04 ")

        underTest = FloatFormatter(precision=5)
        self.assertEqual(underTest.format(1.046), "1.04600 ")
        self.assertEqual(underTest.format(1.045), "1.04500 ")

    def test_formatWithError(self):
        underTest = FloatFormatter()
        self.assertEqual(underTest.format(1.0046, 0.0005), "$1.005 \pm 0.0005$ ")
        self.assertEqual(underTest.format(1.0045, 0.00000423), "$1.004 \pm 0.0000$ ")

        underTest = FloatFormatter(precision=2)
        self.assertEqual(underTest.format(1.046, 0.0005), "$1.05 \pm 0.001$ ")
        self.assertEqual(underTest.format(1.045, 0.00000423), "$1.04 \pm 0.000$ ")

        underTest = FloatFormatter(additionalErrorPrecision=2)
        self.assertEqual(underTest.format(1.046, 0.0005), "$1.046 \\pm 0.00050$ ")
        self.assertEqual(underTest.format(1.045, 0.00000423), "$1.045 \\pm 0.00000$ ")

        underTest = FloatFormatter(precision=4, additionalErrorPrecision=-1)
        self.assertEqual(underTest.format(1.046, 0.0005), "$1.0460 \\pm 0.001$ ")
        self.assertEqual(underTest.format(1.045, 0.00000423), "$1.0450 \\pm 0.000$ ")

        underTest = FloatFormatter(precision=4, additionalErrorPrecision=-1)
        underTest.adjustAdditionalErrorPrecision(desiredErrorPrecision=2)
        self.assertEqual(underTest.format(1.046, 0.0005), "$1.0460 \\pm 0.00$ ")
        self.assertEqual(underTest.format(1.045, 0.00000423), "$1.0450 \\pm 0.00$ ")


class TestExponentialFormatter(TestCase):

    def test_format(self):
        underTest = ExponentialFormatter()
        self.assertEqual(underTest.format(1.0054), "$1.005 \\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21), "$2.000 \\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32), "$1.743 \\cdot 10^{32}$ ")
        underTest = ExponentialFormatter(precision=2)
        self.assertEqual(underTest.format(1.0054), "$1.01 \\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21), "$2.00 \\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32), "$1.74 \\cdot 10^{32}$ ")

    def test_formatWithError(self):
        underTest = ExponentialFormatter()
        self.assertEqual(underTest.format(1.0054, 0.065311), "$(1.005 \\pm 0.0653)\\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21, 5e-24), "$(2.000 \\pm 0.0005)\\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+30), "$(1.743 \\pm 0.0520)\\cdot 10^{32}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+17), "$(1.743 \\pm 0.0000)\\cdot 10^{32}$ ")

        underTest = ExponentialFormatter(precision=2)
        self.assertEqual(underTest.format(1.0054, 0.065311), "$(1.01 \\pm 0.065)\\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21, 5e-24), "$(2.00 \\pm 0.001)\\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+30), "$(1.74 \\pm 0.052)\\cdot 10^{32}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+17), "$(1.74 \\pm 0.000)\\cdot 10^{32}$ ")

        underTest = ExponentialFormatter(additionalErrorPrecision=2)
        self.assertEqual(underTest.format(1.0054, 0.065311), "$(1.005 \\pm 0.06531)\\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21, 5e-24), "$(2.000 \\pm 0.00050)\\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+30), "$(1.743 \\pm 0.05200)\\cdot 10^{32}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+17), "$(1.743 \\pm 0.00000)\\cdot 10^{32}$ ")

        underTest = ExponentialFormatter(precision=4, additionalErrorPrecision=2)
        self.assertEqual(underTest.format(1.0054, 0.065311), "$(1.0054 \\pm 0.065311)\\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21, 5e-24), "$(2.0000 \\pm 0.000500)\\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+30), "$(1.7432 \\pm 0.052000)\\cdot 10^{32}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+17), "$(1.7432 \\pm 0.000000)\\cdot 10^{32}$ ")

        underTest = ExponentialFormatter(precision=4, additionalErrorPrecision=2)
        underTest.adjustAdditionalErrorPrecision(desiredErrorPrecision=3)
        self.assertEqual(underTest.format(1.0054, 0.065311), "$(1.0054 \\pm 0.065)\\cdot 10^{0}$ ")
        self.assertEqual(underTest.format(20e-21, 5e-24), "$(2.0000 \\pm 0.001)\\cdot 10^{-20}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+30), "$(1.7432 \\pm 0.052)\\cdot 10^{32}$ ")
        self.assertEqual(underTest.format(1.74321e+32, 5.2e+17), "$(1.7432 \\pm 0.000)\\cdot 10^{32}$ ")


if __name__ == '__main__':
    main()
