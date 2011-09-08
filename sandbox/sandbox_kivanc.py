#! /usr/bin/env python

__author__ = "Kivanc Esat"
 __copyright__ = "(C) 2011 Mehmet Ali Anil(mehmet.ali.anil@ieee.org)"
__credits__ = ["Kivanc Esat","Mehmet Ali Anil"]
__license__ = " "
__version__ = "0.0.1"
__maintainer__ = "Kivanc Esat"
__email__ = ""
__status__ = "Production"

#import numpy as num
#import pylab
#from mpl_toolkits.mplot3d import Axes3D
#import math
#import matplotlib.pyplot as plt     # Plotting
#import profile                      # For performance analysis


if __name__ == '__main__':
    print 'Hello Word'
    
list_of_spins = [1, -1, 1, -1,1 ]


def magnetization_1d(list_of_spins):
    sum = 0

    N = len(list_of_spins)

    for i in range(N):
        sum = sum + list_of_spins[i]
    print sum

    if sum >0:
        print 'spin up domain'
    elif sum <0:
        print 'spin down domain'
    else:
        print 'no net magnetization'
