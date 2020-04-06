import numpy as np
import rasterio
from Tile import Tile

def buildCollectionTile(pathimage):
    w=2
    h=2
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
    for i in range(itr_w):
        for j in range(itr_h):
            start_w = i * unit_width
            start_h = j* unit_height
            end_w = (i+1) * unit_width-1
            end_h = (j+1) * unit_height-1
            collection.append(Tile(img,start_w,start_h,end_w,end_h))

    return (collection,data.height,data.width,len(data.indexes))
