import time
import random

def inc(x):
    time.sleep(random.random())
    return x + 1

def dec(x):
    time.sleep(random.random())
    return x - 1

def add(x, y):
    time.sleep(random.random())
    return x + y

if __name__ == '__main__':
    t = time.time()
    x = inc(1)
    y = dec(2)
    z = add(x, y)
    print(z, time.time() - t)

    ##########
    import dask
    inc = dask.delayed(inc)
    dec = dask.delayed(dec)
    add = dask.delayed(add)

    t = time.time()
    x = inc(1)
    y = dec(2)
    z = add(x, y)
    z = z.compute()
    print(z, time.time() - t)
