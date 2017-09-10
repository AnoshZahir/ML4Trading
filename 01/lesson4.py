"""The power of Numpy"""

import numpy as np
import time

def get_max_index(a):
    """Return the index of the maximum value in given 1D array."""
    return a.argmax()

def manual_mean(arr):
    """Compute mean of all elements in the given 2D array"""
    my_sum = 0
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            my_sum += arr[i,j]
    return my_sum / arr.size

def numpy_mean(arr):
    """Compute mean using Numpy"""
    return arr.mean()

def how_long(func, *args):
    """Execute function with given arguments, and measure execution time."""
    t0 = time.time()
    result = func(*args) #all arguments are passed in as-is
    t1 = time.time()
    return (result, t1 - t0)

def test_run():
    nd1 = np.random.random((1000,10000))
    res_manual, t_manual = how_long(manual_mean, nd1)
    res_numpy, t_numpy = how_long(numpy_mean, nd1)
    '''print('manual:' + res_manual +" " +  t_manual)
    print('numpy:' + res_numpy + " " + t_numpy)'''
    print(res_manual)
    print(t_manual)
    print(res_numpy)
    print(t_numpy)
    
    
    
if __name__ == '__main__':
    test_run()


