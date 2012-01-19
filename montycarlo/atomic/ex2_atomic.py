#! /usr/bin/env python

import atomic as a
import numpy as num
import logging
logging.basicConfig(level=logging.DEBUG)


Na = a.Atom(atomic_no=11)
Cl = a.Atom(atomic_no=17)
Na.size=25
Cl.size=40

[Na2] = Na.copy(1)
[Cl2] = Cl.copy(1)


Na.position=num.array([0,0])
Cl.position=num.array([.5,0])
Na2.position=num.array([.5,.5])
Cl2.position=num.array([0,.5])


list_of_atoms = [Na,Na2,Cl,Cl2]

unit_vec = (num.array([1,0]),num.array([0,1]))
lat = a.Lattice(unit_vec,list_of_atoms,strech=3)
lat.show()