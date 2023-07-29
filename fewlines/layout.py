# this will draw table, etc.

def top_axis_str(mn, mx, chart_width=60, left_margin=20):
    mn_text, mx_text = f' {mn:.3g}|'[-left_margin:], f'{mx:.3g}'
    if left_margin <= 0:
        return '_' * chart_width + f'|{mx_text}'
    return '~' * (left_margin - len(mn_text)) + mn_text + '~' * chart_width + f'|{mx_text}'