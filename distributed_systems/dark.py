import rasterio
from rasterio.windows import Window
import numpy as np
import itertools
from shapely.geometry import Polygon
from dask.distributed import Client
from distributed_systems.tile import Tile
import dask
import yaml


def load_config(pathfile):
    # Default value
    data = {'imgleft': { 'gain': 1,
                         'mean': 0,
                         'stddev': 1},
            'imgright':{ 'gain': 1,
                         'mean': 0,
                         'stddev': 1}
            }

    with open(pathfile,"r") as src:
        data = yaml.safe_load(src)

    return data

def extract_collections(pathimage,unit_height=500,unit_width=500):

    with rasterio.open(pathimage) as data:
        info = data

    itr_h = int(info.height/unit_height) + (info.height % unit_height > 0)
    itr_w = int(info.width/unit_width) + (info.width % unit_width > 0)

    tile_lim_1 = int((itr_w)/3)
    tile_lim_2 = int((itr_w*2)/3)

    px_lim_1 = tile_lim_1 * unit_width
    px_lim_2 = tile_lim_2 * unit_width


    collection1 = []
    collection2 = []
    nb_item_c1 = 0
    nb_item_c2 = 0

    for i, j in itertools.product(range(itr_h), range(itr_w)):
        x0 = i * unit_height
        y0 = j * unit_width
        x1 = (i+1) * unit_height
        y1 = (j+1) * unit_width

        if y0 < px_lim_2:
            nb_item_c1 += 1
            collection1.append(Tile(pathimage, Polygon([(x0, y0),
                                                       (x1, y0),
                                                       (x1, y1),
                                                       (x0, y1)])))
        if y0 >= px_lim_1:
            nb_item_c2 += 1
            collection2.append(Tile(pathimage, Polygon([(x0, y0),
                                                       (x1, y0),
                                                       (x1, y1),
                                                       (x0, y1)])))
    nb_unit_width_collection1 = tile_lim_2
    nb_unit_width_collection2 = itr_w - tile_lim_1

    return (collection1,
            collection2,
            info,
            nb_unit_width_collection1,
            nb_unit_width_collection2,
            nb_item_c1,
            nb_item_c1,
            nb_unit_width_collection1 * unit_width,
            nb_unit_width_collection2 * unit_width -
                (unit_width - (info.width % unit_width)) *
                (info.width%unit_width > 0) )



def run_dask(pathimage, pathconfig):
    client = Client()
    (collection1, collection2, info, _, _, _, _, w1, w2) = extract_collections(
                                    pathimage)
    config = load_config(pathconfig)

    res1 = []
    res2 = []

    for t in collection1:
        (x0, y0, x1, y1) = t.bounding_polygon.bounds
        (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
        e = dask.delayed(t.add_noise)(config['imgleft']['gain'],
                                      config['imgleft']['mean'],
                                      config['imgleft']['stddev'])
        res1.append(e.compute())

    for t in collection2:
        (x0, y0, x1, y1) = t.bounding_polygon.bounds
        (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
        e = dask.delayed(t.add_noise)(config['imgright']['gain'],
                                      config['imgright']['mean'],
                                      config['imgright']['stddev'])
        res2.append(e.compute())


    with rasterio.open('res1.tif', 'w',
                       driver=info.driver,
                       width=w1, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:

        for t in res1:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)

    dec = info.width - w2
    with rasterio.open('res2.tif', 'w',
                       driver=info.driver,
                       width=w2, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:

        for t in res2:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0-dec), int(x1), int(y1-dec))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)

    client.close()





if __name__ == '__main__':
    from collections import OrderedDict
    from shapely.geometry import mapping
    import fiona
    import pprint

    # r = load_config('config.yaml')
    # print(r)

    run_dask('data/NE1_50M_SR_W/NE1_50M_SR_W.tif', 'config.yaml')


    # (collection1, collection2, info, _, _, _, _, w1, w2) = extract_collections(
    #                                 'data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
    #
    #
    # with rasterio.open('res1.tif', 'w',
    #                    driver=info.driver,
    #                    width=w1, height=info.height, count=info.count,
    #                    dtype=info.dtypes[0], transform=info.transform) as dst:
    #
    #     for t in collection1:
    #         (x0, y0, x1, y1) = t.bounding_polygon.bounds
    #         (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
    #         t.add_noise(1,0,0.1)
    #         for i in info.indexes:
    #             dst.write(t.img[i-1],
    #                       window=Window(y0, x0, y1-y0, x1-x0),
    #                       indexes=i)
    #
    # dec = info.width - w2
    # with rasterio.open('res2.tif', 'w',
    #                    driver=info.driver,
    #                    width=w2, height=info.height, count=info.count,
    #                    dtype=info.dtypes[0], transform=info.transform) as dst:
    #
    #     for t in collection2:
    #         (x0, y0, x1, y1) = t.bounding_polygon.bounds
    #         (x0, y0, x1, y1) = (int(x0), int(y0-dec), int(x1), int(y1-dec))
    #
    #         for i in info.indexes:
    #             dst.write(t.img[i-1],
    #                       window=Window(y0, x0, y1-y0, x1-x0),
    #                       indexes=i)
