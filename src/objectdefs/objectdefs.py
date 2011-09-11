"""
Object definitions for a general system in concern. 
"""

import probes

class Element(object,probes.probeable):
    """
    General definition of an element object.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""
        self.parameters = []

class State(object,probes.probeable):
    """
    Definition of the state object.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""
        self.parameters = []
        self.constituents = None
        
class Action(object,probes.probeable):
    """
    Definition of the action object.
    Encapsulates an action on a state.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""
        self.actson_states = None
        self.actson_elements = None 
        self.language = None
        self.function = None
        
class System(object,probes.probeable):
    """
    Definition of the system object.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""

class Potential (object,probes.probeable):
    """
    A potential class.
    Defined with the presence of two elements of the system.
    """
    def __init__(self):
        self.explanation = ""
        
class ElementalInteraction (object,probes.probeable):
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
        
        
        
class EnergyDefinition (object,probes.probeable):
    """
    Class for energy definitions.
    An enery definition needs an elemental interaction
    And a rule of whom are interacting.
    """
    def __init__(self, elem_inter , rule, *args, **kwargs):
        pass