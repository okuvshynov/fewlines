import numpy as np
from collections import defaultdict
import time
from fewlines.charts import bar_histograms, bar_lines, bar_histograms_multiline, bar_multilines
import math


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

def timeseries_group(groups, bins=60, left_margin=20, offset_s=-3600, n_lines=1, color=None) -> str:
    charts = {}
    now = time.time()
    for group in groups:
        counter_name, *agg = group
        agg = 'avg' if not agg else agg[0]
        series = fewlines_data.get(counter_name, [])
        counts = [0] * bins
        values = [0] * bins
        bin_size_s = - offset_s / bins
        for timestamp, value in series:
            offset = now - timestamp
            bin = int(math.floor(offset / bin_size_s))
            if bin < 0 or bin >= bins:
                continue
            counts[bin], values[bin] = aggregation[agg](counts[bin], values[bin], value) 
        charts[f'{counter_name}.{agg}'] = list(reversed(values))
    if n_lines > 1:
        return bar_multilines(charts, bins, f'-{bins * bin_size_s}s', left_margin=left_margin, n_lines=n_lines, color=color)
    return bar_lines(charts, bins, f'-{bins * bin_size_s}s', left_margin=left_margin)

def timeseries(counter_name, bins=60, left_margin=20, offset_s=-3600, agg='avg') -> str:
    return timeseries_group([(counter_name, agg)], bins, left_margin, offset_s)

def histogram_group(groups, bins=60, left_margin=20, offset_s=-3600, n_lines=1, color='green') -> str:
    now = time.time()
    values = {}
    for group in groups:
        counter_name, *args = group
        series = fewlines_data.get(counter_name, [])
        values[counter_name] = [v for t, v in series if t - offset_s > now]
    
    if n_lines > 1:
        return bar_histograms_multiline(values, bins=bins, header=True, left_margin=left_margin, n_lines=n_lines, color=color)
    return bar_histograms(values, bins=bins, header=True, left_margin=left_margin, color=color)

def histogram(counter_name, bins=60, left_margin=20, offset_s=-3600, n_lines=1) -> str:
    return histogram_group([(counter_name, )], bins, left_margin, offset_s, n_lines)

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