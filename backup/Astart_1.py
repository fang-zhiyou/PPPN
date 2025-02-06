import sys
from queue import PriorityQueue

import hilbert_trans
from backup.final_v2 import dict0, dict1


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


class V4:
    def __init__(self, v4):
        self.v4: list = v4
        self.cost = sys.maxsize    # 总代价
        self.hx = sys.maxsize      # 当前点到终点的代价
        self.base_cost = 0

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.hx < other.hx
        return self.cost < other.cost


class Map:
    """
        Map 的大小为 2^n * 2^n, n 为曲线的阶
        x: [0, 2^n - 1] y: [0, 2^n - 1]
    """

    def __init__(self, n, d0_, d1_, d2_, d3_):
        self.size = 2 ** n
        self.dict0 = d0_
        self.dict1 = d1_
        self.dict2 = d2_
        self.dict3 = d3_
        self.long = 4 ** n

    def is_valid_point(self, x, y):  # 无效点
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        return True


class AStar:
    def __init__(self, mp: Map, start: V4, end: V4):
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

    def is_in_open_list(self, p: Point):
        for point in self.open_set.queue:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def is_st_point(self, p: Point):
        return p.x == self.st.x and p.y == self.st.y

    def is_en_point(self, p: V4):
        if p.v4[0] == self.en.v4[0] and p.v4[1] == self.en.v4[1] and p.v4[2] == self.en.v4[2] and p.v4[3] == self.en.v4[3]:
            return True
        return False


    def process_point(self, x, y, parent):
        if not self.is_valid_point(x, y) or self.close_set[x][y] == 1:
            return
        p = Point(x, y)
        if not self.is_in_open_list(p):
            p.parent = parent
            p.hx = self.heuristic_cost(p)
            p.cost = p.hx + self.base_cost(p)
            self.open_set.put(p)
            print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)

    def process_v4(self, p: V4):
        for val in self.close_set: # 在 close_set 里
            if p.v4[0] == val.v4[0]:
                return
        for val in self.open_set.queue: # 在 open_set 里
            if p.v4[0] == val.v4[0]:
                return
        a = abs(en.v4[0] - p.v4[0])
        b = abs(en.v4[1] - p.v4[1])
        c = abs(en.v4[2] - p.v4[2])
        d = abs(en.v4[3] - p.v4[3])
        half_val = self.mp.long // 2
        # p.hx = min(abs(en.v4[0] - p.v4[0]), abs(en.v4[1] - p.v4[1]), abs(en.v4[2] - p.v4[2]), abs(en.v4[3] - p.v4[3]))  # 方式 1: 3-85.84% 4-71.91% 5-58.9%
        # p.hx =min(a, b, c, d)
        # p.hx = a + b + c + d     # 方式 2: 3-85.82% 4-79.45% 5-74.55%

        # 方式 3：3-95.45% 4-91.89% 5-89.8%
        p.h = 0
        if a < half_val:
            p.h += a
        if b < half_val:
            p.h += b
        if c < half_val:
            p.h += c
        if d < half_val:
            p.h += d

        p.base_cost += 1
        p.cost = p.hx
        # print("chose：", p.v4, p.base_cost)
        self.open_set.put(p)


    def run_algorithm(self):
        # 起始点处理
        self.st.cost = 0
        self.st.hx = 0
        self.st.base_cost = 0
        self.open_set.put(self.st)

        while True:
            if self.open_set.empty():
                print('No path found, algorithm failed!!!')
                return
            p: V4 = self.open_set.get()

            if self.is_en_point(p):
                return p.base_cost

            self.close_set.append(p)

            # 处理邻居 d0
            d0_v = p.v4[0]
            if d0_v != 0:  # left
                new_p = V4(dict0[d0_v - 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)
            if d0_v != self.mp.long - 1:
                new_p = V4(dict0[d0_v + 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)

            # 处理邻居 d1
            d1_v = p.v4[1]
            if d1_v != 0:  # left
                new_p = V4(dict1[d1_v - 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)
            if d1_v != self.mp.long - 1:
                new_p = V4(dict1[d1_v + 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)

            # 处理邻居 d2
            d2_v = p.v4[2]
            if d2_v != 0:  # left
                new_p = V4(dict2[d2_v - 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)
            if d2_v != self.mp.long - 1:
                new_p = V4(dict2[d2_v + 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)

            # 处理邻居 d3
            d3_v = p.v4[3]
            if d3_v != 0:  # left
                new_p = V4(dict3[d3_v - 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)
            if d3_v != self.mp.long - 1:
                new_p = V4(dict3[d3_v + 1])
                new_p.base_cost = p.base_cost
                self.process_v4(new_p)


def get_v4(N, i, j):
    d0 = hilbert_trans.xy2d_up(N, i, j)
    d1 = hilbert_trans.xy2d_down(N, i, j)
    d2 = hilbert_trans.xy2d_left(N, i, j)
    d3 = hilbert_trans.xy2d_right(N, i, j)
    return V4([d0, d1, d2, d3])


if __name__ == '__main__':
    # 阶
    N = 4 # 16 * 16

    dict0 = dict()
    dict1 = dict()
    dict2 = dict()
    dict3 = dict()


    for i in range(2 ** N):
        for j in range(2 ** N):
            d0 = hilbert_trans.xy2d_up(N, i, j)
            d1 = hilbert_trans.xy2d_down(N, i, j)
            d2 = hilbert_trans.xy2d_left(N, i, j)
            d3 = hilbert_trans.xy2d_right(N, i, j)
            dict0[d0] = [d0, d1, d2, d3]
            dict1[d1] = [d0, d1, d2, d3]
            dict2[d2] = [d0, d1, d2, d3]
            dict3[d3] = [d0, d1, d2, d3]

    mp = Map(N, dict0, dict1, dict2, dict3)

    st = get_v4(N, 0, 0)
    en = get_v4(N, 1, 1)

    # 运行
    astar = AStar(mp, st, en)
    re = astar.run_algorithm()
    print(re)

    # sum_A = 0
    # sum_B = 0
    # for i in range(2 ** N):
    #     for j in range(2 ** N):
    #         for ii in range(2 ** N):
    #             for jj in range(2 ** N):
    #                 if i == ii and j == jj:
    #                     continue
    #                 st = get_v4(N, i, j)
    #                 en = get_v4(N, ii, jj)
    #
    #                 astar = AStar(mp, st, en)
    #                 re = astar.run_algorithm()
    #
    #                 # print("percent:", (abs(i - ii) + abs(j -jj)) / re)
    #                 sum_A += re
    #                 sum_B += abs(i - ii) + abs(j -jj)
    #     print("al_percent:", sum_B / sum_A)
    # print("al_percent:", sum_B / sum_A)

    ID_MAX = 4 ** N
    SIDE = 2 ** N
    sum_A = 0
    sum_B = 0
    for first in range(ID_MAX):
        for second in range(first + 1, ID_MAX):
            i = first // SIDE
            j = first % SIDE
            ii = second // SIDE
            jj = second % SIDE
            st = get_v4(N, i, j)
            en = get_v4(N, ii, jj)
            astar = AStar(mp, st, en)
            re = astar.run_algorithm()
            sum_A += re
            sum_B += abs(i - ii) + abs(j - jj)
        print(f"step {first} : {sum_B / sum_A}")
    print(f"ALL : {sum_B / sum_A} ")
