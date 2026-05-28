"""import numpy
a = [1, 2, 3, 4, 5 , 6]
arr = numpy.array(a)
print("list in python: ", a)
print("array in numpy:", arr)"""


'''import numpy as np

sample_array=np.array([[1,2,3], [4,5,6], [7,8,9]])

print(sample_array)
print(sample_array.shape)'''


import numpy as np

var = "hello class"

arr = np.arange(var, dtype= 'U1')
arr = np.arange(len(var), dtype= 'U1')

print("frontier() array :", arr)