import dask.bag as db
from functools import reduce
from pyspark import SparkContext
from pyspark import SparkConf
import time
import numpy as np
from distributed_systems.example import *


if __name__ == '__main__':
    # time.sleep(5)
    collection = []
    for i in range(shape_A[0]):
        for j in range(shape_A[1]):
            collection.append(Tile(i,j,tile_size_A))

    time.sleep(5)

    conf = SparkConf()

    conf.setMaster('local[4]')
    conf.set('spark.driver.memory', '7G')
    sc = SparkContext(conf=conf)
    time.sleep(5)

    rdd = sc.parallelize(collection,4)
    rdd = rdd.flatMap(build_new_tiles)
    rdd = rdd.map(lambda tile:((tile.x,tile.y), tile))
    rdd = rdd.reduceByKey(aggregate_tile)
    time.sleep(5)
    start_time = time.time()
    res = rdd.take(1)
    print(time.time()-start_time)
    time.sleep(5)
