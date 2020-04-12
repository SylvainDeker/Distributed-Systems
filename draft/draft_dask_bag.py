import sys
from dask.distributed import Client
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window
from Truc2 import Truc2



class Truc:

    def __init__(self, n):
        self.n = n

    def operation(self,n):
        self.n = self.n * n
        return self

    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur"""
        return "{}".format(self.n)


if len(sys.argv) != 2:
    print("usage: python3 ", argv[0], " tcp:://0.0.0.0:8786")
    sys.exit(-1)



client = Client(sys.argv[1])

# rdd = db.from_sequence([Truc(1), Truc(2), Truc(3), Truc(4), Truc(5)]).map(lambda n: n.n*2)

# rdd = db.from_sequence([Truc(1), Truc(2), Truc(3), Truc(4), Truc(5)]).map(lambda n: Truc(n.n*n.n))

rdd = db.from_sequence([Truc(1), Truc(2), Truc(3), Truc(4), Truc(5)]).map(lambda n: n.operation(n.n) )

# rdd = db.from_sequence([Truc2(1), Truc2(2), Truc2(3), Truc2(4), Truc2(5)]).map(lambda n: n.operation(n.n) )

# rdd = db.from_sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).map(lambda n: n*n )

collection2 = rdd.compute()
print(collection2)
