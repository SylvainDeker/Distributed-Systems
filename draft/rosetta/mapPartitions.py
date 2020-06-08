import dask.bag as db
from pyspark import SparkContext



def func_count(iterator):#Type: Iterator
    yield sum(1 for _ in iterator)

def func_count_dask(itera):#Type: Iterator or Iterable
    # iterable = itera
    # return sum(1 for _ in iterable)
    # or return len(iterable)

    iterator = itera
    yield sum(1 for _ in iterator)


if __name__ == '__main__':
    collection = [n for n in range(100)]

    sc = SparkContext()
    res = sc.parallelize(collection, 3)\
        .mapPartitions(func_count)\
        .collect()

    print(res)

    # collection = range(100)
    res = db.from_sequence(collection, npartitions=3)\
        .map_partitions(func_count_dask)\
        .map(lambda x: x)\
        .compute()

    print(res)
