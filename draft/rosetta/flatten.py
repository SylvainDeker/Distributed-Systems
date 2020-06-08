import dask.bag as db
from functools import reduce
from pyspark import SparkContext

def f(i):
    return list(range(i))

if __name__ == '__main__':

    rdd = db.from_sequence([[0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]])
    rdd = rdd.flatten()
    res = rdd.compute()

    print(res)


    sc = SparkContext()
    rdd = sc.parallelize([[0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]])
    rdd = rdd.flatMap(lambda x:x)
    res = rdd.collect()
    
    print(res)
