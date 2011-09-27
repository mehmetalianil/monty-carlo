#! /usr/bin/env python



import numpy as num
import math
import matplotlib.pyplot as plt     # Plotting
import profile                      # For performance analysis
import pp                           # For parallelization
import time
job_server = pp.Server() 


__author__ = "Mehmet Ali Anil"
 __copyright__ = "(C) 2011 Mehmet Ali Anil(mehmet.ali.anil@ieee.org)"
__credits__ = ["Mehmet Ali Anil"]
__license__ = " "
__version__ = "0.0.1"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "mehmet.ali.anil@ieee.org"
__status__ = "Production"

def energy_ising_3d(state, type="closest", param={'symmetric_cont':-1, 
    'anti_symmetric_cont':1,'spin_cont':1}):
    """ Gives the energy of an 2D Ising state."""
    
    if (type == "closest"):
        energy=0
        
        symmetric_cont= param['symmetric_cont']
        anti_symmetric_cont=  param['anti_symmetric_cont']
        spin_cont=  param['spin_cont']
        
        for (z,slice) in enumerate(state):
            for (y,row) in enumerate(slice): 
                for (x,spin) in enumerate(row):
                    energy = energy + spin_cont
                    if (state[z][y][x] == state[z-1][y][x]):
                        energy = energy + symmetric_cont
                    else: 
                        energy = energy + anti_symmetric_cont
                        
                    if (state[z][y][x] == state[z][y-1][x]):
                        energy = energy + symmetric_cont
                    else:
                        energy = energy + anti_symmetric_cont
                                                
                    if (state[z][y][x] == state[z][y][x-1]):
                        energy = energy + symmetric_cont
                    else:
                        energy = energy + anti_symmetric_cont
                        
        return  energy


def energy_ising_2d(state, type="closest", param={'symmetric_cont':-1, 
    'anti_symmetric_cont':1,'spin_cont':1}):
    """ Gives the energy of an 2D Ising state."""
    
    if (type == "closest"):
        energy=0
        
        symmetric_cont= param['symmetric_cont']
        anti_symmetric_cont=  param['anti_symmetric_cont']
        spin_cont=  param['spin_cont']
        
        for (y,row) in enumerate(state):
            for (x,spin) in enumerate(row):
                energy = energy + spin_cont
                if (state[x][y] == state[x-1][y]):
                    energy = energy + symmetric_cont
                else: 
                    energy = energy + anti_symmetric_cont
                    
                if (state[x][y] == state[x][y-1]):
                    energy = energy + symmetric_cont
                else:
                    energy = energy + anti_symmetric_cont
    return  energy

def neighbour_preallocation_ising(state):
    """
    http://stackoverflow.com/questions/6841206/
    creating-a-new-list-from-elements-of-an-
    other-list-referencing-the-elements-of-t
    
    
    """
    neighbours = num.zeros((len(state),len(state[0]))).tolist()
    
    for (y,row) in enumerate(state):
        for (x,spin) in enumerate(row):
            if (y == len(state)-1 and x != len(state[0])-1):
                neighbours[y][x] = (y-1,x),(y,x-1),(y,x+1),(0,x)
            elif (y != len(state)-1 and x == len(state[0])-1):
                neighbours[y][x] = (y-1,x),(y,x-1),(y,0),(y+1,x)
            elif (y == len(state)-1 and x == len(state[0])-1):
                neighbours[y][x] = (y-1,x),(y,x-1),(y,0),(0,x)
            else:
                neighbours[y][x] = (y-1,x),(y,x-1),(y,x+1),(y+1,x)    
 
    return neighbours


def neighbour_preallocation_ising_3d(state):
    """
    http://stackoverflow.com/questions/6841206/
    creating-a-new-list-from-elements-of-an-
    other-list-referencing-the-elements-of-t
    """
    
    neighbours = num.zeros((len(state),len(state[0]),len(state[0][0]))).tolist()
    
    for (z,slice) in enumerate(state):
        for (y,row) in enumerate(slice):
            for (x,spin) in enumerate(row):
                if (z == len(state)-1 and y == len(state[0])-1 and x != len(state[0][0])-1):
                    # zy
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,x+1),(z,0,x),(z-1,y,x),(0,y,x)
                elif (z == len(state)-1 and y != len(state[0])-1 and x == len(state[0][0])-1):
                    # zx
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,0),(z,y+1,x),(z-1,y,x),(0,y,x)
                elif (z == len(state)-1 and y == len(state[0])-1 and x == len(state[0][0])-1):
                    # zyx
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,0),(z,0,x),(z-1,y,x),(0,y,x)
                elif (z != len(state)-1 and y == len(state[0])-1 and x != len(state[0][0])-1):
                    # y
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,x+1),(z,0,x),(z-1,y,x),(z+1,y,x)
                elif (z != len(state)-1 and y != len(state[0])-1 and x == len(state[0][0])-1):
                    # x
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,0),(z,y+1,x),(z-1,y,x),(z+1,y,x)
                elif (z == len(state)-1 and y != len(state[0])-1 and x != len(state[0][0])-1):
                    # z
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,0),(z,y+1,x),(z-1,y,x),(0,y,x)
                elif (z != len(state)-1 and y == len(state[0])-1 and x == len(state[0][0])-1):
                    # yx
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,0),(z,0,x),(z-1,y,x),(0,y,x)
                else:
                    neighbours[z][y][x] = (z,y-1,x),(z,y,x-1),(z,y,x+1),(z,y+1,x),(z-1,y,x),(z+1,y,x)
     
    return neighbours


