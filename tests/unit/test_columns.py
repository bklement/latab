from unittest import TestCase, main
from unittest.mock import MagicMock
import numpy as np
from astropy import units
from src.latab import SerialNumberColumn, TextColumn, EmptyColumn, DataColumn, FloatFormatter, ExponentialFormatter
from src.latab.formatters import Formatter

HEADER = "header"
HEADER_WITH_UNIT = "header [AU]"
TEXTS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
LINES = 10
UNIT = "AU"
WRONG_DATA_TYPE_MESSAGE = "Data must be of type numpy.ndarray or astropy.units.Quantity"
WRONG_FORMATTER_MESSAGE = "The argument 'formatter' must be a subclass of latab.Formatter"
WRONG_UNIT_TYPE_MESSAGE = "Unit must be of type str or a subclass of astropy.units.core.UnitBase"
WRONG_FIX_ERROR_TYPE_MESSAGE = "Fix error must be of type float or astropy.units.Quantity"
WRONG_RELATIVE_ERROR_TYPE_MESSAGE = "Relative error must be of type float"
WRONG_ABSOLUTE_ERROR_TYPE_MESSAGE = "Absolute error must be of type numpy.ndarray or astropy.units.Quantity"
DATA = np.random.rand(LINES) * 100
FIX_ERROR = 0.05
RELATIVE_ERROR = 0.025
ABSOLUTE_ERROR = np.random.rand(LINES)


class TestSerialNumberColumn(TestCase):

    def setUp(self):
        self.underTest = SerialNumberColumn(HEADER, LINES)

    def test_shouldReturnCorrectHeader(self):
        self.assertEqual(self.underTest.getHeader(), HEADER)

    def test_shouldReturnCorrectLength(self):
        self.assertEqual(len(self.underTest), LINES)

    def test_shouldReturnCorrectCell(self):
        self.assertEqual(self.underTest.getCell(0), "1.")
        self.assertEqual(self.underTest.getCell(6), "7.")

    def test_shouldRaiseExceptionForIndexOutOfBounds(self):
        with self.assertRaises(IndexError):
            self.underTest.getCell(LINES)


class TestTextColumn(TestCase):

    def setUp(self):
        self.underTest = TextColumn(HEADER, TEXTS)

    def test_shouldReturnCorrectHeader(self):
        self.assertEqual(self.underTest.getHeader(), HEADER)

    def test_shouldReturnCorrectLength(self):
        self.assertEqual(len(self.underTest), LINES)

    def test_shouldReturnCorrectCell(self):
        self.assertEqual(self.underTest.getCell(0), "A")
        self.assertEqual(self.underTest.getCell(6), "G")

    def test_shouldRaiseExceptionForIndexOutOfBounds(self):
        with self.assertRaises(IndexError):
            self.underTest.getCell(LINES)


class TestEmptyColumn(TestCase):

    def setUp(self):
        self.underTest = EmptyColumn(HEADER, LINES)

    def test_shouldReturnCorrectHeader(self):
        self.assertEqual(self.underTest.getHeader(), HEADER)

    def test_shouldReturnCorrectLength(self):
        self.assertEqual(len(self.underTest), LINES)

    def test_shouldReturnCorrectCell(self):
        for i in range(LINES):
            self.assertEqual(self.underTest.getCell(i), "")

    def test_shouldRaiseExceptionForIndexOutOfBounds(self):
        with self.assertRaises(IndexError):
            self.underTest.getCell(LINES)


