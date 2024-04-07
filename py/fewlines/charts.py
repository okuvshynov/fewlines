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


## line_chart and histogram_chart accept following inputs:

# canonical form
#   dictionary of string -> pair(numbers, extra_args). Example: {'latency': ([0, 1, 2, 3], {'n_lines' : 4})} or {'title2': ([0], {})}
# no options:
#   dictionary of string -> numbers. Example {'latency': [0, 1, 2, 3]}. Empty dictionary would be added as options
# numbers and options:
#   tuple of list/array of numbers and options. Example: ([0, 1, 2, 3], {'color': 'green'}). Empty title would be created.
# just numbers:
#   list/array of numbers. Example: [0, 1, 2, 3]. Empty title and options would be created.

def _to_canonical(numbers):
    if isinstance(numbers, tuple):
        return {'': numbers}
    if isinstance(numbers, dict):
        return {k : v if isinstance(v, tuple) else (v, {}) for k, v in numbers.items() }
    # assume it is a list
    return {'': (numbers, {})}

def line_chart(numbers, bins, left_val, header=True, left_margin=20, n_lines=1, color=None):
    numbers = _to_canonical(numbers)

    # TODO: this header is specifically for timeseries, not line chart
    res = [_line_header(left_val, bins, left_margin)] if header else []
    return res + _render_subplots(numbers, n_lines, left_margin, color)

def histogram_chart(numbers, bins=60, header=True, left_margin=20, custom_range=None, n_lines=1, color=None):
    # here mn, mx represent the min and max of values
    numbers = _to_canonical(numbers)
    mn, mx = custom_range if custom_range is not None else _global_range(numbers)
    histograms = {k: (_histogram(v, bins, mn, mx), args) for k, (v, args) in numbers.items()}

    res = [_header(mn, mx, bins=bins, left_margin=left_margin)] if header else []
    return res + _render_subplots(histograms, n_lines, left_margin, color)

# Some test examples; require numpy
if __name__ == '__main__':
    import numpy as np
    data = {'title_A': (np.random.normal(size=10000), {})}
    
    # horizon with colors
    for color in colors:
        for l in histogram_chart(data, bins=40, color=color, n_lines=1):
            print(l)

    # bar chart without colors
    for l in histogram_chart(data, bins=40, n_lines=1):
        print(l)

    # bar chart without colors
    for l in histogram_chart(data, bins=40):
        print(l)

    # horizon with colors
    for l in histogram_chart(data, bins=40, color='green'):
        print(l)

    # horizon with a lot of details
    for l in histogram_chart(data, bins=40, n_lines=8, color='green'):
        print(l)

    for l in histogram_chart({'empty': ([], {})}, n_lines=1):
        print(l)
    
    for l in histogram_chart({'zero': ([0], {})}, n_lines=1):
        print(l)


    data2 = np.random.normal(size=1000)
    # try all 4 ways to pass data:
    print('just data w/o title and options')
    for l in histogram_chart(data2):
        print(l)
    print('data w/o title with options')
    for l in histogram_chart((data2, {'n_lines': 2})):
        print(l)
    print('dict data without options')
    for l in histogram_chart({'B': data2}):
        print(l)
    print('dict data with options')
    for l in histogram_chart({'B': (data2, {'n_lines': 2})}):
        print(l)
