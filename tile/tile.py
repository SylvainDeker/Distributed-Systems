#! /bin/python3

import numpy as np
import cv2 as cv
import rasterio
from rasterio.windows import Window
from shapely.geometry import box
from rasterio.crs import CRS


class Tile:
    """docstring for Tile."""

    def __init__(self, pathimage, bounding_polygon):
        """
        :param pathimage: blabla
        :param bounding_polygon: blabla
        """

        (x0, y0, x1, y1) = [int(i) for i in bounding_polygon.bounds]

        img = []
        with rasterio.open(pathimage) as data:
            for i in data.indexes:
                img.append(data.read(i, window=Window(y0, x0, y1-y0, x1-x0)))

        self._img = np.asarray(img)
        x1 = self._img.shape[1]+x0
        y1 = self._img.shape[2]+y0

        self._bounding_polygon = box(x0, y0, x1, y1)

    @property
    def img(self):
        return self._img

    @property
    def bounding_polygon(self):
        return self._bounding_polygon

    def filter2D(self, kernel):
        """
        :param kernel:
        """
        dtype = self.img.dtype
        img = np.moveaxis(self._img, 0, -1)
        img = cv.filter2D(img, -1, kernel)
        img = np.moveaxis(img, -1, 0)
        self._img = img.astype(dtype)
        return self


if __name__ == "__main__":

    from shapely.geometry import mapping
    import fiona
    from collections import OrderedDict
    import pprint

    x0, y0, x1, y1 = 0, 0, 10800, 5400

    kernel = np.array(
        [[0, -1, 0],
         [-1, 4, -1],
         [0, -1, 0]],
        np.float32
    )
    tile = Tile('../data/NE1_50M_SR_W/NE1_50M_SR_W.tif', box(x0, y0, x1, y1))

    # tile.filter2D(kernel)
    # Result in ./res.png
    tmp = np.moveaxis(tile.img, 0, -1)
    print(tmp.shape)
    cv.imwrite("res.png", cv.cvtColor(tmp, cv.COLOR_RGB2BGR))

    # ----------------- Test de Polygon
    print(tile.bounding_polygon)

    # ----------------- Test de Fiona
    schema = {
        'geometry': 'Polygon',
        'properties': OrderedDict([('id', 'int')])
    }

    with fiona.open("res.shp", mode="w",
                    driver="ESRI Shapefile",
                    schema=schema, crs=CRS.from_epsg(4326)) as dst:
        dst.write(
            {
                'geometry': mapping(tile.bounding_polygon),
                'properties': OrderedDict([('id', '0')])
            }
        )

    with fiona.open("res.shp") as src:
        pprint.pprint(src[0])

    print("OK")
