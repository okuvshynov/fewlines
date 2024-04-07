import unittest

from fewlines.utils import _bin_index, _global_range, _header
from fewlines.charts import _histogram, histogram_chart
from fewlines.line import block_lines

class TestUtils(unittest.TestCase):
    def test_bin_index(self):
        self.assertEqual(_bin_index(0, 0, 1, 0), 0)
        self.assertEqual(_bin_index(0, 0, 1, 10), 0)
        self.assertEqual(_bin_index(0, 0, 1, -10), 0)

        # test inclusive/exclusive intervals
        for x in range(100):
            self.assertEqual(_bin_index(0, 10, 100, x * 0.1), x)
        self.assertEqual(_bin_index(0, 10, 100, 10.0), 99)

        for x in range(10):
            self.assertEqual(_bin_index(0, 10, 10, x), x)
        self.assertEqual(_bin_index(0, 10, 10, 10), 9)

        self.assertEqual(_bin_index(0, 10, 10, 8.9), 8)

    def test_global_range(self):
        self.assertEqual(_global_range({}), (0.0, 0.0))
        self.assertEqual(_global_range({'a': ([], {})}), (0.0, 0.0))
        self.assertEqual(_global_range({'a': ([1], {})}), (1.0, 1.0))
        self.assertEqual(_global_range({'a': ([1], {}), 'b': ([], {})}), (1.0, 1.0))
        self.assertEqual(_global_range({'a': ([1], {}), 'b': ([2], {})}), (1.0, 2.0))

    def test_header(self):
        self.assertEqual(_header(-10, 10, 20, 0), "~~~~~~~~~~0~~~~~~~~~|10")
        self.assertEqual(_header(-10, 10, 20, 10), "~~~~~ -10|~~~~~~~~~~0~~~~~~~~~|10")
        self.assertEqual(_header(-10, 10, 20, 0, show_zero=False), "~~~~~~~~~~~~~~~~~~~~|10")
        self.assertEqual(_header(-10, 10, 20, 10, show_zero=False), "~~~~~ -10|~~~~~~~~~~~~~~~~~~~~|10")
        self.assertEqual(_header(0, 10, 20, 0), "0~~~~~~~~~~~~~~~~~~~|10")
        self.assertEqual(_header(0, 10, 20, 10), "~~~~~~~ 0|0~~~~~~~~~~~~~~~~~~~|10")

    def test_line(self):
        self.assertEqual(block_lines([1,2,3])[0], ["▂▅▇"])
        self.assertEqual(block_lines([])[0], [""])
        self.assertEqual(block_lines([0, 100])[0], [" ▇"])

    def test_histogram(self):
        self.assertEqual(_histogram([], 5, None, None), [0, 0, 0, 0, 0])
        self.assertEqual(_histogram([0], 5, 0, 0), [0, 0, 1, 0, 0])
        self.assertEqual(_histogram([0, 1], 5, 0, 1), [1, 0, 0, 0, 1])
        self.assertEqual(_histogram([0], 5, 0, 1), [1, 0, 0, 0, 0])
        self.assertEqual(_histogram([0, 1, 2], 1, 0, 2), [3])

    def test_bar_histograms(self):
        self.assertEqual(histogram_chart({'A': ([0], {}), 'B': ([1], {})}, 10, header=False, left_margin=0, n_lines=1), ["▇         |", "         ▇|"])
        self.assertEqual(histogram_chart({'A': ([0, 1], {}), 'B': ([1], {})}, 10, header=False, left_margin=0, n_lines=1), ["▇        ▇|", "         ▇|"])
        self.assertEqual(histogram_chart({'A': ([0, 1], {}), 'B': ([1], {})}, 10, left_margin=0, n_lines=1), ["0~~~~~~~~~|1", "▇        ▇|", "         ▇|"])
        self.assertEqual(histogram_chart({'A': ([0, 1], {}), 'B': ([1], {})}, 10, left_margin=10, n_lines=1), ["~~~~~~~ 0|0~~~~~~~~~|1", "    A [1]|▇        ▇|", "    B [1]|         ▇|"])

if __name__ == '__main__':
    unittest.main()