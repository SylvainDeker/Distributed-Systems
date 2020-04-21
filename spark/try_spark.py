#! /bin/python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from pyspark import SparkContext
from Tile.buildCollectionTile import build_collection_tile
from Tile.Tile import Tile
import rasterio
import time

def try_spark_filter2D(pathimage, kernel, output_pathimage):
    (collection, info) = build_collection_tile(pathimage)
    sc = SparkContext()

    timer = time.time()

    rdd = sc.parallelize(collection)
    collection_res = []
    for n in rdd.toLocalIterator():
        collection_res.append(n.filter2D(kernel))

    timer = time.time() - timer

    # rdd = rdd.map(lambda n: n.filter2D(kernel))
    # collection_res = rdd.collect()

    return timer

    img = np.empty((info.count, info.height, info.width)).astype(info.dtypes[0])
    for tile in collection_res:
        (x0, y0, x1, y1) = tile.bounding_polygon.bounds
        (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
        img[:, x0:x1, y0:y1] = tile.img
    res = rasterio.open(output_pathimage, 'w',
                        driver=info.driver,
                        width=info.width,
                        height=info.height,
                        count=info.count,
                        dtype=info.dtypes[0],
                        crs=info.crs,
                        transform=info.transform)

    for i in range(res.count):
        res.write(img[i], i+1)

if __name__ == '__main__':

    kernel = np.array([[-1, -2, -4, -2, -1],
                       [-2, -4, -8, -4, -2],
                       [-4, -8, 84, -8, -4],
                       [-2, -4, -8, -4, -2],
                       [-1, -2, -4, -2, -1]], np.float32)

    t = try_spark_filter2D('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                   kernel,
                   'res_spark.tiff')

    print(t)
