

def d2xy_1(SIDE, id):
    x = id // SIDE
    y = id % SIDE
    if x % 2 == 1:
        y = SIDE - y - 1
    return x, y


def d2xy_2(SIDE, id):
    x = id // SIDE
    y = id % SIDE
    if x % 2 == 1:
        y = SIDE - y - 1
    return rot90(SIDE, x, y)

def xy2d_1(SIDE, x, y):
    d = x * SIDE
    if x % 2 == 1:
        d += SIDE - y - 1
    else:
        d += y
    return d


def xy2d_2(SIDE, x, y):
    x, y = rot270(SIDE, x, y)
    d = x * SIDE
    if x % 2 == 1:
        d += SIDE - y - 1
    else:
        d += y
    return d


def rot90(n, x, y):
    return y, n - 1 - x

def rot270(n, x, y):
    return n - 1 - y, x


if __name__ == '__main__':
    N = 3
    for i in range(2 ** N):
        for j in range(2 ** N):
            d = xy2d_2(2 ** N, i, j)
            x, y = d2xy_2(2 ** N, d)
            if x != i or y != j:
                print(i, j, d)


