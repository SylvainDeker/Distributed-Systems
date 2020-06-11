import dask.bag as db
from pyspark import SparkContext




if __name__ == '__main__':
    collection = [n for n in range(100)]

    sc = SparkContext()
    res = sc.parallelize(collection, 3)\
        .sample(withReplacement=False, fraction=0.1, seed=42)\
        .collect()

    print(res)

    res = db.from_sequence(collection, npartitions=3)\
        .random_sample(prob=0.1,random_state=42)\
        .compute()

    print(res)
