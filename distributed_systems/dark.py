import rasterio
from rasterio.windows import Window
import numpy as np
import itertools
from shapely.geometry import Polygon
from dask.distributed import Client
from distributed_systems.tile import Tile
from pyspark import SparkContext
from pyspark import SparkConf
import dask
import yaml


class Dark:
    def __init__(self, pathimage, shape_tile, pathconfig):
        self.pathimage = pathimage
        self.shape_tile = shape_tile
        self.pathconfig = pathconfig
        self.shape_image = None
        self.collection_left = []
        self.collection_right = []


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

    def index_collection_left(self, i, j):
        (h, w) = self.shape_collection_left
        return i*w+j

    def index_collection_right(self, i, j):
        (h, w) = self.shape_collection_right
        return i*w+j

    def coord_from_index_collection_left(self, i):
        (h, w) = self.shape_collection_left
        return (int(i/w), i%w)

    def coord_from_index_collection_right(self, i):
        (h, w) = self.shape_collection_right
        return (int(i/w), i%w)

    def coord_collection_from_right_to_left(self, i, j):
        return (i, j + self.vertical_frontiers[0] )

    def coord_collection_from_left_to_right(self, i, j):
        return (i, j - self.vertical_frontiers[0])

    def coord_image_from_right_to_left(self, i, j):
        return (i, j+self.vertical_frontiers[0]*self.shape_tile[1])

    def coord_image_from_left_to_right(self, i, j):
        return (i, j-self.vertical_frontiers[0]*self.shape_tile[1])

    def list_intersection_coord_left(self):
        (nb_tile_h, nb_tile_w) = self.shape_all_tiles
        (vf1, vf2) = self.vertical_frontiers

        list = []
        for i, j in itertools.product(range(nb_tile_h), range(nb_tile_w)):
            y0 = j * self.shape_tile[1]
            if j >= vf1 and j < vf2:
                list.append((i, j))
        return list

    def extract_collections(self):

        with rasterio.open(self.pathimage) as data:
            info = data
        self.shape_image = (info.height, info.width)
        self.indexes = len(info.indexes)



        self.collection_left = []
        for i in range(self.shape_collection_left[0]):
            for j in range(self.shape_collection_left[1]):
                x0 = i * self.shape_tile[0]
                y0 = j * self.shape_tile[1]
                x1 = (i+1) * self.shape_tile[0]
                y1 = (j+1) * self.shape_tile[1]

                t1 = Tile(self.pathimage,
                          Polygon([(x0, y0),
                                   (x1, y0),
                                   (x1, y1),
                                   (x0, y1)]),
                          (i,j))
                self.collection_left.append(t1)


        self.collection_right = []
        for i in range(self.shape_collection_right[0]):
            for j in range(self.shape_collection_right[1]):
                i,j = self.coord_collection_from_right_to_left(i,j)
                x0 = i * self.shape_tile[0]
                y0 = j * self.shape_tile[1]
                x1 = (i+1) * self.shape_tile[0]
                y1 = (j+1) * self.shape_tile[1]

                t1 = Tile(self.pathimage,
                          Polygon([(x0, y0),
                                   (x1, y0),
                                   (x1, y1),
                                   (x0, y1)]),
                          (i,j))
                self.collection_right.append(t1)



    def write_image_left(self,pathfile='collection_left.tiff'):
        with rasterio.open(self.pathimage) as data:
            info = data

        with rasterio.open(pathfile, 'w',
                           driver=info.driver,
                           width=self.shape_image_left[1],
                           height=self.shape_image_left[0],
                           count=info.count,
                           dtype=info.dtypes[0],
                           transform=info.transform) as dst:

            for t in self.collection_left:
                (x0, y0, x1, y1) = t.bounding_polygon.bounds
                (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
                for w in info.indexes:
                    dst.write(t.img[w-1],
                              window=Window(y0, x0, y1-y0, x1-x0),
                              indexes=w)

    def write_image_glob(self,pathfile='collection_glob.tiff'):
        with rasterio.open(self.pathimage) as data:
            info = data

        with rasterio.open(pathfile, 'w',
                           driver=info.driver,
                           width=self.shape_image[1],
                           height=self.shape_image[0],
                           count=info.count,
                           dtype=info.dtypes[0],
                           transform=info.transform) as dst:

            for t in self.collection_left:
                (x0, y0, x1, y1) = t.bounding_polygon.bounds
                (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
                for w in info.indexes:
                    dst.write(t.img[w-1],
                              window=Window(y0, x0, y1-y0, x1-x0),
                              indexes=w)

            for t in self.collection_right:
                (x0, y0, x1, y1) = t.bounding_polygon.bounds
                (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
                for w in info.indexes:
                    dst.write(t.img[w-1],
                              window=Window(y0, x0, y1-y0, x1-x0),
                              indexes=w)


    def write_image_right(self,pathfile='collection_right.tiff'):
        with rasterio.open(self.pathimage) as data:
            info = data

        with rasterio.open(pathfile, 'w',
                           driver=info.driver,
                           width=self.shape_image_right[1],
                           height=self.shape_image_right[0],
                           count=info.count,
                           dtype=info.dtypes[0],
                           transform=info.transform) as dst:

            for t in self.collection_right:
                (x0, y0, x1, y1) = t.bounding_polygon.bounds
                (x0, y0, x1, y1) = (int(x0), int(y0), int(x1), int(y1))
                (x0, y0) = self.coord_image_from_left_to_right(x0, y0)
                (x1, y1) = self.coord_image_from_left_to_right(x1, y1)

                for w in info.indexes:
                    dst.write(t.img[w-1],
                              window=Window(y0, x0, y1-y0, x1-x0),
                              indexes=w)


    def load_config(self, pathfile):
        with open(pathfile,"r") as src:
            data = yaml.safe_load(src)
        return data


    def run_dask(self):
        config = self.load_config(self.pathconfig)
        client = Client()
        # DARK-FDR-001 step 1
        self.extract_collections()

        # DARK-FDR-001 step 2
        for i in range(len(self.collection_left)):
            e = dask.delayed(self.collection_left[i].add_noise)(
                                              config['imgleft']['gain'],
                                              config['imgleft']['mean'],
                                              config['imgleft']['stddev'])
            self.collection_left[i] = e.compute()

        for i in range(len(self.collection_right)):
            e = dask.delayed(self.collection_right[i].add_noise)(
                                              config['imgleft']['gain'],
                                              config['imgleft']['mean'],
                                              config['imgleft']['stddev'])
            self.collection_right[i] = e.compute()

        # DARK-FDR-001 step 3
        intersection = self.list_intersection_coord_left()

        # DARK-FDR-001 step 4 & 5
        computed_gains1 = np.empty((len(intersection),self.indexes))
        computed_gains2 = np.empty((len(intersection),self.indexes))


        for i in range(len(intersection)):
            (i_left,j_left) = intersection[i]
            idx = self.index_collection_left(i_left, j_left)
            mr1 = self.collection_left[idx].mean_radiosity
            (i_right, j_right) = self.coord_collection_from_left_to_right(i_left,j_left)
            idx = self.index_collection_right(i_right, j_right)
            mr2 = self.collection_right[idx].mean_radiosity
            computed_gains1[i] = np.sqrt(mr2/mr1)
            computed_gains2[i] = np.sqrt(mr1/mr2)

        # DARK-FDR-001 step 6
        computed_gains1 = np.moveaxis(computed_gains1,1,0)
        computed_gains2 = np.moveaxis(computed_gains2,1,0)
        for i in range(self.indexes):
            computed_gains1[i] = np.convolve(computed_gains1[i],
                                             config['kernel_gain'],
                                             'same')
            computed_gains2[i] = np.convolve(computed_gains2[i],
                                             config['kernel_gain'],
                                             'same')
        computed_gains1 = np.moveaxis(computed_gains1,1,0)
        computed_gains2 = np.moveaxis(computed_gains2,1,0)

        # DARK-FDR-001 step 7 & 8
        for i in range(len(intersection)):
            (i_left,j_left) = intersection[i]
            idx_l = self.index_collection_left(i_left, j_left)
            (i_right, j_right) = self.coord_collection_from_left_to_right(i_left,j_left)
            idx_r = self.index_collection_right(i_right, j_right)
            e1 = dask.delayed(self.collection_left[idx_l].apply_gain)(computed_gains1[i])
            e2 = dask.delayed(self.collection_right[idx_r].apply_gain)(computed_gains2[i])
            e1 = dask.delayed(e1.filter2D)(np.array(config['kernel_blur']))
            e2 = dask.delayed(e2.filter2D)(np.array(config['kernel_blur']))
            self.collection_left[idx_l] = e1.compute()
            self.collection_right[idx_r] = e2.compute()

        client.close()

    def run_spark(self):
        config = self.load_config(self.pathconfig)
        conf = SparkConf()
        conf.set('spark.driver.memory', '4G')
        sc = SparkContext(conf=conf)
        sc.setLogLevel("WARN")
        # DARK-FDR-001 step 1
        self.extract_collections()

        # DARK-FDR-001 step 2
        rdd_left = sc.parallelize(self.collection_left)
        for n in rdd_left.toLocalIterator():
            idx = self.index_collection_left(n.index[0],n.index[1])
            self.collection_left[idx] = n.add_noise(
                                        config['imgleft']['gain'],
                                        config['imgleft']['mean'],
                                        config['imgleft']['stddev'])

        rdd_right = sc.parallelize(self.collection_right)
        for n in rdd_right.toLocalIterator():
            (i,j) = self.coord_collection_from_left_to_right(n.index[0],n.index[1])
            idx = self.index_collection_right(i,j)
            self.collection_right[idx] = n.add_noise(
                                        config['imgright']['gain'],
                                        config['imgright']['mean'],
                                        config['imgright']['stddev'])

        # DARK-FDR-001 step 3
        intersection = self.list_intersection_coord_left()

        # DARK-FDR-001 step 4 & 5
        computed_gains1 = np.empty((len(intersection),self.indexes))
        computed_gains2 = np.empty((len(intersection),self.indexes))


        for i in range(len(intersection)):
            (i_left,j_left) = intersection[i]
            idx = self.index_collection_left(i_left, j_left)
            mr1 = self.collection_left[idx].mean_radiosity
            (i_right, j_right) = self.coord_collection_from_left_to_right(i_left,j_left)
            idx = self.index_collection_right(i_right, j_right)
            mr2 = self.collection_right[idx].mean_radiosity
            computed_gains1[i] = np.sqrt(mr2/mr1)
            computed_gains2[i] = np.sqrt(mr1/mr2)

        # DARK-FDR-001 step 6
        computed_gains1 = np.moveaxis(computed_gains1,1,0)
        computed_gains2 = np.moveaxis(computed_gains2,1,0)
        for i in range(self.indexes):
            computed_gains1[i] = np.convolve(computed_gains1[i],
                                             config['kernel_gain'],
                                             'same')
            computed_gains2[i] = np.convolve(computed_gains2[i],
                                             config['kernel_gain'],
                                             'same')
        computed_gains1 = np.moveaxis(computed_gains1,1,0)
        computed_gains2 = np.moveaxis(computed_gains2,1,0)


        # DARK-FDR-001 step 7 & 8
        for i in range(len(intersection)):
            (i_left,j_left) = intersection[i]
            idx_l = self.index_collection_left(i_left, j_left)
            (i_right, j_right) = self.coord_collection_from_left_to_right(i_left,j_left)
            idx_r = self.index_collection_right(i_right, j_right)
            e1 = self.collection_left[idx_l].apply_gain(computed_gains1[i])
            e2 = self.collection_right[idx_r].apply_gain(computed_gains2[i])
            e1 = e1.filter2D(np.array(config['kernel_blur']))
            e2 = e2.filter2D(np.array(config['kernel_blur']))
            self.collection_left[idx_l] = e1
            self.collection_right[idx_r] = e2


        sc.stop()

    def run(self):
        config = self.load_config(self.pathconfig)

        # DARK-FDR-001 step 1
        self.extract_collections()

        # DARK-FDR-001 step 2
        for n in self.collection_left:
            n.add_noise(config['imgleft']['gain'],
                        config['imgleft']['mean'],
                        config['imgleft']['stddev'])

        for n in self.collection_right:
            n.add_noise(config['imgright']['gain'],
                        config['imgright']['mean'],
                        config['imgright']['stddev'])

        # DARK-FDR-001 step 3
        intersection = self.list_intersection_coord_left()

        # DARK-FDR-001 step 4 & 5
        computed_gains1 = np.empty((len(intersection),self.indexes))
        computed_gains2 = np.empty((len(intersection),self.indexes))


        for i in range(len(intersection)):
            (i_left,j_left) = intersection[i]
            idx = self.index_collection_left(i_left, j_left)
            mr1 = self.collection_left[idx].mean_radiosity
            (i_right, j_right) = self.coord_collection_from_left_to_right(i_left,j_left)
            idx = self.index_collection_right(i_right, j_right)
            mr2 = self.collection_right[idx].mean_radiosity
            computed_gains1[i] = np.sqrt(mr2/mr1)
            computed_gains2[i] = np.sqrt(mr1/mr2)

        # DARK-FDR-001 step 6
        computed_gains1 = np.moveaxis(computed_gains1,1,0)
        computed_gains2 = np.moveaxis(computed_gains2,1,0)
        for i in range(self.indexes):
            computed_gains1[i] = np.convolve(computed_gains1[i],
                                             config['kernel_gain'],
                                             'same')
            computed_gains2[i] = np.convolve(computed_gains2[i],
                                             config['kernel_gain'],
                                             'same')
        computed_gains1 = np.moveaxis(computed_gains1,1,0)
        computed_gains2 = np.moveaxis(computed_gains2,1,0)


        # DARK-FDR-001 step 7 & 8
        for i in range(len(intersection)):
            (i_left,j_left) = intersection[i]
            idx_l = self.index_collection_left(i_left, j_left)
            (i_right, j_right) = self.coord_collection_from_left_to_right(i_left,j_left)
            idx_r = self.index_collection_right(i_right, j_right)
            self.collection_left[idx_l]\
                .apply_gain(computed_gains1[i])\
                .filter2D(np.array(config['kernel_blur']))

            self.collection_right[idx_r]\
                .apply_gain(computed_gains2[i])\
                .filter2D(np.array(config['kernel_blur']))





if __name__ == '__main__':
    dark = Dark('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',(200,200),'config.yaml')

    # dark.run_dask()
    # dark.run_spark()
    dark.run()
    dark.write_image_left()
    dark.write_image_right()
    dark.write_image_glob()
