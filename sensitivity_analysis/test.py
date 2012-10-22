# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 13:41:23 2012

@author: Pooder
"""

import numpy as np
from datetime import *
import csv
import os
import Statistic_Tool as stat

R=stat.R_squared([627,3548],[10.5437244,542.714621])
r =np.corrcoef([627,3548],[10.5437244,542.714621])
print r


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
#csvfile =file('Measured_yield_Kersebaum_Plot1.csv') 
#Headers=csvfile.readline().split(';')[4:]
#Headers_new=Headers.strip('\n')
#String=csvfile.readline()
#Plot=[]
#for line in csvfile:
#    columns = line.split(';')
#    Plot.append(columns[0])
#    
#print Plot[0]

#Result=[]
#
#Result.append('String;String2;String3')
#Result.append(str(1)+';'+str(2)+';'+str(3))
#
#with open('Test_Data.csv', 'wb') as f:    
#    writer = csv.writer(f)
#    writer.writerow(['Settings:'+';'+'Plot'+';'+'Hallo'])
#    for i in range(len(Result)):    
#        writer.writerow([Result[i]])


#String =str('Apfel')+';'+str('Brine')
#
#print String.split(';')[0]

#Liste=[-99999,1,2,3,-99999,3]
#
#Liste_calc=[555,555,555,555,555,555]
#
##Copy_Liste=[]
##for i in range(len(Liste)):
##    Copy_Liste.append(Liste[i])
#k=0
#for i in range(len(Liste)):
#    if Liste[i] ==-99999:
#        Liste_calc[i]=-99999        
#        #Copy_Liste.pop(i-k)
#        #k+=1      
#
##for i in range(len(i_Liste)):
#print Liste
#print Liste_calc

#l = [('a', 1), ('b', 2), ('c', 3)]
#k = 1
#
#l_without_num = l[:k] + l[(k + 1):]    
            


            
#            
#with open('Test.csv', 'wb') as f:    
#    writer = csv.writer(f)
#    writer.writerow(['hello'])
#    writer.writerow([''])
#    writer.writerow(['Year','Month','Day'])
#    for i in range(5):
#        writer.writerow([1,2,3])
#
#os.remove('Test.csv')
#
#open('Test.csv')
#


#Result_Parameter_List = np.zeros((3),dtype=[('Result_Parameter', 'f8',(2,5)),('Year', 'int16'),('Month','int16'),('Day','int16')])
#
#Result_Parameter_List['Result_Parameter'][0][0]=[1,2,3,4,5]        
#
#Start=datetime(1999,12,31)
#End=datetime(2000,1,31)
#
#duration=End-Start
#
#Result_Parameter_List = np.zeros((duration.days),dtype=[('Result_Parameter', '|S20'),('Year', 'int16'),('Month','int16'),('Day','int16')])
#
#for i in range(int(duration.days)):
#    Day=Start+timedelta(days=i)
#    Result_Parameter_List['Result_Parameter'][i]=str(Day.date())
#    
#
#
#print Result_Parameter_List['Result_Parameter']
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
   