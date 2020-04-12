from dask.distributed import Client
import dask.bag as db


class Truc:

    def __init__(self, n):
        self.n = n

    def operation(self,n):
        self.n = self.n * n
        return self

    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur"""
        return "{}".format(self.n)

client = Client(sys.argv[1])
rdd = db.from_sequence([Truc(1), Truc(2), Truc(3), Truc(4), Truc(5)]).map(lambda n: n.operation(n.n) )
res = rdd.compute()

print(res) # ERROR !
