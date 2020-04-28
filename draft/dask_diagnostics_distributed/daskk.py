import sys
from dask.distributed import Client
import  dask.array as da


if __name__ == '__main__':

    client = Client(sys.argv[1])  # start distributed scheduler locally.  Launch dashboard

    # input("open browser")



    x = da.random.random((10000, 10000, 10), chunks = (1000, 1000, 5))
    y = da.random.random((10000, 10000, 10), chunks = (1000, 1000, 5))
    z = (da.arcsin(x) + da.arccos(y)).sum(axis=(1, 2))

    z.compute()

    # input("[Enter] to quit")

    client.close()
