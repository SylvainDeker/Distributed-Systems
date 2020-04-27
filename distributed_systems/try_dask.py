import os
import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dask.distributed import Client
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window

from distributed_systems.buildCollectionTile import build_collection_tile
from distributed_systems.tile import Tile
import time


def try_dask_filter2D(pathimage, kernel, output_pathimage,output_graphSVG=None):
    client = Client()
    # client.upload_file("tile/tile.py")
    (collection, info) = build_collection_tile(pathimage)


    timer = time.time()
    rdd = db.from_sequence(collection).map(lambda n: n.filter2D(kernel))
    timer_graph = time.time() - timer

    timer = time.time()
    collection2 = rdd.compute()
    timer_compute = time.time() - timer

    if output_graphSVG != None:
        rdd.visualize(filename=output_graphSVG)

    with rasterio.open(output_pathimage, 'w',
                       driver=info.driver,
                       width=info.width, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:

        for t in collection2:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)
    client.close()
    return (timer_graph, timer_compute)

if __name__ == '__main__':

    kernel = np.array([[-1, -2, -4, -2, -1],
                       [-2, -4, -8, -4, -2],
                       [-4, -8, 84, -8, -4],
                       [-2, -4, -8, -4, -2],
                       [-1, -2, -4, -2, -1]], np.float32)

    t = try_dask_filter2D('./data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                          kernel,
                          'res_dask.tiff',
                          'graph_try_dask.svg')
    print("Time results:")
    print("\t", "Graph: ",t[0])
    print("\t", "Compute: ",t[1])
    su = sum(t)
    print("Time results in %:")
    print("\t", "Graph: ",t[0]/su)
    print("\t", "Compute: ",t[1]/su)
