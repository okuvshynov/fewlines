# basic primitives to just write single line/multiple lines 
# without any aggregation/bucketing
# is the building block for charts.py

# not using the largest block so that two histograms on two lines won't collide
bar_blocks =      [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇']
bar_blocks_full = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
# For horizon we can use the largest block, as we'll use color coding
horizon_blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def _clamp(v, a ,b):
    return max(a, min(v, b))

def multiline(y, n_lines=4, max_y=None, cells=bar_blocks_full, top_cells=bar_blocks):
    if not y:
        return [""], 0

    max_y = max(y) if max_y is None else max_y
    if max_y == 0:
        return [cells[0] * len(y) for _ in range(n_lines)], 0
    n_cells = len(cells)
    n_top_cells = len(top_cells)

    ##
    # here's an example, imagine we have 3 blocks [' ', '▄', '█']
    # we need to take into account the lower level '█' + upper level ' ' represent same value. 
    # Example with 4 layers:
    #                                ' ', '▄'        
    #                      ' ', '▄', '█'        
    #            ' ', '▄', '█'    
    #  ' ', '▄', '█'
    n_multicells = (n_lines - 1) * (n_cells - 1) + n_top_cells

    multicell_idx = lambda v: _clamp(int(v * n_multicells / max_y), 0, n_multicells - 1)
    idxs = [multicell_idx(v) for v in y]

    res = []
    for li in range(n_lines):
        # this is max possible value (index) representable by all layers below current
        below = (n_cells - 1) * (n_lines - li - 1)
        curr_cells = top_cells if li == 0 else cells
        mind = len(curr_cells) - 1
        res.append("".join([curr_cells[_clamp(idx - below, 0, mind)] for idx in idxs]))

    return res, max_y

def line(y, max_y=None, cells=bar_blocks) -> str:
    s, max_y = multiline(y, n_lines=1, max_y=max_y, top_cells=cells)
    return s[0], max_y


# colorschemes in 256 ansi colors 
colors = {
    'green': [-1, 150, 107, 22],
    'red'  : [-1, 196, 124, 52],
    'gray' : [-1, 252, 248, 244, 240, 236],
}

def gen_horizon_blocks(n_lines, cells=horizon_blocks):
    res = []
    for i in range(n_lines):
        lower = []
        upper = []
        
        for j in range(i):
            lower.append(cells[-1])
        for j in range(i + 1, n_lines):
            upper.append(cells[0])


        # the one we are filling in now:
        for b in cells[1:]:
            res.append(lower + [b] + upper)

    return res

# for horizon multiline it might be a good idea to leave 
# one entire line empty in case of adjacent horizon charts
def horizon_multiline(y, n_lines=4, max_y=None, color='green', cells=horizon_blocks):
    if not y:
        return "", 0

    max_y = max(y) if max_y is None else max_y
    if max_y == 0:
        return [cells[0] * len(y) for _ in range(n_lines)], 0
    bg = [f'\33[48;5;{c}m' if c >= 0 else '' for c in colors[color]]
    fg = [f'\33[38;5;{c}m' if c >= 0 else '' for c in colors[color]]
    rst = '\33[0m'

    multiline_blocks = gen_horizon_blocks(n_lines, cells)
    cells = [(f'{fg[1]}{bg[0]}',  [cells[0]] * n_lines)] + [(f'{f}{b}', mb) for f, b in zip(fg[1:], bg[:-1]) for mb in multiline_blocks]
    n_cells = len(cells)

    multicell_idx = lambda v: _clamp(int(v * n_cells / max_y), 0, n_cells - 1)
    idxs = [multicell_idx(v) for v in y]

    res = []
    for li in range(n_lines):
        fmt_cell = lambda idx: f'{cells[idx][0]}{cells[idx][1][n_lines - li - 1]}{rst}'
        res.append("".join(fmt_cell(idx) for idx in idxs))

    return res, max_y

def horizon_line(y, max_y=None, color='green', cells=horizon_blocks) -> str:
    s, max_y = horizon_multiline(y, n_lines=1, color=color, cells=cells) 
    return s[0], max_y


if __name__ == '__main__':
    gen_horizon_blocks(3)
    for l in multiline([i for i in range(100)], n_lines=4, cells=[' ', '▄', '█'], top_cells=[' ', '▄'])[0]:
        print(l)

    for l in horizon_multiline([i for i in range(100)], n_lines=4, cells=[' ', '▄', '█'])[0]:
        print(l)