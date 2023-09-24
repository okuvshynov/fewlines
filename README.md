# fewlines

Whether we like it or not, we debug things by putting print statements around.

`fewlines` is a supplement for this, allowing to plot bar charts which only take few lines in a terminal output, but can be a very useful piece of information.

Currently python and c++20 version.

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

c++ installation:

copy header file, try out the demo:

```
$ c++ -std=c++2a -x c++ ./bar.h -I. -D__FEWLINES_DEMO_ -o /tmp/bar_demo && /tmp/bar_demo

bar_line: 
 ▁▂▃▄▄▅▆▇▇

bar_histogram: 
                ▁▁▁▁▂▃▃▄▄▅▆▆▆▆▇▇▇▇▆▆▅▅▄▃▃▂▂▁▁▁              

bar_histograms<vector<list>>: 
~~~~~~~~~~~~~ -2.59|~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|2.99
~~~~~~~~~~~~~~~ one| ▁ ▁ ▁▁ ▂ ▁▃▁ ▃▃▂▃▃▂▂▂▄▁▆▅ ▆ ▇▇▁▄▄ ▇▃▂ ▃▂▁ ▂ ▁   ▂          |
~~~~~~~~~~~~~~~ two|  ▁     ▁ ▁   ▃▁▂▂▃▄▂▁▂▃▃▄▅▃▇▃▂▂▄▃▅▂▃▁▂▁▁▃▁▂  ▂             |

bar_histograms<map<vector>>: 
~~~~~~~~~~~~~~ -3.6|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~~~|3.02
~~~~~~~~~~~~~~ four|              ▁▁   ▁▁▂▂▃▂▄▃▅▅▃▅▅▆▄▇▇▆▆▃▅▅▂▃▁▁▁▁ ▁           |
~~~~~~~~~~~~~ three|               ▂  ▂▂▃▃▂▂▅▄▇▂▅▆▅▅▄▃▂▅▄▅▃▄▅▂▂▄▂ ▂▁▁           |

bar_histograms<map<set>>: 
~~~~~~~~~~~~~ -3.26|~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|3.8
~~~~~~~~~~~~~~ five|         ▁▁▁▁▁▁▄▁▄▂▄▃▇▇▄▅▇▄▆▄▇▄▆▄▆▅▄▁▄▂▁▂▁▁▁                |
~~~~~~~~~~~~~~~ six|            ▁▁▁▂▃▂▃▄▃▄▅▃▄▆▇▆▇▅▄▄▄▄▄▃▅▂▁▂ ▁▁▁▁               |
```

## Usage example


python
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

c++
```
c++ -std=c++2a -x c++ ./bar.h -I. -D__FEWLINES_DEMO_ -o ./bar_demo && ./bar_demo
```
