import sys
import time
from queue import PriorityQueue

import numpy as np
import hilbert_trans
import peano_trans


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0
    def __lt__(self, other):
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

    def __init__(self, n, d0_, d1_, d2_, d3_, d4_, d5_):
        self.N = n
        self.size = 2 ** n
        self.dict0 = d0_
        self.dict1 = d1_
        self.dict2 = d2_
        self.dict3 = d3_
        self.dict4 = d4_
        self.dict5 = d5_
        self.long = 4 ** n


class AStar:
    def __init__(self, mp: Map, start: V4, end: V4):
        self.mp = mp
        self.open_set = PriorityQueue()
        self.close_set = []
        self.st = start
        self.en = end

    def is_en_point(self, p: V4):
        if p.v4[0] == self.en.v4[0]:
            return True
        return False

    def process_v4(self, p: V4):

        for val in self.close_set: # 在 close_set 里
            if p.v4[0] == val.v4[0]:
                return
        for val in self.open_set.queue: # 在 open_set 里
            if p.v4[0] == val.v4[0]:
                return
        # x, y = hilbert_trans.d2xy_up(3, p.v4[0])
        # print(f"point({x}, {y}) {p.base_cost}")

        a = abs(self.en.v4[0] - p.v4[0])
        b = abs(self.en.v4[1] - p.v4[1])
        c = abs(self.en.v4[2] - p.v4[2])
        d = abs(self.en.v4[3] - p.v4[3])
        half_val = self.mp.long // 2

        #p.hx = min(a, b, c, d)  # 方式 1: 3-85.84% 4-71.91% 5-58.9%
        p.hx = a + b + c + d     # 方式 2: 3-85.82% 4-79.45% 5-74.55%

        # 方式 3：3-95.45% 4-91.89% 5-89.8%
        # p.h = 0
        # if a < half_val:
        #     p.h += a
        # if b < half_val:
        #     p.h += b
        # if c < half_val:
        #     p.h += c
        # if d < half_val:
        #     p.h += d

        p.base_cost += 1
        p.cost = p.base_cost + p.hx
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
                tt = []
                t = p
                while True:
                    if t.v4[0] == self.st.v4[0]:
                        break
                    x, y = hilbert_trans.d2xy_up(self.mp.N, t.v4[0])
                    tt.append((x, y))
                    t = t.parent
                # print(tt)
                return p.base_cost

            self.close_set.append(p)

            # 处理邻居 d4
            d4_v = p.v4[4]
            if d4_v != 0 and self.mp.dict4[d4_v - 1][6] == 0:  # left
                new_p = V4(self.mp.dict4[d4_v - 1])
                new_p.base_cost = p.base_cost
                new_p.parent = p
                self.process_v4(new_p)
            if d4_v != self.mp.long - 1 and self.mp.dict4[d4_v + 1][6] == 0:
                new_p = V4(self.mp.dict4[d4_v + 1])
                new_p.base_cost = p.base_cost
                new_p.parent = p
                self.process_v4(new_p)

            # 处理邻居 d5
            d5_v = p.v4[5]
            if d5_v != 0 and self.mp.dict5[d5_v - 1][6] == 0:
                new_p = V4(self.mp.dict5[d5_v - 1])
                new_p.base_cost = p.base_cost
                new_p.parent = p
                self.process_v4(new_p)
            if d5_v != self.mp.long - 1 and self.mp.dict5[d5_v + 1][6] == 0:
                new_p = V4(self.mp.dict5[d5_v + 1])
                new_p.base_cost = p.base_cost
                new_p.parent = p
                self.process_v4(new_p)


def get_v4(N, i, j):
    d0 = hilbert_trans.xy2d_up(N, i, j)
    d1 = hilbert_trans.xy2d_down(N, i, j)
    d2 = hilbert_trans.xy2d_left(N, i, j)
    d3 = hilbert_trans.xy2d_right(N, i, j)
    d4 = peano_trans.xy2d_1(2 ** N, i, j)
    d5 = peano_trans.xy2d_2(2 ** N, i, j)
    return V4([d0, d1, d2, d3, d4, d5])

