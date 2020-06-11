import dask.bag as db
from pyspark import SparkContext




if __name__ == '__main__':
    collection = [1,2,2,2,3]


    sc = SparkContext()
    res = sc.parallelize(collection, 3)\
        .count()

    print(res)

    res = db.from_sequence(collection, npartitions=3)\
        .count()\
        .compute()

    print(res)
