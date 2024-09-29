from unittest import TestCase, main
from unittest.mock import MagicMock, patch
import numpy as np
from src.latab import Table

HEADER = "header"
DIFFERENT_LENGTHS_MESSAGE = "^Columns have different lengths$"
DATA = np.random.rand(10) * 100


class TestTable(TestCase):

    def test_shouldRaiseExceptionForDifferentColumnLength(self):
        with self.assertRaisesRegex(Exception, DIFFERENT_LENGTHS_MESSAGE):
            Table().serialColumn(HEADER, 10).textColumn(HEADER, ["", ""])

    def test_shouldLinesReplaceTabs(self):
        lines = Table().serialColumn(HEADER, 1).serialColumn(HEADER, 1).lines()
        self.assertTrue(lines[1].startswith("    \\centering"))
        self.assertTrue(lines[3].startswith("        header"))

    def test_shouldLinesSetTabLength(self):
        lines = Table().serialColumn(HEADER, 1).serialColumn(HEADER, 1).lines(tabLength=8)
        self.assertTrue(lines[1].startswith("        \\centering"))
        self.assertTrue(lines[3].startswith("                header"))

    def test_shouldPrintCallLinesWithDefaultArguments(self):
        table = Table().serialColumn(HEADER, 1).serialColumn(HEADER, 1)
        table.lines = MagicMock()
        table.print()
        table.lines.assert_called_once_with(4, '.')

    def test_shouldPrintPassArgumentsToLines(self):
        table = Table().serialColumn(HEADER, 1).serialColumn(HEADER, 1)
        table.lines = MagicMock()
        table.print(tabLength=6, separator=',')
        table.lines.assert_called_once_with(6, ',')

    @patch('builtins.print')
    def test_shouldPrintReplaceTabs(self, mock_print):
        Table().serialColumn(HEADER, 1).serialColumn(HEADER, 1).print()
        calls = mock_print.call_args_list
        self.assertTrue(calls[1].args[0].startswith("    \\centering"))
        self.assertTrue(calls[3].args[0].startswith("        header"))

    @patch('builtins.print')
    def test_shouldPrintSetTabLength(self, mock_print):
        Table().serialColumn(HEADER, 1).serialColumn(HEADER, 1).print(tabLength=8)
        calls = mock_print.call_args_list
        self.assertTrue(calls[1].args[0].startswith("        \\centering"))
        self.assertTrue(calls[3].args[0].startswith("                header"))


if __name__ == '__main__':
    main()
