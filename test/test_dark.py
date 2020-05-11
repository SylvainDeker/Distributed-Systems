import os
import sys
import pytest

from collections import namedtuple

from distributed_systems.dark import Dark

IMG_PATH = 'data/NE1_50M_SR_W/NE1_50M_SR_W.tif'
IMG_PATH_w9_h13 = 'data/NE1_50M_SR_W_w9_h13/NE1_50M_SR_W.tif'
IMG_PATH_w12_h10 = 'data/NE1_50M_SR_W_w12_h10/NE1_50M_SR_W.tif'
IMG_PATH_w13_h7 = 'data/NE1_50M_SR_W_w13_h7/NE1_50M_SR_W.tif'


Data = namedtuple(
    "Data",
    (    'shape_image',
         'shape_tile',
         'expected_shape_all_tiles',
         'expected_vertical_frontiers',
         'expected_shape_collection_left',
         'expected_shape_collection_right',
         'expected_shape_image_left',
         'expected_shape_image_right',
         'expected_list_intersection_coord_glob'
     )
)

@pytest.mark.parametrize(
    "data",
    (
        Data(shape_image = (8,10),
             shape_tile = (7,3),
             expected_shape_all_tiles = (2,4),
             expected_vertical_frontiers = (1,2),
             expected_shape_collection_left = (2,2),
             expected_shape_collection_right = (2,3),
             expected_shape_image_left = (8,6),
             expected_shape_image_right = (8,7),
             expected_list_intersection_coord_glob = [(0,1),(1,1)]
             ),

        Data(shape_image = (8,10),
             shape_tile = (2,4),
             expected_shape_all_tiles = (4,3),
             expected_vertical_frontiers = (1,2),
             expected_shape_collection_left = (4,2),
             expected_shape_collection_right = (4,2),
             expected_shape_image_left = (8,8),
             expected_shape_image_right = (8,6),
             expected_list_intersection_coord_glob = [(0,1),(1,1),(2,1),(3,1)]
             ),

        Data(shape_image = (11,13),
             shape_tile = (7,3),
             expected_shape_all_tiles = (2,5),
             expected_vertical_frontiers = (1,3),
             expected_shape_collection_left = (2,3),
             expected_shape_collection_right = (2,4),
             expected_shape_image_left = (11,9),
             expected_shape_image_right = (11,10),
             expected_list_intersection_coord_glob = [(0,1),(1,1),
                                                      (0,2),(1,2)]
             ),

        Data(shape_image = (11,13),
             shape_tile = (2,4),
             expected_shape_all_tiles = (6,4),
             expected_vertical_frontiers = (1,2),
             expected_shape_collection_left = (6,2),
             expected_shape_collection_right = (6,3),
             expected_shape_image_left = (11,8),
             expected_shape_image_right = (11,9),
             expected_list_intersection_coord_glob = [(0,1),
                                                      (1,1),
                                                      (2,1),
                                                      (3,1),
                                                      (4,1),
                                                      (5,1)]
             )

    ),
    ids=(
        "ih8_iw10_th7_tw3",
        "ih8_iw10_th2_tw4",
        "ih11_iw13_th7_tw3",
        "ih11_iw13_th2_tw4",
    )
)
def test_indices(data):
    dark = Dark()
    dark.shape_image = data.shape_image
    dark.shape_tile = data.shape_tile

    assert data.expected_shape_all_tiles == dark.shape_all_tiles
    assert data.expected_vertical_frontiers == dark.vertical_frontiers
    assert data.expected_shape_collection_left == dark.shape_collection_left
    assert data.expected_shape_collection_right == dark.shape_collection_right
    assert data.expected_shape_image_left == dark.shape_image_left
    assert data.expected_shape_image_right == dark.shape_image_right
    assert set(data.expected_list_intersection_coord_glob) == set(dark.list_intersection_coord_glob())
