

### PPPN: An Efficient Privacy-Preserving Path Navigation Approach in Outsourced Environments

This is the associated artifact for the paper "PPPN: An Efficient Privacy-Preserving Path Navigation Approach in Outsourced Environments".

#### Detailed Usage

Our experiments assume prior installation of Python 3 via the conda. First clone the repository. A list of dependancies can be found in requirements.txt.

Folder beijing, feicheng, and chicago contain the processed map of these cities by grid technique. Folder zero contains the processed map without road network.

In `benchmark.py` file, please set the parameter and run the code. For example.

```python
if __name__ == '__main__':
    # the start point and destination in different parameter.
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
        PPPN.map_init(6 + idx, 'zero/zero') # parameter: dataset
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
```

Lastly, please run the code in conda environment.
```python
python Benchmark.py
```


#### Others

GTKandPathGES.zip contains the source code of GTK and PathGES scheme.