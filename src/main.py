'''
Created on 15.05.2011

@author: Mehmet Ali Anil


'''

import numpy as num
import energy_def_lib as mc
import profile 

#import psyco ; psyco.jit() 
#from psyco.classes import *

__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"

if __name__ == '__main__':
    profile.run('print mc.monte_carlo_2d(); print')