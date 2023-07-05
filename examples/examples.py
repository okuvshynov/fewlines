import sys
sys.path.append('../fewlines')

from horizon import horizon_line, horizon_histogram, print_histogram, print_histograms

def one_char_one_color():
    print(horizon_line([0, 10, 11, 12, 0, 13], colors=[-1, 0], chrs=[' ', '#']))
    print(horizon_line([i for i in range(10)], colors=[-1, 0], chrs=[' ', '#']))

def negatives_ignored():
    print(horizon_line([0, 10, 11, -3, 0, 13], colors=[-1, 0], chrs=[' ', '#']))

def bubble():
    print(horizon_line([i for i in range(10)], colors=[-1, 0], chrs=[' ', '.', 'o', 'O']))

def monochrome():
    print(horizon_line([i for i in range(80)], colors=[-1, 0]))

def default():
    print(horizon_line([i for i in range(80)]))

def shades_of_gray():
    print(horizon_line([i for i in range(80)], colors=[-1]+[i for i in range(255, 232, -1)]))

def histogram_empty():
    print(horizon_histogram([])[0])

def histograms():
    print(horizon_histogram([0])[0])
    for bincount in range(1, 6):
        print(horizon_histogram([0, 1, 2, 3, 4, 5, 5, 5, 5], bins=bincount)[0])

    chart, domain = horizon_histogram([i for i in range (100)])
    print(f'{chart} [{domain}]')

    print_histograms([('A', [10, 20, 30, 10, 20, 30]), ('B', [1, 2, 3, 0.00001])])
    print_histograms({'A': [10, 20, 30, 10, 20, 30], 'B': [1, 2, 3, 0.00001]})

if __name__ == '__main__':
    one_char_one_color()
    negatives_ignored()
    bubble()
    monochrome()
    default()
    shades_of_gray()
    histogram_empty()
    histograms()
