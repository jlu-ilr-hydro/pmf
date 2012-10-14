# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 13:41:23 2012

@author: Pooder
"""

import numpy as np
from datetime import *



#Start = datetime(1992,1,1)
#End = datetime(1998,12,31)

#Duration.days=End-Start
#Date = '%smm.%rmm.%nmmmmm'(s=01,r=12,n=1223)
#String ='01.01.1992'#

#Split = str.split(String)

#Dare=datetime(2002, 3, 11)

#class Res(object):
#    def __init__(self):
#        self.Liste=[]
#        
#        
#if __name__=='__main__':
#    
#    res=Res()
#    res.Liste.append(2)
#    
#    String='Liste'
#
#    print res.String

#fname = '.csv'
#dtype=[('Jahr', '|S10'), ('Monat', '|S10'), ('Tag', '|S10'), ('Biomasse', '<f8',(2))]
#myFile = np.empty((2),dtype=dtype)
#
#print myFile['Biomasse'][0][0]
#

Result_Parameter_List = np.zeros((3),dtype=[('Result_Parameter', 'f8',(2,5)),('Year', 'int16'),('Month','int16'),('Day','int16')])

Result_Parameter_List['Result_Parameter'][0][]=[1,2,3,4,5]        

print Result_Parameter_List
#Res = np.zeros([1],dtype=[('flux','f8',(5)),('water_uptake','f8',(5)),('branching','f8',(5)),
#    ('transpiration','f8'),('evaporation','f8'),('biomass','f8'),('root_biomass','f8'),
#    ('shoot_biomass','f8'),('lai','f8'),('root_growth','f8',(5)),('ETo','f8'),
#    ('ETc','f8'),('wetness','f8',(5)),('porosity','f8',(5)),('rain','f8'),
#    ('temperature','f8'),('DAS','|S20'),('stress','f8',(2)),('leaf','f8'),
#    ('stem','f8'),('steam_and_leaf','f8'),('storage','f8'),('potential_depth','f8'),
#    ('rooting_depth','f8'),('time','|S20'),('developementstage','|S20'),('PotentialGrowth','f8'),
#    ('ActualGrowth','f8'),('developementindex','|S20'),('deep_perlocation','f8'),('baresoil_evaporation','f8'),
#    ('waterstorage','f8',(5)),('watercontent_0_30cm','f8'),('watercontent_30_60cm','f8'),('watercontent_60_90cm','f8'),
#    ('watercontent_30_60_90cm','f8',(3))])
#Zahl = 4
#
#String = 'A'
#
#x = ','.join([np.str(i) for i in SetupFile['ClimateData']])
#New_String=''
#
#for i in range(Zahl):
#    if i == Zahl-1:
#        New_String+=String+str(i)
#    else:
#        New_String+=String+str(i)+','
#
#print New_String[2]
#
#x = np.zeros((Zahl,),dtype=('i4,f4,a10'))
#
#x[1] = (1,2.,'Hello')



#
#Liste=[]
#Liste.append('Run_ID')
#for i in range(4):
#    Liste.append(i)
#
#
#x = np.core.defchararray.array(Liste)    
#
#print x
#
#String=
#Parameterset = np.zeros((),dtype=[('Parameter', 'a20'),('Min_value', 'f8'),('Max_value', 'f8')])

#print np.random.random_integers(1.0,10.0, 20.0)
#
#for i in range(10):
#    print np.random.uniform(0.1, 20)

# x = np.genfromtxt('Tabelle_RUE.csv',delimiter=',',names=True)
#dtype=[('ID', '|S10'),('OFAT_factor', '|S10'),('OFAT_value', 'f8'),('Pot.biomass', 'f'),('Act.biomass', 'f')]
   