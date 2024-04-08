import math 

def _bin_index(min_val, max_val, bins, x):
    if min_val == max_val:
        if x == min_val:
            return bins // 2
        return 0 if x < min_val else bins - 1
    bin_index = int((x - min_val) * bins / (max_val - min_val))
    return max(0, min(bin_index, bins - 1))

def _histogram(data, bins, min_val, max_val):    
    # Initialize the bin counts to zero.
    bin_counts = [0] * bins

    # Count the data points in each bin.
    for x in data:
        if x is None or x is math.isnan(x):
            continue
        bin_counts[_bin_index(min_val, max_val, bins, x)] += 1
    
    return bin_counts

# for things like min/max for dict of str: tuple(list, {})
def _global_stat(numbers, fn):
    res = None
    if numbers:  # check if dictionary is not empty
        non_empty_values = [fn(v) for v, _ in numbers.values() if len(v) > 0]
        if non_empty_values:
            res = fn(non_empty_values) 
    return res

def _global_range(numbers):
    mn = _global_stat(numbers, min)
    mx = _global_stat(numbers, max)

    if mn is None or mx is None:
        mn, mx = 0.0, 0.0
    return mn, mx

def _line_header(left_label, right_label, bins, title_width):
    mn_text, mx_text = f' {left_label}|'[-title_width:], right_label
    
    line = '~' * bins
    
    if title_width <= 0:
        return line + f'|{mx_text}'
    return '~' * (title_width - len(mn_text)) + mn_text + line + f'|{mx_text}'

def _header(mn, mx, bins, title_width, show_zero=True):
    mn_text, mx_text = f' {mn:.3g}|'[-title_width:], f'{mx:.3g}'
    
    zero_at = _bin_index(mn, mx, bins, 0.0) if mn <= 0 and mx >= 0 and show_zero else None
    line = ''.join(['0' if b == zero_at else '~' for b in range(bins)])
    
    if title_width <= 0:
        return line + f'|{mx_text}'
    return '~' * (title_width - len(mn_text)) + mn_text + line + f'|{mx_text}'