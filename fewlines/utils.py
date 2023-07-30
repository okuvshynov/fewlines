import math

def histogram(data, bins, scale_range=None, ignore_outliers=False):
    # If a range is specified, use it. Otherwise, use the min/max of the data.
    min_val = scale_range[0] if scale_range else min(data)
    max_val = scale_range[1] if scale_range else max(data)
    
    # Create the bins. We'll have one more bin edge than the number of bins.
    bin_edges = [min_val + i * (max_val - min_val) / bins for i in range(bins + 1)]
    
    # Initialize the bin counts to zero.
    bin_counts = [0] * bins

    # Count the data points in each bin.
    for x in data:
        if x is None or x is math.isnan(x):
            continue
        if x < min_val or x > max_val:
            if ignore_outliers:
                continue
            else:
                bin_index = 0 if x < min_val else bins - 1
        else:
            bin_index = min(int((x - min_val) * bins / (max_val - min_val)), bins - 1)
        bin_counts[bin_index] += 1
    
    return bin_counts, bin_edges


def percentile(n, percentile):
    index = percentile * (len(n) - 1) / 100
    if (len(n) - 1) % 100 == 0:
        return sorted(n)[int(index)]
    else:
        lower = sorted(n)[int(index)]
        upper = sorted(n)[int(index) + 1]
        interpolation = index - int(index)
        return lower + (upper - lower) * interpolation

def compute_stats(numbers):
    if not numbers:
        return None
    
    numbers = sorted(numbers)  # It's better to sort the numbers only once
    min_num = numbers[0]
    max_num = numbers[-1]
    p25 = percentile(numbers, 25)
    p50 = percentile(numbers, 50)
    p75 = percentile(numbers, 75)

    return min_num, max_num, p25, p50, p75

# for things like min/max for dict of lists
def global_stat(numbers, fn):
    res = None
    if numbers:  # check if dictionary is not empty
        non_empty_values = [fn(v) for v in numbers.values() if v]
        if non_empty_values:
            res = fn(non_empty_values) 
    return res