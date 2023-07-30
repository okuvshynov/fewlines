# this is similar to horizon, but doesn't rely on ANSI colors, thus, better suited for logs 

import utils
from layout import top_axis_str

# not using the largest block so that two histograms on two lines 
# won't collide
default_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇']

# this just plots a line using blocks. 
def bar_line(y, chrs=default_blocks) -> str:
    Y = max(y)
    if Y == 0:
        return chrs[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: chrs[clamp(int(v * len(chrs) / Y), 0, len(chrs) - 1)]
    horizon = ''.join([cell(v) for v in y])
    return horizon

def bar_histograms(numbers, chart_width=80, axis=True, left_margin=20):
    mn, mx = utils.global_range(numbers)
    res = []

    if axis:
        res.append(top_axis_str(mn, mx, chart_width=chart_width, left_margin=left_margin))

    for title, values in numbers.items():
        values, bin_edges = utils.histogram(values, chart_width, (mn, mx))
        chart = bar_line(values)
        if left_margin <= 0:
            left = ''
        else:
            title = f'{title}|'
            left = f'{title}'[-left_margin:]
            left = f"{left:>{left_margin}}"
        
        right = '|'
        res.append(left + chart + right)

    return res

def bar_histogram(values, title='', chart_width=80, axis=True, left_margin=20):
    return bar_histograms({title: values}, chart_width, axis, left_margin)

if __name__ == '__main__':
    for l in bar_histograms({'a': [1,2,3,4,5,6,6,6], 'b': [3,3,3,3,3,3,3,3,3]}, chart_width=10):
        print(l)

    for l in bar_histogram([1,2,34,234,2,34,23,4,12,3,2,2,3,3,3,4]):
        print(l)