import sys
from dask.distributed import Client
import dask.bag as db
import numpy as np
import rasterio
from rasterio.windows import Window



if len(sys.argv) != 2:
    print("usage: python3 ", argv[0], " tcp:://0.0.0.0:8786")
    sys.exit(-1)



client = Client(sys.argv[1])
rdd = db.from_sequence([0,1,2,3,4,5,6,7,8,9]).map(lambda n: n*2)
collection2 = rdd.compute()
print(collection2)
