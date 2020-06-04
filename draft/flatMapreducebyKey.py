import dask.bag as db
from functools import reduce
from pyspark import SparkContext

def printt(n):
    print(n)
    return n

if __name__ == '__main__':
    collection =[0,0,1,1,2,3]
    print("ref = ",collection)
    rdd = db.from_sequence(collection)
    # rdd = rdd.repartition(8).map_partitions(printt)
    rdd = rdd.map(lambda n:[(str(n),1) for x in range(100)])
    rdd = rdd.flatten()
    rdd = rdd.foldby(key=lambda collection:collection[0],
                    binop=lambda acc,b: (acc[0],acc[1]+b[1]))
    # rdd = rdd.map(lambda e:(e[0],e[1][1]))
    rdd.visualize(filename='flatMapreducebyKey.png')

    res = rdd.compute()
    print('dask =',res)
    print("###############################################")

    sc = SparkContext()
    rdd = sc.parallelize(collection)
    rdd = rdd.flatMap(lambda n:[(str(n),1) for x in range(100)])
    rdd = rdd.reduceByKey(lambda a,b:a+b)
    res = rdd.collect()

    print('spark =',res)
    print("###############################################")
