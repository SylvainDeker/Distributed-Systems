import os
import sys
import pytest
import numpy as np
import rasterio

from distributed_systems.try_dask import try_dask_filter2D
from distributed_systems.try_dask_delayed import try_dask_delayed_filter2D
from distributed_systems.try_spark import try_spark_filter2D


kernel = np.array([[-1, -2, -4, -2, -1],
                   [-2, -4, -8, -4, -2],
                   [-4, -8, 84, -8, -4],
                   [-2, -4, -8, -4, -2],
                   [-1, -2, -4, -2, -1]], np.float32)

pathimage = 'data/NE1_50M_SR_W/NE1_50M_SR_W.tif'


FIXTURE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.datafiles(FIXTURE_DIR)
def test_dask(datafiles):
    output_pathimage = str(datafiles) + "/res_dask.tiff"
    try_dask_filter2D(str(datafiles)+"/"+pathimage, kernel, output_pathimage)
    with rasterio.open(output_pathimage) as src:
        assert src.read(1)[0, 0] == 255
        assert src.read(1)[900, 10] == 255
        assert src.read(1)[3215, 7895] == 0
        assert src.read(1)[258, 6547] == 0
        assert src.read(1)[1236, 147] == 0
        assert src.read(1)[123, 7896] == 16
        assert src.read(1)[5355, 10755] == 68
        assert src.read(1)[5366, 10750] == 0
        assert src.read(2)[1236, 147] == 0
        assert src.read(2)[123, 7896] == 23
        assert src.read(2)[5355, 10755] == 0
        assert src.read(2)[5366, 10750] == 0
        assert src.read(3)[1236, 147] == 0
        assert src.read(3)[123, 7896] == 178
        assert src.read(3)[5355, 10755] == 0
        assert src.read(3)[5366, 10750] == 0


@pytest.mark.datafiles(FIXTURE_DIR)
def test_dask_delayed(datafiles):
    output_pathimage = str(datafiles) + "/res_dask.tiff"
    try_dask_delayed_filter2D(str(datafiles)+"/"+pathimage, kernel,
                              output_pathimage)
    with rasterio.open(output_pathimage) as src:
        assert src.read(1)[0, 0] == 255
        assert src.read(1)[900, 10] == 255
        assert src.read(1)[3215, 7895] == 0
        assert src.read(1)[258, 6547] == 0
        assert src.read(1)[1236, 147] == 0
        assert src.read(1)[123, 7896] == 16
        assert src.read(1)[5355, 10755] == 68
        assert src.read(1)[5366, 10750] == 0
        assert src.read(2)[1236, 147] == 0
        assert src.read(2)[123, 7896] == 23
        assert src.read(2)[5355, 10755] == 0
        assert src.read(2)[5366, 10750] == 0
        assert src.read(3)[1236, 147] == 0
        assert src.read(3)[123, 7896] == 178
        assert src.read(3)[5355, 10755] == 0
        assert src.read(3)[5366, 10750] == 0
