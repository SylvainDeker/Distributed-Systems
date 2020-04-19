import os
import sys
from dask.distributed import Client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window

from tile.buildCollectionTile import build_collection_tile
from tile.tile import Tile


from collections import OrderedDict
from shapely.geometry import mapping
import fiona
import pprint
import dask

print(Client(sys.argv[1]))


kernel = np.array([[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]], np.float32)

(collection, info) = build_collection_tile(
                                    'data/NE1_50M_SR_W/NE1_50M_SR_W.tif')

output = []
for t in collection:
    output.append(dask.delayed(t.filter2D)(kernel))

with rasterio.open('res.tif', 'w',
                   driver=info.driver,
                   width=info.width, height=info.height, count=info.count,
                   dtype=info.dtypes[0], transform=info.transform) as dst:

# TODO fixme: unknow type t:
    for t in output:
        (x0, y0, x1, y1) = t.bounding_polygon.bounds
        (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
        for i in info.indexes:
            dst.write(t.img[i-1],
                      window=Window(y0, x0, y1-y0, x1-x0),
                      indexes=i)
