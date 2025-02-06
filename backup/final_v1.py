import sys
import time
from queue import PriorityQueue

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import hilbert_trans

# 版本 1

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = sys.maxsize
        self.hx = sys.maxsize

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.hx < other.hx
        return self.cost < other.cost


class Map:
    """
        Map 的大小为 2^n * 2^n, n 为曲线的阶
        x: [0, 2^n - 1] y: [0, 2^n - 1]
    """

    def __init__(self, n):
        self.size = 2 ** n
        self.obstacle = np.zeros((self.size, self.size), dtype=int)

    def add_obstacle(self, x, y):
        self.obstacle[x][y] = 1

    def is_valid_point(self, x, y):  # 无效点
        if x < 0 or y < 0 or x >= self.size or y >= self.size or self.obstacle[x][y] == 1:
            return False
        return True


class HilbertStar:
    def __init__(self, mp: Map, vec, n: int):
        self.n = n
        self.mp = mp
        self.vec = vec


    def run_algorithm(self):
        path = []
        while True:
            flag = 0
            for v in self.vec:
                if v[0] == v[1]:
                    flag = 1
            if flag == 1:
                break

            ind = -1
            t_min = sys.maxsize
            for i, v in enumerate(self.vec):
                if t_min > abs(v[0] - v[1]):
                    t_min = abs(v[0] - v[1])
                    ind = i

            self.vec[ind][0] = self.vec[ind][0] - (self.vec[ind][0] - self.vec[ind][1]) // abs(self.vec[ind][0] - self.vec[ind][1])

            if ind == 0:
                x, y = hilbert_trans.d2xy_up(self.n, self.vec[0][0])
                self.vec[1][0] = hilbert_trans.xy2d_down(self.n, x, y)
                self.vec[2][0] = hilbert_trans.xy2d_left(self.n, x, y)
                self.vec[3][0] = hilbert_trans.xy2d_right(self.n, x, y)
                path.append([x, y])
            elif ind == 1:
                x, y = hilbert_trans.d2xy_down(self.n, self.vec[1][0])
                self.vec[0][0] = hilbert_trans.xy2d_up(self.n, x, y)
                self.vec[2][0] = hilbert_trans.xy2d_left(self.n, x, y)
                self.vec[3][0] = hilbert_trans.xy2d_right(self.n, x, y)
                path.append([x, y])
            elif ind == 2:
                x, y = hilbert_trans.d2xy_left(self.n, self.vec[2][0])
                self.vec[0][0] = hilbert_trans.xy2d_up(self.n, x, y)
                self.vec[1][0] = hilbert_trans.xy2d_down(self.n, x, y)
                self.vec[3][0] = hilbert_trans.xy2d_right(self.n, x, y)
                path.append([x, y])
            elif ind == 3:
                x, y = hilbert_trans.d2xy_right(self.n, self.vec[3][0])
                self.vec[0][0] = hilbert_trans.xy2d_up(self.n, x, y)
                self.vec[1][0] = hilbert_trans.xy2d_down(self.n, x, y)
                self.vec[2][0] = hilbert_trans.xy2d_left(self.n, x, y)
                path.append([x, y])
        return path


# 服务器只有曲线信息
if __name__ == '__main__':
    n = 4
    mp = Map(n)

    # 运行
    st = Point(6, 1)
    en = Point(15, 0)

    vec = []
    a, b = hilbert_trans.xy2d_up(n, st.x, st.y), hilbert_trans.xy2d_up(n, en.x, en.y)
    vec.append([a, b])
    a, b = hilbert_trans.xy2d_down(n, st.x, st.y), hilbert_trans.xy2d_down(n, en.x, en.y)
    vec.append([a, b])
    a, b = hilbert_trans.xy2d_left(n, st.x, st.y), hilbert_trans.xy2d_left(n, en.x, en.y)
    vec.append([a, b])
    a, b = hilbert_trans.xy2d_right(n, st.x, st.y), hilbert_trans.xy2d_right(n, en.x, en.y)
    vec.append([a, b])
    print(vec)

    hilbert_star = HilbertStar(mp, vec, n)
    re = hilbert_star.run_algorithm()
    print(re)
    dis = abs(st.x - en.x) + abs(st.y - en.y)
    print(dis / len(re))

    #
    # 画图
    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    ax.set_xlim([0, mp.size])
    ax.set_ylim([0, mp.size])

    for i in range(mp.size):
        for j in range(mp.size):
            if mp.obstacle[i][j] == 1:
                rec = Rectangle((i, j), width=1, height=1, facecolor='gray')
                ax.add_patch(rec)
            else:
                rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
                ax.add_patch(rec)
    for v in re:
        rec = Rectangle((v[0], v[1]), width=1, height=1, edgecolor='gray', facecolor='g')
        ax.add_patch(rec)
    rec = Rectangle((en.x, en.y), width=1, height=1, edgecolor='gray', facecolor='r')
    ax.add_patch(rec)


    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

