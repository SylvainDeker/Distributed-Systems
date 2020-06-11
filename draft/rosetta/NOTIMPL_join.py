import dask.bag as db
from pyspark import SparkContext




if __name__ == '__main__':
    collection1 = [(str(n),n) for n in range(0,6)]
    collection2 = [(str(n),n) for n in range(4,10)]

    sc = SparkContext()
    rdd1 = sc.parallelize(collection1, 3)
    rdd2 = sc.parallelize(collection2, 3)
    res = rdd1.join(rdd2).collect()

    print(res)

    rdd1 = db.from_sequence(collection1, npartitions=3)
    rdd2 = db.from_sequence(collection2, npartitions=3)
    res = rdd1.join(rdd2, on_self=lambda kv:kv[0]).compute() #Not Implemented in 2.16 but it is in 2.18

    print(res)
