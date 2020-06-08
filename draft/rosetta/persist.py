import dask
import dask.bag as db
from functools import reduce
from dask.distributed import Client


if __name__ == '__main__':

    # client = Client()

    collection =[1,2,3,4,5,6]

    rdd = db.from_sequence(collection)\
            .map(lambda x:[x for n in range(x)])

    rdd= rdd.persist(  scheduler='processes',
                       traversal=False,
                       optimize_graph=True)
    rdd.visualize('persist.png')
    # print(res)
    res = rdd.compute()
    print('dask =',res)

    print("###############################################")
