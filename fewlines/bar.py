import math

# not using the largest block so that two histograms on two lines won't collide
bar_blocks     = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇']
horizon_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
colors = {
    'green': [-1, 150, 107, 22]
}

def histogram(data, bins, scale_range=None, ignore_outliers=False):
    # If a range is specified, use it. Otherwise, use the min/max of the data.
    min_val = scale_range[0] if scale_range else min(data)
    max_val = scale_range[1] if scale_range else max(data)
    
    # Create the bins. We'll have one more bin edge than the number of bins.
    bin_edges = [min_val + i * (max_val - min_val) / bins for i in range(bins + 1)]
    
    # Initialize the bin counts to zero.
    bin_counts = [0] * bins

    # Count the data points in each bin.
    for x in data:
        if x is None or x is math.isnan(x):
            continue
        if x < min_val or x > max_val:
            if ignore_outliers:
                continue
            else:
                bin_index = 0 if x < min_val else bins - 1
        else:
            bin_index = min(int((x - min_val) * bins / (max_val - min_val)), bins - 1)
        bin_counts[bin_index] += 1
    
    return bin_counts, bin_edges

def top_axis_str(mn, mx, chart_width=60, left_margin=20):
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
        mn, mx = 0, 0

    if mn == mx:
        mx += 1
        mn -= 1
    
    return mn, mx

# this just plots a line using blocks. 
# more suitable for log files
def bar_line(y, chr=bar_blocks) -> str:
    Y = max(y)
    if Y == 0:
        return chr[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: chr[clamp(int(v * len(chr) / Y), 0, len(chr) - 1)]
    horizon = ''.join([cell(v) for v in y])
    return horizon

# this plots line using block characters and color - suitable for terminals
def horizon_line(y, color='green', chrs=horizon_blocks) -> str:
    bg = [f'\33[48;5;{c}m' if c >= 0 else '' for c in colors[color]]
    fg = [f'\33[38;5;{c}m' if c >= 0 else '' for c in colors[color]]
    rst = '\33[0m'
    cells = [f'{f}{b}{c}{rst}' for f, b in zip(fg[1:], bg[:-1]) for c in chrs]
    Y = max(y)
    if Y == 0:
        return chrs[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: cells[clamp(int(v * len(cells) / Y), 0, len(cells) - 1)]
    horizon = ''.join([cell(v) for v in y])
    return horizon

### Actual API

def bar_histograms(numbers, chart_width=60, axis=True, left_margin=20, color=None):
    mn, mx = global_range(numbers)
    res = []

    if axis:
        res.append(top_axis_str(mn, mx, chart_width=chart_width, left_margin=left_margin))

    for title, values in numbers.items():
        values, bin_edges = histogram(values, chart_width, (mn, mx))
        chart = bar_line(values) if color is None else horizon_line(values, color=color)
        if left_margin <= 0:
            left = ''
        else:
            title = f'{title}|'
            left = f'{title}'[-left_margin:]
            left = f"{left:>{left_margin}}"
        
        right = '|'
        res.append(left + chart + right)

    return res

def bar_histogram(values, title='', chart_width=80, axis=True, left_margin=20, color=None):
    return bar_histograms({title: values}, chart_width, axis, left_margin, color)

if __name__ == '__main__':
    import numpy as np
    data = {'title_A': list(np.random.normal(size=10000))}

    # horizon with colors
    for l in bar_histograms(data, chart_width=40, color='green'):
        print(l)

    # bar chart without colors
    for l in bar_histograms(data, chart_width=40):
        print(l)
