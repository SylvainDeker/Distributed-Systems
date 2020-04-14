#! /bin/python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyspark import SparkContext
from Truc import Truc

print(Truc(123456789))

# class Truc:
#
#     def __init__(self, n):
#         self.n = n
#
#     def operation(self,n):
#         self.n = self.n * n
#         return self
#
#     def __repr__(self):
#         """Quand on entre notre objet dans l'interpréteur"""
#         return "{}".format(self.n)
#     def __copy__(self):
#         return Truc(self.n+1)
#
#     def __deepcopy__(self):
#         return Truc(self.n.copy()+1)
#
#     def __len__(self):
#         return 1


data = [Truc(1), Truc(2), Truc(3), Truc(4), Truc(5)]

sc = SparkContext()
rdd1 = sc.parallelize(data).map(lambda n: Truc(n.n*10))
collection_res = rdd1.collect()

print(collection_res)
