import math

# not using the largest block so that two histograms on two lines won't collide
bar_blocks     = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇']

# For horizon we can use the largest block, as we'll use color coding
horizon_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

# colorschemes
colors = {
    'green': [-1, 150, 107, 22],
    'red'  : [-1, 196, 124, 52],
}

def _bin_index(min_val, max_val, bins, x):
    if min_val == max_val:
        if x == min_val:
            return bins // 2
        return 0 if x < min_val else bins - 1
    bin_index = int((x - min_val) * bins / (max_val - min_val))
    return max(0, min(bin_index, bins - 1))

def _histogram(data, bins, min_val, max_val):    
    # Initialize the bin counts to zero.
    bin_counts = [0] * bins

    # Count the data points in each bin.
    for x in data:
        if x is None or x is math.isnan(x):
            continue
        bin_counts[_bin_index(min_val, max_val, bins, x)] += 1
    
    return bin_counts

# for things like min/max for dict of lists
def _global_stat(numbers, fn):
    res = None
    if numbers:  # check if dictionary is not empty
        non_empty_values = [fn(v) for v in numbers.values() if v]
        if non_empty_values:
            res = fn(non_empty_values) 
    return res

def _global_range(numbers):
    mn = _global_stat(numbers, min)
    mx = _global_stat(numbers, max)

    if mn is None or mx is None:
        mn, mx = 0.0, 0.0
    return mn, mx

def _time_header(left_val, bins, left_margin):
    mn_text, mx_text = f' {left_val}|'[-left_margin:], 'now'
    
    line = '~' * bins
    
    if left_margin <= 0:
        return line + f'|{mx_text}'
    return '~' * (left_margin - len(mn_text)) + mn_text + line + f'|{mx_text}'

def _header(mn, mx, bins, left_margin, show_zero=True):
    mn_text, mx_text = f' {mn:.3g}|'[-left_margin:], f'{mx:.3g}'
    
    zero_at = _bin_index(mn, mx, bins, 0.0) if mn <= 0 and mx >= 0 and show_zero else None
    line = ''.join(['0' if b == zero_at else '~' for b in range(bins)])
    
    if left_margin <= 0:
        return line + f'|{mx_text}'
    return '~' * (left_margin - len(mn_text)) + mn_text + line + f'|{mx_text}'

# bar_line plots a line using provided blocks or default bar_blocks
def bar_line(y, mx=None, cells=bar_blocks) -> str:
    if not y:
        return ""

    Y = max(y) if mx is None else mx
    if Y == 0:
        return cells[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: cells[clamp(int(v * len(cells) / Y), 0, len(cells) - 1)]
    return ''.join([cell(v) for v in y])

def bar_lines(numbers, bins, left_val, header=True, left_margin=20, shared_scale=True):
    res = []
    if header:
        res.append(_time_header(left_val, bins, left_margin))

    _, mx = _global_range(numbers)
    if not shared_scale:
        mx = None

    for title, values in numbers.items():
        chart = bar_line(values, mx=mx)
        if left_margin <= 0:
            left = ''
        else:
            left = f'{title}|'[-left_margin:]
            left = f'{left:>{left_margin}}'
        
        right = '|'
        res.append(left + chart + right)

    return res

# horizon_line plots line using blocks and color - suitable for terminal output
def horizon_line(y, color='green', cells=horizon_blocks) -> str:
    bg = [f'\33[48;5;{c}m' if c >= 0 else '' for c in colors[color]]
    fg = [f'\33[38;5;{c}m' if c >= 0 else '' for c in colors[color]]
    rst = '\33[0m'
    cells = [f'{f}{b}{c}{rst}' for f, b in zip(fg[1:], bg[:-1]) for c in cells]
    return bar_line(y, cells)

# Plot multiple histograms on the same scale.
#   numbers     - a dictionary{str: list_of_numbers} of data to plot distribution on
#   bins - how many characters to use. Histogram will use that many bins.
#   header        - show a line with range at the top
#   left_margin - width of the space for each data title
#   color       - name of the colorscheme. If None, uses blocks only.
def bar_histograms(numbers, bins=60, header=True, left_margin=20, color=None, custom_range=None):
    # here mn, mx represent the min and max of values
    mn, mx = custom_range if custom_range is not None else _global_range(numbers)

    res = []

    if header:
        res.append(_header(mn, mx, bins=bins, left_margin=left_margin))

    histograms = {k: _histogram(v, bins, mn, mx) for k, v in numbers.items()}
    _, freq_mx = _global_range(histograms)
    for title, values in histograms.items():
        chart = bar_line(values, mx=freq_mx) if color is None else horizon_line(values, color=color)
        if left_margin <= 0:
            left = ''
        else:
            left = f'{title}|'[-left_margin:]
            left = f'{left:>{left_margin}}'
        
        right = '|'
        res.append(left + chart + right)

    return res

# Plot single histogram
#   values      - a list of numbers to plot distribution on
#   title       - name of the data
#   bins - how many characters to use. Histogram will use that many bins.
#   header        - show a line with range at the top
#   left_margin - width of the space for each data title
#   color       - name of the colorscheme. If None, uses blocks only.
def bar_histogram(values, title='', bins=60, header=True, left_margin=20, color=None):
    return bar_histograms({title: values}, bins, header, left_margin, color)

# Some test example, requires numpy
if __name__ == '__main__':
    import numpy as np
    data = {'title_A': list(np.random.normal(size=10000))}
    
    # horizon with colors
    for color in colors:
        for l in bar_histograms(data, bins=40, color=color):
            print(l)

    # bar chart without colors
    for l in bar_histograms(data, bins=40):
        print(l)

    for l in bar_histograms({'empty': []}):
        print(l)
    
    for l in bar_histograms({'zero': [0]}):
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

        def test_bar_line(self):
            self.assertEqual(bar_line([1,2,3]), "▂▅▇")
            self.assertEqual(bar_line([]), "")
            self.assertEqual(bar_line([0, 100]), " ▇")

        def test_histogram(self):
            self.assertEqual(_histogram([], 5, None, None), [0, 0, 0, 0, 0])
            self.assertEqual(_histogram([0], 5, 0, 0), [0, 0, 1, 0, 0])
            self.assertEqual(_histogram([0, 1], 5, 0, 1), [1, 0, 0, 0, 1])
            self.assertEqual(_histogram([0], 5, 0, 1), [1, 0, 0, 0, 0])
            self.assertEqual(_histogram([0, 1, 2], 1, 0, 2), [3])

        def test_bar_histograms(self):
            self.assertEqual(bar_histograms({'A': [0], 'B': [1]}, 10, header=False, left_margin=0), ["▇         |", "         ▇|"])
            self.assertEqual(bar_histograms({'A': [0, 1], 'B': [1]}, 10, header=False, left_margin=0), ["▇        ▇|", "         ▇|"])
            self.assertEqual(bar_histograms({'A': [0, 1], 'B': [1]}, 10, left_margin=0), ["0~~~~~~~~~|1", "▇        ▇|", "         ▇|"])
            self.assertEqual(bar_histograms({'A': [0, 1], 'B': [1]}, 10, left_margin=5), ["~~ 0|0~~~~~~~~~|1", "   A|▇        ▇|", "   B|         ▇|"])


    unittest.main()
