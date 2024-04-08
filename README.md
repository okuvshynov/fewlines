# fewlines - log your dashboard

Whether we like it or not, we debug things by putting print statements around.

`fewlines` is a supplement for this, allowing to plot bar charts which only take few lines in a terminal output, but can be a very useful piece of information.
In a more extended form fewlines can be used for logging collections of charts in a dashboard-like form.

Currently python
c++ and js versions in progress and experimental.

Requires Unicode block characters.
Horizon-style color output requires terminal with 256 ANSI colors.
Monochrome version can be used for logging distributions to text files. 

Example: plotting distribution of weights, gradients and activations for layers in LoRA neural net modules:

```
=== WEIGHTS ===
~~~~~~~~~ -0.000912|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|0.000912
               Q0.B|▃▇▅▄▄▃▃▃▃▂▂▂▃▂▂▂▂▂▂▂▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▂▃▃▂▂▂▂▃▃▃▃▄▄▆▇▃|
               V0.B|▁▆▇▇▆▅▄▃▃▄▃▃▃▃▃▃▃▂▂▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▂▃▃▃▃▃▃▃▃▃▄▄▅▆▇▇▆▁|
               Q1.B|▃▇▇▇▅▅▄▄▃▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▂▃▃▃▃▃▃▃▃▂▃▃▃▃▃▃▃▃▃▃▃▃▄▄▅▅▆▇▇▃|
               V1.B|▂▇▇▆▅▄▄▃▃▂▂▂▂▂▂▂▂▁▂▂▁▂▁▁▁▁▁▁▁▁▁▁▁▂▁▁▁▂▁▂▂▁▁▂▂▂▂▂▂▂▂▂▃▄▅▅▆▇▇▂|
               Q2.B|▂▆▇▆▅▄▃▃▃▃▃▃▃▃▃▃▂▃▃▃▃▂▃▃▂▂▂▂▂▃▂▂▃▂▃▃▂▃▃▂▃▃▃▃▃▃▃▃▃▃▃▃▃▄▄▅▆▇▇▂|
               V2.B|▂▇▇▆▅▄▃▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▁▁▂▂▂▁▁▂▁▁▂▁▁▁▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▃▃▄▅▆▇▇▂|
               Q3.B|▃▇▇▇▅▅▄▄▃▃▃▃▃▃▃▃▂▃▂▂▂▂▂▂▂▂▂▂▂▃▂▂▂▂▂▂▂▂▂▂▃▂▂▃▃▂▃▃▃▃▃▃▄▄▅▅▆▇▇▃|
               V3.B|▃▇▇▆▅▄▃▂▂▂▂▂▂▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▂▂▂▂▂▃▄▄▆▇▇▃|
               Q4.B|▂▆▇▇▅▅▄▃▃▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▁▁▂▁▁▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▃▄▅▅▆▇▆▂|
               V4.B|▃▇▆▅▄▃▂▂▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▂▃▄▅▆▇▃|
               Q5.B|▃▇▇▆▆▅▄▄▃▃▃▃▃▃▃▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▂▃▃▂▂▃▂▃▃▃▃▃▄▄▄▅▆▇▇▆▃|
               V5.B|▃▇▆▅▄▃▂▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▂▂▃▄▅▆▇▄|
               Q6.B|▃▇▇▆▅▄▃▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▁▁▂▂▂▂▂▁▁▂▁▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▃▄▅▆▇▇▃|
               V6.B|▄▇▆▄▃▃▂▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▃▄▅▆▇▃|
               Q7.B|▃▇▇▆▅▄▄▃▃▃▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▃▃▃▄▅▆▇▇▃|
               V7.B|▄▇▆▄▃▂▂▁▁▁▁▁▁▁▁▁▁▁▁ ▁▁   ▁▁      ▁   ▁  ▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▃▄▆▇▅|
               Q8.B|▄▇▆▅▄▃▃▂▂▂▂▂▂▂▂▂▂▂▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▁▂▁▂▂▂▂▂▂▂▃▃▃▄▅▆▇▄|
               V8.B|▅▇▅▄▃▂▂▁▁▁▁▁▁▁▁▁▁▁  ▁▁ ▁▁            ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▃▄▅▇▅|
```

As we can see, it's very compact, can be put to log files with any other relevant info and gives a good insight into what do weights look like: bimodal, close to 1e-4, earlier layers move closer to center. 

While created originally to plot distributions of weights/gradients or ML models it is not restricted to ML use cases, obviously. Can be used to show latency distribution, for example.

python installation:
```
pip install fewlines
```


## Usage example



### Basic charts

```
from fewlines import charts as fc
import numpy as np

A = np.random.normal(size=100)
print('Just the list of numbers')
for l in fc.histogram_chart(A):
    print(l)
print('the list of numbers with extra options')
for l in fc.histogram_chart((A, {'n_lines': 3})):
    print(l)
print('the dict title -> numbers')
for l in fc.histogram_chart({'series_A': A}):
    print(l)
print('the dict title -> numbers, options')
for l in fc.histogram_chart({'series_A': (A, {'n_lines': 3})}):
    print(l)
```

Output:
Note that multi-line charts rendering might depend on terminal spacing settings. Here in markdown it is messed up, so I'm attaching it as image.

<img width="516" alt="Screenshot 2024-04-04 at 11 20 12 AM" src="https://github.com/okuvshynov/fewlines/assets/661042/89c8d036-9e86-400c-83ff-47bc35affd59">


### Dashboards

```
from fewlines import metrics as fm
from fewlines import dashboard as fd
import numpy as np
import time

# logging data somewhere
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
    "title_width": 40, # default 30
    "n_lines": 3,
    "color": None,
}
print('\n## detailed complicated config with different aggregations')
for s in fd.dashboard(conf):
    print(s)
```

Output:

<img width="668" alt="Screenshot 2024-04-04 at 11 18 33 AM" src="https://github.com/okuvshynov/fewlines/assets/661042/5c95a06d-1182-44b8-a4af-9949ca8b68a7">
