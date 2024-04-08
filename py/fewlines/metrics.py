import time
from fewlines.charts import histogram_chart, line_chart
import math
import fnmatch, re

from collections import defaultdict, deque
from functools import partial

default_maxlen = 16384
fewlines_data = defaultdict(partial(deque, maxlen=default_maxlen))

# TODO: aggregation on add, so that we can not waste space
# maybe need to support some form of tdigest for percentiles
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

def counter_expand(counter):
    res = []
    pattern = re.compile(fnmatch.translate(counter))
    for counter_name in fewlines_data.keys():
        if pattern.match(counter_name):
            res.append(counter_name)
    return res

def timeseries_group(counters, bins=60, title_width=20, offset_s=-3600, n_lines=1, color=None) -> str:
    charts = {}
    now = time.time()
    for counter_name, args in counters:
        series = fewlines_data.get(counter_name, [])
        counts = [0] * bins
        values = [0] * bins
        bin_size_s = - offset_s / bins
        agg = args.get('agg', 'avg')
        for timestamp, value in series:
            offset = now - timestamp
            bin = int(math.floor(offset / bin_size_s))
            if bin < 0 or bin >= bins:
                continue
            counts[bin], values[bin] = aggregation[agg](counts[bin], values[bin], value)
        charts[f'{counter_name}.{agg}'] = (list(reversed(values)), args)
    return line_chart(charts, bins, left_label=f'-{bins * bin_size_s}s', right_label='now', title_width=title_width, n_lines=n_lines, color=color)

def histogram_group(counters, bins=60, title_width=20, offset_s=-3600, n_lines=1, color=None, custom_range=None) -> str:
    now = time.time()
    charts = {}
    for counter_name, args in counters:
        series = fewlines_data.get(counter_name, [])
        # TODO: values in the future?
        charts[counter_name] = ([v for t, v in series if t - offset_s >= now], args)
    
    return histogram_chart(charts, bins=bins, header=True, title_width=title_width, n_lines=n_lines, color=color, custom_range=custom_range)

def timeseries(counter_name, bins=60, title_width=20, offset_s=-3600, agg='avg', n_lines=1, color=None) -> str:
    return timeseries_group([(counter_name, {'agg': agg})], bins, title_width, offset_s, n_lines=n_lines, color=color)

def histogram(counter_name, bins=60, title_width=20, offset_s=-3600, n_lines=1, color=None, custom_range=None) -> str:
    return histogram_group([(counter_name, {})], bins, title_width, offset_s, n_lines=n_lines, color=color, custom_range=custom_range)
