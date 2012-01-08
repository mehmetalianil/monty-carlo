from objectdefs import *
from ising2d import *
import matplotlib.pylab as plt
import time

params={"J":1,"H":0.0,"beta":0.2, "N":100,"spin_length":50,"error":0.001}

ensemble = ising_generate(params["spin_length"],**{"params":params})
ensemble.picker = boltzmann_picker
original_ensemble = ensemble


MB=[]
for beta in num.linspace(0.1,3,100):
    M=[]
    params["beta"] = beta
    std= 1.0
    while std>params["error"] and len(M)<100:
        for counter in xrange(params["N"]):
            element = ensemble.choose_element()
            init_config = element.state 
            #energies = []
            configurations = element.states[:]
            #for configuration in element.states:
                #element.state = configuration
                #energies.append(ensemble.energy())
                
            energies = ensemble.energy_diff(element)
            where_initial = configurations.index(init_config)
            relative_energies = [energy - energies[where_initial] for energy in energies]
            chosen_one = ensemble.picker(energies,where_initial,**{"params":params})
            element.state = configurations[chosen_one]
        M.append(ensemble.magnetization())
        if len(M)> 10:
            std = num.std(M[-10:])
            if std > params["error"]:
                MB.append([beta,num.mean(M[-10:])])
                print "For B = "+str(beta)
                print "Magnetization = "+str(num.mean(M[-10:]))
        
    
        