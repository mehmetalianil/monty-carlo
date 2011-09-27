#!/usr/bin/env python

from objectdefs import *
import matplotlib.pyplot as plt
import copy
import numpy as num
import pylab
from mpl_toolkits.mplot3d import Axes3D

print_en = True

def ising_interaction_func(element,surroundings,self_contrib=1,surr_contrib=1):
    energy = self_contrib * element.spin
    for other_object in surroundings:
        energy = energy + element.spin*other_object.spin*surr_contrib
        
ising_interaction = ElementalInteraction() 
ising_interaction.function = ising_interaction_func()

def ising_energy_def():
    pass