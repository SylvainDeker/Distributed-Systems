#! /bin/python3
import sys
from pyspark import SparkContext
import numpy as np


collection = [1,2,3,4,5,6,7,8,9]
sc = SparkContext()
rdd1 = sc.parallelize(collection)

rdd2 = rdd1.map(lambda n: n+1)
collection_res = rdd2.collect()

print(collection_res)
