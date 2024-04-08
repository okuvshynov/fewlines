from fewlines.line import block_lines, horizon_lines
from fewlines.utils import _line_header, _global_range, _header, _histogram

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

def _render_subplots(numbers, n_lines, title_width, color):
    res = []
    _, max_y = _global_range(numbers)
    for title, (values, args) in numbers.items():
        current_color = args.get('color', color)
        current_n_lines = args.get('n_lines', n_lines)
        lines, max_value = block_lines(values, max_y=max_y, n_lines=current_n_lines) if current_color is None else horizon_lines(values, color=current_color, max_y=max_y, n_lines=current_n_lines)
        legend_renderer = _oneline_legend_render if current_n_lines == 1 else _multiline_legend_render
        res.extend(legend_renderer(lines, title, max_value, width=title_width))
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

# if bins is None, autodetect length from numbers
def line_chart(numbers, bins=None, left_label="", right_label="", header=True, title_width=20, n_lines=1, color=None):
    numbers = _to_canonical(numbers)
    if bins is None:
        if len(numbers) > 0:
            bins = len(next(iter(numbers.values()))[0])

    # TODO: this header is specifically for timeseries, not line chart
    res = [_line_header(left_label, right_label, bins, title_width)] if header else []
    return res + _render_subplots(numbers, n_lines, title_width, color)

def histogram_chart(numbers, bins=60, header=True, title_width=20, custom_range=None, n_lines=1, color=None):
    # here mn, mx represent the min and max of values
    numbers = _to_canonical(numbers)
    mn, mx = custom_range if custom_range is not None else _global_range(numbers)
    histograms = {k: (_histogram(v, bins, mn, mx), args) for k, (v, args) in numbers.items()}

    res = [_header(mn, mx, bins=bins, title_width=title_width)] if header else []
    return res + _render_subplots(histograms, n_lines, title_width, color)

