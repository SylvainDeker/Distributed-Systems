import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tile.buildCollectionTile import build_collection_tile


def test_collection():
    (collection, info) = build_collection_tile(
                                    'data/NE1_50M_SR_W/NE1_50M_SR_W.tif')
    assert len(collection) == 242

def test_collection1():
    (collection, info) = build_collection_tile(
                                    'data/NE1_50M_SR_W/NE1_50M_SR_W.tif',
                                    1000, 1000)
    assert len(collection) == 66
