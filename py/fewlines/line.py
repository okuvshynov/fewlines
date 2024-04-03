# primitives to just write single line/multiple lines without any aggregation/bucketing

# not using the largest block so that two histograms on two lines won't collide
bar_blocks =      [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇']
bar_blocks_full = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

# bar_line plots a line using provided blocks or default bar_blocks
def bar_line(y, max_y=None, cells=bar_blocks) -> str:
    if not y:
        return "", 0

    max_y = max(y) if max_y is None else max_y
    if max_y == 0:
        return cells[0] * len(y), 0
    n_cells = len(cells)

    clamp = lambda v, a, b: max(a, min(v, b))
    cell = lambda v: cells[clamp(int(v * n_cells / max_y), 0, n_cells - 1)]
    return ''.join([cell(v) for v in y]), max_y

def bar_multiline(y, n_lines=4, max_y=None, cells=bar_blocks_full, top_cells=bar_blocks):
    if not y:
        return "", 0

    max_y = max(y) if max_y is None else max_y
    if max_y == 0:
        return [cells[0] * len(y) for _ in range(n_lines)], 0
    clamp = lambda v, a, b: max(a, min(v, b))
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

    multicell_idx = lambda v: clamp(int(v * n_multicells / max_y), 0, n_multicells - 1)
    idxs = [multicell_idx(v) for v in y]

    res = []
    for li in range(n_lines):
        # this is max possible value (index) representable by all layers below current
        below = (n_cells - 1) * (n_lines - li - 1)
        curr_cells = top_cells if li == 0 else cells
        mind = len(curr_cells) - 1
        res.append("".join([curr_cells[clamp(idx - below, 0, mind)] for idx in idxs]))

    return res, max_y

if __name__ == '__main__':
    for l in bar_multiline([i for i in range(100)], n_lines=4, cells=[' ', '▄', '█'], top_cells=[' ', '▄'])[0]:
        print(l)