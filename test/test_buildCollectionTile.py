import os
import sys
import pytest

from collections import namedtuple

from distributed_systems.buildCollectionTile import build_collection_tile

IMG_PATH = 'data/NE1_50M_SR_W/NE1_50M_SR_W.tif'
TestData = namedtuple(
    "TestData",
    ('img_path', 'unit_height', 'unit_width', 'nb_expected_items')
)

@pytest.mark.parametrize(
    "data",
    (
            TestData(img_path=IMG_PATH, unit_height=500, unit_width=500, nb_expected_items=242),
            TestData(img_path=IMG_PATH, unit_height=1000, unit_width=1000, nb_expected_items=66),
    ),
    ids=(
        "all",
        "subset",
    )
)
def test_collection(data):
    (collection, info) = build_collection_tile(
        data.img_path,
        data.unit_height,
        data.unit_width)
    assert len(collection) == data.nb_expected_items
