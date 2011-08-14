#!/usr/bin/env python

"""Provides classes relating to MC statistics with atoms
"""

import copy
import numpy as num

class particle (object):
    """Particle class, a representation of small particles
	"""
    def __init__(self, type='p'):
        self.spin = None
        self.energy = None
        self.type = type
    
    def copy(self):
        new_particle = copy.copy(self)
        return new_particle 
 
class atom(object):
    """Atom class, a representation of an atom.
    """
    def __init__(self):
        
        # initialization of an atom class
        self.atomic_number = None
        self.mass_number = None
        self.charge = None
        self.magnetic_moment = None
        self.stable = True
        
        # Probability of decay per unit time 
        self.decay_prob = None
        
        # Decay process: [Change in proton number, neutron number, particle object] 
        self.decay_process = [None, None, None]
        
        # A pseudo radius for close packing
        self.radius = None
    
        # Derived Properties
        
        self.neutron = self.mass_number - self.atomic_number
        self.proton = self.atomic_number
        
    def copy(self):
        """Copies an existing atom and returns a copy of it
        """
        atom_copy = copy.copy(self)
                
        return atom_copy
    def reinit(self):
        """Derived properties of the atom is reinitalized
        """
        self.neutron = self.mass_number - self.atomic_number
        self.proton = self.atomic_number

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
            
            This is a Python list of the tuple of atoms and coordinates of 
			the atoms with respect to 
            the coordinate system formed with (vector_1,vector_2,vector_3).
            
            An example may be:
            
            [([0,0,0],atom_a),([0,0.5,0.5],atom_a),([0.5,0.5,0],atom_a),
            ([0.5,0,0.5],atom_a),([1,0.5,0.5],atom_a),
            ([0.5,0.5,1],atom_a),([0.5,1,0.5],atom_a),([1,0,0],atom_a),
            ([0,1,0],atom_a),([0,0,1],atom_a),
            ([1,1,0],atom_a),([1,0,1],atom_a),
            ([0,1,1],atom_a),([1,1,1],atom_a)]
            
            which is the list for all atoms in a face centered cubic structure.
        """
        
        self.explanation = None
        
        print "Initializing the unit cell.."
        self.vectors_n_norm = num.array([vector_1,vector_2,vector_3])
        #Normalizes the bases vector.
        self.vectors = [self.n_norm_vec/num.linalg.norm(self.n_norm_vec) 
                        for self.n_norm_vec in self.vectors_n_norm]
       
        self.atoms_unit_coor = num.array(atoms_unit)
        self.atoms_cartesian_unit = num.array([num.dot(atom_position,self.vectors) for 
                           (atom_no,atom_position) in enumerate(self.atoms_unit_coor)])

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