import os
import sys
import pytest

from collections import namedtuple

from distributed_systems.dark import extract_collections

IMG_PATH = 'data/NE1_50M_SR_W/NE1_50M_SR_W.tif'
IMG_PATH_w9_h13 = 'data/NE1_50M_SR_W_w9_h13/NE1_50M_SR_W.tif'
IMG_PATH_w12_h10 = 'data/NE1_50M_SR_W_w12_h10/NE1_50M_SR_W.tif'
IMG_PATH_w13_h7 = 'data/NE1_50M_SR_W_w13_h7/NE1_50M_SR_W.tif'


Data = namedtuple(
    "Data",
    ('img_path',
     'unit_height',
     'unit_width',
     'expected_nb_unit_width_collection1',
     'expected_nb_unit_width_collection2',
     'expected_nb_item_collection1',
     'expected_nb_item_collection2',
     'expected_width_img1',
     'expected_width_img2',
     )
)

@pytest.mark.parametrize(
    "data",
    (
        # Data(img_path=IMG_PATH,
        #          unit_height=500,
        #          unit_width=500,
        #          expected_nb_unit_width_collection1 = 2,
        #          expected_nb_unit_width_collection2 = 2,
        #          expected_nb_item_collection1 = 10,
        #          expected_nb_item_collection2 = 10,
        #          expected_width_img1 = 6,
        #          expected_width_img2 = 6
        #          ),
        #
        # Data(img_path=IMG_PATH,
        #          unit_height=1000,
        #          unit_width=1000,
        #          expected_nb_unit_width_collection1 = 2,
        #          expected_nb_unit_width_collection2 = 2,
        #          expected_nb_item_collection1 = 10,
        #          expected_nb_item_collection2 = 10,
        #          expected_width_img1 = 6,
        #          expected_width_img2 = 6
        #          ),

        Data(img_path=IMG_PATH_w9_h13,
                 unit_height=3,
                 unit_width=3,
                 expected_nb_unit_width_collection1 = 2,
                 expected_nb_unit_width_collection2 = 2,
                 expected_nb_item_collection1 = 10,
                 expected_nb_item_collection2 = 10,
                 expected_width_img1 = 6,
                 expected_width_img2 = 6
                 ),

        Data(img_path=IMG_PATH_w9_h13,
                 unit_height=6,
                 unit_width=4,
                 expected_nb_unit_width_collection1 = 2,
                 expected_nb_unit_width_collection2 = 2,
                 expected_nb_item_collection1 = 6,
                 expected_nb_item_collection2 = 6,
                 expected_width_img1 = 8,
                 expected_width_img2 = 5
                 ),

        Data(img_path=IMG_PATH_w9_h13,
                 unit_height=13,
                 unit_width=9,
                 expected_nb_unit_width_collection1 = 0,
                 expected_nb_unit_width_collection2 = 1,
                 expected_nb_item_collection1 = 0,
                 expected_nb_item_collection2 = 1,
                 expected_width_img1 = 0,
                 expected_width_img2 = 9
                 ),

        Data(img_path=IMG_PATH_w12_h10,
                 unit_height=3,
                 unit_width=3,
                 expected_nb_unit_width_collection1 = 2,
                 expected_nb_unit_width_collection2 = 3,
                 expected_nb_item_collection1 = 8,
                 expected_nb_item_collection2 = 12,
                 expected_width_img1 = 6,
                 expected_width_img2 = 9
                 ),

        Data(img_path=IMG_PATH_w12_h10,
                 unit_height=6,
                 unit_width=4,
                 expected_nb_unit_width_collection1 = 2,
                 expected_nb_unit_width_collection2 = 2,
                 expected_nb_item_collection1 = 4,
                 expected_nb_item_collection2 = 4,
                 expected_width_img1 = 8,
                 expected_width_img2 = 8
                 ),

        Data(img_path=IMG_PATH_w12_h10,
                 unit_height=10,
                 unit_width=12,
                 expected_nb_unit_width_collection1 = 0,
                 expected_nb_unit_width_collection2 = 1,
                 expected_nb_item_collection1 = 0,
                 expected_nb_item_collection2 = 1,
                 expected_width_img1 = 0,
                 expected_width_img2 = 12
                 ),

        Data(img_path=IMG_PATH_w13_h7,
                 unit_height=3,
                 unit_width=3,
                 expected_nb_unit_width_collection1 = 3,
                 expected_nb_unit_width_collection2 = 4,
                 expected_nb_item_collection1 = 9,
                 expected_nb_item_collection2 = 12,
                 expected_width_img1 = 9,
                 expected_width_img2 = 10
                 ),

        Data(img_path=IMG_PATH_w13_h7,
                 unit_height=6,
                 unit_width=4,
                 expected_nb_unit_width_collection1 = 2,
                 expected_nb_unit_width_collection2 = 3,
                 expected_nb_item_collection1 = 4,
                 expected_nb_item_collection2 = 6,
                 expected_width_img1 = 8,
                 expected_width_img2 = 9
                 ),

        Data(img_path=IMG_PATH_w13_h7,
                 unit_height=7,
                 unit_width=13,
                 expected_nb_unit_width_collection1 = 0,
                 expected_nb_unit_width_collection2 = 1,
                 expected_nb_item_collection1 = 0,
                 expected_nb_item_collection2 = 1,
                 expected_width_img1 = 0,
                 expected_width_img2 = 13
                 ),

    ),
    ids=(
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
    (collection1,
     collection2,
     info,
     nb_unit_width_collection1,
     nb_unit_width_collection2,
     nb_item_c1,
     nb_item_c1,
     width_img1,
     width_img2, _ ) = extract_collections(data.img_path,
                                        data.unit_height,
                                        data.unit_width)

    assert len(collection1) == data.expected_nb_item_collection1
    assert len(collection2) == data.expected_nb_item_collection2
    assert nb_unit_width_collection1 == data.expected_nb_unit_width_collection1
    assert nb_unit_width_collection2 == data.expected_nb_unit_width_collection2
    assert width_img1 == data.expected_width_img1
    assert width_img2 == data.expected_width_img2
