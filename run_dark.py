#!/usr/bin/env python3


import argparse
from distributed_systems.dark import Dark

# python3 run_dark.py --dask --image-left data/NE1_50M_SR_W/NE1_50M_SR_W.tif config.yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("IMAGE",help="Image file with which the process is carried out")
    parser.add_argument("CONFIG",help="config.yaml")
    parser.add_argument("--dask",help="Test dask", action='store_true')
    parser.add_argument("--spark",help="Test spark",action='store_true')
    parser.add_argument("--no-distrib",help="Dark doesnt distribute computes",action='store_true')
    parser.add_argument("--image-left",help="Write the image (left part)", action='store_true')
    parser.add_argument("--image-right",help="Write the image (right part)", action='store_true')
    parser.add_argument("--image-global",help="Write the image (All)", action='store_true')
    args = parser.parse_args()


    dark = Dark(args.IMAGE,(500,500), args.CONFIG)

    if args.dask:
        dark.run_dask()
        if args.image_left:
            dark.write_image_left()
        if args.image_right:
            dark.write_image_right()
        if args.image_global:
            dark.write_image_glob()
    if args.spark:
        dark.run_spark()
        if args.image_left:
            dark.write_image_left()
        if args.image_right:
            dark.write_image_right()
        if args.image_global:
            dark.write_image_glob()
    if args.no_distrib:
        dark.run()
        if args.image_left:
            dark.write_image_left()
        if args.image_right:
            dark.write_image_right()
        if args.image_global:
            dark.write_image_glob()
