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
    list_intersection_c1_c2 = []
    for i, j in itertools.product(range(itr_h), range(itr_w)):
        x0 = i * unit_height
        y0 = j * unit_width
        x1 = (i+1) * unit_height
        y1 = (j+1) * unit_width

        t1 = None
        t2 = None
        if y0 < px_lim_2:
            nb_item_c1 += 1
            t1 = Tile(pathimage,
                     Polygon([(x0, y0),
                              (x1, y0),
                              (x1, y1),
                              (x0, y1)]),
                     (i,j))
            collection1.append(t1)

        if y0 >= px_lim_1:
            nb_item_c2 += 1
            t2 = Tile(pathimage,
                      Polygon([(x0, y0),
                               (x1, y0),
                               (x1, y1),
                               (x0, y1)]),
                        (i,j))
            collection2.append(t2)

        if y0 >= px_lim_1 and y0 < px_lim_2 and t1 != None and t2 != None:
            list_intersection_c1_c2.append((len(collection1)-1,len(collection2)))

    nb_unit_width_collection1 = tile_lim_2
    nb_unit_width_collection2 = itr_w - tile_lim_1

    return (collection1,
            collection2,
            info,
            nb_unit_width_collection1,
            nb_unit_width_collection2,
            nb_item_c1,
            nb_item_c2,
            nb_unit_width_collection1 * unit_width,
            nb_unit_width_collection2 * unit_width -
                (unit_width - (info.width % unit_width)) *
                (info.width%unit_width > 0),
            list_intersection_c1_c2 )


def run_dask(pathimage, pathconfig):
    client = Client()
    # DARK-FDR-001 step 1
    (collection1, collection2, info, _, _, _, _, w1, w2,list_intersection_c1_c2) = extract_collections(
                                    pathimage)
    config = load_config(pathconfig)


    # DARK-FDR-001 step 2
    collection1_res = []
    collection2_res = []
    for t in collection1:
        (x0, y0, x1, y1) = t.bounding_polygon.bounds
        (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
        e = dask.delayed(t.add_noise)(config['imgleft']['gain'],
                                      config['imgleft']['mean'],
                                      config['imgleft']['stddev'])
        collection1_res.append(e.compute())

    for t in collection2:
        (x0, y0, x1, y1) = t.bounding_polygon.bounds
        (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
        e = dask.delayed(t.add_noise)(config['imgright']['gain'],
                                      config['imgright']['mean'],
                                      config['imgright']['stddev'])
        collection2_res.append(e.compute())

    collection1 = collection1_res
    collection2 = collection2_res

    # DARK-FDR-001 step 3
    # Already given by list_intersection_c1_c2

    # DARK-FDR-001 step 4 & 5
    computed_gains1 = np.empty((len(list_intersection_c1_c2),len(info.indexes)))
    computed_gains2 = np.empty((len(list_intersection_c1_c2),len(info.indexes)))
    for i in range(len(list_intersection_c1_c2)):
        mr1 = collection1[list_intersection_c1_c2[i][0]].mean_radiosity
        mr2 = collection2[list_intersection_c1_c2[i][1]].mean_radiosity
        computed_gains1[i] = np.sqrt(mr2/mr1)
        computed_gains2[i] = np.sqrt(mr1/mr2)

    # DARK-FDR-001 step 6
    computed_gains1 = np.moveaxis(computed_gains1,1,0)
    computed_gains2 = np.moveaxis(computed_gains2,1,0)
    for i in range(len(info.indexes)):
        computed_gains1[i] = np.convolve(computed_gains1[i],
                                         config['kernel_gain'],
                                         'same')
        computed_gains2[i] = np.convolve(computed_gains2[i],
                                         config['kernel_gain'],
                                         'same')
    computed_gains1 = np.moveaxis(computed_gains1,1,0)
    computed_gains2 = np.moveaxis(computed_gains2,1,0)

    # DARK-FDR-001 step 7
    intersection_res = []
    for i in range(len(list_intersection_c1_c2)):
        e1 = dask.delayed(collection1[list_intersection_c1_c2[i][0]].apply_gain)(computed_gains1[i])
        e2 = dask.delayed(collection2[list_intersection_c1_c2[i][1]].apply_gain)(computed_gains2[i])
        intersection_res.append((e1.compute(), e2.comptue()))

    # DARK-FDR-001 step 8
    res4 = []
    for i in range(len(intersection_res)):
        e1 = dask.delayed(intersection_res[i][0].filter2D)(np.array(config['kernel_blur']))
        e2 = dask.delayed(intersection_res[i][1].filter2D)(np.array(config['kernel_blur']))
        res4.append((e1.compute(), e2.comptue()))


    with rasterio.open('collection1.tif', 'w',
                       driver=info.driver,
                       width=w1, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:

        for t in collection1:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)

    dec = info.width - w2
    with rasterio.open('collection2.tif', 'w',
                       driver=info.driver,
                       width=w2, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:

        for t in collection2:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0-dec), int(x1), int(y1-dec))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)

    with rasterio.open('All.tif', 'w',
                       driver=info.driver,
                       width=info.width, height=info.height, count=info.count,
                       dtype=info.dtypes[0], transform=info.transform) as dst:
        for t in collection1:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)

        for t in collection2:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
            for i in info.indexes:
                dst.write(t.img[i-1],
                          window=Window(y0, x0, y1-y0, x1-x0),
                          indexes=i)
        for (t,_) in res4:
            (x0, y0, x1, y1) = t.bounding_polygon.bounds
            (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
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
