import random
import time

import numpy

"""
    完成 Hilbert 曲线，1 维和 2 维坐标的相互转换
"""


def d2xy_down(n: int, d: int):
    """ n: 曲线的阶   d: 曲线的 id 编号 """
    return fast_d2xy(n, d)


def xy2d_down(n: int, x: int, y: int):
    """ n: 曲线的阶   x, y: 方格坐标"""
    return fast_xy2d(n, x, y)


def d2xy_left(n: int, d: int):
    """ n: 曲线的阶  d: 曲线的 id 编号 """
    x, y = fast_d2xy(n, d)
    return rot90(2**n, x, y)


def xy2d_left(n: int, x: int, y: int):
    """ n: 曲线的阶   x, y: 方格坐标 """
    x, y = rot270(2 ** n, x, y)
    return fast_xy2d(n, x, y)


def d2xy_up(n: int, d: int):
    """ n: 曲线的阶 d: 曲线的 id 编号 """
    x, y = fast_d2xy(n, d)
    return rot180(2**n, x, y)


def xy2d_up(n: int, x: int, y: int):
    """ n: 曲线的阶   x, y: 方格坐标 """
    x, y = rot180(2 ** n, x, y)
    return fast_xy2d(n, x, y)


def d2xy_right(n: int, d: int):
    """ n: 曲线的阶  d: 曲线的 id 编号 """
    x, y = fast_d2xy(n, d)
    return rot270(2**n, x, y)


def xy2d_right(n: int, x: int, y: int):
    """ n: 曲线的阶   x, y: 方格坐标"""
    x, y = rot90(2 ** n, x, y)
    return fast_xy2d(n, x, y)


def fast_d2xy(n, d):
    """将一维 Hilbert 索引 d 转换为二维坐标 (x, y)。"""
    x = y = 0
    t = d
    s = 1
    while s < (1 << n):  # 循环直到 s 达到 2^n
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            # 交换 x 和 y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def rot90(n, x, y):
    return y, n - 1 - x


def rot180(n, x, y):
    return n - 1 - x, n - 1 - y


def rot270(n, x, y):
    return n - 1 - y, x


def fast_xy2d(n, x, y):
    """将二维坐标 (x, y) 转换为 Hilbert 曲线上的一维索引 d。"""
    d = 0
    s = 1 << (n - 1)  # s 是当前要处理的位
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s * s * ((3 * rx) ^ ry)  # 计算当前子块的索引贡献
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            # 交换 x 和 y
            x, y = y, x
        s //= 2
    return d


if __name__ == '__main__':
    # Hilbert 转换时间测试----------------------------------------------------------------
    for i in range(1, 9):
        N = 128 * i
        SIDE = 2 ** N
        MAX_ID = SIDE * SIDE

        x = random.randint(0, SIDE - 1)
        y = random.randint(0, SIDE - 1)

        start_time = time.time()
        for _ in range(1000):
            d = d2xy_up(N, 1)
        end_time = time.time()
        print(f"N = {N}; 时间 {1000 * end_time - 1000 * start_time} ms")
