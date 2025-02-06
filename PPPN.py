import sys
from queue import PriorityQueue
import numpy as np
import hilbert_trans
import peano_trans


class Point:
    def __init__(self, vec):
        self.vec: list = vec
        self.cost = sys.maxsize  # 总代价
        self.hc = sys.maxsize  # 当前点到终点的代价
        self.bc = 0

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.hc < other.hc
        return self.cost < other.cost


N = 8
MAX_ID = 4 ** N
H1 = dict()
H2 = dict()
H3 = dict()
H4 = dict()
D1 = dict()
D2 = dict()
VIS = dict()

open_set = PriorityQueue()
hx_cache = dict()

st: Point = Point([0, 0, 0])
en: Point = Point([0, 1, 0])


def run_algorithm():
    # 起始点处理
    st.cost = 0
    st.hx = 0
    st.base_cost = 0
    open_set.put(st)
    VIS[st.vec[0]] = 1

    while True:
        if open_set.empty():
            print('No path found, algorithm failed!!!')
            return

        p: Point = open_set.get()

        if p.vec[0] == en.vec[0]:
            # tt = []
            # t = p
            # while True:
            #     if t.v4[0] == self.st.v4[0]:
            #         break
            #     x, y = hilbert_trans.d2xy_up(self.mp.N, t.v4[0])
            #     tt.append((x, y))
            #     t = t.parent
            # # print(tt)
            return p.bc

        # 处理邻居 d4
        t = p.vec[4]
        for direct in [-1, 1]:
            d45 = t + direct
            if d45 == -1 or d45 == MAX_ID:
                continue
            v4 = D1[d45]
            if v4[6] == 1 or VIS[v4[0]] == 1:
                continue

            new_p = Point(v4)
            new_p.bc = p.bc + 1
            new_p.parent = p

            new_p.hx = hx_cache[v4[0]]
            new_p.cost = new_p.bc + new_p.hx
            open_set.put(new_p)
            VIS[v4[0]] = 1

        # 处理邻居 d5
        t = p.vec[5]
        for direct in [-1, 1]:
            d45 = t + direct
            if d45 == -1 or d45 == MAX_ID:
                continue
            v4 = D2[d45]
            if v4[6] == 1 or VIS[v4[0]] == 1:
                continue
            new_p = Point(v4)
            new_p.bc = p.bc + 1
            new_p.parent = p

            new_p.hx = hx_cache[v4[0]]
            new_p.cost = new_p.bc + new_p.hx
            open_set.put(new_p)
            VIS[v4[0]] = 1


def get_point(i, j):
    d0 = hilbert_trans.xy2d_up(N, i, j)
    d1 = hilbert_trans.xy2d_down(N, i, j)
    d2 = hilbert_trans.xy2d_left(N, i, j)
    d3 = hilbert_trans.xy2d_right(N, i, j)
    d4 = peano_trans.xy2d_1(2 ** N, i, j)
    d5 = peano_trans.xy2d_2(2 ** N, i, j)
    return Point([d0, d1, d2, d3, d4, d5])


def map_init(n: int, path: str):
    global N, MAX_ID
    N = n
    MAX_ID = 4 ** N
    # fn = "zero/zero" + str(2 ** N) + ".npy"
    fn = path + str(2 ** N) + ".npy"
    graph_data = np.load(fn)

    for i in range(2 ** N):
        for j in range(2 ** N):
            d0 = hilbert_trans.xy2d_up(N, i, j)
            d1 = hilbert_trans.xy2d_down(N, i, j)
            d2 = hilbert_trans.xy2d_left(N, i, j)
            d3 = hilbert_trans.xy2d_right(N, i, j)
            d4 = peano_trans.xy2d_1(2 ** N, i, j)
            d5 = peano_trans.xy2d_2(2 ** N, i, j)
            H1[d0] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
            H2[d1] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
            H3[d2] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
            H4[d3] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
            D1[d4] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
            D2[d5] = [d0, d1, d2, d3, d4, d5, graph_data[i, j]]
            VIS[d0] = 0
            # if graph_data[i, j] == 0:
            #     print(f'{i, j} ;', end="")


def cache_init():
    for i in range(4 ** N):
        aa = abs(H1[i][0] - en.vec[0])
        bb = abs(H1[i][1] - en.vec[1])
        cc = abs(H1[i][2] - en.vec[2])
        dd = abs(H1[i][3] - en.vec[3])
        hx_cache[i] = aa + bb + cc + dd
        # hx_cache[i] = min(aa, bb, cc, dd)


def get_map_size():
    return sys.getsizeof(H1) + sys.getsizeof(H2) + sys.getsizeof(H3) + sys.getsizeof(H4) + sys.getsizeof(D1) + sys.getsizeof(D2)