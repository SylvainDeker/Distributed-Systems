import dask.bag as db
from functools import reduce
from dask.distributed import performance_report, Client
import time
import numpy as np
from distributed_systems.example import *


if __name__ == '__main__':

    collection = []
    for i in range(shape_A[0]):
        for j in range(shape_A[1]):
            collection.append(Tile(i,j,tile_size_A))

    client = Client(n_workers=4, threads_per_worker=1)

    rdd = db.from_sequence(collection)
    rdd = rdd.map(build_new_tiles).flatten()
    rdd = rdd.foldby(key=lambda tile:(tile.x,tile.y),
                    binop=aggregate_tile)

    res = rdd.take(1)
