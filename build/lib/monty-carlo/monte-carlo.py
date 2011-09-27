#! /usr/bin/env python

'''
Created on 15.05.2011

@author: Mehmet Ali Anil

The Monte-Carlo Simulation Engine
'''

import numpy as num
import pylab
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt     # Plotting
import profile                      # For performance analysis


__author__ = "Mehmet Ali Anil, Ege Ozgun, Kivanc Esat, Deniz Gunceler"
 __copyright__ = "(C) 2011 Mehmet Ali Anil(mehmet.ali.anil@ieee.org)"
__credits__ = ["Mehmet Ali Anil", "Ege Ozgun", "Kivanc Esat", "Deniz Gunceler"]
__license__ = " "
__version__ = "0.0.1"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "mehmet.ali.anil@ieee.org"
__status__ = "Production"



class atomic_lattice(object):
    """
    Atomic Lattice class for Monty Carlo simulations
        This object is meant to be a sole representative of a monatomic 
        lattice class, in which all atoms incorporated will have the same 
        structure.
    """
    def __init__(self,(vector_1,vector_2,vector_3),atoms_unit,strech=1):
        """
        Defines the lattice object
        lattice((vector_1,vector_2,vector_3), atoms, strech = 1)
                
                (vector_1,vector_2,vector_3)
            
            These are the translational symmetry vectors that the unit cell will 
            repeat itself. Their types can be a python list. 
        
            Example:
            
            ([1,0,0],[0,1,0],[0,0,1]) 
            
            will create a lattice with the unit cell is a cube, 
            and it repeats itself for all linear combinations
            of these unit vectors.
            
                atoms
            
            This is a Python list of the coordinates of the atoms with respect to 
            the coordinate system formed with (vector_1,vector_2,vector_3).
            
            An example may be:
            
            [[0,0,0],[0,0.5,0.5],[0.5,0.5,0],[0.5,0,0.5],[1,0.5,0.5],
            [0.5,0.5,1],[0.5,1,0.5],[1,0,0],[0,1,0],[0,0,1],
            [1,1,0],[1,0,1],[0,1,1],[1,1,1]]
            
            which is the list for all atoms in a face centered cubic structure.
        """
        
        self.explanation = None
        
        print "Initializing the unit cell.."
        self.vectors_n_norm = num.array([vector_1,vector_2,vector_3])
        #Normalizes the bases vector.
        self.vectors = [self.n_norm_vec/num.linalg.norm(self.n_norm_vec) 
                        for self.n_norm_vec in self.vectors_n_norm]
       
        self.atoms_unit = num.array(atoms_unit)
        self.atoms_cartesian_unit = num.array([num.dot(atom_position,self.vectors) for 
                           (atom_no,atom_position) in enumerate(self.atoms_unit)])

        self.atoms = num.array([0,0,0])
        
        # list of all vectors that are linear superpositions of basis vectors
        
        symmetries = num.array([[x_ctr,y_ctr,z_ctr]
                                for x_ctr in range(strech+1) 
                                for y_ctr in range(strech+1) 
                                for z_ctr in range(strech+1)])
                        
        print "  Done!"
        print "Streching the crystal.."
    
        for atom in self.atoms_cartesian_unit:
            for symmetry_vec in symmetries:
      
                newcomer  = atom + symmetry_vec
                self.atoms = num.vstack([self.atoms,newcomer])
        print "  Done!"
        
    def show(self,unit=False):
        """
        Visualizes the structure of the crystal with an interactive 3d 
        interface.
        
            unit = False:
            
            If true, will show the unit cell only.
            
        """
        figure = pylab.figure()
        axes = Axes3D(figure)
        if unit:
            axes.scatter(self.atoms_unit[:,0],self.atoms_unit[:,1],
                         self.atoms_unit[:,2])
        else:
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



