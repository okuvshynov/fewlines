from collections import defaultdict

from fewlines.metrics import histogram_group, timeseries_group, add

chart_types = {
    'histogram': histogram_group,
    'timeseries': timeseries_group,
}

# TODO some autoconf - generate dashboard from everything we have?
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
        if not isinstance(chart_group, list):
            chart_group = [chart_group]

        values = defaultdict(list)
        for counter, chart_type, *args in chart_group:
            kvargs = args[0] if args and isinstance(args[0], dict) else {}
            if chart_type in chart_types:
                values[chart_type].append((counter, {**base_kvargs, **kvargs}))
        
        for chart_type, counters in values.items():
            res.extend(chart_types[chart_type](counters, bins, left_margin, t))
        res.append("")
    return res

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
        "title": "Test Dashboard",
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

    mu, sigma = 1.0, 0.7
    sample_size = 100
    while True:
        for s in dashboard(conf):
            print(s)
        for lat in np.random.lognormal(mean=mu, sigma=sigma, size=sample_size):
            add('ssd_read_latency', abs(lat))
        time.sleep(0.4)
