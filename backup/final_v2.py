import queue
import sys
import time
from enum import global_enum
from queue import PriorityQueue

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import hilbert_trans

# 版本 2
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class V3Point:
    def __init__(self, v, d, cost, parent=None):
        self.v = v
        self.d = d
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost


dict0 = dict()
dict1 = dict()
dict2 = dict()
dict3 = dict()

ORDER = 5   # 曲线信息
ID_MAX = 2 ** (2*ORDER)
SIDE = 2 ** ORDER

vis = np.zeros((4, ID_MAX), dtype=int)


def is_ok(v, d):
    if (0 <= d < ID_MAX) and vis[v][d] == 0:
        return True
    return False


def dict_init():
    # Hilbert 曲线初始化
    for i in range(SIDE):
        for j in range(SIDE):
            d0 = hilbert_trans.xy2d_up(ORDER, i, j)
            d1 = hilbert_trans.xy2d_down(ORDER, i, j)
            d2 = hilbert_trans.xy2d_left(ORDER, i, j)
            d3 = hilbert_trans.xy2d_right(ORDER, i, j)
            dict0[d0] = [d0, d1, d2, d3]
            dict1[d1] = [d0, d1, d2, d3]
            dict2[d2] = [d0, d1, d2, d3]
            dict3[d3] = [d0, d1, d2, d3]


def bfs(st: Point, en: Point):
    st_d = hilbert_trans.xy2d_up(ORDER, st.x, st.y)
    en0 = hilbert_trans.xy2d_up(ORDER, en.x, en.y)

    # bfs 算法
    que = queue.PriorityQueue()

    que.put(V3Point(0, st_d, 0))
    vis[0][st_d] = 1

    while True:
        p: V3Point = que.get()
        vis[p.v][p.d] = 1

        if p.v == 0 and p.d == en0:  # 判断是终点
            return p.cost

        if p.v == 0:
            v1_d = dict0[p.d][1]
            if vis[1][v1_d] == 0:
                que.put(V3Point(1, v1_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
        elif p.v == 1:
            v0_d = dict1[p.d][0]
            v2_d = dict1[p.d][2]
            if vis[0][v0_d] == 0:
                que.put(V3Point(0, v0_d, p.cost, p))
            if vis[2][v2_d] == 0:
                que.put(V3Point(2, v2_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
        elif p.v == 2:
            v1_d = dict2[p.d][1]
            v3_d = dict2[p.d][3]
            if vis[1][v1_d] == 0:
                que.put(V3Point(1, v1_d, p.cost, p))
            if vis[3][v3_d] == 0:
                que.put(V3Point(3, v3_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
        elif p.v == 3:
            v2_d = dict3[p.d][2]
            if vis[2][v2_d] == 0:
                que.put(V3Point(2, v2_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))


def bfs_path(st: Point, en: Point):
    st_d = hilbert_trans.xy2d_up(ORDER, st.x, st.y)
    en0 = hilbert_trans.xy2d_up(ORDER, en.x, en.y)
    # bfs 算法
    que = queue.PriorityQueue()

    que.put(V3Point(0, st_d, 0))
    vis[0][st_d] = 1
    path = []
    while True:
        p: V3Point = que.get()
        vis[p.v][p.d] = 1

        if p.v == 0 and p.d == en0:  # 判断是终点
            print(f"cost: {p.cost}")
            # 输出路径
            path.insert(0, p)
            while True:
                p = p.parent
                path.insert(0, p)
                if p.v == 0 and p.d == st_d:
                    break
            break

        if p.v == 0:
            v1_d = dict0[p.d][1]
            if vis[1][v1_d] == 0:
                que.put(V3Point(1, v1_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
        elif p.v == 1:
            v0_d = dict1[p.d][0]
            v2_d = dict1[p.d][2]
            if vis[0][v0_d] == 0:
                que.put(V3Point(0, v0_d, p.cost, p))
            if vis[2][v2_d] == 0:
                que.put(V3Point(2, v2_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
        elif p.v == 2:
            v1_d = dict2[p.d][1]
            v3_d = dict2[p.d][3]
            if vis[1][v1_d] == 0:
                que.put(V3Point(1, v1_d, p.cost, p))
            if vis[3][v3_d] == 0:
                que.put(V3Point(3, v3_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
        elif p.v == 3:
            v2_d = dict3[p.d][2]
            if vis[2][v2_d] == 0:
                que.put(V3Point(2, v2_d, p.cost, p))
            for_l = p.d - 1
            if is_ok(p.v, for_l):
                que.put(V3Point(p.v, for_l, p.cost + 1, p))
            for_r = p.d + 1
            if is_ok(p.v, for_r):
                que.put(V3Point(p.v, for_r, p.cost + 1, p))
    return path


# 服务器只有曲线信息, 局部的曲线信息
if __name__ == '__main__':
    # 初始化地图
    dict_init()

    # 起点和终点
    st = Point(0, 0)
    en = Point(0, 3)
    print(bfs(st, en))


    sum_A = 0
    sum_B = 0
    for first in range(ID_MAX):
        for second in range(first + 1, ID_MAX):
            i = first // SIDE
            j = first % SIDE
            ii = second // SIDE
            jj = second % SIDE
            st = Point(i, j)
            en = Point(ii, jj)
            vis = np.zeros((4, ID_MAX), dtype=int)
            cost = bfs(st, en)
            sum_A += cost
            sum_B += abs(i - ii) + abs(j - jj)
        print(f"step {first} : {sum_B / sum_A}")
    print(f"ALL : {sum_B / sum_A} ")

    # 实验结果：3-95.45% 4-91.89% 5-89.8%

    # path = bfs(st, en)
    # # 画图函数
    # plt.figure(figsize=(5, 5))
    # ax = plt.gca()
    # ax.set_xlim([0, SIDE])
    # ax.set_ylim([0, SIDE])
    #
    # for i in range(SIDE):
    #     for j in range(SIDE):
    #         rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
    #         ax.add_patch(rec)
    #
    # for point in path:
    #     if point.v == 0:
    #         x, y = hilbert_trans.d2xy_up(ORDER, point.d)
    #         rec = Rectangle((x, y), width=1, height=1, edgecolor='gray', facecolor='g')
    #         ax.add_patch(rec)
    #     if point.v == 1:
    #         x, y = hilbert_trans.d2xy_down(ORDER, point.d)
    #         rec = Rectangle((x, y), width=1, height=1, edgecolor='gray', facecolor='g')
    #         ax.add_patch(rec)
    #     if point.v == 2:
    #         x, y = hilbert_trans.d2xy_left(ORDER, point.d)
    #         rec = Rectangle((x, y), width=1, height=1, edgecolor='gray', facecolor='g')
    #         ax.add_patch(rec)
    #     if point.v == 3:
    #         x, y = hilbert_trans.d2xy_right(ORDER, point.d)
    #         rec = Rectangle((x, y), width=1, height=1, edgecolor='gray', facecolor='g')
    #         ax.add_patch(rec)
    #
    # plt.axis('equal')
    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()

