import dask.bag as db
from functools import reduce
from dask.distributed import performance_report, Client
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

    client = Client(n_workers=4, threads_per_worker=1)

    time.sleep(5)

    rdd = db.from_sequence(collection,npartitions=4)
    # rdd = rdd.repartition(8).map_partitions(printt)
    rdd = rdd.map(build_new_tiles).flatten()
    rdd = rdd.foldby(key=lambda tile:(tile.x,tile.y),
                    binop=aggregate_tile,combine=aggregate_tile2)
    time.sleep(5)
    start_time = time.time()
    res = rdd.take(1)
    print(time.time()-start_time)
    # client.shutdown()
    time.sleep(5)

    # print("###############################################")




    # input("wait")