if __name__ == '__main__':

    # 时间测试-----------------------------0 数据集-------------------------------------------------------------------
    for N in range(8, 11):
        # fn = "zero/zero" + str(2 ** N) + ".npy"
        fn = "beijing/beijing" + str(2 ** N) + ".npy"

        graph_data = np.load(fn)

        dict0 = dict()
        dict1 = dict()
        dict2 = dict()
        dict3 = dict()
        dict4 = dict()
        dict5 = dict()

        t1 = time.time()
        for i in range(2 ** N):
            for j in range(2 ** N):
                d0 = hilbert_trans.xy2d_up(N, i, j)
                d1 = hilbert_trans.xy2d_down(N, i, j)
                d2 = hilbert_trans.xy2d_left(N, i, j)
                d3 = hilbert_trans.xy2d_right(N, i, j)
                d4 = peano_trans.xy2d_1(2 ** N, i, j)
                d5 = peano_trans.xy2d_2(2 ** N, i, j)

                dict0[d0] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
                dict1[d1] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
                dict2[d2] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
                dict3[d3] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
                dict4[d4] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
                dict5[d5] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
        t2 = time.time()
        print(f'构造地图时间 {t2*1000-t1*1000} seconds')

        mp = Map(N, dict0, dict1, dict2, dict3, dict4, dict5)

        st = get_v4(N, 0,34)
        en = get_v4(N, 254, 231)


        # 时间运行
        ts = []
        for i in range(1):
            astar = AStar(mp, st, en)

            time_start = time.time()
            re1 = astar.run_algorithm()
            time_end = time.time()
            if N == 10:
                print(f"处理第 {i} 条")
            ts.append(round(time_end - time_start, 2))
        print(ts)
        print(np.mean(ts))
        break





    # 时间测试------------------------------------------------------------------------------------------------------------
    # # Chicago data
    # # N = 7
    # # graph_data = np.load('graph_data.npy') # 0 表示通 1 表示不通
    #
    # # ChiPts = [[0, 0, 63, 62], [0, 0, 127, 127], [0, 1, 255, 255], [0, 3, 511, 500], [0, 6, 1023, 1000]] Chicago
    # # ChiPts = [[0, 0, 63, 61], [0, 1, 126, 127], [0, 3, 254, 254], [0, 6, 510, 509], [0, 13, 1023, 1018]] # 费城
    # ChiPts = [[0, 8, 63, 62], [0, 17, 127, 125], [0, 34, 255, 250], [0, 69, 511, 501], [0, 139, 1023, 1003]]
    #
    # for n in range(5):
    #     print(f"N = {n + 6}")
    #     N = n + 6
    #     # fn = 'chicago/Chicago' + str(2**N) + '.npy'
    #     # fn = 'feicheng/Philadelphia' + str(2**N) + '.npy'
    #     fn = 'beijing/beijing' + str(2**N) + '.npy'
    #     graph_data = np.load(fn)
    #
    #     dict0 = dict()
    #     dict1 = dict()
    #     dict2 = dict()
    #     dict3 = dict()
    #     dict4 = dict()
    #     dict5 = dict()
    #
    #     t1 = time.time()
    #     for i in range(2 ** N):
    #         for j in range(2 ** N):
    #             d0 = hilbert_trans.xy2d_up(N, i, j)
    #             d1 = hilbert_trans.xy2d_down(N, i, j)
    #             d2 = hilbert_trans.xy2d_left(N, i, j)
    #             d3 = hilbert_trans.xy2d_right(N, i, j)
    #             d4 = peano_trans.xy2d_1(2 ** N, i, j)
    #             d5 = peano_trans.xy2d_2(2 ** N, i, j)
    #
    #             dict0[d0] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
    #             dict1[d1] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
    #             dict2[d2] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
    #             dict3[d3] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
    #             dict4[d4] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
    #             dict5[d5] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
    #     t2 = time.time()
    #     print(f'构造地图时间 {t2*1000-t1*1000} seconds')
    #
    #     mp = Map(N, dict0, dict1, dict2, dict3, dict4, dict5)
    #
    #     st = get_v4(N, ChiPts[n][0], ChiPts[n][1])
    #     en = get_v4(N, ChiPts[n][2], ChiPts[n][3])
    #     # print(st.v4 , en.v4)
    #
    #     #
    #     # astar = AStar(mp, st, en)
    #     # re1 = astar.run_algorithm()
    #     # print(re1)
    #
    #     # 时间运行
    #     ts = []
    #     for i in range(10):
    #         astar = AStar(mp, st, en)
    #
    #         time_start = time.time()
    #         re1 = astar.run_algorithm()
    #         time_end = time.time()
    #         print(f"长度 {re1}")
    #         # print(f'路径长度 {re1}, 花费时间: {1000 * time_end - 1000 * time_start} ms')
    #         ts.append(round(time_end*1000 - time_start*1000, 2))
    #     print(ts)
    #     print(np.mean(ts))



