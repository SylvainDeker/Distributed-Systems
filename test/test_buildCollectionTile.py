import os
import sys
import pytest

from collections import namedtuple

from distributed_systems.buildCollectionTile import build_collection_tile

IMG_PATH = 'data/NE1_50M_SR_W/NE1_50M_SR_W.tif'
IMG_PATH_w9_h13 = 'data/NE1_50M_SR_W_w9_h13/NE1_50M_SR_W.tif'
IMG_PATH_w12_h10 = 'data/NE1_50M_SR_W_w12_h10/NE1_50M_SR_W.tif'
IMG_PATH_w13_h7 = 'data/NE1_50M_SR_W_w13_h7/NE1_50M_SR_W.tif'

TestData = namedtuple(
    "TestData",
    ('img_path', 'unit_height', 'unit_width', 'nb_expected_items')
)

@pytest.mark.parametrize(
    "data",
    (
            TestData(img_path=IMG_PATH,
                     unit_height=500,
                     unit_width=500,
                     nb_expected_items=242),

            TestData(img_path=IMG_PATH,
                     unit_height=1000,
                     unit_width=1000,
                     nb_expected_items=66),

            TestData(img_path=IMG_PATH_w9_h13,
                     unit_height=3,
                     unit_width=3,
                     nb_expected_items=15),

            TestData(img_path=IMG_PATH_w9_h13,
                     unit_height=6,
                     unit_width=4,
                     nb_expected_items=9),

            TestData(img_path=IMG_PATH_w9_h13,
                     unit_height=13,
                     unit_width=9,
                     nb_expected_items=1),

            TestData(img_path=IMG_PATH_w12_h10,
                     unit_height=3,
                     unit_width=3,
                     nb_expected_items=16),

            TestData(img_path=IMG_PATH_w12_h10,
                     unit_height=6,
                     unit_width=4,
                     nb_expected_items=6),

            TestData(img_path=IMG_PATH_w12_h10,
                     unit_height=10,
                     unit_width=12,
                     nb_expected_items=1),

            TestData(img_path=IMG_PATH_w13_h7,
                     unit_height=3,
                     unit_width=3,
                     nb_expected_items=15),

            TestData(img_path=IMG_PATH_w13_h7,
                     unit_height=6,
                     unit_width=4,
                     nb_expected_items=8),

            TestData(img_path=IMG_PATH_w13_h7,
                     unit_height=7,
                     unit_width=13,
                     nb_expected_items=1)
    ),
    ids=(
        "original",
        "original",
        "w9_h13_3_3",
        "w9_h13_6_4",
        "w9_h13_u",
        "w12_h10_3_3",
        "w12_h10_6_4",
        "w12_h10_u",
        "w13_h7_3_3",
        "w13_h7_6_4",
        "w13_h7_u",
    )

)
def test_collection(data):
    (collection, info) = build_collection_tile(
        data.img_path,
        data.unit_height,
        data.unit_width)
    assert len(collection) == data.nb_expected_items
