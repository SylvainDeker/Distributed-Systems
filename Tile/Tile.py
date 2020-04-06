#! /bin/python3
import numpy as np
import cv2 as cv
from shapely.geometry import Polygon

def zero_padding(dim,x0,y0,x1,y1):
    # print("dim",dim)
    # print("x0",x0)
    # print("y0",y0)
    # print("x1",x1)
    # print("y1",y1)
    lx,ly = np.clip(x1-dim[0],0,None), np.clip(y1-dim[1],0,None)
    edge_x,edge_y = min(dim[0],x1), min(dim[1],y1)
    # print("edge_x,edge_y",edge_x,edge_y)
    # print("lx,ly",lx,ly)
    return (edge_x,edge_y,lx,ly)

class Tile:
    """docstring for Tile."""

    def __init__(self,img,x0,y0,x1,y1):
        assert x0>=0
        assert y0>=0
        assert x1>x0
        assert y1>y0
        dim = (img.shape[1],img.shape[2])
        assert x0 < dim[0]
        assert x1 < dim[1]
        self.points = ((x0,y0),(x1,y1))

        (edge_x,edge_y,lx,ly) = zero_padding(dim,x0,y0,x1,y1)
        img_0_padded = np.pad(img[:,x0:edge_x,y0:edge_y], ((0,0),(0, lx),(0,ly)), 'constant', constant_values=0)
        self.img = np.copy(img_0_padded)

        assert x1-x0==self.img.shape[1]
        assert y1-y0==self.img.shape[2]


    def getPolygon(self):
        ((x0,y0),(x1,y1)) = self.points
        wide = x1-x0
        height = y1-y0
        return Polygon([(x0,y0),(x0,y0+height),(x0+wide,y0+height),(x0+wide,y0)])

    def filter2D(self,kernel):
        img = np.moveaxis(self.img,0,-1)
        img = cv.filter2D(img,-1,kernel)
        img = np.moveaxis(img,-1,0)
        ((x0,y0),(x1,y1)) = self.points
        return Tile(img,x0,y0,x1,y1)


if __name__ == "__main__":
    import rasterio

    data = rasterio.open('../data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
    img = np.array([data.read(1),data.read(2),data.read(3)])

    print("Input img shape:",img.shape)

    # tile = Tile(img,5200,10500,6000,13000)
    tile = Tile(img,0,0,1000,900)

    kernel = np.array([[0, -1, 0],
                   [-1, 4, -1],
                   [0, -1, 0]], np.float32)

    tile.filter2D(kernel)
    # Result in ./res.png
    tmp = np.moveaxis(tile.img,0,-1)
    # print(tmp.shape)
    cv.imwrite("res.png",cv.cvtColor(tmp,cv.COLOR_RGB2BGR))


    print(tile.getPolygon())
    print("Area:",tile.getPolygon().area)
