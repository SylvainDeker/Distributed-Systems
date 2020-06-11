import dask.bag as db
from pyspark import SparkContext




if __name__ == '__main__':
    collection1 = [n for n in range(0,6)]
    collection2 = [n for n in range(4,10)]

    sc = SparkContext()
    rdd1 = sc.parallelize(collection1, 3)
    rdd2 = sc.parallelize(collection2, 3)
    res = rdd1.union(rdd2).collect()

    print(res)

    rdd1 = db.from_sequence(collection1, npartitions=3)
    rdd2 = db.from_sequence(collection2, npartitions=3)
    res = db.concat([rdd1, rdd2]).compute()

    print(res)
