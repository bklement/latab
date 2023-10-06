from unittest import TestCase, main
from unittest.mock import MagicMock
from src.latab import Table, EmptyColumn, SerialNumberColumn

HEADER = "header"
DIFFERENT_LENGTHS_MESSAGE = "Columns have different lengths"


class TestTable(TestCase):

    def test_shouldRaiseExceptionForDifferentColumnLength(self):
        with self.assertRaisesRegex(Exception, DIFFERENT_LENGTHS_MESSAGE):
            Table([SerialNumberColumn(HEADER, 10), EmptyColumn(HEADER, 12)])

    def test_shouldReplaceTabs(self):
        lines = Table([SerialNumberColumn(HEADER, 1), EmptyColumn(HEADER, 1)]).lines()
        self.assertEqual(lines[1], "    \centering")
        self.assertTrue(lines[3].startswith("        header"))

    def test_shouldSetTabLength(self):
        lines = Table([SerialNumberColumn(HEADER, 1), EmptyColumn(HEADER, 1)]).lines(tabLength=8)
        self.assertEqual(lines[1], "        \centering")
        self.assertTrue(lines[3].startswith("                header"))

    def test_shouldPrintPassArgumentsToLines(self):
        table = Table([SerialNumberColumn(HEADER, 1), EmptyColumn(HEADER, 1)])
        table.lines = MagicMock()
        table.print(tabLength=6, separator=',')
        table.lines.assert_called_once_with(6, ',')


if __name__ == '__main__':
    main()
