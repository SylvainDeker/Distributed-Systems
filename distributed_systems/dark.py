import rasterio
from rasterio.windows import Window
import numpy as np
import itertools
from shapely.geometry import Polygon
from dask.distributed import Client
from distributed_systems.tile import Tile
import dask
import yaml


class Dark:
    def __init__(self):
        self.shape_image = (0, 0)
        self.shape_tile = (500, 500)

    # def __init__(self, shape_image, shape_tile = (500,500)):
    #     (height, width) = shape_image
    #     self.shape_image = (height, width)
    #     self.shape_tile = shape_tile

    @property
    def shape_all_tiles(self):
        nb_tile_h = int(self.shape_image[0] / self.shape_tile[0]) + (self.shape_image[0] % self.shape_tile[0] > 0)
        nb_tile_w = int(self.shape_image[1] / self.shape_tile[1]) + (self.shape_image[1] % self.shape_tile[1] > 0)
        return (nb_tile_h, nb_tile_w)

    @property
    def vertical_frontiers(self):
        (_, nb_tile_w) = self.shape_all_tiles
        return (int(nb_tile_w/3),int((2*nb_tile_w)/3))

    @property
    def shape_collection_left(self):
        (nb_tile_h, nb_tile_w) = self.shape_all_tiles
        (vf1, vf2) = self.vertical_frontiers
        return (nb_tile_h, vf2 )

    @property
    def shape_collection_right(self):
        (nb_tile_h, nb_tile_w) = self.shape_all_tiles
        (vf1, vf2) = self.vertical_frontiers
        return (nb_tile_h, nb_tile_w - vf1 )


    @property
    def shape_collection_intersection(self):
        (nb_tile_h, nb_tile_w) = self.shape_all_tiles
        (vf1, vf2) = self.vertical_frontiers
        return (nb_tile_h, vf2 - vf1 )

    @property
    def shape_image_left(self):
        (sih, siw) = self.shape_image
        (sclh, sclw) = self.shape_collection_left
        (sth, stw) = self.shape_tile
        return (sih, sclw*stw)

    @property
    def shape_image_right(self):
        (sih, siw) = self.shape_image
        (scrh, scrw) = self.shape_collection_right
        (sth, stw) = self.shape_tile
        h = sih
        w = scrw * stw - (stw - (siw % stw)) * (siw % stw > 0)
        return (h, w)

    def coord_collection_from_right_to_left(self, i, j):
        return (i, j + self.vertical_frontiers[0] )

    def coord_collection_from_left_to_right(self, i, j):
        return (i, j - self.vertical_frontiers[0])

    def coord_collection_from_right_to_global(self, i, j):
        return (i, j + self.vertical_frontiers[0])

    def coord_collection_from_left_to_global(self, i, j):
        return (i, j)

    def list_intersection_coord_glob(self):
        (nb_tile_h, nb_tile_w) = self.shape_all_tiles
        (vf1, vf2) = self.vertical_frontiers

        list = []
        for i, j in itertools.product(range(nb_tile_h), range(nb_tile_w)):
            y0 = j * self.shape_tile[1]
            if j >= vf1 and j < vf2:
                list.append((i, j))
        return list
