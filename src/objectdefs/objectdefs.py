"""
Object definitions for a general system in concern. 
"""

class Element(object):
    """
    General definition of an element object.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""
        self.parameters = []

class State(object):
    """
    Definition of the state object.
    """
    def __init__(self, *args, **kwargs):
        self.explanation = ""
        self.parameters = []
        self.constituents = None
        
class Action(object):
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