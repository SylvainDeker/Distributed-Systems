#! /bin/python3

from pycallgrind import callgrind


with callgrind(tag="Graph"):
    print("A")
    print("B")
    print("C")

with callgrind(tag="Compute"):
    print("A")
    print("B")
    print("C")
