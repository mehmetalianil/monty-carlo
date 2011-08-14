class atom(object):
    """
    Atom class, a representation of an atom.
    """
    def __init__(self):
        self.atomic_number = None
        self.mass_number = None
        self.charge = None
        self.magnetic_moment = None
    
    def copy(self):
        """
        Copies an existing atom and returns a copy of it
        """
        atom_copy = self()
        atom_copy.atomic_number = self.atomic_number
        atom_copy.mass_number = self.mass_number
        atom_copy.charge = self.charge
        atom_copy.magnetic_moment = self.magnetic_moment
        
        return atom_copy
    
    
        

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