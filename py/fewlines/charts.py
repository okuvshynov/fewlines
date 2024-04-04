from fewlines.line import line, multiline, colors, horizon_line, horizon_multiline
from fewlines.utils import _line_header, _global_range, _header, _histogram, _bin_index

# charts we can format as lists of strings
# supports histograms and lines, with different formatting
# for single-line and multi-line charts

def _multiline_legend_render(lines, title, max_value, width):
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

def _oneline_legend_render(lines, title, max_value, width):
    if width <= 0:
        left = ''
    else:
        left = f'{title} [{max_value:.3g}]|'[-width:]
        left = f'{left:>{width}}'
    
    right = '|'
    return [left + lines[0] + right]

def _render_subplots(numbers, n_lines, left_margin, color):
    res = []
    _, max_y = _global_range(numbers)
    for title, (values, args) in numbers.items():
        current_color = args.get('color', color)
        current_n_lines = args.get('n_lines', n_lines)
        lines, max_value = multiline(values, max_y=max_y, n_lines=current_n_lines) if current_color is None else horizon_multiline(values, color=current_color, max_y=max_y, n_lines=current_n_lines)
        legend_renderer = _oneline_legend_render if current_n_lines == 1 else _multiline_legend_render
        res.extend(legend_renderer(lines, title, max_value, width=left_margin))
    return res

def line_chart(numbers, bins, left_val, header=True, left_margin=20, n_lines=1, color=None):
    res = [_line_header(left_val, bins, left_margin)] if header else []
    return res + _render_subplots(numbers, n_lines, left_margin, color)

def histogram_chart(numbers, bins=60, header=True, left_margin=20, custom_range=None, n_lines=1, color=None):
    # here mn, mx represent the min and max of values
    mn, mx = custom_range if custom_range is not None else _global_range(numbers)
    histograms = {k: (_histogram(v, bins, mn, mx), args) for k, (v, args) in numbers.items()}

    res = [_header(mn, mx, bins=bins, left_margin=left_margin)] if header else []
    return res + _render_subplots(histograms, n_lines, left_margin, color)

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
