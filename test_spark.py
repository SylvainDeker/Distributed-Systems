#! /bin/python3
import sys
from pyspark import SparkContext
from Tile.buildCollectionTile import buildCollectionTile
from Tile import Tile
import cv2 as cv
import numpy as np


(collection,height,width,channels) = buildCollectionTile('./data/NE1_50M_SR_W/NE1_50M_SR_W.tif')

sc = SparkContext()
rdd1 = sc.parallelize(collection)
kernel = np.array([[0, -1, 0],
               [-1, 4, -1],
               [0, -1, 0]], np.float32)
rdd2 = rdd1.map(lambda n: n.filter2D(kernel))
collection_res = rdd2.collect()

# print(collection_res)
# build puzzle
# img = np.zeros((channels,height,width))
# for tile in collection_res:
#     ((x0,y0),(x1,y1)) = tile.points
#     img[:,x0:x1,y0:y1] = tile.img
#
# # get result
# img = np.uint8(img)
# tmp = np.moveaxis(img,0,-1)
# cv.imwrite("res.png",cv.cvtColor(tmp,cv.COLOR_RGB2BGR))
#



# print(result)
