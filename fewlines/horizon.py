# base function, returns a horizon-formatted string suitable for printing in the terminal

default_green = [-1, 150, 107, 22]
default_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def horizon_line(y, colors=default_green, chrs=default_blocks) -> str:
    bg = [f'\33[48;5;{c}m' if c >= 0 else '' for c in colors]
    fg = [f'\33[38;5;{c}m' if c >= 0 else '' for c in colors]
    rst = '\33[0m'
    cells = [f'{f}{b}{c}{rst}' for f, b in zip(fg[1:], bg[:-1]) for c in chrs]
    Y = max(y)
    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: cells[clamp(int(v * len(cells) / Y), 0, len(cells) - 1)]
    horizon = ''.join([cell(v) for v in y])
    return horizon

def _horizon_list(series, bins, shared_scale):
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy is required to use _horizon_list.")
    if shared_scale:
        scale_range = (min(v.min() for _, v in series), max(v.max() for _, v in series))
        interval = scale_range
    res = []
    for name, values in series:
        if shared_scale:
            hist_values, _ = np.histogram(values, bins=bins, range=scale_range)
        else:
            interval = (min(values), max(values))
            hist_values, _ = np.histogram(values, bins=bins)
        
        res.append((name, horizon_line(y=hist_values), interval))

    return res

def horizon_torch_weights(model, bins=80, module_prefix='', shared_scale=True):
    weights = []
    for name, module in model.named_modules(prefix=module_prefix):
        # Check if the module has a weight attribute
        if hasattr(module, 'weight'):
            # Get the weight tensor
            weight = module.weight.data

            # Flatten the weight tensor
            weight_flat = weight.view(-1).cpu().numpy()
            weights.append((name, weight_flat))

    return _horizon_list(weights, bins, shared_scale)


def horizon_torch_gradients(model, bins=80, module_prefix='', shared_scale=True):
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy is required to use horizon_torch_gradients.")
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
    return _horizon_list(grads, bins, shared_scale)