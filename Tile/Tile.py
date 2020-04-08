#! /bin/python3
import numpy as np
import cv2 as cv

from shapely.geometry import Polygon


def zero_padding(dim, x0, y0, x1, y1):
    edge_x, edge_y = min(dim[0]-x0, x1-x0), min(dim[1]-y0, y1-y0)
    lx, ly = np.clip(x1-dim[0], 0, None), np.clip(y1-dim[1], 0, None)

    return (edge_x, edge_y, lx, ly)


class Tile:
    """docstring for Tile."""

    def __init__(self, img, x0, y0, x1, y1):
        dim = (img.shape[1], img.shape[2])
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("dim",dim)
        # print("x0",x0)
        # print("y0",y0)
        # print("x1",x1)
        # print("y1",y1)

        assert x0 >= 0
        assert y0 >= 0
        assert x1 > x0
        assert y1 > y0
        assert x0 < dim[0]
        assert y0 < dim[1]
        self.bounds = ((x0, y0), (x1, y1))
        wide = x1-x0
        height = y1-y0
        self._bounding_polygon = Polygon([(x0, y0),
                                          (x0, y0+height),
                                          (x0+wide, y0+height),
                                          (x0+wide, y0)])
        (edge_x, edge_y, lx, ly) = zero_padding(dim, x0, y0, x1, y1)

        img_0_padded = np.pad(img[:, x0:edge_x+x0, y0:edge_y+y0],
                              ((0, 0), (0, lx), (0, ly)),
                              'constant', constant_values=0)
        self.img = np.copy(img_0_padded)

        # print("x1-x0,y1-y0",x1-x0,y1-y0)
        # print("lx,ly",lx,ly)
        # print("edge_x,edge_y",edge_x,edge_y)

        assert x1-x0 == self.img.shape[1]
        assert y1-y0 == self.img.shape[2]

    def _get_bounding_polygon(self):
        return self._bounding_polygon

    def _set_bounding_polygon(self):
        sys.stderr.write("Write access forbidden in \"bounding_polygon\"\n")
        sys.exit(-1)

    def filter2D(self, kernel):
        img = np.moveaxis(self.img, 0, -1)
        img = cv.filter2D(img, -1, kernel)
        img = np.moveaxis(img, -1, 0)
        self.img = img
        return self

    bounding_polygon = property(_get_bounding_polygon, _set_bounding_polygon)


if __name__ == "__main__":
    from shapely.geometry import mapping
    import rasterio
    import fiona
    from collections import OrderedDict
    import pprint

    data = rasterio.open('../data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
    img = np.array([data.read(1), data.read(2), data.read(3)])

    print("Input img shape:", img.shape)

    # tile = Tile(img,5200,10500,6000,13000)
    tile = Tile(img, 0, 0, 1000, 900)

    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]], np.float32)

    tile.filter2D(kernel)
    # Result in ./res.png
    tmp = np.moveaxis(tile.img, 0, -1)
    # print(tmp.shape)
    cv.imwrite("res.png", cv.cvtColor(tmp, cv.COLOR_RGB2BGR))

    # ----------------- Test de Polygon
    print(tile.bounding_polygon)

    # ----------------- Test de Fiona
    schema = {'geometry': 'Polygon',
              'properties': OrderedDict([('id', 'int')])}

    with fiona.open("res.shp", mode="w",
                    driver="ESRI Shapefile",
                    schema=schema, crs=data.crs) as dst:
        record = {'geometry': mapping(tile.bounding_polygon),
                  'properties': OrderedDict([('id', '0')])}
        dst.write(record)

    with fiona.open("res.shp") as src:
        pprint.pprint(src[0])

    print("OK")
