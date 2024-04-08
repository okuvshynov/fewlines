import unittest

from fewlines.charts import _histogram, histogram_chart, _to_canonical

class TestCharts(unittest.TestCase):
    def test_to_canonical(self):
        self.assertEqual({'': ([1, 2, 3], {})}, _to_canonical([1, 2, 3]))
        self.assertEqual({'': ([1, 2, 3], {'n_lines': 2})}, _to_canonical(([1, 2, 3], {'n_lines': 2})))
        self.assertEqual({'onetwothree': ([1, 2, 3], {})}, _to_canonical({'onetwothree': [1, 2, 3]}))
        self.assertEqual({'x': ([1, 2, 3], {}), 'y': ([4, 5, 6], {'color': 'green'})}, _to_canonical({'x': [1, 2, 3], 'y': ([4, 5, 6], {'color': 'green'})}))

    def test_histogram(self):
        self.assertEqual(_histogram([], 5, None, None), [0, 0, 0, 0, 0])
        self.assertEqual(_histogram([0], 5, 0, 0), [0, 0, 1, 0, 0])
        self.assertEqual(_histogram([0, 1], 5, 0, 1), [1, 0, 0, 0, 1])
        self.assertEqual(_histogram([0], 5, 0, 1), [1, 0, 0, 0, 0])
        self.assertEqual(_histogram([0, 1, 2], 1, 0, 2), [3])

    def test_bar_histograms(self):
        self.assertEqual(histogram_chart({'A': ([0], {}), 'B': ([1], {})}, 10, header=False, title_width=0, n_lines=1), ["▇         |", "         ▇|"])
        self.assertEqual(histogram_chart({'A': ([0, 1], {}), 'B': ([1], {})}, 10, header=False, title_width=0, n_lines=1), ["▇        ▇|", "         ▇|"])
        self.assertEqual(histogram_chart({'A': ([0, 1], {}), 'B': ([1], {})}, 10, title_width=0, n_lines=1), ["0~~~~~~~~~|1", "▇        ▇|", "         ▇|"])
        self.assertEqual(histogram_chart({'A': ([0, 1], {}), 'B': ([1], {})}, 10, title_width=10, n_lines=1), ["~~~~~~~ 0|0~~~~~~~~~|1", "    A [1]|▇        ▇|", "    B [1]|         ▇|"])

if __name__ == '__main__':
    unittest.main()