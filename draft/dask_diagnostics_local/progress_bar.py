import dask.array as da
from dask.diagnostics import ProgressBar

if __name__ == '__main__':

    a = da.random.normal(size=(1000,10000),
                         chunks=(1000,1000))

    res = a.dot(a.T).mean(axis=0)


    # pbar = ProgressBar()
    # pbar.register()
    # out = res.compute()
    # pbar.unregister()


    with ProgressBar():
        out = res.compute()
