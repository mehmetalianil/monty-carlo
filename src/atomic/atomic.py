#!/usr/bin/env python
from __future__ import division


"""
Provides classes relating to MC statistics with atoms
"""

from objectdefs import *
import matplotlib.pyplot as plt
import copy
import numpy as num
import pylab
from mpl_toolkits.mplot3d import Axes3D

class particle (element):
    """Particle class, a representation of small particles
	"""
    def __init__(self, type='p'):
        self.spin = None
        self.energy = None
        self.type = type
    
    def copy(self):
        new_particle = copy.copy(self)
        return new_particle 
 
class atom(element):
    """Atom class, a representation of an atom.
    """
    def __init__(self, atomic_no = None):
        
        # initialization of an atom class
        self.atomic_number = atomic_no
        self.mass_number = None
        self.charge = None
        self.magnetic_moment = None
        self.stable = True
        self.position = num.array([0,0,0],dtype=float)
        self.momentum = num.array([0,0,0],dtype=float)
        
        # Probability of decay per unit time 
        self.decay_prob = None
        
        # Decay process: [Change in proton number, neutron number, particle object] 
        self.decay_process = [None, None, None]
        
        # A pseudo radius for close packing
        self.radius = None
        
        # COLOR
        
        if self.atomic_number == None:
            self.color = 'r'
        else:
            color_1 = (self.atomic_number % 7) / 6
            color_2 = ((self.atomic_number / 7) % 7) / 6
            color_3 = ((self.atomic_number / 7) / 7) / 6
            self.color = (color_1 ,color_2 ,color_3)
            
    def copy(self,n=1):
        """Copies an existing atom and returns a copy of it
        """
        
        atom_copy_list = [copy.copy(self) for n in range(n)]
                
        return atom_copy_list
    
    def reinit(self):
        """Derived properties of the atom is reinitalized
        """
        if (self.mass_number != None and self.atomic_number != None):
            self.neutron = self.mass_number - self.atomic_number
            self.proton = self.atomic_number
        else:
            print "The mass number or the atomic number is defined as null "
            
        # COLOR
                
        if self.atomic_number == None:
            self.color = 'r'
        else:
            color_1 = (self.atomic_number % 7) / 6
            color_2 = ((self.atomic_number / 7) % 7) / 6
            color_3 = ((self.atomic_number / 7) / 7) / 6
            self.color = (color_1 ,color_2 ,color_3)
        

    def decay(self):
        """The atom undergoes a nuclear decay, as defined in __init__
        if the atom.stable = False
        """
        if self.decay_prob == False:
            print "This atom is stable, it wont undergo any decay."
            print "Please define the atom as unstable first."
        else:
            print "Atom is undergoing decay."
            
            self.atomic_number = self.atomic_number - self.decay_process[0]
            self.mass_number = self.mass_number - (self.decay_process[1] +
                                                    self.decay_process[0])
            self.reinit()
            radiation = self.decay_process[2]
            
            return radiation
        
    def position(self,new_position):
        """
        Checks whether a valid position vector is defined for the atom and then 
        assigns it.
        """
        if type(new_position) == list:
            self.position = num.array(new_position).astype(float)
        else:
            print "There's something wrong with the assigned value for the"
            print "position vector. Please assign it as a list or a numpy array."
            print "e.g.  atom.position([0,0,0])"
            print "e.g.  atom.position(num.array([0,0,0]))"
            

class lattice(state):
    """
    Atomic Lattice class for Monty Carlo simulations
        This object is meant to be a sole representative of a monatomic 
        lattice class, in which all atoms incorporated will have the same 
        structure.
    """
    def __init__(self,(vector_1,vector_2,vector_3),atoms_basis,strech=1):
        """
        Defines the lattice object
        lattice((vector_1,vector_2,vector_3), atoms, strech = 1)
                
                (vector_1,vector_2,vector_3)
            
            These are the translational symmetry vectors that the unit cell will 
            repeat itself. Their types can be a Python list. 
        
            Example:
            
            ([1,0,0],[0,1,0],[0,0,1]) 
            
            will create a lattice with the unit cell is a cube, 
            and it repeats itself for all linear combinations
            of these unit vectors.
            
                atoms
            
            This is a list of atom objects, with defined coordinates.
        """
        
        self.explanation = None
        
        print "Initializing the unit cell.."
        self.unit_vectors_not_norm = num.array([vector_1,vector_2,vector_3])
        
        # Normalizes the bass vectors.
        self.unit_vectors = [self.n_norm_vec/num.linalg.norm(self.n_norm_vec) 
                             for self.n_norm_vec in self.unit_vectors_not_norm]
        
        # atoms_unit is a list of (num.array(x,y,z), atom)
        self.atoms_basis = atoms_basis
        self.atoms_unit = [(num.dot(atom.position,self.unit_vectors),atom) 
                                               for atom in self.atoms_basis]

        self.atoms = []
        
        # list of all vectors that are linear superpositions of basis vectors
        
        symmetries = num.array([[x_ctr,y_ctr,z_ctr]
                                for x_ctr in range(strech) 
                                for y_ctr in range(strech) 
                                for z_ctr in range(strech)])
        print symmetries
                        
        print "  Done!"
        print "Streching the crystal.."
    
        coordinates_only = []
        for (atom_coordinate, atom) in self.atoms_unit:
            for symmetry_vec in symmetries:
                
                newcomer_coordinate  = atom_coordinate + symmetry_vec
                [newcomer] = atom.copy()
                
                if any(((newcomer_coordinate == coor).all() 
                        for coor in coordinates_only)):
                    print "WARNING: Duplicate coordinate, newcomer ignored."
                else:
                    self.atoms.append((newcomer_coordinate,newcomer))
                    coordinates_only.append(newcomer_coordinate)
                
        print "  Done!"
        
    def strech(self,strech):
        """
        Streches the crystal from scratch
        """
        
        print "Streching the crystal.."
        
        symmetries = num.array([[x_ctr,y_ctr,z_ctr]
                                for x_ctr in range(strech+1) 
                                for y_ctr in range(strech+1) 
                                for z_ctr in range(strech+1)])
    
        for (atom_coordinate, atom) in self.atoms_cartesian_unit:
            for symmetry_vec in symmetries:
      
                newcomer_coordinate  = atom_coordinate + symmetry_vec
                newcomer = atom.copy()
                self.atoms.append((newcomer_coordinate,newcomer))
                
        print "  Done!"        
        
    def show(self,unit=False):
        """
        Visualizes the structure of the crystal with an interactive 3d 
        interface.
        
            unit = False:
            
            If true, will show the unit cell only.
            
        """
        figure = pylab.figure()
        axes =Axes3D(figure)

        if unit:
            for (atom_coor , atom) in self.atoms_cartesian_unit:
                axes.scatter3D(num.array([atom_coor[0]]),
                             num.array([atom_coor[1]]),
                             num.array([atom_coor[2]]),
                             c=atom.color,
                             s=atom.size)
        else:
            for (atom_coor , atom) in self.atoms:
                axes.scatter3D(num.array([atom_coor[0]]),
                             num.array([atom_coor[1]]),
                             num.array([atom_coor[2]]),
                             c=atom.color,
                             s=atom.radius)
        plt.show()
        
    def prepare(self,):