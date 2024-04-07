from collections import defaultdict

from fewlines.metrics import histogram_group, timeseries_group, add, counter_expand

chart_types = {
    'histogram': histogram_group,
    'timeseries': timeseries_group,
}

def dashboard(config):
    # these are global settings, no override
    t = config.get("time", -3600)
    bins = config.get("bins", 60)
    left_margin = config.get("left_margin", 30)

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
            new_group = []
            for counter_name, chart_type, *args in chart_group:
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