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

print_en = True

def print_en(selection):
    """
    Print enable function
    """
    global print_en
    if selection:
        print_en = True
    else:
        print_en = False
        
        
class Particle (Element):
    """
    Particle class, a representation of small particles
	"""
    def __init__(self, type='p', *args, **kwargs):
        self.spin = None
        self.energy = None
        self.type = type
    
    def copy(self):
        new_particle = copy.copy(self)
        return new_particle 
 
class Atom(Element):
    """
    Atom class, a representation of an atom.
    """
    def __init__(self, atomic_no = None, *args, **kwargs):
        
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
        self.size = None
        
        # COLOR
        if self.atomic_number == None:
            self.color = 'r'
        else:
            color_1 = (self.atomic_number % 7) / 6
            color_2 = ((self.atomic_number / 7) % 7) / 6
            color_3 = ((self.atomic_number / 7) / 7) / 6
            self.color = (color_1 ,color_2 ,color_3)
            
    def copy(self,n=1):
        """
        Copies an existing atom and returns a copy of it
        """
        atom_copy_list = [copy.copy(self) for n in range(n)]
        return atom_copy_list
    
    def reinit(self):
        """
        Derived properties of the atom is reinitalized
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
            
class AtomicConfiguration(State):
    """
    Atomic Configuration is a looser Lattice Class
    in which the lattice symmetry is not mandatory.
    """
    def __init__(self,dim,*args,**kwargs):
        """
        Defines the Atomic Configuration Class
        """
        self.atoms = []
        self.dim = dim
        
    def copy(self):
        new_lattice = copy.copy(self)
        return new_lattice
        
        
class Lattice(State):
    """
    Atomic Lattice class for Monty Carlo simulations
        This object is meant to be a sole representative of a monatomic 
        lattice class, in which all atoms incorporated will have the same 
        structure.
    """
    def __init__(self,vectors,atoms_basis,strech=1, *args, **kwargs):
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
        self.dim = len(vectors)
        
        if print_en:
            print "Initializing the unit cell.."
        
        self.unit_vectors_not_norm = num.array(vectors)
        
        # Normalizes the base vectors.
        self.unit_vectors = [self.n_norm_vec/num.linalg.norm(self.n_norm_vec) 
                             for self.n_norm_vec in self.unit_vectors_not_norm]
        
        # atoms_unit is a list of (num.array(x,y,z), atom)
        self.atoms_basis = atoms_basis
        self.atoms_unit = [(num.dot(atom.position,self.unit_vectors),atom) 
                                               for atom in self.atoms_basis]

        self.atoms = []
        
        # list of all vectors that are linear super positions of basis vectors
        if self.dim==3: 
            symmetries = num.array([[x_ctr,y_ctr,z_ctr]
                                    for x_ctr in range(strech) 
                                    for y_ctr in range(strech) 
                                    for z_ctr in range(strech)])
        elif self.dim==2:
            symmetries = num.array([[x_ctr,y_ctr]
                                    for x_ctr in range(strech) 
                                    for y_ctr in range(strech)])
        elif self.dim==1:
            symmetries = num.array([[x_ctr]
                                    for x_ctr in range(strech)])
            
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
                    newcomer.coordiante = newcomer_coordinate
                    self.atoms.append(newcomer)
                    coordinates_only.append(newcomer_coordinate)
                
        print "  Done!"
        
    def strech(self,strech):
        """
        Streches the crystal from scratch
        """
        if print_en:
            print "Streching the crystal.."
        
        self.atoms = []
        
        # list of all vectors that are linear superpositions of basis vectors
        if self.dim==3: 
            symmetries = num.array([[x_ctr,y_ctr,z_ctr]
                                    for x_ctr in range(strech) 
                                    for y_ctr in range(strech) 
                                    for z_ctr in range(strech)])
        elif self.dim==2:
            symmetries = num.array([[x_ctr,y_ctr]
                                    for x_ctr in range(strech) 
                                    for y_ctr in range(strech)])
        elif self.dim==1:
            symmetries = num.array([[x_ctr]
                                    for x_ctr in range(strech)])
            
        print symmetries
        
        if print_en:                
            print "  Done!"
            print "Streching the crystal.."
    
        coordinates_only = []
        for (atom_coordinate, atom) in self.atoms_unit:
            for symmetry_vec in symmetries:
                
                newcomer_coordinate  = atom_coordinate + symmetry_vec
                [newcomer] = atom.copy()
                
                if any(((newcomer_coordinate == coor).all() 
                        for coor in coordinates_only)):
                    if print_en:
                        print "WARNING: Duplicate coordinate, newcomer ignored."
                else:
                    newcomer.coordinate = newcomer_coordinate
                    self.atoms.append(newcomer)
                    coordinates_only.append(newcomer_coordinate)
        if print_en:           
            print "  Done!"    
            
    def show(self,unit=False):
        """
        Visualizes the structure of the crystal with an interactive 3d 
        interface.
        
            unit = False:
            
            If true, will show the unit cell only.
            
        """
        if self.dim == 3:
            figure = pylab.figure()
            axes = Axes3D(figure)
                
            if unit and self.unit != None :
                for (atom_coor , atom) in self.atoms_unit:
                    if hasattr(atom, 'color') and hasattr(atom, 'size'):
                        plot_dict = {'c':atom.color,'s':atom.size}
                    elif  hasattr(atom, 'size'): 
                        plot_dict = {'s':atom.size}
                    elif  hasattr(atom, 'color'):
                        plot_dict = {'c':atom.color}
                    else:
                        plot_dict = {}
                        
                    axes.scatter3D(num.array([atom_coor[0]]),
                                 num.array([atom_coor[1]]),
                                 num.array([atom_coor[2]]),
                                 **plot_dict)
            elif not(unit):
                for atom in self.atoms:
                    if hasattr(atom, 'color') and hasattr(atom, 'size'):
                        plot_dict = {'c':atom.color,'s':atom.size}
                    elif  hasattr(atom, 'size'):
                        plot_dict = {'s':atom.size}
                    elif  hasattr(atom, 'color'):
                        plot_dict = {'c':atom.color}
                    else:
                        plot_dict = {}
                    
                    axes.scatter3D(num.array([atom.position[0]]),
                                 num.array([atom.position[1]]),
                                 num.array([atom.position[2]]),
                                 **plot_dict)
        elif self.dim < 3:
            figure = pylab.figure()
    
            if unit and self.unit != None:
                for (atom_coor , atom) in self.atoms_unit:
                    if hasattr(atom, 'color') and hasattr(atom, 'size'):
                        plot_dict = {'c':atom.color,'s':atom.size}
                    elif  hasattr(atom, 'size'):
                        plot_dict = {'s':atom.size}
                    elif  hasattr(atom, 'color'):
                        plot_dict = {'c':atom.color}
                    else:
                        plot_dict = {}
                    plt.scatter(num.array([atom_coor[0]]),
                                 num.array([atom_coor[1]]),
                                 **plot_dict)
            elif not(unit):
                for atom in self.atoms:
                    if hasattr(atom, 'color') and hasattr(atom, 'size'):
                        plot_dict = {'c':atom.color,'s':atom.size}
                    elif  hasattr(atom, 'size'):
                        plot_dict = {'s':atom.size}
                    elif  hasattr(atom, 'color'):
                        plot_dict = {'c':atom.color}
                    else:
                        plot_dict = {}
                    plt.scatter(num.array([atom.position[0]]),
                                 num.array([atom.position[1]]),
                                 **plot_dict)
        plt.show()
        
    def merge(self, lattice_prim , lattice_sec, offset = [0,0,0]):
        """
        Merges two crystals with an offset for the second one.
        """
        dim = max(len(lattice_prim.dim),len(lattice_sec.dim),len(offset))
        output_conf = AtomicConfiguration(dim)
        lattice_prim_newatoms= lattice_prim.deepcopy().atoms
        new_lattice = lattice_sec.deepcopy()
        for atom in new_lattice:
            atom.position = atom.position + offset
        lattice_sec_newatoms= new_lattice.atoms
        output_conf.atoms = lattice_prim_newatoms.append(lattice_sec_newatoms)
        return output_conf
    
    def copy(self):
        new_lattice = copy.copy(self)
        return new_lattice
    
