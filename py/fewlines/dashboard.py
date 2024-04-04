from collections import defaultdict

from fewlines.metrics import histogram_group, timeseries_group, add

chart_types = {
    'histogram': histogram_group,
    'timeseries': timeseries_group,
}

# TODO some autoconf - generate dashboard from everything we have?
def dashboard(config):
    t = config.get("time", -3600)
    bins = config.get("bins", 60)
    left_margin = config.get("left_margin", 20)

    w = bins + left_margin + 1
    res = ["=" * w]

    title = config.get("title")
    if title is not None:
        res.append("= " + title)
        res.append("=" * w)

    for chart_group in config["charts"]:
        if not isinstance(chart_group, list):
            chart_group = [chart_group]

        values = defaultdict(list)
        for counter, chart, *args in chart_group:
            if chart in chart_types:
                values[chart].append((counter, *args))
        
        for chart_type, v in values.items():
            res.extend(chart_types[chart_type](v, bins, left_margin, t, n_lines=2))
        res.append("")
    return res


if __name__ == '__main__':
    # tests/demo   
    
    import time
    import numpy as np
    import random

    now = time.time()
    for lat in np.random.normal(size=1000):
        timestamp = now - random.randint(0, 7200)
        add('ssd_read_latency', abs(lat), timestamp=timestamp)

    conf = {
        "title": "Test Dashboard",
        "charts": [
            ('ssd_read_latency', 'histogram'),
            [
                ('ssd_read_latency', 'timeseries'),
                ('ssd_read_latency', 'timeseries', 'max'),
                ('ssd_read_latency', 'timeseries', 'min'),
            ]
        ],
        "time": -3600, # default -3600
        "bins": 40, # default 60
        "left_margin": 40, # default 20
    }
    for s in dashboard(conf):
        print(s)
