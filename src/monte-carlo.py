#! /usr/bin/env python

'''
Created on 15.05.2011

@author: Mehmet Ali Anil

The Monte-Carlo Simulation Engine
'''

import numpy as num
import profile
import pylab
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt     # Plotting
import profile                      # For performance analysis


__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"



class lattice(object):
    """
    Defines the lattice object
    This definition is strictly 3D.
    I don't know any reason for it to be 4D and more, though it can be made.
    """
    def __init__(self,(vector_1,vector_2,vector_3),atoms_unit,strech=1):
        
        self.vectors_n_norm = num.array([vector_1,vector_2,vector_3])
        
        #Normalizes the bases vector.
        self.vectors = [self.n_norm_vec/num.linalg.norm(self.n_norm_vec) 
                        for self.n_norm_vec in self.vectors_n_norm]
       
        self.atoms_unit = atoms_unit
        self.atoms_cartesian_unit = num.array([num.dot(atom_position,self.vectors) for 
                           (atom_no,atom_position) in enumerate(self.atoms_unit)])

        self.atoms = num.array([])
        
        for base in self.vectors:
            for x_ctr in range(strech+1):
                for y_ctr in range(strech+1): 
                    for z_ctr in range(strech+1):
                        for atom in self.atoms_cartesian_unit:
                            newcomer = atom + num.array([x_ctr,y_ctr,z_ctr])*base
                            num.append(newcomer,self.atoms)

        self.atoms = num.array(self.atoms)
    
    def show(self):
        figure = pylab.figure()
        axes = Axes3D(figure)
        axes.scatter(self.atoms[:,0],self.atoms[:,1],self.atoms[:,2])
        plt.show()
        
    
class ising_2d(object):
    """   
    This is the object for the system definitions of the 2d ising spin model.
    """   
    def __init__(self):
        self.state = None
        self.complementary_obj = {'neigh':None}
        self.parameters = {'anti_symmetric_cont':None,'symmetric_cont':None}
        self.dependencies = {'beta' : num.arange(0.01,1,0.01)}
        self.output_variables = ('magnetization',None)
        self.user_parameters = None
        self.energy = array([])
    
    def generate(self,type='random'):
        """
        Generates and returns a spin configuration. 
        """
        if type == 'random':
            num.random.seed()
            self.state = ((num.random.randint(0,2,(n,n))*2)-1)
        
    def post_generate(self):
        """
        Generates the spin neighborhood matrix for the state
        """
        if self.state == None:
            print "Please generate the spin configurations first by calling"
            print "name_of_system.generate()"
       
        else:
            print "Generating the neighborhood matrix of the state..."
            
            neighbours = num.zeros((len(self.state),len(len.state[0]))).tolist()
        
            for (y,row) in enumerate(self.state):
                for (x,spin) in enumerate(row):
                    if (y == len(self.state)-1 and x != len(self.state[0])-1):
                        neighbours[y][x] = (y-1,x),(y,x-1),(y,x+1),(0,x)
                    elif (y != len(self.state)-1 and x == len(self.state[0])-1):
                        neighbours[y][x] = (y-1,x),(y,x-1),(y,0),(y+1,x)
                    elif (y == len(self.state)-1 and x == len(self.state[0])-1):
                        neighbours[y][x] = (y-1,x),(y,x-1),(y,0),(0,x)
                    else:
                        neighbours[y][x] = (y-1,x),(y,x-1),(y,x+1),(y+1,x)    
         
            self.complementary_obj['neigh'] = neighbours 
            print "    Done."

    def energy(self):
        """ Gives the energy of an 2D Ising state."""

        energy=0
        
        symmetric_cont= self.parameters['symmetric_cont']
        anti_symmetric_cont=  self.parameters['anti_symmetric_cont']
        spin_cont=  self.parameters['spin_cont']
        
        for (y,row) in enumerate(self.state):
            for (x,spin) in enumerate(row):
                energy = energy + spin_cont
                if (self.state[x][y] == self.state[x-1][y]):
                    energy = energy + symmetric_cont
                else: 
                    energy = energy + anti_symmetric_cont
                    
                if (self.state[x][y] == self.state[x][y-1]):
                    energy = energy + symmetric_cont
                else:
                    energy = energy + anti_symmetric_cont
        
        return energy

    def energy_difference(self):
        """Calculates the energy difference of a particular spin, if it had been reversed."""
        energy = 0
        for neighbour in state_neigh[ctr_y][ctr_x]:
            energy = energy + state[neighbour[0]][neighbour[1]]
        delta_E = 2*spin*energy
    
def monte_carlo_2d(system):
    if type(system) != system:
        print "The Monte Carlo engine must have the input system of type system."
        print "Please prepare your state as an system type object."
    else:
        
        print "Initializing the algorithm..."
        
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
        
class system(object):
    """   
    This is the system object for the simulation.
    It incorporates objects that are affiliated with the simulation,
    and 
    """
    def __init__(self):
        self.state_def = None
        self.parameters = None
        self.t = 0
        self.user_parameters = None
        self.energy = array([])

        
    def compute_energy(self):
        """ Computes the energy of the state and appends it into the list"""
        self.energy.append(self.energy_def(self.state_indicator))   

lattice_bases_fcc = (num.array([1,0,0]),num.array([0,1,0]),num.array([0,0,1]))
atoms_fcc = num.array([[0,0,0],[0,0.5,0.5],[0.5,0.5,0],[0.5,0,0.5],[1,0.5,0.5],
                       [0.5,0.5,1],[0.5,1,0.5],[1,0,0],[0,1,0],[0,0,1],
                       [1,1,0],[1,0,1],[0,1,1],[1,1,1]])
fcc = lattice(lattice_bases_fcc, atoms_fcc,strech=2)
