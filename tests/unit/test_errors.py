from unittest import TestCase, main
from src.latab.errors import Error, FixError, RelativeError, AbsoluteError
import numpy as np
from astropy import units

DATA = np.random.rand(10) * 100
FIX_ERROR = 0.05
FIX_ERROR_ERROR_MESSAGE = "^Fix error must be of type float or astropy.units.Quantity$"
RELATIVE_ERROR = 0.001
RELATIVE_ERROR_ERROR_MESSAGE = "^Relative error must be of type float$"
ABSOLUTE_ERROR = np.random.rand(10)
ABSOLUTE_ERROR_ERROR_MESSAGE = "^Absolute error must be of type numpy.ndarray or astropy.units.Quantity$"


class TestError(TestCase):

    def test_abstarct(self):
        with self.assertRaises(TypeError):
            Error()


class TestFixError(TestCase):

    def test_withFloat(self):
        underTest = FixError(FIX_ERROR)
        errors = underTest.getErrors(DATA)
        self.assertTrue(np.array_equal(errors, np.ones(10) * FIX_ERROR))

    def test_withQuantity(self):
        underTest = FixError(FIX_ERROR * units.kg)
        errors = underTest.getErrors(DATA)
        self.assertTrue(np.array_equal(errors, np.ones(10) * FIX_ERROR))

    def test_shouldRaiseException(self):
        with self.assertRaisesRegex(Exception, FIX_ERROR_ERROR_MESSAGE):
            FixError("")


class TestRelativeError(TestCase):

    def test_withFloat(self):
        underTest = RelativeError(RELATIVE_ERROR)
        errors = underTest.getErrors(DATA)
        self.assertTrue(np.array_equal(errors, DATA * RELATIVE_ERROR))

    def test_shouldRaiseException(self):
        with self.assertRaisesRegex(Exception, RELATIVE_ERROR_ERROR_MESSAGE):
            RelativeError("")


class TestAbsoluteError(TestCase):

    def test_withFloat(self):
        underTest = AbsoluteError(ABSOLUTE_ERROR)
        errors = underTest.getErrors(DATA)
        self.assertTrue(np.array_equal(errors, ABSOLUTE_ERROR))

    def test_withQuantity(self):
        underTest = AbsoluteError(ABSOLUTE_ERROR * units.kg)
        errors = underTest.getErrors(DATA)
        self.assertTrue(np.array_equal(errors, ABSOLUTE_ERROR))

    def test_shouldRaiseException(self):
        with self.assertRaisesRegex(Exception, ABSOLUTE_ERROR_ERROR_MESSAGE):
            AbsoluteError("")


if __name__ == '__main__':
    main()
