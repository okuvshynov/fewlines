from boxplot import boxplot_table
from bar import bar_histograms

if __name__ == '__main__':
    data = {
        'A': [1, 2, 3,4, 100],
        'B': [-10, -5, -1, -2, -3, -1],
        'C': [10, 20, 30, 40, 50, 60],
        'D': [0, 10, 50, 60, 50, 50, 50, 50],
        'E': [-5, -4, -3, -2, -1, -1, -1, -1, -1, 1],
        'F': [1]
    }

    print(f'\n=== BOXPLOT ===')
    for l in boxplot_table(data):
        print(l)


    print(f'\n=== BAR CHART ===')
    for l in bar_histograms(data):
        print(l)

    print(f'\n=== HORIZON CHART ===')
    for l in bar_histograms(data, color='green'):
        print(l)