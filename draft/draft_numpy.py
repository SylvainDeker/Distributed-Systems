import numpy as np

x = np.array([0,1,2,3,4,5,6,7,8,9])

print(x[1:7:2])
print(x[2:])
print(x[:5])


x = np.array([[0,1,2],
              [4,5,6],
              [7,8,9]])

print(x[1:3,1:3])

x = np.array([ [[0],[1],[2],[3]],
               [[4],[5],[6],[7]],
               [[8],[9],[10],[11]] ])
print(x)
print(x[1:2,3:4])


x = np.array([
              [[0,1,2],
               [7,8,9],
               [13,14,15],
               [18,19,20] ] ,
              [[0,1,2],
               [7,8,9],
               [13,14,15],
               [18,19,20] ]
             ])

print(x)
print(x[:,:2,1:3])


a = np.ones((3,4,5,6))
res = np.rollaxis(a,1)
print(res.shape)
res = np.rollaxis(a,2)
print(res.shape)
res = np.rollaxis(a,3)
print(res.shape)

print('|||||||||||||||||||||||||')
x = np.array([[0,1,2,99],
              [4,5,6,99],
              [7,8,9,99],
              [10,11,12,99]])
print(x)
x = np.moveaxis(x,1,0)
print(x)
x = np.moveaxis(x,1,0)
print(x)


# print(res)
