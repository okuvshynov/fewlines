import time

import numpy as np

from fewlines.charts import colors, histogram_chart, line_chart
from fewlines import metrics as fm
from fewlines import dashboard as fd
from fewlines.line import block_lines, horizon_lines
import fewlines.metrics as fm

def demo_lines():
    for l in block_lines([i for i in range(100)], n_lines=4)[0]:
        print(l)

    for l in horizon_lines([i for i in range(100)], n_lines=4)[0]:
        print(l)

def demo_charts():
    print()
    print("HISTOGRAM CHART DEMO")

    data = {'title_A': (np.random.normal(size=10000), {})}
    small_data = np.random.normal(size=50)
    

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

    print()
    print('LINECHART DEMO')
    for l in line_chart(small_data):
        print(l)
    
    for l in line_chart(small_data, left_label=min(small_data), right_label=max(small_data)):
        print(l)

    for l in line_chart({'tiny!': small_data}, left_label=min(small_data), right_label=max(small_data), n_lines=3):
        print(l)

    for l in line_chart({'tiny!': small_data}, left_label=min(small_data), right_label=max(small_data), n_lines=3, color='green'):
        print(l)

    for l in line_chart([]):
        print(l)
    for l in line_chart([], color='green'):
        print(l)
    for l in line_chart([], n_lines=3):
        print(l)
    for l in line_chart([], color='green', n_lines=3):
        print(l)

def demo_dashboard():
    print()
    print("DASHBOARD DEMO")
    for i, v in enumerate(np.random.lognormal(mean=1.0, sigma=0.7, size=1000)):
        fm.add('ssd_read_latency', v, time.time() - i)
    for i, v in enumerate(np.random.lognormal(mean=3.0, sigma=0.7, size=1500)):
        fm.add('nw_recv_latency', v, time.time() - i)

    print("\n## one-line dashboards with wildcard metrics selection")
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

def demo_metrics():
    print()
    print("METRICS DEMO")
    fm.add('latency_ms', 1.2)
    fm.add('latency_ms', 1.3)
    fm.add('latency_ms', 1.4)
    fm.add('latency_ms', 1.5)
    fm.add('latency_ms', 1.6)
    fm.add('latency_ms', 1.7)
    fm.add('latency_ms', 1.8)
    for error in np.random.normal(size=10000):
        fm.add('error', error)

    for h in fm.timeseries('latency_ms', color='green', left_margin=40, n_lines=3):
        print(h)
    for h in fm.histogram('latency_ms', n_lines=2):
        print(h)

if __name__ == '__main__':
    demo_lines()
    demo_charts()
    demo_dashboard()
    demo_metrics()