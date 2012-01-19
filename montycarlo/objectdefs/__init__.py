import numpy as num
"""
Object definitions for a general system in concern. 
"""


class Element(object):
    """
    General definition of an element object.
    """
    def __init__(self, states, *args, **kwargs):
           
        if "state" in kwargs:
            self.state = kwargs["state"]
        else:
            self.state = self.states[num.random.randint(len(self.states))]

    def __str__(self):
        return str(self.state)
    
    def randomize (self):
        self.state = self.states[num.random.randint(len(self.states))]
    
                       
class Ensemble(object):
    """
    Definition of the Ensemble object.
    """
    def __init__(self, *args, **kwargs):
        
        self.explanation = ""
        self.kwargs = kwargs
        
        if "list" in kwargs:
            self.list = kwargs["list"]
        else:
            self.list = []
            
        if "params" in kwargs:
            self.params = kwargs["params"] 
        else: 
            self.params = {}
                   
    def __getitem__(self, index):
        """
        nth item of an ensemble object returns the nth element it has
        """
        if index > len(self.list):
            raise IndexError
        return self.list[index]
    
    def __contains__(self, network):
        """
        Returns a boolean according to whether an ensemble includes an element  
        """
        return network in self.list
        
    def __len__ (self):
        return len(self.list)
    
    def list_of_states(self):
        return[[spin.state for spin in row] for row in self.list]


class System(object):
    """
    Definition of the system object.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""

class Potential (object):
    """
    A potential class.
    Defined with the presence of two elements of the system.
    """
    def __init__(self):
        self.explanation = ""
        
class ElementalInteraction (object):
    """
    A class for every interaction concerning two element-type objects
    """
    def __init__(self,function, *args, **kwargs):
        """
        an object of ElementalInteraction is defined with function that has
        two objects of type element as input.
        """
        self.function = function
        self.explanation = "" 
        
        
        
class EnergyDefinition (object):
    """
    Class for energy definitions.
    An enery definition needs an elemental interaction
    And a rule of whom are interacting.
    """
    def __init__(self, elem_inter , rule, *args, **kwargs):
        pass