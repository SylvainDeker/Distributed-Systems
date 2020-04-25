#! /bin/python3
class MyObject1:
    def __init__(self):
        self.a = 1

class MyObject2:
    def __init__(self):
        self.a = 2

class MyObject3:
    def __init__(self):
        self.a = 3

class MyObject3:
    def __init__(self):
        self.a = 3

def main():
    ac =0
    for i in range(100):
        ac += MyObject3().a
    return ac

main()
