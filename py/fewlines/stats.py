import numpy as np
from collections import defaultdict
import time
from enum import Enum

from bar import bar_histogram, bar_histograms, bar_lines
import math
import random

fewlines_data = defaultdict(list)

def add(counter_name, value, timestamp=None, aggregation=None):
    timestamp = time.time() if timestamp is None else timestamp
    fewlines_data[counter_name].append((timestamp, value))

def hit(counter_name, timestamp=None, aggregation=None):
    add(counter_name, 1, timestamp, aggregation)

def agg_avg(count, old, val):
    return (count + 1, (count * old + val) / (count + 1))

def agg_max(count, old, val):
    return count + 1, max(old, val)

def agg_min(count, old, val):
    return count + 1, min(old, val)

def agg_sum(count, old, val):
    return count + 1, old + val

def agg_count(count, old, val):
    return count + 1, old + 1

aggregation = {
    'avg': agg_avg,
    'max': agg_max,
    'min': agg_min,
    'sum': agg_sum,
    'count': agg_count
}

def timeseries_group(groups, bins=60, offset_s=-3600) -> str:
    charts = {}
    for group in groups:
        if isinstance(group, tuple):
            counter_name, *agg = group
            agg = 'avg' if not agg else agg[0]
        else:
            counter_name, agg = group, 'avg'
        print(counter_name, agg)
        series = fewlines_data.get(counter_name, [])
        counts = [0] * bins
        values = [0] * bins
        now = time.time()
        bin_size_s = - offset_s / bins
        for timestamp, value in series:
            offset = now - timestamp
            bin = int(math.floor(offset / bin_size_s))
            if bin < 0 or bin >= bins:
                continue
            counts[bin], values[bin] = aggregation[agg](counts[bin], values[bin], value) 
        charts[f'{counter_name}.{agg}'] = list(reversed(values))
    return bar_lines(charts, bins, f'-{bins * bin_size_s}s')

def timeseries(counter_name, bins=60, offset_s=-3600, agg='avg') -> str:
    series = fewlines_data.get(counter_name, [])
    counts = [0] * bins
    values = [0] * bins
    now = time.time()
    bin_size_s = - offset_s / bins
    for timestamp, value in series:
        offset = now - timestamp
        bin = int(math.floor(offset / bin_size_s))
        if bin < 0 or bin >= bins:
            continue
        counts[bin], values[bin] = aggregation[agg](counts[bin], values[bin], value) 
    return bar_lines({f'{counter_name}.{agg}': list(reversed(values))}, bins, f'-{bins * bin_size_s}s')

def histogram(counter_name, bins=60, offset_s=-3600) -> str:
    series = fewlines_data.get(counter_name, [])
    now = time.time()
    values = [v for t, v in series if t - offset_s > now]
    
    return bar_histogram(values, counter_name, bins=bins, header=True)

def histogram_group(groups, bins=60, offset_s=-3600) -> str:
    now = time.time()
    values = {}
    for group in groups:
        if isinstance(group, tuple):
            counter_name, *args = group
        else:
            counter_name = group
        series = fewlines_data.get(counter_name, [])
        values[counter_name] = [v for t, v in series if t - offset_s > now]
    
    return bar_histograms(values, bins=bins, header=True)

charts = {
    'histogram': histogram_group,
    'timeseries': timeseries_group,
    'timeseries_group': timeseries_group,
    'histogram_group': histogram_group,
}

# TODO some autoconf - generate dashboard from everything we have?
def dashboard(config):
    t = config.get("time", -3600)
    bins = config.get("bins", 60)
    left_margin = config.get("left_margin", 20)

    title = config.get("title")
    if title is not None:
        extra = max(0, bins + left_margin - len(title) - 2)
        title = "= " + title + " " + "=" * extra

    res = [] if title is None else [title]

    for chart_group in config["charts"]:
        if not isinstance(chart_group, list):
            chart_group = [chart_group]

        values = defaultdict(list)
        for counter, chart, *args in chart_group:
            # TODO: counter here should be 
            #  - string of a counter name
            #  - prefix/or regex for counter name
            #  - list of the above
            if chart in charts:
                values[chart].append((counter, *args))
        
        for chart_type, v in values.items():
            print(v)
            res.extend(charts[chart_type](v, bins, t))
    return res

def gen_timeseries():
    now = time.time()
    for lat in np.random.normal(size=10000):
        timestamp = now - random.randint(0, 7200)
        add('ssd_read_latency', abs(lat), timestamp=timestamp)

# need to get shared Y scale for timeseries

if __name__ == '__main__':
    add('latency_ms', 1.2)
    add('latency_ms', 1.3)
    add('latency_ms', 1.4)
    add('latency_ms', 1.5)
    add('latency_ms', 1.6)
    add('latency_ms', 1.7)
    add('latency_ms', 1.8)
    for error in np.random.normal(size=10000):
        add('error', error)

    for h in timeseries('latency_ms'):
        print(h)
    for h in histogram('latency_ms'):
        print(h)

    print()
    gen_timeseries()
    conf = {
        "title": "Test Dashboard",
        "charts": [
            ('latency_ms', 'timeseries'),
            ('latency_ms', 'histogram'),
            ('error', 'histogram'),
            ('ssd_read_latency', 'histogram'),
            [
                ('ssd_read_latency', 'timeseries_group'),
                ('ssd_read_latency', 'timeseries_group', 'max'),
                ('ssd_read_latency', 'timeseries_group', 'min'),
            ]
        ],
        "time": -3600, # default -3600
        "bins": 40, # default 60
        "left_margin": 20, # default 20
    }
    for s in dashboard(conf):
        print(s)
