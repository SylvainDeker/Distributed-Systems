#! /bin/python3
import sys
import numpy as np
from pyspark import SparkContext
from Tile.buildCollectionTile import build_collection_tile
from Tile import Tile


(collection, info) = build_collection_tile(
                    './data/NE1_50M_SR_W/NE1_50M_SR_W.tif')

sc = SparkContext()
rdd1 = sc.parallelize(collection)
kernel = np.array([[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]], np.float32)
rdd2 = rdd1.map(lambda n: n.filter2D(kernel))
collection_res = rdd2.collect()

# print(collection_res)
# # build puzzle
# img = np.zeros((channels, height, width))
# for tile in collection_res:
#     ((x0, y0), (x1, y1)) = tile.bounds
#     img[:, x0:x1, y0:y1] = tile.img
# res = rasterio.open("res.tiff", 'w',
#                     driver=info.driver,
#                     width=info.width,
#                     height=info.height,
#                     count=info.count,
#                     dtype=info.dtypes[0],
#                     crs=info.crs,
#                     transform=info.transform)
#
# for i in range(res.count):
#     res.write(img[i], i+1)
