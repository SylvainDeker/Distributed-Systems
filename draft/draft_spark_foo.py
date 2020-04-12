#! /bin/python3
import sys
from pyspark import SparkContext
import numpy as np
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


collection = [Truc(1), Truc(2), Truc(3), Truc(4), Truc(5), Truc(6), Truc(7), Truc(8), Truc(9)]
# collection = [1,2,3,4,5,6,7,8,9]

sc = SparkContext()
rdd1 = sc.parallelize(collection)

# rdd2 = rdd1.map(lambda n: n.operation(n.n))
rdd2 = rdd1.map(lambda n: n)
collection_res = rdd2.collect()

print(collection_res)
