import dask.bag as db
from pyspark import SparkContext




if __name__ == '__main__':
    collection = [0,1,2,3,4,5,7,8,9]


    sc = SparkContext()
    lazy = sc.parallelize(collection, 3)
    lazy = lazy.map(lambda a:a+1)
    lazy = lazy.filter(lambda a:a%2)
    res = lazy.collect()
    print(res)

    lazy = db.from_sequence(collection, npartitions=3)
    lazy = lazy.map(lambda a:a+1)
    lazy = lazy.filter(lambda a:a%2)
    res = lazy.compute()
    print(res)
