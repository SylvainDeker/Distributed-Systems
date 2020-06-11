import dask.bag as db
from pyspark import SparkContext




if __name__ == '__main__':
    collection = [1,2,2,2,3]


    sc = SparkContext()
    res = sc.parallelize(collection, 3)\
        .take(3)

    print(res)

    res = db.from_sequence(collection, npartitions=3)\
        .take(3,npartitions=-1)#Take from all the partitions
    res = list(res)

    print(res)
