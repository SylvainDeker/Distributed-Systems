import dask.bag as db
import time
import numpy as np

scale = 28
shape_A = (3*scale, 3*scale)
tile_size_A = (4*scale,4*scale)

shape_B = (4*scale, 4*scale)
tile_size_B = (3*scale,3*scale)


class Tile:
    def __init__(self,x,y,tile_size):
        self.x = x
        self.y = y
        self.data = np.zeros(tile_size)

    def disp_data(self):
        print(self.data)

def bbox_A(x,y):
    left_up_corner = (x*tile_size_A[0], y*tile_size_A[1])
    right_bottom_corner = (left_up_corner[0] + tile_size_A[0], left_up_corner[1] + tile_size_A[1])
    return (left_up_corner,right_bottom_corner)

def bbox_B(x,y):
    left_up_corner = (x*tile_size_B[0], y*tile_size_B[1])
    right_bottom_corner = (left_up_corner[0] + tile_size_B[0], left_up_corner[1] + tile_size_B[1])
    return (left_up_corner,right_bottom_corner)

def index_tile_A_form_coord(i,j):
    return (i//tile_size_A[0], j//tile_size_A[1])

def index_tile_B_form_coord(i,j):
    return (i//tile_size_B[0], j//tile_size_B[1])

def global_coord_to_local_A_coord(x,y):
    return (x % tile_size_A[0], y % tile_size_A[1])

def global_coord_to_local_B_coord(x,y):
    return (x % tile_size_B[0], y % tile_size_B[1])

def is_in_bbox(x,y,bbox):
    (x0,y0), (x1,y1) = bbox
    return x>=x0 and x<x1 and y>=y0 and y<y1

def overlap_zone(bbox1, bbox2):
    # print(bbox1)
    # print(bbox2)
    (lux1,luy1), (brx1,bry1) = bbox1
    (lux2,luy2), (brx2,bry2) = bbox2
    lst_i = set()
    lst_j = set()

    for i in range(lux1,brx1):
        for j in range(luy1,bry1):
            if is_in_bbox(i,j,bbox2):
                # print(i,j)
                lst_i.add(i)
                lst_j.add(j)

    return ((min(lst_i),min(lst_j)),(max(lst_i)+1,max(lst_j)+1))

def build_new_tiles(tile):
    # time.sleep(5)
    lst = set()
    # print("For: ",tile.x,tile.y)
    left_up_corner, right_bottom_corner = bbox_A(tile.x,tile.y)
    for i in range(left_up_corner[0],right_bottom_corner[0]):
        for j in range(left_up_corner[1],right_bottom_corner[1]):
            lst.add(index_tile_B_form_coord(i,j))
    res = []
    for i,j in lst:
        t = Tile(i,j,tile_size_B)
        (lux,luy), (brx,bry) = overlap_zone(bbox_A(tile.x,tile.y), bbox_B(i,j))
        (local_B_lux,local_B_luy), (local_B_brx,local_B_bry) = global_coord_to_local_B_coord(lux,luy), global_coord_to_local_B_coord(brx-1,bry-1)
        (local_B_lux,local_B_luy), (local_B_brx,local_B_bry) = (local_B_lux,local_B_luy), (local_B_brx+1, local_B_bry+1)
        (local_A_lux,local_A_luy), (local_A_brx,local_A_bry) = global_coord_to_local_A_coord(lux,luy), global_coord_to_local_A_coord(brx-1,bry-1)
        (local_A_lux,local_A_luy), (local_A_brx,local_A_bry) = (local_A_lux,local_A_luy), (local_A_brx+1, local_A_bry+1)
        t.data[local_B_lux:local_B_brx,local_B_luy:local_B_bry] = tile.data[local_A_lux:local_A_brx,local_A_luy:local_A_bry]
        res.append(t)

    return res

def aggregate_tile(tile_a,tile_b):
    # time.sleep(5)
    t = Tile(tile_a.x,tile_a.y,tile_size_B)
    t.data = tile_a.data + tile_b.data
    return t

def aggregate_tile2(tile_a,tile_b):
    # time.sleep(10)
    # print("##################")
    t = Tile(tile_a.x,tile_a.y,tile_size_B)
    t.data = tile_a.data + tile_b.data
    return t
