import dask.bag as db
from functools import reduce
from pyspark import SparkContext


def f_dask(iter):
    print(type(iter), iter)
    for e in iter:
        print(type(e),e)
    return iter

def f_spark(iter):
    print(type(iter), iter)
    for e in iter:
        print(type(e),e)
    return iter

if __name__ == '__main__':
    collection = [0,1,2,3,4,5,6,7,8,9]

    rdd = db.from_sequence(collection, npartitions=2)
    rdd = rdd.map_partitions(f_dask)
    rdd = rdd.repartition(3)
    rdd = rdd.map_partitions(f_dask)
    res = rdd.compute()
    print(res)

    sc = SparkContext()
    rdd = sc.parallelize(collection,2)
    rdd = rdd.mapPartitions(f_spark)
    rdd = rdd.partitionBy(3)
    rdd = rdd.mapPartitions(f_spark)
    rdd = rdd.collect()
    print(res)
