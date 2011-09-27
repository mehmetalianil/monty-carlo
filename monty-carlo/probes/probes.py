import numpy as num 

class SubRoutine(object):
    def __init__ (self):
        pass
        
    
monte_carlo = SubRoutine()
dice_throw = SubRoutine()


class probe (object):
    """
    Definition of the probe 
    A probe is has an assignee, and it is defined by listing a probe
    in the list "probes" within that object. (it can be a family or
    a network, obviously)
    The function is defined due to the Network 
    """
    def __init__ (self):
        self.function = None
        self.subroutine = None
        self.data = num.array([])

class mean_score_probe (probe):
    def __init__ (self):       
        probe.__init__(self)
        self.function = self.mean_score
        self.subroutine = dice_throw
        
    def mean_score(self,probeable):
        return num.mean(probeable.scores)
    
class eq_score_probe (probe):
    def __init__ (self):       
        probe.__init__(self)
        self.function = self.eq_score
        self.subroutine = monte_carlo
        
    def eq_score(self,probeable):
        print num.mean(probeable.equilibria)
        return num.mean(probeable.equilibria)


    
    