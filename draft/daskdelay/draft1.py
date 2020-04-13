import dask
import sys
from dask.distributed import Client, progress
import random
import time
# client = Client(threads_per_worker=4, n_workers=1)
client = Client(sys.argv[1])
print(client)

def inc(x):
    time.sleep(random.random())
    return x + 1

def dec(x):
    time.sleep(random.random())
    return x + 2

def add(x, y):
    time.sleep(random.random())
    return x + y

inc = dask.delayed(inc)
dec = dask.delayed(dec)
add = dask.delayed(add)

x = inc(2)
y = dec(3)
z = add(x, y)

g = z.visualize(rankdir='LR')
with open("res.png", "wb") as png:
    png.write(g.data)

############################################

output = []
for x in range(1024):
    a = inc(x)
    b = dec(x)
    c = add(a, b)
    output.append(c)

# sum is the built-in python's function
total = dask.delayed(sum)(output)

res = total.compute()
print(res)
