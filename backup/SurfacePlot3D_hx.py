import numpy as np

import hilbert_trans

N = 5 # 32
SIDE = 2 ** N

m1 = np.zeros((SIDE, SIDE),dtype=np.int32)
m2 = np.zeros((SIDE, SIDE),dtype=np.int32)
m3 = np.zeros((SIDE, SIDE),dtype=np.int32)
m4 = np.zeros((SIDE, SIDE),dtype=np.int32)

for i in range(SIDE):
    for j in range(SIDE):
        m1[i,j] = hilbert_trans.xy2d_up(N, i, j)
        m2[i,j] = hilbert_trans.xy2d_down(N, i, j)
        m3[i,j] = hilbert_trans.xy2d_left(N, i, j)
        m4[i,j] = hilbert_trans.xy2d_right(N, i, j)

x, y = 15, 16
for i in range(SIDE):
    for j in range(SIDE):
        m1[i,j] = abs(hilbert_trans.xy2d_up(N, x, y) - m1[i, j])
        m2[i,j] = abs(hilbert_trans.xy2d_down(N, x, y) - m2[i, j])
        m3[i,j] = abs(hilbert_trans.xy2d_left(N, x, y) - m3[i, j])
        m4[i,j] = abs(hilbert_trans.xy2d_right(N, x, y) - m4[i, j])

# hx 方式 2
hx = m1 + m2 + m3 + m4


# hx 方式 1
# hx = np.zeros((SIDE, SIDE),dtype=np.int32)
#
# for i in range(SIDE):
#     for j in range(SIDE):
#         hx[i,j] = min(m1[i,j], m2[i,j], m3[i,j], m4[i,j])

hx = hx / np.max(hx)
print(hx)
np.savetxt('../test.txt', hx, fmt="%.6f", delimiter=' ')   # X 是一个数组
