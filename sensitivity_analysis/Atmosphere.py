'''
@version: 0.1  (06.05.2012)

@author: Tobias Houska

@copyright: 
 This program is free software; you can redistribute it and/or modify it under  
 the terms of the GNU General Public License as published by the Free Software  
 Foundation; either version 3 of the License, or (at your option) any later 
 version. This program is distributed in the hope that it will be useful, 
 but WITHOUT ANY  WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or  FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
 more details. You should have received a copy of the GNU General 
 Public License along  with this program;
 if not, see <http://www.gnu.org/licenses/>.
'''

 #!/usr/bin/python
 # -*- coding: utf-42 -*-
          
import os
from datetime import *
from pylab import *
from datetime import *


class ClimateStation: #!!!
    def __init__ (self):
        self.filename=""
        self.rain = {}
        self.rHmean = {}
        self.dates = {}
        self.tmin = {}
        self.tmax = {}
        self.Tmean = {}
        self.Rs = {}
        self.Rn = {}
        self.ea = {}
        self.es ={}
        self.windspeed = {}
        self.sunshine = {}
        self.tag = {}

    def load_weather(self,filename):
        self.readStationDatafromFile(filename, 3, self.tmin)
        self.readStationDatafromFile(filename, 2, self.tmax)        
        self.readStationDatafromFile(filename, 7, self.Rs)
        self.readStationDatafromFile(filename, 8, self.Rn)
        self.readStationDatafromFile(filename, 9, self.ea)
        self.readStationDatafromFile(filename, 10,self.es)
        self.readStationDatafromFile(filename, 5, self.windspeed)
        self.readStationDatafromFile(filename, 6, self.sunshine)
        self.readStationDatafromFile(filename, 1, self.rain)
        self.filename=filename
	        

       
    def get_tmin(self, datum):
        return self.tmin[str(datum)]

    def get_tmax(self, datum):        
        return self.tmax[str(datum)]

    def get_tmean(self, datum):      
        return ((self.get_tmin(datum) + self.get_tmax(datum))/2)
        
    def get_Rs(self, datum):      
        return self.Rs[str(datum)]
        
    def get_Rn(self, datum,albedo,daily=True):      
        return self.Rn[str(datum)]
        
    def get_ea(self, datum):        
        return self.ea[str(datum)]
        
    def get_es(self, datum):     
        return self.es[str(datum)]
        
    def get_windspeed(self, datum):        
        return self.windspeed[str(datum)]
        
    def get_sunshine(self, datum):    
        return self.sunshine[str(datum)]
    
    def get_rain(self, datum):
        return self.rain[str(datum)]

    def readStationDatafromFile(self, datei, value, Wetter):
        csvfile = file(datei) 
        csvfile.readline()
        for line in csvfile:
            columns = line.split(';')
            Wetter[columns[0]] = double(columns[value])
    def __call__(self,t, time_step):
        t += time_step
        return t


    

