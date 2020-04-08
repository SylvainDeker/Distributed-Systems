import rasterio
import numpy as np
import itertools
from shapely.geometry import Polygon

if __name__ == '__main__':
    from Tile import Tile
else:
    from Tile.Tile import Tile


def build_collection_tile(pathimage):
    w = 9
    h = 9
    data = rasterio.open(pathimage)
    img = np.array([data.read(1), data.read(2), data.read(3)])
    unit_height = int(data.height/h)
    unit_width = int(data.width/w)

    print(img.shape)
    print(unit_height)
    print(unit_width)

    itr_w = w + (1 if data.width % w > 0 else 0)
    itr_h = h + (1 if data.height % h > 0 else 0)
    start_w = 0
    start_h = 0
    collection = []
    print(itr_h, itr_w)

    for j, i in itertools.product(range(itr_h), range(itr_w)):
        start_h = j * unit_height
        start_w = i * unit_width
        end_h = (j+1) * unit_height
        end_w = (i+1) * unit_width
        # collection.append(Tile(img, start_h, start_w, end_h, end_w))
        collection.append(Tile(img, Polygon([(start_h, start_w),
                                             (start_h, end_w),
                                             (end_h, end_w),
                                             (end_h, start_w)])))

    return (collection, data)


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
    height = info.height
    width = info.width
    channels = info.count

    img = np.zeros((channels, height, width))
    schema = {'geometry': 'Polygon',
              'properties': OrderedDict([('id', 'int')])}

    with fiona.open("res.shp", mode="w",
                    driver="ESRI Shapefile",
                    schema=schema, crs=info.crs) as dst:

        for tile in collection:
            record = {'geometry': mapping(tile.bounding_polygon),
                      'properties': OrderedDict([('id', '0')])}
            dst.write(record)
            (x0, y0, x1, y1) = tile.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            tile.filter2D(kernel)
            img[:, x0:x1, y0:y1] = tile.img

    img = np.uint8(img)

    res = rasterio.open("res.tiff", 'w',
                        driver=info.driver,
                        width=info.width,
                        height=info.height,
                        count=info.count,
                        dtype=info.dtypes[0],
                        crs=info.crs,
                        transform=info.transform)

    for i in range(res.count):
        res.write(img[i], i+1)

    with fiona.open("res.shp") as src:
        for i in src:
            pprint.pprint(i)
