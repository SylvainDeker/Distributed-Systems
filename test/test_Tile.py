import os, sys
from collections import namedtuple
import pytest
from shapely.geometry import Polygon, box

from distributed_systems.tile import Tile


Bounds = namedtuple("Bounds", ('x0', 'y0', 'x1', 'y1'))
@pytest.mark.parametrize(
    "bounds",
    (
            Bounds(0, 0, 5400, 10800),
            Bounds(500, 500, 5400, 10800),
            Bounds(0, 0, 0, 0),
    ),
    ids=(
        "load_all",
        "load_lim_max",
        "load_lim_value"
    )
)
def test_data_loading(bounds):
    extent = box(*bounds) # depliage des tuples avec *
    tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif', extent)
    assert tile.bounding_polygon.bounds == bounds
    assert tile.bounding_polygon.bounds == (
        bounds.x0,
        bounds.y0,
        tile.img.shape[1] + bounds.x0,
        tile.img.shape[2] + bounds.y0
    )

@pytest.mark.parametrize(
    "bounds",
    (
            Bounds(5200, 10600, 5800, 11000),
            Bounds(-50, -50, 50, 50),
    ),
    ids=(
        "load_positive_edge_corner",
        "load_negative_edge_corner",
    )
)
def test_load_edge_corner(bounds):
    extent = box(*bounds) # depliage des tuples avec *
    tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif', extent)
    assert tile.bounding_polygon.bounds < bounds
    assert tile.bounding_polygon.bounds == (
        bounds.x0,
        bounds.y0,
        tile.img.shape[1] + bounds.x0,
        tile.img.shape[2] + bounds.y0
    )