def generate_random(n):
    '''
    Generates and returns a spin configuration. 
    '''
    
    num.random.seed()
    random_booleans = ((num.random.randint(0,2,(n,n))*2)-1)
   
    return random_booleans

def generate_random_3d(n):
    '''
    Generates and returns a 3d spin configuration. 
    '''
    
    num.random.seed()
    random_booleans = ((num.random.randint(0,2,(n,n,n))*2)-1)
   
    return random_booleans

def monte_carlo_iter(state_neigh,state,beta,plot=False,return_energy=True,
                     return_magnetization=True):
    for (ctr_y,row) in enumerate(state):
        for (ctr_x,spin) in enumerate(row):
            energy = 0
            for neighbour in state_neigh[ctr_y][ctr_x]:
                energy = energy + state[neighbour[0]][neighbour[1]]
            delta_E = 2*spin*energy
            random_num = num.random.rand()
            if random_num < math.exp(-beta*delta_E):
                state[ctr_y][ctr_x] = -state[ctr_y][ctr_x]
    if return_energy:                            
        energy = energy_ising_2d(state)
    else: 
        energy = None
    if return_magnetization:
        magnetization = state.sum()
    else:
        magnetization = None
    
    if plot :
        plot_state(state)
        time.sleep(0.05)
    return state,(magnetization,energy)


def monte_carlo_iter_3d(state_neigh,state,beta,plot=False,return_energy=True,
                     return_magnetization=True):
    for (ctr_z,slice) in enumerate(state):    
        for (ctr_y,row) in enumerate(slice):
            for (ctr_x,spin) in enumerate(row):
                energy = 0
                for neighbour in state_neigh[ctr_z][ctr_y][ctr_x]:
                    energy = energy + state[neighbour[0]][neighbour[1]][neighbour[2]]
                delta_E = 2*spin*energy
                random_num = num.random.rand()
                if random_num < math.exp(-beta*delta_E):
                    state[ctr_z][ctr_y][ctr_x] = -state[ctr_z][ctr_y][ctr_x]
    if return_energy:                            
        energy = energy_ising_3d(state)
    else: 
        energy = None
    if return_magnetization:
        magnetization = state.sum()
    else:
        magnetization = None
    
    if plot :
        plot_state(state)
        time.sleep(0.05)
        
    return state,(magnetization,energy)


def plot_state(state):
    plt.imshow(state,cmap=plt.cm.binary,interpolation='nearest')
    plt.show()
    plt.draw()
    

def monte_carlo_2d():
    state = generate_random(20)
    neigh = neighbour_preallocation_ising(state)
    magnetization_beta = []
    for beta in num.arange(0.02,1,0.02):
        magnetization_list = num.array([])
        energy_list = num.array([])
        standard_dev = 0
        err=0
        ctr=0
        print "Simulating the system with beta = "+str(beta)
        while  (err > 0.1 or err == 0) or ctr<40:
            (state,params) = monte_carlo_iter(neigh,state,beta,plot=False)
            magnetization_list = num.append(magnetization_list,params[0])
            energy_list = num.append(energy_list,params[1])
            standard_dev = num.std(num.abs(magnetization_list[-4:]))
            err = standard_dev/num.mean(num.abs(magnetization_list[-4:]))
            ctr = ctr + 1      
        print "    ["+str(ctr)+"]Error: " + str(err)
        magnetization_beta.append(num.mean(magnetization_list[-4:]))
    return magnetization_beta
        
        
def monte_carlo_3d():
    state = generate_random_3d(15)
    neigh = neighbour_preallocation_ising_3d(state)
    magnetization_beta = []
    for beta in num.arange(0.01,1,0.01):
        magnetization_list = num.array([])
        energy_list = num.array([])
        standard_dev = 0 
        ctr=0
        print "Simulating the system with beta = "+str(beta)
        while  (standard_dev > 25 or standard_dev == 0) or ctr<20:
            (state,params) = monte_carlo_iter_3d(neigh,state,beta,plot=False)
            magnetization_list = num.append(magnetization_list,params[0])
            energy_list = num.append(energy_list,params[1])
            standard_dev = num.std(energy_list[-4:])
            print "    ["+str(ctr)+"]Standard Deviation: " + str(standard_dev)  
            ctr = ctr + 1      
        magnetization_beta.append(magnetization_list[-1])
    return(state,magnetization_beta)
    