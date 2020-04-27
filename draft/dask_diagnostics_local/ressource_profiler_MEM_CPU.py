import dask.array as da
from dask.diagnostics import ResourceProfiler

if __name__ == '__main__':

    a = da.random.normal(size=(1000,10000),
                         chunks=(1000,1000))

    res = a.dot(a.T).mean(axis=0)

    dt = 0.5 # timestep recording
    with ResourceProfiler(dt) as rprof:
        out = res.compute()

    rprof.visualize() # profile.html
    for res in rprof.results:
        print(res)
