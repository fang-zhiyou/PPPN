import time
import PPPN

if __name__ == '__main__':
    # bj_st = [[0, 8], [0, 17], [0, 34], [0, 69], [0, 139]]
    # bj_en = [[63, 62], [127, 125], [255, 250], [511, 501], [1023, 1003]]

    # chi_st = [[0, 0], [0, 0], [0, 1], [0, 3], [0, 6]]
    # chi_en = [[63, 62], [127, 127], [255, 255], [511, 500], [1023, 1000]]

    # fei_st = [[0, 0], [0, 1], [0, 3], [0, 6], [0, 13]]
    # fei_en = [[63, 61], [126, 127], [254, 254], [510, 509], [1023, 1018]]

    zero_st = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    zero_en = [[63, 63], [127, 127], [254, 254], [511, 511], [1023, 1023]]
    for idx in range(0, 5):
        print(f'N = {6 + idx}')

        t1 = time.time()
        PPPN.map_init(6 + idx, 'zero/zero')
        t2 = time.time()

        print(f'HCM generation: {round((t2 - t1) * 1000, 2)} ms')
        print(f'Map size：{PPPN.get_map_size()} B')
        PPPN.st = PPPN.get_point(zero_st[idx][0], zero_st[idx][1])
        PPPN.en = PPPN.get_point(zero_en[idx][0], zero_en[idx][1])

        PPPN.cache_init()

        t1 = time.time_ns()
        re = PPPN.run_algorithm()
        t2 = time.time_ns()
        print(f'time cost: {t2-t1} ns')



