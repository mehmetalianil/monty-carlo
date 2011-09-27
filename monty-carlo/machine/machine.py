'''
Created on Aug 12, 2011

@author: mali
'''

from objectdefs import *
import numpy as num
import pylab
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt     # Plotting
import profile                      # For performance analysis


def machine(system):
    if type(system) != system:
        print "The Monte Carlo engine must have the input system of type system."
        print "Please prepare your state as an system type object."
    else:
        print "Initializing the algorithm..."
        
        
        # Checks are to be made with the other input parameters.
        magnetization_beta = []
        
        for dependency in system.dependencies:
            for dep_name in dependency:
                magnetization_list = num.array([])
                energy_list = num.array([])
                standard_dev = 0
                err=0
                ctr=0
                print "Simulating the system with beta = "+str(beta)
                while  (err > 20 or err == 0) or ctr<20:
                    (state,params) = monte_carlo_iter(neigh,state,beta,plot=False)
                    magnetization_list = num.append(magnetization_list,params[0])
                    energy_list = num.append(energy_list,params[1])
                    # We take the standard deviation of the last four  divided by the 
                    standard_dev = num.std(energy_list[-4:])
                    err = standard_dev/num.mean(energy_list[-4:])
                    print "    ["+str(ctr)+"]Standard Deviation: " + str(standard_dev)  
                    ctr = ctr + 1      
                magnetization_beta.append(magnetization_list[-1])