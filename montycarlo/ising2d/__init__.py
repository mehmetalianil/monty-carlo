from montycarlo.objectdefs import *
import logging
import numpy as num
import copy
import matplotlib.pylab as plt
            
def boltzmann_picker(energy_list,init_config, *args, **kwargs):
    if "params" in kwargs:
        params = kwargs ["params"]   
        if "beta" in params:
            mbeta = -params["beta"]
        else:
            logging.error("Boltzmann Distribution needs temperature!")
    else:
        logging.error("Boltzmann Distribution needs params dict!")
    
    initial_energy = energy_list[init_config]
    less_energetic = num.where(energy_list < energy_list[init_config])[0]
    
    if len(less_energetic) == 0:    
        random_number = num.random.random()
        probs = num.exp(num.multiply(energy_list,mbeta))
        probabilities = num.divide(probs,probs.sum())
        summed = 0.0
        summed_probs = probabilities[:]
        for ctr,item in enumerate(probabilities):
            summed = item+summed
            summed_probs[ctr] = summed
        larger = num.where(summed_probs > random_number)[0]
        if len(larger)== 0 :
            minimum_index = num.argmin(energy_list)
            return minimum_index
        else:            
            return larger[0]
    else:
        minimum_index = num.argmin(energy_list)
        return minimum_index
    
    

class Spin(Element):
    def __init__(self, *args, **kwargs):
        self.states = [-1,1]
        Element.__init__(self,self.states)
        
class ThreeSpin(Element):
    def __init__(self, *args, **kwargs):
        self.states = [-1,0,1]
        Element.__init__(self,self.states)

class FiveSpin(Element):
    def __init__(self, *args, **kwargs):
        self.states = [-1,-0.5,0,0.5,1]
        Element.__init__(self,self.states)
            
class SpinGlass (Ensemble):
    def __init__(self,spins,*args,**kwargs):
        Ensemble.__init__(self,**kwargs)
        self.list = spins
        self.picker = None
        
    def energy(self):
        energy = 0
        for rowctr,row in enumerate(self):
            for colctr,spin in enumerate(row):
                energy = energy - self.params["J"]*spin.state*(
                    self[rowctr][colctr-1].state+self[rowctr-1][colctr].state)
        energy = energy - self.params["H"] * sum([spin.state for spin in row for row in self.list])
        return energy 
    
    def energy_diff(self,element):
        where = num.where([[spin == element for spin in row]for row in self.list])
        length_of_list = len(self.list)
        rowctr = where[0][0]
        colctr = where[1][0]
        
        init_energy =  - self.params["J"]*element.state*(
                    self[rowctr][colctr-1].state+self[rowctr-1][colctr].state+
                    self[rowctr][(colctr+1)%length_of_list].state+
                    self[(rowctr+1)%length_of_list][colctr].state)
        
        states = element.states
        
        energies = [ - self.params["J"]*state*(
                    self[rowctr][colctr-1].state+self[rowctr-1][colctr].state+
                    self[rowctr][(colctr+1)%length_of_list].state+
                    self[(rowctr+1)%length_of_list][colctr].state) - init_energy
                       for state in states]
        return energies
        
        
    def random_element(self):
        randrow = num.random.randint(len(self))
        randcol = num.random.randint(len(self[0]))
        return self.list[randrow][randcol]
    
    def randomize(self):
        for row in self:
            for spin in row:
                spin.randomize()
        logging.info("All spins randomized")
        
    def choose_element(self):
        return self.random_element()
    
    def plot(self):
        plt.imshow(self.list_of_states(),cmap=plt.cm.gray,interpolation="nearest")
        plt.show()
        plt.draw()
        
    def save_plot(self,name):
        plt.imshow(self.list_of_states(),cmap=plt.cm.gray,interpolation="nearest")
        plt.savefig(name)
    
    def magnetization(self):
        return abs(num.mean(self.list_of_states()))

    
def ising_generate(number,**kwargs):
    spins  =  [[Spin() for i in range(number)]for j in range(number)]
    return SpinGlass(spins,**kwargs)

def ising_3_generate(number,**kwargs):
    spins  =  [[ThreeSpin() for i in range(number)]for j in range(number)]
    return SpinGlass(spins,**kwargs)

def ising_5_generate(number,**kwargs):
    spins  =  [[FiveSpin() for i in range(number)]for j in range(number)]
    return SpinGlass(spins,**kwargs)
