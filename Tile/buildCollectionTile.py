import rasterio
from rasterio.windows import Window
import numpy as np
import itertools
from shapely.geometry import Polygon

if __name__ == '__main__':
    from Tile import Tile
else:
    from Tile.Tile import Tile


def build_collection_tile(pathimage):

    with rasterio.open(pathimage) as data:
        info = data

    unit_height = 500
    unit_width = 500
    itr_h = int(info.height/unit_height) + (1 if unit_height % info.height > 0
                                            else 0)
    itr_w = int(info.width/unit_width) + (1 if unit_width % info.width > 0
                                          else 0)

    collection = []
    for i, j in itertools.product(range(itr_h), range(itr_w)):
        x0 = i * unit_height
        y0 = j * unit_width
        x1 = (i+1) * unit_height
        y1 = (j+1) * unit_width

        collection.append(Tile(pathimage, Polygon([(x0, y0),
                                                   (x1, y0),
                                                   (x1, y1),
                                                   (x0, y1)])))
    return (collection, info)


if __name__ == '__main__':
    from collections import OrderedDict
    from shapely.geometry import mapping
    import fiona
    import pprint

    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]], np.float32)

    (collection, info) = build_collection_tile(
                                    '../data/NE1_50M_SR_W/NE1_50M_SR_W.tif')

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
