import numpy as np
import rasterio
from Tile import Tile

def buildCollectionTile(pathimage):
    w=9
    h=9
    data = rasterio.open(pathimage)
    img = np.array([data.read(1),data.read(2),data.read(3)])
    unit_height =int(data.height/h)
    unit_width = int(data.width/w)

    print(img.shape)
    print(unit_height)
    print(unit_width)

    itr_w = w + (1 if data.width % w > 0 else 0 )
    itr_h = h + (1 if data.height % h > 0 else 0 )
    start_w=0
    start_h=0
    collection = []
    print(itr_h,itr_w)
    for j in range(itr_h):
        for i in range(itr_w):
            start_h = j* unit_height
            start_w = i * unit_width
            end_h = (j+1) * unit_height
            end_w = (i+1) * unit_width
            collection.append(Tile(img,start_h,start_w,end_h,end_w))

    return (collection,data.height,data.width,len(data.indexes))


if __name__ == '__main__':
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
