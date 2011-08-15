#! /usr/bin/env python

import atomic as a
import numpy as num

Na = a.atom(atomic_no=55)
Cl = a.atom(atomic_no=91)

Na.position=num.array([0,0,0])
Cl.position=num.array([0.5,0.5,0.5])

list_of_atoms = [Na,Cl]
unit_vec = (num.array([1,0,0]),num.array([0,1,0]),num.array([0,0,1]))
lat = a.atomic_lattice(unit_vec,list_of_atoms,strech=2)
lat.show(unit=True)