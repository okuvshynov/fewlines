from collections import defaultdict

from fewlines.metrics import histogram_group, timeseries_group, add, counter_expand

chart_types = {
    'histogram': histogram_group,
    'timeseries': timeseries_group,
}

# TODO some autoconf - generate dashboard from everything we have?
# some configuration shortcuts might include
# adding chart by some prefix:
#
"""
    conf = {
        "charts": [('ssd_read_*', 'histogram')],
    }
"""



def dashboard(config):
    # these are global settings, no override
    t = config.get("time", -3600)
    bins = config.get("bins", 60)
    left_margin = config.get("left_margin", 20)

    # these can be overridden on chart level
    base_kvargs = {
        'n_lines': config.get("n_lines", 1),
        'color': config.get("color", None)
    }
    
    title = config.get("title")

    w = bins + left_margin + 1
    res = ["=" * w]

    if title is not None:
        res.append("= " + title)
        res.append("=" * w)

    for chart_group in config["charts"]:
        new_groups = []
        if not isinstance(chart_group, list):
            
            # we had individual counter here. expand it as individual counters within their own group
            for counter_name in counter_expand(chart_group[0]):
                new_groups.append([(counter_name, ) + chart_group[1:]])
        else:
            # we had a group of counters, expand them within the group
            for counter_name, chart_type, *args in chart_group:
                new_group = []
                for expanded_counter_name in counter_expand(counter_name):
                    new_group.append((expanded_counter_name, chart_type, *args))
                new_groups.append(new_group)

        for new_group in new_groups:
            values = defaultdict(list)
            for counter, chart_type, *args in new_group:
                kvargs = args[0] if args and isinstance(args[0], dict) else {}
                if chart_type in chart_types:
                    values[chart_type].append((counter, {**base_kvargs, **kvargs}))
            
            for chart_type, counters in values.items():
                res.extend(chart_types[chart_type](counters, bins, left_margin, t))
            res.append("")
    return res

def histograms(pattern):
    return dashboard({"charts": [(pattern, 'histogram')],})

def timeseries(pattern):
    return dashboard({"charts": [(pattern, 'timeseries')],})

if __name__ == '__main__':
    # tests/demo   
    
    import numpy as np
    import time

    # some configuration is for entire dashboard:
    #   - time
    #   - bins 
    #   - left_margin
    # some configuration is per group:
    #   - color (or none)
    #   - n_lines
    # some configuration is per individual chart
    #   - chart_type 
    #   - aggregation type for timeseries chart


    #   - color and n_lines can be supplied at the dashboard level as well, and overridden

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
        "left_margin": 40, # default 20
        "n_lines": 3,
        "color": None,
    }

    for lat in np.random.lognormal(mean=1.0, sigma=0.7, size=1000):
        add('ssd_read_latency', abs(lat))
    for lat in np.random.lognormal(mean=3.0, sigma=0.7, size=1500):
        add('recv_latency', abs(lat))

    for s in dashboard(conf):
        print(s)

    # default dashboard
    for s in histograms('*latency'):
        print(s)

    for s in timeseries('*latency'):
        print(s)

    print('## two separate histograms')
    for s in dashboard({"charts": [('*latency', 'histogram')],}):
        print(s)

    print('## two histograms sharing the scale as they are part of the same group')
    for s in dashboard({"charts": [[('*latency', 'histogram')]]}):
        print(s)

    print('## two histograms sharing the scale as they are part of the same group with horizon colors')
    for s in dashboard({"charts": [[('*latency', 'histogram')]], "color": 'gray'}):
        print(s) 

    print('## two histograms sharing the scale as they are part of the same group with larger height and horizon colors')
    for s in dashboard({"charts": [[('*latency', 'histogram')]], "n_lines": 3, "color": 'green'}):
        print(s) 