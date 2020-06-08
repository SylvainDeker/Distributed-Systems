import dask.bag as db
from functools import reduce
from pyspark import SparkContext


# def sum_value(cplA,cplB):
#
#     (k, a) = cplA
#     (_, b) = cplB
#     return (k, a+b)
#
# def linreduce(bag):
#     reduce(sum_value, bag, 0)
#
# def fu1(kv):
#     k,v = kv
#
#     return (k,reduce(lambda acc,b:acc+b[1],v,0))




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
    rdd = db.from_sequence(collection)

    # rdd = rdd.groupby(lambda collection:collection[0])\
    #       .map(lambda kv:(kv[0],reduce(lambda acc,b: (acc[0],acc[1]+b[1]),kv[1])))
    # rdd.visualize(filename='groupby_map.png')

    rdd = rdd.foldby(key=lambda collection:collection[0],
                    binop=lambda acc,b: (acc[0],acc[1]+b[1]))
    rdd.visualize(filename='foldby.png')

    res = rdd.compute()
    for r in res:
        print(r)


    sc = SparkContext()
    rdd = sc.parallelize(collection)
    rdd = rdd.reduceByKey(lambda a,b:a+b)
    res = rdd.collect()

    for r in res:
        print(r)
