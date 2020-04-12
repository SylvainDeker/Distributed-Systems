
class Truc2:
    def __init__(self, n):
        self.n = n

    def operation(self,n):
        self.n = self.n * n
        return self

    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur"""
        return "{}".format(self.n)
