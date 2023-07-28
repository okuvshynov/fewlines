import math

# returns boxplot from 1 series in a list of size 'width'
def _boxplot_chart(numbers, mn, mx, width=80):
    if not (width > 0):
        # TODO: raise something
        return '' 
    scale = lambda v: max(0, min(width - 1, int(width * 1.0 * (v - mn) / (mx - mn))))
    res = [' '] * width
    if len(numbers) == 0:
        return res

    min_num, max_num, p25, p50, p75 = _compute_stats(numbers)
    p25i = scale(p25)
    p75i = scale(p75)
    p50i = scale(p50)
    min_i = scale(min_num)
    max_i = scale(max_num)

    for i in range(min_i + 1, p25i):
        res[i] = '-'
    for i in range(p75i + 1, max_i):
        res[i] = '-'
    for i in range(p25i + 1, p75i):
        res[i] = '='
    
    res[min_i] = '|'
    res[max_i] = '|'

    if p50i == p25i and p50i == p75i:
        # 1 symbol for 3 marks. Use median
        res[p50i] = ':'
    else:
        # we have at least 2 symbols for 3 marks. In this case, p50 might get overwritten
        # TODO: this is confusing if p50 is overwritten but p25 and p75 are far from each other 
        res[p50i] = ':'
        res[p25i] = '['
        res[p75i] = ']'

    return res

def _boxplot_line(numbers, mn, mx, title='', chart_width=80, left_margin=20):
    chart = _boxplot_chart(numbers, mn, mx, width=chart_width)
    if left_margin <= 0:
        left = ''
    else:
        title = f'{title}|'
        left = f'{title}'[-left_margin:]
        left = f"{left:>{left_margin}}"
    
    right = '|'
    return left + ''.join(chart) + right

def _axis_str(mn, mx, chart_width=80, left_margin=20):
    mn_text, mx_text = f' {mn:.3g}|'[-left_margin:], f'{mx:.3g}'
    if left_margin <= 0:
        return '_' * chart_width + f'|{mx_text}'
    return '~' * (left_margin - len(mn_text)) + mn_text + '~' * chart_width + f'|{mx_text}'

def boxplot(numbers, title='', chart_width=80, axis=True, left_margin=20):
    mn = min(numbers)
    mx = max(numbers)
    res = _boxplot_line(numbers, mn, mx, title=title)

    if axis:
        return [_axis_str(mn, mx, chart_width=chart_width, left_margin=left_margin), res]
    return [res]
 
def boxplot_table(numbers, chart_width=80, axis=True, left_margin=20):
    mn = min(min(v) for v in numbers.values())
    mx = max(max(v) for v in numbers.values())
    res = []
    if axis:
        res.append(_axis_str(mn, mx, chart_width=chart_width, left_margin=left_margin))
    for title, values in numbers.items():
        res.append(_boxplot_line(values, mn, mx, title=title, chart_width=chart_width, left_margin=left_margin))
    return res

def _percentile(n, percentile):
    index = percentile * (len(n) - 1) / 100
    if (len(n) - 1) % 100 == 0:
        return sorted(n)[int(index)]
    else:
        lower = sorted(n)[int(index)]
        upper = sorted(n)[int(index) + 1]
        interpolation = index - int(index)
        return lower + (upper - lower) * interpolation

def _compute_stats(numbers):
    numbers = sorted(numbers)  # It's better to sort the numbers only once
    min_num = numbers[0]
    max_num = numbers[-1]
    p25 = _percentile(numbers, 25)
    p50 = _percentile(numbers, 50)
    p75 = _percentile(numbers, 75)

    return min_num, max_num, p25, p50, p75

if __name__ == '__main__':
    data = {
        'A': [1, 2, 3,4, 100],
        'B': [-10, -5, -1, -2, -3, -1],
        'C': [10, 20, 30, 40, 50, 60],
        'D': [0, 10, 50, 60, 50, 50, 50, 50],
        'E': [-5, -4, -3, -2, -1, -1, -1, -1, -1, 1],
        'F': [1]
    }
    for l in boxplot_table(data, chart_width=80, left_margin=20):
        print(l)

    print()
    
    for l in boxplot([1,2], title='2 poindsjkfhkajsdhflkajsdhflkasdjhfts'):
        print(l)