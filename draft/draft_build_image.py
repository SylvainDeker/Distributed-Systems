import numpy as np
from rasterio.windows import Window
import rasterio


im = rasterio.open('data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
print(im.name)
print(im.driver)
print(im.mode)
print(im.count)
print(im.width)
print(im.height)
print(im.indexes)
print(im.dtypes)

print(im.bounds) # Boundingbox
# BoundingBox(left=-179.9, bottom=-89.9, right=179.9, top=90.0)
#  Covers the world from -179.9 meters (in this case) to 179.9 meters, left to right
#   and -89,9 meters to 90.0 meters bottom to top


print(im.transform)
print(im.transform*(0,0)) #  Upper left corner
print(im.transform*(im.width,im.height)) #  Lower right corner
print(im.crs)#  Result in meters from the CRS (Coordinate Reference System)
print(im.read(1)) #  return a numpy N-D array
print(im.read(1)[1,0]) #  return a numpy 1st color value from the [1,0] pixel
print(im.index(x=-190.1,y=-80.1)) #  get the coord pixel from distance corrd

im.close

h = 11
w = 13

res = rasterio.open('data/NE1_50M_SR_W_w'+str(w)+'_h'+str(h)+'/NE1_50M_SR_W.tif','w',
                    driver=im.driver,
                    width=w,
                    height=h,
                    count=im.count,
                    dtype=im.dtypes[0],
                    crs=im.crs,
                    transform=im.transform)

res.write(im.read(1, window=Window(5365,1334,w,h)),1)
res.write(im.read(2, window=Window(5365,1334,w,h)),2)
res.write(im.read(3, window=Window(5365,1334,w,h)),3)



# print(im.read(1, window=Window(0, 0, 10, 10)).shape) #  return a numpy N-D array
# print(im.read(1).shape)