class TestDataColumn(TestCase):

    def test_shouldReturnCorrectHeaderForInlineFalse(self):
        underTest = DataColumn(HEADER, DATA).unit(UNIT)
        self.assertEqual(underTest.getHeader(), HEADER_WITH_UNIT)

    def test_shouldReturnCorrectHeaderForInlineTrue(self):
        underTest = DataColumn(HEADER, DATA, inlineUnit=True).unit(UNIT)
        self.assertEqual(underTest.getHeader(), HEADER)

    def test_shouldReturnCorrectHeaderForNoUnit(self):
        underTest = DataColumn(HEADER, DATA, inlineUnit=True)
        self.assertEqual(underTest.getHeader(), HEADER)

    def test_shouldReturnCorrectLength(self):
        underTest = DataColumn(HEADER, DATA)
        self.assertEqual(len(underTest), LINES)

    def test_shouldRaiseExceptionForWrongFormatter(self):
        with self.assertRaisesRegex(Exception, WRONG_FORMATTER_MESSAGE):
            DataColumn(HEADER, DATA, formatter=HEADER)

    def test_shouldHaveDefaultFloatFormatter(self):
        formatter = DataColumn(HEADER, DATA)._DataColumn__formatter
        self.assertTrue(isinstance(formatter, FloatFormatter))
        self.assertEqual(formatter._precision, 3)
        self.assertEqual(formatter._additionalErrorPrecision, 1)

    def test_shouldHaveDefaultExponentialFormatter(self):
        formatter = DataColumn(HEADER, DATA * 1000)._DataColumn__formatter
        self.assertTrue(isinstance(formatter, ExponentialFormatter))
        self.assertEqual(formatter._precision, 3)
        self.assertEqual(formatter._additionalErrorPrecision, 1)

    def test_shouldNotSetUnitWhenDataIsNumpyArray(self):
        underTest = DataColumn(HEADER, DATA)
        self.assertIsNone(underTest._DataColumn__unit)
        self.assertTrue(np.array_equal(underTest._DataColumn__data, DATA))

    def test_shouldSetUnitWhenDataIsQuantity(self):
        underTest = DataColumn(HEADER, DATA * units.K)
        self.assertEqual(underTest._DataColumn__unit, "$\mathrm{K}$")
        self.assertTrue(np.array_equal(underTest._DataColumn__data, DATA))

    def test_shouldSetUnitFromString(self):
        underTest = DataColumn(HEADER, DATA).unit(UNIT)
        self.assertEqual(underTest._DataColumn__unit, UNIT)

    def test_shouldSetUnitFromUnit(self):
        underTest = DataColumn(HEADER, DATA).unit(units.kg * units.m / units.s**2)
        self.assertEqual(underTest._DataColumn__unit, "$\\mathrm{kg\\cdot m/s^{2}}$")

    def test_shouldUnitRaiseExceptionForWrongArgumentType(self):
        with self.assertRaisesRegex(Exception, WRONG_UNIT_TYPE_MESSAGE):
            DataColumn(HEADER, DATA).unit(137)

    def test_shouldSetDataAndUnitFromQuantity(self):
        underTest = DataColumn(HEADER, DATA * units.C)
        self.assertEqual(underTest._DataColumn__unit, "$\\mathrm{C}$")
        self.assertTrue(np.array_equal(underTest._DataColumn__data, DATA))

    def test_shouldDataRaiseExceptionForWrongArgument(self):
        with self.assertRaisesRegex(Exception, WRONG_DATA_TYPE_MESSAGE):
            DataColumn(HEADER, HEADER)

    def test_shouldUnitRaiseExceptionForCallingWhenAlreadySet(self):
        with self.assertRaises(Exception):
            DataColumn(HEADER, DATA * units.kg).unit(units.g)

    def test_shouldFixErrorSetCorrectErrorAndCallAdjustAdditionalErrorPrecisionOnFormatterForFloat(self):
        underTest = DataColumn(HEADER, DATA)
        underTest._DataColumn__formatter.adjustAdditionalErrorPrecision = MagicMock()
        underTest.fixError(FIX_ERROR, 2)
        underTest._DataColumn__formatter.adjustAdditionalErrorPrecision.assert_called_once_with(2)
        self.assertTrue(np.array_equal(underTest._DataColumn__errors, np.ones(LINES) * FIX_ERROR))

    def test_shouldFixErrorSetCorrectErrorAndCallAdjustAdditionalErrorPrecisionOnFormatterForQuantity(self):
        underTest = DataColumn(HEADER, DATA)
        underTest._DataColumn__formatter.adjustAdditionalErrorPrecision = MagicMock()
        underTest.fixError(FIX_ERROR * units.kg, 2)
        underTest._DataColumn__formatter.adjustAdditionalErrorPrecision.assert_called_once_with(2)
        self.assertTrue(np.array_equal(underTest._DataColumn__errors, np.ones(LINES) * FIX_ERROR))

    def test_shouldFixErrorRaiseExceptionForWrongArgumentType(self):
        with self.assertRaisesRegex(Exception, WRONG_FIX_ERROR_TYPE_MESSAGE):
            DataColumn(HEADER, DATA).fixError(HEADER, 2)

    def test_shouldAbsoluteErrorSetCorrectErrorForFloat(self):
        underTest = DataColumn(HEADER, DATA).absoluteError(ABSOLUTE_ERROR)
        self.assertTrue(np.array_equal(underTest._DataColumn__errors, ABSOLUTE_ERROR))

    def test_shouldAbsoluteErrorSetCorrectErrorForQuantity(self):
        underTest = DataColumn(HEADER, DATA).absoluteError(ABSOLUTE_ERROR * units.kg)
        self.assertTrue(np.array_equal(underTest._DataColumn__errors, ABSOLUTE_ERROR))

    def test_shouldAbsoluteErrorRaiseExceptionForWrongArgumentType(self):
        with self.assertRaisesRegex(Exception, WRONG_ABSOLUTE_ERROR_TYPE_MESSAGE):
            DataColumn(HEADER, DATA).absoluteError(HEADER)

    def test_shouldRelativeErrorSetCorrectError(self):
        underTest = DataColumn(HEADER, DATA).relativeError(RELATIVE_ERROR)
        self.assertTrue(np.array_equal(underTest._DataColumn__errors, DATA * RELATIVE_ERROR))

    def test_shouldRelativeErrorRaiseExceptionForWrongArgumentType(self):
        with self.assertRaisesRegex(Exception, WRONG_RELATIVE_ERROR_TYPE_MESSAGE):
            DataColumn(HEADER, DATA).relativeError(HEADER)

    def __mockFormatter(self):
        mock = MagicMock(spec=Formatter)
        mock.format.return_value = "X "
        mock.formatWithError.return_value = "Y "
        return mock

    def test_shouldGetCellReturnCorrectCellForInlineFalse(self):
        underTest = DataColumn(HEADER, DATA, formatter=self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "X ")

    def test_shouldGetCellReturnCorrectCellForInlineFalseWithError(self):
        underTest = DataColumn(HEADER, DATA, formatter=self.__mockFormatter()).fixError(0.5, 1)
        self.assertEqual(underTest.getCell(3), "Y ")

    def test_shouldGetCellReturnCorrectCellForInlineFalseWithUnit(self):
        underTest = DataColumn(HEADER, DATA * units.kg, formatter=self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "X ")

    def test_shouldGetCellReturnCorrectCellForInlineFalseWithErrorWithUnit(self):
        underTest = DataColumn(HEADER, DATA * units.kg, formatter=self.__mockFormatter()).fixError(0.5, 1)
        self.assertEqual(underTest.getCell(3), "Y ")

    def test_shouldGetCellReturnCorrectCellForInlineTrue(self):
        underTest = DataColumn(HEADER, DATA, inlineUnit=True, formatter=self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "X ")

    def test_shouldGetCellReturnCorrectCellForInlineTrueWithError(self):
        underTest = DataColumn(HEADER, DATA, inlineUnit=True, formatter=self.__mockFormatter()).fixError(0.5, 1)
        self.assertEqual(underTest.getCell(3), "Y ")

    def test_shouldGetCellReturnCorrectCellForInlineTrueWithUnit(self):
        underTest = DataColumn(HEADER, DATA * units.kg, inlineUnit=True, formatter=self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "X $\mathrm{kg}$")

    def test_shouldGetCellReturnCorrectCellForInlineTrueWithErrorWithUnit(self):
        underTest = DataColumn(HEADER, DATA * units.kg, inlineUnit=True, formatter=self.__mockFormatter()).fixError(0.5, 1)
        self.assertEqual(underTest.getCell(3), "Y $\mathrm{kg}$")

    def test_shouldRaiseExceptionForIndexOutOfBounds(self):
        with self.assertRaises(IndexError):
            DataColumn(HEADER, np.random.rand(LINES)).getCell(LINES)


if __name__ == '__main__':
    main()
