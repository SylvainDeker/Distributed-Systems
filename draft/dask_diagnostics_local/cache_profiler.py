import dask.array as da
from dask.diagnostics import CacheProfiler
from cachey import nbytes

if __name__ == '__main__':

    a = da.random.normal(size=(1000,10000),
                         chunks=(1000,1000))

    res = a.dot(a.T).mean(axis=0)

    with CacheProfiler(metric=nbytes) as rprof:
        out = res.compute()

    rprof.visualize()
    # for res in rprof.results:
    #     print(res)
