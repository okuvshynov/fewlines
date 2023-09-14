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

def histogram(data, bins, min_val, max_val):    
    # Initialize the bin counts to zero.
    bin_counts = [0] * bins

    # Count the data points in each bin.
    for x in data:
        if x is None or x is math.isnan(x):
            continue
        bin_index = int((x - min_val) * bins / (max_val - min_val))
        bin_counts[max(0, min(bin_index, bins - 1))] += 1
    
    return bin_counts
def top_axis_str(mn, mx, chart_width, left_margin):
    mn_text, mx_text = f' {mn:.3g}|'[-left_margin:], f'{mx:.3g}'
    if left_margin <= 0:
        return '_' * chart_width + f'|{mx_text}'
    return '~' * (left_margin - len(mn_text)) + mn_text + '~' * chart_width + f'|{mx_text}'

# for things like min/max for dict of lists
def global_stat(numbers, fn):
    res = None
    if numbers:  # check if dictionary is not empty
        non_empty_values = [fn(v) for v in numbers.values() if v]
        if non_empty_values:
            res = fn(non_empty_values) 
    return res

def global_range(numbers):
    mn = global_stat(numbers, min)
    mx = global_stat(numbers, max)

    if mn is None or mx is None:
        mn, mx = 0.0, 0.0

    if mn == mx:
        mx += 1
        mn -= 1
    
    return mn, mx

# bar_line plots a line using blocks without color coding. more suitable for log files
def bar_line(y, cells=bar_blocks) -> str:
    Y = max(y)
    if Y == 0:
        return cells[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: cells[clamp(int(v * len(cells) / Y), 0, len(cells) - 1)]
    return ''.join([cell(v) for v in y])

# horizon_line plots line using blocks and color - suitable for terminal output
def horizon_line(y, color='green', chrs=horizon_blocks) -> str:
    bg = [f'\33[48;5;{c}m' if c >= 0 else '' for c in colors[color]]
    fg = [f'\33[38;5;{c}m' if c >= 0 else '' for c in colors[color]]
    rst = '\33[0m'
    cells = [f'{f}{b}{c}{rst}' for f, b in zip(fg[1:], bg[:-1]) for c in chrs]
    return bar_line(y, cells)

# Plot multiple histograms on the same scale.
#   numbers     - a dictionary{str: list_of_numbers} of data to plot distribution on
#   chart_width - how many characters to use. Histogram will use that many bins.
#   axis        - show a line with range at the top
#   left_margin - width of the space for each data title
#   color       - name of the colorscheme. If None, uses blocks only.
def bar_histograms(numbers, chart_width=60, axis=True, left_margin=20, color=None):
    mn, mx = global_range(numbers)
    res = []

    if axis:
        res.append(top_axis_str(mn, mx, chart_width=chart_width, left_margin=left_margin))

    for title, values in numbers.items():
        values = histogram(values, chart_width, mn, mx)
        chart = bar_line(values) if color is None else horizon_line(values, color=color)
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
#   chart_width - how many characters to use. Histogram will use that many bins.
#   axis        - show a line with range at the top
#   left_margin - width of the space for each data title
#   color       - name of the colorscheme. If None, uses blocks only.
def bar_histogram(values, title='', chart_width=60, axis=True, left_margin=20, color=None):
    return bar_histograms({title: values}, chart_width, axis, left_margin, color)

# Some test example, requires numpy
if __name__ == '__main__':
    import numpy as np
    data = {'title_A': list(np.random.normal(size=10000))}
    
    # horizon with colors
    for color in colors:
        for l in bar_histograms(data, chart_width=40, color=color):
            print(l)

    # bar chart without colors
    for l in bar_histograms(data, chart_width=40):
        print(l)
