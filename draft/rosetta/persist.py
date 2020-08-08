import dask
import dask.bag as db
from functools import reduce
from dask.distributed import Client
import time

def my_wait(d):
    print("coucou "+str(d))
    return d+1


if __name__ == '__main__':

    client = Client()

    collection =[1,1,1,1,1,1]

    rdd = db.from_sequence(collection)\
            .map(my_wait)

    rdd = rdd.persist()
    print("before")
    # time.sleep(5)
    rdd = rdd.map(my_wait)
    print("After")

    time.sleep(5)
    res = rdd.compute()
    print('dask =',res)

    print("###############################################")
