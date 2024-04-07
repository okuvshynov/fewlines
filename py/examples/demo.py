import time

import numpy as np

from fewlines.charts import colors, histogram_chart
from fewlines import metrics as fm
from fewlines import dashboard as fd
from fewlines.line import multiline, horizon_multiline

def demo_lines():
    for l in multiline([i for i in range(100)], n_lines=4, cells=[' ', '▄', '█'], top_cells=[' ', '▄'])[0]:
        print(l)

    for l in horizon_multiline([i for i in range(100)], n_lines=4, cells=[' ', '▄', '█'])[0]:
        print(l)

def demo_charts():
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

def demo_dashboard():
    for i, v in enumerate(np.random.lognormal(mean=1.0, sigma=0.7, size=1000)):
        fm.add('ssd_read_latency', v, time.time() - i)
    for i, v in enumerate(np.random.lognormal(mean=3.0, sigma=0.7, size=1500)):
        fm.add('nw_recv_latency', v, time.time() - i)

    print("\n## Default one-line dashboards with wildcard")
    for s in fd.histograms('*latency'):
        print(s)

    for s in fd.timeseries('*latency'):
        print(s)

    print()
    print('\n## two histograms with separate scales with larger height and horizon colors')
    for s in fd.dashboard({"charts": [('*latency', 'histogram')], "n_lines": 3, "color": 'green'}):
        print(s) 

    print()
    print('\n## two histograms sharing the scale as they are part of the same group with larger height and horizon colors')
    for s in fd.dashboard({"charts": [[('*latency', 'histogram')]], "n_lines": 3, "color": 'green'}):
        print(s)

    print()
    conf = {
        "title": "Custom Dashboard",
        "charts": [
            ('ssd_read_latency', 'timeseries', {'n_lines': 3, 'color': None}),
            [
                ('ssd_read_latency', 'timeseries'),
                ('ssd_read_latency', 'timeseries', {'agg': 'max'}),
                ('ssd_read_latency', 'timeseries', {'agg': 'min'}),
            ],
            ('ssd_read_latency', 'histogram', {'n_lines': 4, 'color': 'green'}),
            ('ssd_read_latency', 'histogram', {'n_lines': 4, 'color': 'gray'}),
            ('ssd_read_latency', 'histogram', {'n_lines': 6, 'color': None}),
        ],
        "time": -600, # default -3600
        "bins": 60, # default 60
        "left_margin": 25, # default 30
        "n_lines": 3,
        "color": None,
    }
    print('\n## detailed complicated config with different aggregations')
    for s in fd.dashboard(conf):
        print(s)

if __name__ == '__main__':
    demo_lines()
    demo_charts()
    demo_dashboard()