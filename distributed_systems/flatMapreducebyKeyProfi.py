import dask.bag as db
from functools import reduce
from pyspark import SparkContext
from pyspark import SparkConf
from dask.distributed import performance_report, Client
import time
import numpy as np
from distributed_systems.example import *


if __name__ == '__main__':
    collection = []
    for i in range(shape_A[0]):
        for j in range(shape_A[1]):
            collection.append(Tile(i,j,tile_size_A))

    #
    # conf = SparkConf()
    #
    # conf.setMaster('local[4]')
    # conf.set('spark.driver.memory', '2G')
    # sc = SparkContext(conf=conf)
    # print(sc)
    #
    # rdd = sc.parallelize(collection)
    # rdd = rdd.flatMap(build_new_tiles)
    # rdd = rdd.map(lambda tile:((tile.x,tile.y), tile))
    # rdd = rdd.reduceByKey(aggregate_tile)
    # start_time = time.time()
    # res = rdd.collect()
    # print(time.time()-start_time)
    # print("###############################################")

    # time.sleep(6)

    #
    client = Client(n_workers=4, threads_per_worker=1)
    print(client)


    rdd = db.from_sequence(collection)
    # rdd = rdd.repartition(8).map_partitions(printt)
    rdd = rdd.map(build_new_tiles).flatten()
    rdd = rdd.foldby(key=lambda tile:(tile.x,tile.y),
                    binop=aggregate_tile,combine=aggregate_tile2)
    # rdd.visualize(filename='flatMapreducebyKey.png')

    # with performance_report(filename="dask-report.html"):
    #     res = rdd.compute()
    start_time = time.time()
    res = rdd.compute()
    print(time.time()-start_time)
    # client.shutdown()


    print("###############################################")




    # input("wait")
