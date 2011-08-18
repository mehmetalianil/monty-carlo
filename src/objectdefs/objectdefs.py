"""
Object definitions for a general system in concern. 
"""

class element(object):
    """
    General definition of an element object.
    """
    def __init__(self):
        self.explanation = ""
        self.parameters = []

class state(object):
    """
    Definition of the state object.
    """
    def __init__(self):
        self.explanation = ""
        self.parameters = []
        self.constituents = None
        
class action(object):
    """
    Definition of the action object.
    This object will be an ancestor of all actions on one state
    """
    def __init__(self):
        self.explanation = ""
        self.actson_states = None
        self.actson_elements = None 
        self.language = None
        self.function = None
        
class system(object):
    """
    Definition of the system object.
    
    """


        