import dask.bag as db
from functools import reduce
from pyspark import SparkContext




if __name__ == '__main__':
    collection =[('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 ('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 ('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 ('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 ('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 ('a',1),('b',1),('c',2),#('a',1),('b',1),('c',2),('a',1),
                 ('a',1),('b',1),('c',2),#('a',1),('b',1),('c',2),('a',1),
                 ('a',1),('c',1),('c',2),#('a',1),('c',1),('c',2),('a',1),
                 # ('a',1),('c',1),('c',2),#('a',1),('c',1),('c',2),('a',1),
                 # ('a',1),('c',1),('a',2),#('a',1),('c',1),('a',2),('a',1),
                 # ('a',1),('c',1),('a',2),#('a',1),('c',1),('a',2),('a',1),
                 # ('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 # ('a',1),('b',1),('a',2),#('a',1),('b',1),('a',2),('a',1),
                 # ('a',1),('a',1),('c',2),#('a',1),('a',1),('c',2),('a',1),
                 ]

    sc = SparkContext()
    res = sc.parallelize(collection)\
        .groupByKey()\
        .mapValues(list)\
        .collect()

    for i in res:
        print(i)

    print("==================")

    res = db.from_sequence(collection)\
        .map(lambda kv:(kv[0], [kv[1]]))\
        .foldby(lambda collection:collection[0],
                lambda acc,b:(acc[0],acc[1]+b[1]))\
        .map(lambda kv:(kv[0], kv[1][1]))\
        .compute()

    for i in res:
        print(i)
