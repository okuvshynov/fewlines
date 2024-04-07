import unittest

from fewlines.line import block_lines

class TestLines(unittest.TestCase):
    def test_line_basic(self):
        self.assertEqual(block_lines([1,2,3])[0], ["▂▅▇"])
        self.assertEqual(block_lines([])[0], [""])
        self.assertEqual(block_lines([0, 100])[0], [" ▇"])

    def test_line_multi(self):
        self.assertEqual(block_lines([1,2,3], n_lines=2)[0], [" ▂▇", "▅██"])
        self.assertEqual(block_lines([], n_lines=2)[0], ["", ""])
        self.assertEqual(block_lines([0, 100], n_lines=2)[0], [" ▇", " █"])


if __name__ == '__main__':
    unittest.main()