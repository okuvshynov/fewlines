# fewlines

Whether we like it or not, we debug things by putting print statements around.

`fewlines` is a supplement for this, allowing to plot bar charts which only take few lines in a terminal output, but can be a very useful piece of information.

Requires Unicode block characters.
Horizon-style color output requires terminal with 256 ANSI colors.
Monochrome version can be used for logging distributions to text files. 

Example: plotting distribution of weights, gradients and activations for layers in LoRA neural net modules:

```
=== WEIGHTS ===
~~~~~~~~~ -0.000912|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|0.000912
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

Installation:
```
pip install fewlines
```

## Usage example

```
import numpy as np
data = {'title_A': list(np.random.normal(size=10000))}

# horizon with colors - works in terminals with ANSI color codes support
for l in bar_histograms(data, chart_width=40, color='green'):
    print(l)

# bar chart without colors - can be used in text log files, as long as Unicode characters are available
for l in bar_histograms(data, chart_width=40):
    print(l)

```
