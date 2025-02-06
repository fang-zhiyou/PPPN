import sys
import time
from queue import PriorityQueue

import numpy as np
import hilbert_trans
import peano_trans


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

    def __init__(self, n, d0_, d1_, d2_, d3_, d4_, d5_, vis_):
        self.N = n
        self.size = 2 ** n
        self.dict0 = d0_
        self.dict1 = d1_
        self.dict2 = d2_
        self.dict3 = d3_
        self.dict4 = d4_
        self.dict5 = d5_
        self.long = 4 ** n
        self.vis = vis_


class AStar:
    def __init__(self, mp: Map, start: V4, end: V4, hx_cache):
        self.mp = mp
        self.open_set = PriorityQueue()
        self.st = start
        self.en = end
        self.hx_cache = hx_cache

    def run_algorithm(self):
        # 起始点处理
        self.st.cost = 0
        self.st.hx = 0
        self.st.base_cost = 0
        self.open_set.put(self.st)
        self.mp.vis[self.st.v4[0]] = 1

        while True:
            if self.open_set.empty():
                print('No path found, algorithm failed!!!')
                return

            p: V4 = self.open_set.get()

            if p.v4[0] == self.en.v4[0]:
                # tt = []
                # t = p
                # while True:
                #     if t.v4[0] == self.st.v4[0]:
                #         break
                #     x, y = hilbert_trans.d2xy_up(self.mp.N, t.v4[0])
                #     tt.append((x, y))
                #     t = t.parent
                # # print(tt)
                return p.base_cost

            # 省时间
            # self.close_set.append(p)

            # 处理邻居 d4
            t = p.v4[4]
            for direct in [-1, 1]:
                d45 = t + direct
                if d45 == -1 or d45 == self.mp.long:
                    continue
                v4 = self.mp.dict4[d45]
                if v4[6] == 1 or self.mp.vis[v4[0]] == 1:
                    continue

                new_p = V4(v4)
                new_p.base_cost = p.base_cost + 1
                new_p.parent = p

                new_p.hx = self.hx_cache[v4[0]]
                new_p.cost = new_p.base_cost + new_p.hx
                self.open_set.put(new_p)
                mp.vis[v4[0]] = 1

            # 处理邻居 d5
            t = p.v4[5]
            for direct in [-1, 1]:
                d45 = t + direct
                if d45 == -1 or d45 == self.mp.long:
                    continue
                v4 = self.mp.dict5[d45]
                if v4[6] == 1 or self.mp.vis[v4[0]] == 1:
                    continue
                new_p = V4(v4)
                new_p.base_cost = p.base_cost + 1
                new_p.parent = p

                new_p.hx = self.hx_cache[v4[0]]
                new_p.cost = new_p.base_cost + new_p.hx
                self.open_set.put(new_p)
                mp.vis[v4[0]] = 1


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
        vis = dict()

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
                vis[d0] = 0
                # if graph_data[i, j] == 0:
                #     print(f'{i, j} ;', end="")
        t2 = time.time()
        print(f'构造地图时间 {t2*1000-t1*1000} seconds')

        mp = Map(N, dict0, dict1, dict2, dict3, dict4, dict5, vis)

        st = get_v4(N, 0,34)
        en = get_v4(N, 254, 231)


        # 减法 cache
        hx_dict = dict()
        for i in range(4 ** N):
            aa = abs(dict0[i][0] - en.v4[0])
            bb = abs(dict0[i][1] - en.v4[1])
            cc = abs(dict0[i][2] - en.v4[2])
            dd = abs(dict0[i][3] - en.v4[3])
            hx_dict[i] = aa + bb + cc + dd
            #  hx_dict[i] = min(aa, bb, cc, dd)


        # 时间运行
        astar = AStar(mp, st, en, hx_dict)

        time_start = time.time()
        re1 = astar.run_algorithm()
        time_end = time.time()
        print(f'Time cost: {round(1000*(time_end - time_start), 2)} ms, re = {re1}')
        break



