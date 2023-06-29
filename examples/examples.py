import sys
sys.path.append('../fewlines')

from fewlines import horizon

def one_char_one_color():
    print(horizon([0, 10, 11, 12, 0, 13], colors=[-1, 0], chrs=[' ', '#']))
    print(horizon([i for i in range(10)], colors=[-1, 0], chrs=[' ', '#']))

def negatives_ignored():
    print(horizon([0, 10, 11, -3, 0, 13], colors=[-1, 0], chrs=[' ', '#']))

def bubble():
    print(horizon([i for i in range(10)], colors=[-1, 0], chrs=[' ', '.', 'o', 'O']))

def monochrome():
    print(horizon([i for i in range(80)], colors=[-1, 0]))

def default():
    print(horizon([i for i in range(80)]))

def shades_of_gray():
    print(horizon([i for i in range(80)], colors=[-1]+[i for i in range(255, 232, -1)]))

if __name__ == '__main__':
    one_char_one_color()
    negatives_ignored()
    bubble()
    monochrome()
    default()
    shades_of_gray()
