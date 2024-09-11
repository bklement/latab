from unittest import TestCase, main
from unittest.mock import MagicMock
import numpy as np
from astropy import units
from src.latab import SerialNumberColumn, TextColumn, DataColumn, FloatFormatter, ExponentialFormatter
from src.latab.formatters import Formatter
from src.latab.columns import Column
from src.latab.errors import Error, FixError

HEADER = "header"
HEADER_WITH_UNIT = "header [$\mathrm{AU}$]"
TEXTS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
LINES = 10
WRONG_DATA_TYPE_MESSAGE = "^Data must be of type numpy.ndarray or astropy.units.Quantity$"
WRONG_ERROR_TYPE_MESSAGE = "^Error must be of type latab.Error$"
WRONG_FORMATTER_MESSAGE = "^The argument 'formatter' must be a subclass of latab.Formatter$"
DATA = np.random.rand(LINES) * 100
ERRORS = DATA * 0.05


class TestColumn(TestCase):

    def test_ColumnIsAbstract(self):
        with self.assertRaises(TypeError):
            Column()


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


class TestDataColumn(TestCase):

    def test_shouldReturnCorrectHeaderForQuantity(self):
        underTest = DataColumn(HEADER, DATA * units.astrophys.AU)
        self.assertEqual(underTest.getHeader(), HEADER_WITH_UNIT)

    def test_shouldReturnCorrectHeaderForNDArray(self):
        underTest = DataColumn(HEADER, DATA)
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
        self.assertEqual(formatter._errorPrecision, 4)

    def test_shouldHaveDefaultExponentialFormatter(self):
        formatter = DataColumn(HEADER, DATA * 1000)._DataColumn__formatter
        self.assertTrue(isinstance(formatter, ExponentialFormatter))
        self.assertEqual(formatter._precision, 3)
        self.assertEqual(formatter._errorPrecision, 4)

    def test_shouldNotSetUnitWhenDataIsNumpyArray(self):
        underTest = DataColumn(HEADER, DATA)
        self.assertTrue(np.array_equal(underTest._DataColumn__data, DATA))

    def test_shouldSetUnitWhenDataIsQuantity(self):
        underTest = DataColumn(HEADER, DATA * units.AU)
        self.assertTrue(np.array_equal(underTest._DataColumn__data, DATA))

    def test_shouldSetDataFromQuantity(self):
        underTest = DataColumn(HEADER, DATA * units.AU)
        self.assertTrue(np.array_equal(underTest._DataColumn__data, DATA))

    def test_shouldDataRaiseExceptionForWrongArgument(self):
        with self.assertRaisesRegex(Exception, WRONG_DATA_TYPE_MESSAGE):
            DataColumn(HEADER, HEADER)

    def test_shouldErrorRaiseExceptionForWrongArgument(self):
        with self.assertRaisesRegex(Exception, WRONG_ERROR_TYPE_MESSAGE):
            DataColumn(HEADER, DATA, HEADER)

    def __mockError(self):
        def sideEffect(*args):
            return ERRORS
        mock = MagicMock(spec=Error)
        mock.getErrors.side_effect = sideEffect
        return mock

    def test_shouldCallErrorGetErrors(self):
        error = self.__mockError()
        DataColumn(HEADER, DATA, error)
        error.getErrors.assert_called_once_with(DATA)

    def __mockFormatter(self):
        def sideEffect(*args):
            if len(args) == 1:
                return "X "
            else:
                return "Y "
        mock = MagicMock(spec=Formatter)
        mock.format.side_effect = sideEffect
        return mock

    def test_shouldGetCellReturnCorrectCell(self):
        underTest = DataColumn(HEADER, DATA, formatter=self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "X ")

    def test_shouldGetCellReturnCorrectCellWithError(self):
        underTest = DataColumn(HEADER, DATA, FixError(0.5), self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "Y ")

    def test_shouldGetCellReturnCorrectCellWithUnit(self):
        underTest = DataColumn(HEADER, DATA * units.kg, formatter=self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "X ")

    def test_shouldGetCellReturnCorrectCellWithErrorWithUnit(self):
        underTest = DataColumn(HEADER, DATA * units.kg, FixError(0.5), self.__mockFormatter())
        self.assertEqual(underTest.getCell(3), "Y ")

    def test_shouldRaiseExceptionForIndexOutOfBounds(self):
        with self.assertRaises(IndexError):
            DataColumn(HEADER, np.random.rand(LINES)).getCell(LINES)

    def test_shouldCreateExponentialFormatterForDataOrder5(self):
        underTest = DataColumn(HEADER, DATA * 1000)
        self.assertIsInstance(underTest._DataColumn__formatter, ExponentialFormatter)

    def test_shouldCreateFloatFormatterForDataOrder5(self):
        underTest = DataColumn(HEADER, DATA * 100)
        self.assertIsInstance(underTest._DataColumn__formatter, FloatFormatter)


if __name__ == '__main__':
    main()
