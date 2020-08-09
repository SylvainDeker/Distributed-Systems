import dask.bag as db
from functools import reduce
from pyspark import SparkContext
from dask.distributed import performance_report, Client
import time
import numpy as np
from distributed_systems.example import *

# if __name__ == '__main__':
#     tile = Tile(1,1,tile_size_A)
#     tile.data += 100
#     tile.disp_data()
#
#
#     res = build_new_tiles(tile)
#     for t in res:
#         t.disp_data()

if __name__ == '__main__':
    # client = Client()
    # print(client)
    # time.sleep(5)
    collection = []
    for i in range(shape_A[0]):
        for j in range(shape_A[1]):
            collection.append(Tile(i,j,tile_size_A))
    #
    # rdd = db.from_sequence(collection)
    # # rdd = rdd.repartition(8).map_partitions(printt)
    # rdd = rdd.map(build_new_tiles).flatten()
    # rdd = rdd.foldby(key=lambda tile:(tile.x,tile.y),
    #                 binop=aggregate_tile)
    # rdd.visualize(filename='flatMapreducebyKey.png')
    #
    # with performance_report(filename="dask-report.html"):
    #     res = rdd.compute()
    #
    #


    print("###############################################")

    sc = SparkContext()
    print(sc)
    rdd = sc.parallelize(collection)
    rdd = rdd.flatMap(build_new_tiles)
    rdd = rdd.map(lambda tile:((tile.x,tile.y), tile))
    rdd = rdd.reduceByKey(aggregate_tile)
    res = rdd.collect()
    print(len(res))
    print("###############################################")
