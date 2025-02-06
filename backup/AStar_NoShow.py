import sys
import time
from queue import PriorityQueue

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


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


class AStar:
    def __init__(self, mp: Map, start: Point, end: Point):
        self.mp = mp
        self.open_set = PriorityQueue()
        self.close_set = np.zeros((mp.size, mp.size), dtype=int)
        self.st = start
        self.en = end

    def base_cost(self, p: Point):  # 当前点到起始点的代价
        # Distance to start point
        return abs(p.x - self.st.x) + abs(p.y - self.st.y)

    def heuristic_cost(self, p: Point):  # 当前点到结束点的代价
        # Distance to end point
        return abs(p.x - self.en.x) + abs(p.y - self.en.y)

    def is_valid_point(self, x, y):  # 无效点
        return self.mp.is_valid_point(x, y)

    def is_st_point(self, p: Point):
        return p.x == self.st.x and p.y == self.st.y

    def is_en_point(self, p: Point):
        return p.x == self.en.x and p.y == self.en.y

    def process_point(self, x, y, parent):
        if not self.is_valid_point(x, y) or self.close_set[x][y] == 1:
            return
        p = Point(x, y)
        p.parent = parent
        p.hx = self.heuristic_cost(p)
        p.cost = p.hx + self.base_cost(p)
        self.open_set.put(p)

    def build_path(self, p):
        path = []
        while True:
            path.insert(0, p)
            if self.is_st_point(p):
                break
            else:
                p = p.parent
        return path

    def run_algorithm(self):
        self.st.cost = 0
        self.st.hx = 0
        self.open_set.put(self.st)
        while True:
            if self.open_set.empty():
                return None
            p = self.open_set.get()

            if self.is_en_point(p):
                return self.build_path(p)

            self.close_set[p.x][p.y] = 1
            vecx = [-1, 0, 1, 0]
            vecy = [0, -1, 0, 1]
            for i in range(4):
                self.process_point(p.x + vecx[i], p.y + vecy[i], p)


if __name__ == '__main__':
    mp = Map(4)
    mp.add_obstacle(5, 0)
    mp.add_obstacle(5, 1)
    mp.add_obstacle(5, 2)
    mp.add_obstacle(5, 3)
    mp.add_obstacle(5, 4)

    # 运行
    st = Point(0, 0)
    en = Point(15, 1)
    astar = AStar(mp, st, en)
    re = astar.run_algorithm()

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
    for point in re:
        rec = Rectangle((point.x, point.y), width=1, height=1, edgecolor='gray', facecolor='g')
        ax.add_patch(rec)
    rec = Rectangle((en.x, en.y), width=1, height=1, edgecolor='gray', facecolor='r')
    ax.add_patch(rec)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

