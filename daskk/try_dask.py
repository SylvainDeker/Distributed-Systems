import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dask.distributed import Client
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window

from tile.buildCollectionTile import build_collection_tile
from tile.tile import Tile

if __name__ == '__main__':


    client = Client()
    # client.upload_file("tile/tile.py")
    (collection, info) = build_collection_tile(
                        './data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
    kernel = np.array([[-2, -1, -2],
                       [-1, 12, -1],
                       [-2, -1, -2]], np.float32)



    rdd = db.from_sequence(collection).map(lambda n: n.filter2D(kernel))
    collection2 = rdd.compute()
    print(len(collection2))
    with rasterio.open('res_dask.tiff', 'w',
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
