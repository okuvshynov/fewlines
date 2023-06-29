try:
    import numpy as np
    has_nupmy = True
except ImportError:
    has_nupmy = False

default_green = [-1, 150, 107, 22]
default_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def horizon_line(y, colors=default_green, chrs=default_blocks) -> str:
    bg = [f'\33[48;5;{c}m' if c >= 0 else '' for c in colors]
    fg = [f'\33[38;5;{c}m' if c >= 0 else '' for c in colors]
    rst = '\33[0m'
    cells = [f'{f}{b}{c}{rst}' for f, b in zip(fg[1:], bg[:-1]) for c in chrs]
    Y = max(y)
    if Y == 0:
        return chrs[0] * len(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: cells[clamp(int(v * len(cells) / Y), 0, len(cells) - 1)]
    horizon = ''.join([cell(v) for v in y])
    return horizon

# returns a tuple of ('line', (x_min, x_max))
def horizon_histogram(values, bins=40, scale_range=None):
    if not has_nupmy:
        raise ImportError("numpy is required to use horizon_histogram.")
    values, bin_edges = np.histogram(values, bins, scale_range)
    return horizon_line(values), (bin_edges[0], bin_edges[-1])

def horizon_multi_histogram(series, bins, shared_scale):
    if not has_nupmy:
        raise ImportError("numpy is required to use horizon_multi_histogram.")
    
    scale_range = (min(v.min() for _, v in series), max(v.max() for _, v in series)) if shared_scale else None

    res = []
    for name, values in series:
        line, interval = horizon_histogram(values, bins=bins, scale_range=scale_range)
        res.append((name, line, interval))

    return res

def print_histogram(values, title='', bins=40, scale_range=None):
    line, (a, b) = horizon_histogram(values, bins, scale_range)
    print(f'{title}: {line} [{a}; {b}]')

## Helper functions for torch

def print_torch_weights(model, bins=80, module_prefix='', shared_scale=True):
    weights = []
    for name, module in model.named_modules(prefix=module_prefix):
        # Check if the module has a weight attribute
        if hasattr(module, 'weight'):
            weights.append((name, module.weight.data.view(-1).cpu().numpy()))
        
    for name, chart, (a, b) in horizon_multi_histogram(weights, bins=bins, shared_scale=shared_scale):
        print(f'{name}: [{a:.3f}; {b:.3f}]')
        print(f'[{chart}]')


def print_torch_gradients(model, bins=80, module_prefix='', shared_scale=True):
    if not has_nupmy:
        raise ImportError("numpy is required to use print_torch_gradients.")
    grads = []

    for name, module in model.named_modules(prefix=module_prefix):
        # Check if the module has a weight attribute
        grads_rec = []
        for param in module.parameters():
            # Get the weight tensor
            if param.grad is not None:
                grads_rec.append(param.grad.data.cpu().numpy().flatten())
        if grads_rec:
            grads_flat = np.concatenate(grads_rec)
            grads.append((name, grads_flat))

    for name, chart, (a, b) in horizon_multi_histogram(grads, bins=bins, shared_scale=shared_scale):
        print(f'{name}: [{a:.3f}; {b:.3f}]')
        print(f'[{chart}]')