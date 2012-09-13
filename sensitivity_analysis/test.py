# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 13:41:23 2012

@author: Pooder
"""

import numpy as np


fname = 'test.csv'
dtype=[('Jahr', '<f8'), ('Monat', '<f8'), ('Tag', '<f8'), ('Biomasse', '<f8')]
myFile = np.genfromtxt(fname,delimiter=';',names=True,dtype=dtype)

#print np.random.random_integers(1.0,10.0, 20.0)

for i in range(10):
    print np.random.uniform(0.1, 20)

# x = np.genfromtxt('Tabelle_RUE.csv',delimiter=',',names=True)
#dtype=[('ID', '|S10'),('OFAT_factor', '|S10'),('OFAT_value', 'f8'),('Pot.biomass', 'f'),('Act.biomass', 'f')]
   