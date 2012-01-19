from montycarlo.objectdefs import *
import logging
import numpy as num
import copy
import matplotlib.pylab as plt
import math


            
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
    


class Kink(Element):
    def __init__(self, **kwargs):
        if "previous" in kwargs:
            x_init = kwargs["previous"].x
            y_init = kwargs["previous"].y
            self.previous =  kwargs["previous"]
        else:
            x_init = 0.0
            y_init = 0.0
            self.previous = None
            
        if "state" in kwargs:
            state = kwargs["state"]
        else:
            state = 0
            
        if "charge" in kwargs:
            charge = kwargs["charge"]
        else:
            charge = num.random.randint(3)-1
        
        if state > math.pi:
            new_state = state - 2*(math.pi)
        if state < -math.pi:
            state = state + 2*(math.pi)
            
        self.state = state
        self.x = x_init + math.cos(self.state)
        self.y = y_init + math.sin(self.state)
        self.charge = charge
        
    def set_state(self,new_state, **kwargs):
    
        if self.previous == None:
            if new_state > (math.pi):
                new_state = new_state - 2*math.pi
            if new_state < -(math.pi):
                new_state = new_state + 2*math.pi
            self.state = new_state
            self.x = 0.0
            self.y = 0.0
        else:
            if new_state > (math.pi):
                new_state = new_state - 2*math.pi
            if new_state < -(math.pi):
                new_state = new_state + 2*math.pi
            self.state = new_state
            self.x = self.previous.x + math.cos(self.state)
            self.y = self.previous.y + math.sin(self.state)
        
        if "charge" in kwargs:
            self.charge = kwargs["charge"]
    
    def randomize(self):
        random_angle = (num.random.random()-0.5)*2*math.pi
        random_charge = num.random.randint(3)-1
        self.set_state(random_angle,charge=random_charge)
        
        
class Chain(Ensemble):
    def __init__(self,kink_list,*args,**kwargs):
        Ensemble.__init__(self,**kwargs)
        self.list = kink_list
        #self.energy = self.energy()
        self.picker = None
        
    def energy(self):
        xy_list = [[kink.x,kink.y,kink.charge] for kink in self.list]
        energy_coulomb = 0
        for ctr,init in enumerate(xy_list):
            without_init = xy_list[:]
            without_init.remove(init)
            energy_cont = [kink[2]*init[2]/math.sqrt((kink[0]-init[0])**2 +(kink[1]-init[1])**2)  
                           for kink in without_init]
            for energy in energy_cont:
                if energy > 1000:
                    energy = 1000
            energy_coulomb = energy_coulomb + sum(energy_cont)
        return energy_coulomb
    
    def energy_diff(self,element, **kwargs):
        energy_init = self.energy()
        if "change" in  kwargs:
            change = kwargs["change"]
        else: 
            change = [(math.pi)/180 , 0.0 , -(math.pi)/180]
        
        old_state = element.state 
        energy = []
        
        for difference in change:
            element.set_state(old_state+difference)
            energy.append(self.energy()-energy_init)
        
        element.set_state(old_state)
        return energy
        
    def random_element(self):
        randrow = num.random.randint(len(self))
        return self.list[randrow]
    
    def randomize(self):
        for item in self.list:
            item.randomize()
        
    def choose_element(self):
        return self.random_element()
    
    def plot(self):
        x = [kink.x for kink in self.list]
        y = [kink.y for kink in self.list]
        c = [kink.charge for kink in self.list]
        plt.plot(x,y)
        plt.show()
                
    def save_plot(self,name):
        x = [kink.x for kink in self.list]
        y = [kink.y for kink in self.list]
        c = [kink.charge for kink in self.list]
        plt.plot(x,y)        
        plt.savefig(name)
        
    
    def straightness(self):
        return abs(num.mean([kink.state for kink in self.list]))

    
def chain_generate(number,**kwargs):
    starter = Kink()
    list  = [starter]
    
    for i in xrange(number-1):
        follower = Kink(previous=list[-1])
        follower.randomize()
        list.append(follower)
        
    return Chain(list)

