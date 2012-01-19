'''
Created on Aug 12, 2011

@author: mali, ege
'''

import numpy as num
import datetime
import profile



#class MyClass(object):
#    '''
#    classdocs
#    '''


def random_number(k):       # for the ideal case one should choose k as large as 
                            # possible lets say 12 at least, since we will have  
                            # 2**(k-2) numbers between [0,1], inreasing k exponentially 
                            # increases our sample of random numbers
    """
    generates a uniform list consisting of 
    2**(k-2) numbers in random order in the
    interval [0,1] 

    our recursion is in the following form:
    x_n+1=x_n * rho (mod 2**k)
    we work in base 2 and we drop the last
    2 digits of each element(again in base 
    2) and then convert it to decimal, so
    we will have each number from 0 to 
    2**(k-2) once in a shuffled order then
    by dividing each element by 2**(k-2)
    we will have a uniform list in the
    interval [0,1] 

    (since it is lengthy and harder to go
    from binary <--> decimal couple of
    times in this code we extend the same
    logic such that we can use the same algorithm
    using the decimal representation only, details
    can be found in the comments)

    when rho=8t-3 our list is 
    guaranteed to have a period of 2**(k-2)
        
    """
    
    now = datetime.datetime.now()
    
    x = num.zeros(2**(k-2),num.float64)
    rand_num = num.zeros(2**(k-2),num.float64)
    rand_num_normal = num.zeros(2**(k-2),num.float64)
    rand_num_bin = '0'  
    t = now.second    
#    ms = now.microsecond
    x[0] = (2*t+3) % (2**k)
    

    if t != 0:                   # to aviod rho being negative 
        rho = 8*t-3
    else:
        rho = 3
#    print rho
    for n in range(2**(k-2)-1):
        x[n+1] = (x[n] * rho) % (2**k)
#        print x
    for n in range(2**(k-2)):
        rand_num[n] = ( x[n] - ( x[n] % 4 ) ) / 4           # since all different x values are seperated
        rand_num_normal[n] = rand_num[n] / (2**(k-2) -1)    # by an interval of 4, by this procedure
                                                            # we generate all possible numbers between
    return  rand_num_normal #,rand_num                      # [0,2**(k-2)) then by normalizing it
                                                            # we obtain the uniform set of numbers
                                                            # in the interval [0,1]
                
#        '''
#        Constructor
#        '''

# Random Generator Trial

                                # it's hard to see the result in the command window 
                                # for k=12 so for the sake of illusturation k is
                                # chosen to be 10 here
def bigloop():
    randoms = []
    for stack in range(100):
        randoms = num.append(randoms,random_number(15))
        print stack
    return randoms


#profile.run('print bigloop(); print')

