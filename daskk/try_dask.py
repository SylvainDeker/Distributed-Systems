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

if __name__ == '__main__':


    client = Client()
    # client.upload_file("Tile/Tile.py")
    (collection, info) = build_collection_tile(
                        './data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]], np.float32)



    rdd = db.from_sequence(collection)#.map(lambda n: n.filter2D(kernel))
    collection2 = rdd.compute()
    print(len(collection2))
    with rasterio.open('res.tif', 'w',
                       driver=info.driver,
                       width=info.width, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:

        for t in collection:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)
