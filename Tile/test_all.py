#! /bin/python3
from Tile import Tile
from buildCollectionTile import buildCollectionTile
import numpy as np
import rasterio
import cv2 as cv

kernel = np.array([[0, -1, 0],
               [-1, 4, -1],
               [0, -1, 0]], np.float32)

(collection,height,width,chanels) = buildCollectionTile('../data/NE1_50M_SR_W/NE1_50M_SR_W.tif')

img = np.zeros((chanels,height,width))

for tile in collection:
    ((x0,y0),(x1,y1)) = tile.points
    tile.filter2D(kernel)
    img[:,x0:x1,y0:y1] = tile.img
img = np.uint8(img)





tmp = np.moveaxis(img,0,-1)

print(tmp)
print(tmp.shape)

cv.imwrite("res.png",cv.cvtColor(tmp,cv.COLOR_RGB2BGR))
