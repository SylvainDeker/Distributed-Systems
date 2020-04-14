import sys
from dask.distributed import Client
import dask.bag as db
from Truc import Truc

print(Truc(12))

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

if __name__ == '__main__':
    data = [Truc(1), Truc(2), Truc(3), Truc(4), Truc(5)]
    client = Client(sys.argv[1])
    client.upload_file(sys.argv[2]) #path/to/Truc.py
    rdd = db.from_sequence(data).map(lambda n: Truc(100*n.n))
    res = rdd.compute()

    print(res) # ERROR !
