from montycarlo.objectdefs import *
from montycarlo.kink import *
import matplotlib.pylab as plt
import time
import os 

params={"beta":10, "N":100,"chain_length":30,"error":0.1}

ensemble = chain_generate(params["chain_length"],**{"params":params})
ensemble.picker = boltzmann_picker
original_ensemble = ensemble


if not(os.path.exists("kink1")):
    os.mkdir("kink1")
os.chdir("kink1")

SB=[]
STD=[]

for beta in num.linspace(4,.1,100):
    E = []
    S=[]
    params["beta"] = beta
    std= 1.0
    error = 1.0
    ensemble.randomize()
    
    while len(S) < 1000 or std>params["error"]:
        for counter in xrange(params["N"]):
            
            element = ensemble.choose_element()
            init_config = element.state 
            energies = ensemble.energy_diff(element)
            minimum  = min(energies)
            
            if energies[0] == minimum:
                element.set_state(element.state + (math.pi)/180)
            
            if energies[2] == minimum:
                element.set_state(element.state -(math.pi)/180)
            
            if energies[1] == minimum:
                mbeta = -beta
                random_number = num.random.random()
                probs = num.exp(num.multiply(energies,beta))
                probabilities = num.divide(probs,probs.sum())    
                summed = 0.0
                summed_probs = probabilities[:]
                for ctr,item in enumerate(probabilities):
                    summed = item+summed
                    summed_probs[ctr] = summed
                larger = num.where(summed_probs > random_number)[0]
                
                if len(larger)== 0 :
                    element.set_state(element.state)
                else:
                    if larger[0] == 0:
                        element.set_state(element.state + (math.pi)/180)
                    
                    if larger[0] == 1:
                        element.set_state(element.state)
                
                    if larger[0] == 2:
                        element.set_state(element.state -(math.pi)/180)
                                
        straight =  ensemble.straightness()
        E.append(ensemble.energy())
        S.append(straight)
        print "For B = "+str(beta)+"\t Pre-Control:["+str(len(S))+"] \t"+str(S[-1])+"\t Energy = "+str(E[-1])
        std = num.std(S[-100:])
        mean = num.mean(S[-100:])
        error = std/mean
        if len(S) >= 1000 and std<params["error"]:
            print ("S = "+str(straight)+"\t<S> = "+str(mean)+"\tstd(S) = "+str(std)+"\terror = "+str(error))
            SB.append(S)
            STD.append(std)
            print "For B = "+str(beta)
            print "Straightness = "+str(mean)
                
    ensemble.save_plot(str(beta)+".eps")
    
        
