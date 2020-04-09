import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tile.Tile import Tile
from shapely.geometry import Polygon


class TestTile:

    def test_load_all(self):
        x0 = 0
        y0 = 0
        x1 = 5400
        y1 = 10800
        tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                    Polygon([(x0, y0),
                             (x0, y1),
                             (x1, y1),
                             (x1, y0)]))
        assert tile.bounding_polygon.bounds == (x0, y0, x1, y1)
        assert tile.bounding_polygon.bounds == (x0, y0, tile.img.shape[1] +
                                                x0, tile.img.shape[2]+y0)
        assert tile.img.shape == (3,5400,10800)

    def test_load_lim_max(self):
        x0 = 500
        y0 = 500
        x1 = 5400
        y1 = 10800
        tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                    Polygon([(x0, y0),
                             (x0, y1),
                             (x1, y1),
                             (x1, y0)]))
        assert tile.bounding_polygon.bounds == (x0, y0, x1, y1)
        assert tile.bounding_polygon.bounds == (x0, y0, tile.img.shape[1] +
                                                x0, tile.img.shape[2]+y0)
    def test_load_positive_edge_corner(self):
        x0 = 5200
        y0 = 10600
        x1 = 5800
        y1 = 11000
        tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                    Polygon([(x0, y0),
                             (x0, y1),
                             (x1, y1),
                             (x1, y0)]))
        assert tile.bounding_polygon.bounds < (x0, y0, x1, y1)
        assert tile.bounding_polygon.bounds == (x0, y0, tile.img.shape[1] +
                                                x0, tile.img.shape[2]+y0)
    def test_load_negative_edge_corner(self):
        x0 = -50
        y0 = -50
        x1 = 50
        y1 = 50
        tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                    Polygon([(x0, y0),
                             (x0, y1),
                             (x1, y1),
                             (x1, y0)]))
        assert tile.bounding_polygon.bounds < (x0, y0, x1, y1)
        assert tile.bounding_polygon.bounds == (x0, y0, tile.img.shape[1] +
                                                x0, tile.img.shape[2]+y0)
    def test_load_lim_value(self):
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 0
        tile = Tile('data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                    Polygon([(x0, y0),
                             (x0, y1),
                             (x1, y1),
                             (x1, y0)]))
        assert tile.bounding_polygon.bounds == (x0, y0, x1, y1)
        assert tile.bounding_polygon.bounds == (x0, y0, tile.img.shape[1] +
                                                x0, tile.img.shape[2]+y0)
