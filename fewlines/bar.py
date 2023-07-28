# this is similar to horizon, but doesn't rely on ANSI colors, thus, better suited for logs 

try:
    import numpy as np
    has_nupmy = True
except ImportError:
    has_nupmy = False

default_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def bar_line(y, chrs=default_blocks) -> str:
    Y = max(y)
    if Y == 0:
        return chrs[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: chrs[clamp(int(v * len(chrs) / Y), 0, len(chrs) - 1)]
    horizon = ''.join([cell(v) for v in y])
    return horizon

def bar_histogram(values, chart_width=80, scale_range=None):
    if not has_nupmy:
        raise ImportError("numpy is required to use horizon_histogram.")
    values, bin_edges = np.histogram(values, chart_width, scale_range)
    return bar_line(values), (bin_edges[0], bin_edges[-1])

def bar_histograms(series, chart_width=80, shared_scale=True):
    if not has_nupmy:
        raise ImportError("numpy is required to use horizon_multi_histogram.")
    
    scale_range = (min(min(v) for _, v in series), max(max(v) for _, v in series)) if shared_scale else None

    res = []
    for name, values in series:
        line, interval = bar_histogram(values, chart_width=chart_width, scale_range=scale_range)
        res.append((name, line, interval))

    return res

def print_histogram(values, title='', chart_width=80, scale_range=None):
    line, (a, b) = bar_histogram(values, chart_width, scale_range)
    title = f'{title}: ' if title != '' else ''
    print(f'{title}{line} [{a:.4g}; {b:.4g}]')

def print_histograms(series, chart_width=80, shared_scale=True):
    if isinstance(series, dict):
        series = series.items()
    for name, chart, (a, b) in bar_histograms(series, chart_width=chart_width, shared_scale=shared_scale):
        print(f'{name}: [{a:.4g}; {b:.4g}]')
        print(f'[{chart}]')

if __name__ == '__main__':
    print_histograms({'a': [1,2,3,4,5,6,6], 'b': [3,3,3,3,3,3,3,3,3]})