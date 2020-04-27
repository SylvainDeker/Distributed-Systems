import os
import sys
from dask.distributed import Client
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window



from collections import OrderedDict
from shapely.geometry import mapping
import fiona
import pprint
import dask
import time

from distributed_systems.buildCollectionTile import build_collection_tile
from distributed_systems.tile import Tile

def try_dask_delayed_filter2D(pathimage, kernel, output_pathimage):
    client = Client()
    (collection, info) = build_collection_tile(pathimage)


    res = []

    timer = time.time()
    for i in range(len(collection)):
        e = dask.delayed(collection[i].filter2D)(kernel)
        # e.visualize(filename='graph_'+str(i)+'.svg')
        res.append(e.compute())


    timer = time.time() - timer

    with rasterio.open(output_pathimage, 'w',
                       driver=info.driver,
                       width=info.width, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:
        for t in res:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)
    client.close()
    return timer


if __name__ == '__main__':

    kernel = np.array([[-1, -2, -4, -2, -1],
                       [-2, -4, -8, -4, -2],
                       [-4, -8, 84, -8, -4],
                       [-2, -4, -8, -4, -2],
                       [-1, -2, -4, -2, -1]], np.float32)
    t = try_dask_delayed_filter2D('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                          kernel,
                          'res_dask_delayed.tiff')
    print(t)
