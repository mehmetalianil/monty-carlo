from montycarlo.objectdefs import *
from montycarlo.ising2d import *
import matplotlib.pylab as plt
import time
import os 

params={"J":1,"H":0.0,"beta":0.1, "N":100,"spin_length":15,"error":0.1}

ensemble = ising_5_generate(params["spin_length"],**{"params":params})
ensemble.picker = boltzmann_picker
original_ensemble = ensemble



#os.chdir("plots15-5spins")

MB=[]
STD=[]

for beta in num.linspace(0.5,2.5,100):

    M=[]
    params["beta"] = beta
    std= 1.0
    error = 1.0
    ensemble.randomize()
    
    while len(M) < 1000 or std>params["error"]:
        for counter in xrange(params["N"]):
            
            element = ensemble.choose_element()
            init_config = element.state 
            configurations = element.states[:]
            energies = ensemble.energy_diff(element)
            where_initial = configurations.index(init_config)
            relative_energies = [energy - energies[where_initial] for energy in energies]
            chosen_one = ensemble.picker(energies,where_initial,**{"params":params})
            element.state = configurations[chosen_one]
        
        mag =  ensemble.magnetization()
        M.append(mag)
        print "For B = "+str(beta)+"\t Pre-Control:["+str(len(M))+"] \t"+str(M[-1])
        std = num.std(M[-100:])
        mean = num.mean(M[-100:])
        error = std/mean
        if len(M) >= 1000 and std<params["error"]:
            print ("M = "+str(mag)+"\t<M> = "+str(mean)+"\tstd(M) = "+str(std)+"\terror = "+str(error))
            MB.append([beta,mean])
            STD.append([std])
            print "For B = "+str(beta)
            print "Magnetization = "+str(mean)
                
    ensemble.save_plot(str(beta)+".eps")
    
        
