from fewlines.line import line, multiline, colors, horizon_line, horizon_multiline
from fewlines.utils import _time_header, _global_range, _header, _histogram, _bin_index

# charts we can format as lists of strings
# supports histograms and lines, with different formatting
# for single-line and multi-line charts

def multiline_legend_render(lines, title, max_value, width):
    res = []
    if width <= 0:
        left_top = ''
        left = ''
        left_bottom = ''
    else:
        left_top = f'{max_value:.3g} |'[-width:]
        left_top = f'{left_top:>{width}}'
        left_bottom = f'{title} |'[-width:]
        left_bottom = f'{left_bottom:>{width}}'
        left = f'{"|":>{width}}'

    right = '|'
    res.append(left_top + lines[0] + right)
    res.extend(left + chart + right for chart in lines[1:-1])
    res.append(left_bottom + lines[-1] + right)
    return res

def oneline_legend_render(lines, title, max_value, width):
    if width <= 0:
        left = ''
    else:
        left = f'{title} [{max_value:.3g}]|'[-width:]
        left = f'{left:>{width}}'
    
    right = '|'
    return [left + lines[0] + right]

def line_chart(numbers, bins, left_val, header=True, left_margin=20, shared_scale=True, n_lines=3, color=None):
    res = []
    if header:
        res.append(_time_header(left_val, bins, left_margin))

    _, mx = _global_range(numbers)
    if not shared_scale:
        mx = None
    
    legend_renderer = oneline_legend_render if n_lines == 1 else multiline_legend_render

    for title, values in numbers.items():
        lines, max_value = multiline(values, max_y=mx, n_lines=n_lines) if color is None else horizon_multiline(values, n_lines=n_lines, color=color, max_y=mx)
        res.extend(legend_renderer(lines, title, max_value, width=left_margin))

    return res

# Plot multiple histograms on the same scale.
#   numbers     - a dictionary{str: list_of_numbers} of data to plot distribution on
#   bins - how many characters to use. Histogram will use that many bins.
#   header        - show a line with range at the top
#   left_margin - width of the space for each data title
#   color       - name of the colorscheme. If None, uses blocks only.

def histogram_chart(numbers, bins=60, header=True, left_margin=20, custom_range=None, n_lines=3, color=None):
    # here mn, mx represent the min and max of values
    mn, mx = custom_range if custom_range is not None else _global_range(numbers)
    res = []
    if header:
        res.append(_header(mn, mx, bins=bins, left_margin=left_margin))

    legend_renderer = oneline_legend_render if n_lines == 1 else multiline_legend_render

    histograms = {k: _histogram(v, bins, mn, mx) for k, v in numbers.items()}
    _, freq_mx = _global_range(histograms)
    for title, values in histograms.items():
        lines, max_value = multiline(values, max_y=freq_mx, n_lines=n_lines) if color is None else horizon_multiline(values, color=color, max_y=freq_mx, n_lines=n_lines)
        res.extend(legend_renderer(lines, title, max_value, width=left_margin))

    return res

# Some test examples; require numpy
if __name__ == '__main__':
    import numpy as np
    data = {'title_A': list(np.random.normal(size=10000))}
    
    # horizon with colors
    for color in colors:
        for l in histogram_chart(data, bins=40, color=color, n_lines=1):
            print(l)

    # bar chart without colors
    for l in histogram_chart(data, bins=40, n_lines=1):
        print(l)

    # bar chart without colors, spanning default 3 lines
    for l in histogram_chart(data, bins=40):
        print(l)

    # horizon with colors spanning default 3 lines
    for l in histogram_chart(data, bins=40, color='green'):
        print(l)

    # horizon with a lot of details
    for l in histogram_chart(data, bins=40, n_lines=8, color='green'):
        print(l)

    for l in histogram_chart({'empty': []}, n_lines=1):
        print(l)
    
    for l in histogram_chart({'zero': [0]}, n_lines=1):
        print(l)

# while probably not idiomatic, I like unit tests right where the code is. 

    import unittest

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
            self.assertEqual(_global_range({'a': []}), (0.0, 0.0))
            self.assertEqual(_global_range({'a': [1]}), (1.0, 1.0))
            self.assertEqual(_global_range({'a': [1], 'b': []}), (1.0, 1.0))
            self.assertEqual(_global_range({'a': [1], 'b': [2]}), (1.0, 2.0))

        def test_header(self):
            self.assertEqual(_header(-10, 10, 20, 0), "~~~~~~~~~~0~~~~~~~~~|10")
            self.assertEqual(_header(-10, 10, 20, 10), "~~~~~ -10|~~~~~~~~~~0~~~~~~~~~|10")
            self.assertEqual(_header(-10, 10, 20, 0, show_zero=False), "~~~~~~~~~~~~~~~~~~~~|10")
            self.assertEqual(_header(-10, 10, 20, 10, show_zero=False), "~~~~~ -10|~~~~~~~~~~~~~~~~~~~~|10")
            self.assertEqual(_header(0, 10, 20, 0), "0~~~~~~~~~~~~~~~~~~~|10")
            self.assertEqual(_header(0, 10, 20, 10), "~~~~~~~ 0|0~~~~~~~~~~~~~~~~~~~|10")

        def test_line(self):
            self.assertEqual(line([1,2,3])[0], "▂▅▇")
            self.assertEqual(line([])[0], "")
            self.assertEqual(line([0, 100])[0], " ▇")

        def test_histogram(self):
            self.assertEqual(_histogram([], 5, None, None), [0, 0, 0, 0, 0])
            self.assertEqual(_histogram([0], 5, 0, 0), [0, 0, 1, 0, 0])
            self.assertEqual(_histogram([0, 1], 5, 0, 1), [1, 0, 0, 0, 1])
            self.assertEqual(_histogram([0], 5, 0, 1), [1, 0, 0, 0, 0])
            self.assertEqual(_histogram([0, 1, 2], 1, 0, 2), [3])

        def test_bar_histograms(self):
            self.assertEqual(histogram_chart({'A': [0], 'B': [1]}, 10, header=False, left_margin=0, n_lines=1), ["▇         |", "         ▇|"])
            self.assertEqual(histogram_chart({'A': [0, 1], 'B': [1]}, 10, header=False, left_margin=0, n_lines=1), ["▇        ▇|", "         ▇|"])
            self.assertEqual(histogram_chart({'A': [0, 1], 'B': [1]}, 10, left_margin=0, n_lines=1), ["0~~~~~~~~~|1", "▇        ▇|", "         ▇|"])
            self.assertEqual(histogram_chart({'A': [0, 1], 'B': [1]}, 10, left_margin=10, n_lines=1), ["~~~~~~~ 0|0~~~~~~~~~|1", "    A [1]|▇        ▇|", "    B [1]|         ▇|"])


    unittest.main()
