import dask.array as da
from dask.diagnostics import Profiler

if __name__ == '__main__':

    a = da.random.normal(size=(1000,10000),
                         chunks=(1000,1000))

    res = a.dot(a.T).mean(axis=0)

    with Profiler() as prof:
        out = res.compute()

    prof.visualize() # see profile.html
    # print(prof.results[0])
    # print(prof.results[1])
