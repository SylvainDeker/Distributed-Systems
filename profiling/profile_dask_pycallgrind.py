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

from pycallgrind import callgrind

def try_dask_filter2D(pathimage,
                      kernel,
                      output_pathimage,
                      unit_height=500,
                      unit_width=500):
    client = Client()
    # client.upload_file("tile/tile.py")
    (collection, info) = build_collection_tile(pathimage,unit_height,unit_width)


    with callgrind(tag="Graph"):
        rdd = db.from_sequence(collection).map(lambda n: n.filter2D(kernel))


    with callgrind(tag="Compute"):
        collection2 = rdd.compute()



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


if __name__ == '__main__':
    if len(sys.argv) !=3:
        print("Usage example: ", sys.argv[0]," 500 500")
        exit(-1)

    kernel = np.array([[-1, -2, -4, -2, -1],
                       [-2, -4, -8, -4, -2],
                       [-4, -8, 84, -8, -4],
                       [-2, -4, -8, -4, -2],
                       [-1, -2, -4, -2, -1]], np.float32)

    t = try_dask_filter2D('./data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                          kernel,
                          'res_dask.tiff',
                          int(sys.argv[1]),
                          int(sys.argv[2]))
