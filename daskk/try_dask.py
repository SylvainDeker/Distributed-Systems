import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dask.distributed import Client
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window

from Tile.buildCollectionTile import build_collection_tile
from Tile.Tile import Tile



def try_dask_filter2D(pathimage, kernel, output_pathimage):
    client = Client()
    # client.upload_file("Tile/Tile.py")
    (collection, info) = build_collection_tile(pathimage)


    rdd = db.from_sequence(collection).map(lambda n: n.filter2D(kernel))
    collection2 = rdd.compute()
    # print(len(collection2))
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

if __name__ == '__main__':

    kernel = np.array([[-1, -2, -4, -2, -1],
                       [-2, -4, -8, -4, -2],
                       [-4, -8, 84, -8, -4],
                       [-2, -4, -8, -4, -2],
                       [-1, -2, -4, -2, -1]], np.float32)

    dask_filter2D('./data/NE1_50M_SR_W/NE1_50M_SR_W.tif', kernel, 'res_dask.tiff')
