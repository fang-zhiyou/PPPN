import random
import sys
import time
from queue import PriorityQueue

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = sys.maxsize    # 总代价
        self.hx = sys.maxsize      # 当前点到终点的代价

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.hx < other.hx
        return self.cost < other.cost


class Map:

    def __init__(self, graph_):
        self.size = graph_.shape[0]
        self.graph = graph_

    def is_valid_point(self, x, y):  # 无效点
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        if self.graph[x][y] == 1:
            return False
        return True


class AStar:
    def __init__(self, mp: Map, start: Point, end: Point):
        self.mp = mp
        self.open_set = PriorityQueue()
        self.close_set = []
        self.st = start
        self.en = end

    def base_cost(self, p: Point):  # 当前点到起始点的代价
        return abs(p.x - self.st.x) + abs(p.y - self.st.y)

    def heuristic_cost(self, p: Point):  # 当前点到结束点的代价
        return abs(p.x - self.en.x) + abs(p.y - self.en.y)

    def is_valid_point(self, x, y):  # 无效点
        return self.mp.is_valid_point(x, y)

    def is_st_point(self, p: Point):
        return p.x == self.st.x and p.y == self.st.y

    def is_en_point(self, p: Point):
        return p.x == self.en.x and p.y == self.en.y

    def process_point(self, x, y, parent):
        if not self.is_valid_point(x, y):
            return

        for val in self.close_set:
            if val.x == x and val.y == y:
                return

        for val in self.open_set.queue:
            if val.x == x and val.y == y:
                return

        p = Point(x, y)

        p.parent = parent
        p.hx = self.heuristic_cost(p)
        p.cost = p.hx + self.base_cost(p)
        self.open_set.put(p)
        # print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)


    def run_algorithm(self):

        self.st.cost = 0
        self.st.hx = 0
        self.open_set.put(self.st)

        while True:
            if self.open_set.empty():
                print('No path found, algorithm failed!!!')
                return

            p: Point = self.open_set.get()

            if self.is_en_point(p):
                tt = []
                t = p
                while True:
                    if t.x == self.st.x and t.y == self.st.y:
                        break
                    tt.append((t.x, t.y))
                    t = t.parent
                # print(tt)
                return p.cost

            self.close_set.append(p)

            # 处理邻居
            x = p.x
            y = p.y
            self.process_point(x + 1, y, p)
            self.process_point(x - 1, y, p)
            self.process_point(x, y - 1, p)
            self.process_point(x, y + 1, p)


if __name__ == '__main__':

    # 计算时间 ------------------------------ 0 数据集
    for N in range(6, 11):
        fn = "zero/zero" + str(2**N) + ".npy"
        chicago = np.load(fn)
        mp = Map(chicago)

        ts = []
        for i in range(10):
            astar = AStar(mp, Point(0, 0), Point(2**N - 1, 2**N - 1))
            start_time = time.time()
            re = astar.run_algorithm()
            end_time = time.time()
            # print(f"路径长度 {re}, 花费时间 {end_time * 1000 - start_time * 1000} ms")
            ts.append(round(end_time*1000 - start_time*1000, 2))
        print(ts)
        print(np.mean(ts))

    # # 计算时间 ------------------------------ 非 0 数据集
    # ts = []
    # for i in range(10):
    #     astar = AStar(mp, Point(0, 13), Point(1023, 1018))
    #     start_time = time.time()
    #     re = astar.run_algorithm()
    #     end_time = time.time()
    #     print(f"路径长度 {re}, 花费时间 {end_time * 1000 - start_time * 1000} ms")
    #     ts.append(round(end_time*1000 - start_time*1000, 2))
    # print(ts)
    # print(np.mean(ts))

