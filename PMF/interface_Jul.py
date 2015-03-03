# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:54:46 2014

:author: kellner-j
"""

import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
from pandas import DataFrame, Series


import datetime
from datetime import timedelta



#df=pd.read_csv('CO2_extension/ClimateDataFace.csv')
#df

#r'C:\Users\kellner-j\WinPython-64bit-2.7.5.amd64\Lib\site-packages\PMF\ClimateDataFace.csv'
#fpath='D:\Daten\Documents\Code\MeteorologischeDaten\ClimateDataFace.csv'

class Atmosphere_FACE:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        #self.np_weather = np.genfromtxt(self.fpath,names=True,delimiter='\t',dtype=[('Date', '<S10'), ('Rain_mmday', '<f8'), ('Tmax_degC', '<f8'), ('Tmin_degC', '<f8'), ('rHmean_', '<f8'), ('sunshine_', '<f8'), ('Windspeed_ms', '<f8')])
        #self.datum = self.weather['Date']        
        #self.datum = self.weather['Date']
#        self.tmax = self.weather['Tmax_C']
#        self.tmin = self.weather['Tmin_C']
#        self.rain = self.weather['Rain_mm']
#        self.tmean = (self.tmax/self.tmin)/2.
#        self.Rs = self.weather['RS_MJ_qm*d']
##        self.Rn = self.weather['Rn_MJ_qm*d']
##        self.sunshine = self.weather['Sunshine_h']
#        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
                
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]  
        #return self.tmin[self.datum == time]         
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
        #return self.tmax[self.datum == time] 
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
#    def get_Rn(self,time, albedo, daily=True):
#        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
#        index = self.weather[self.datum==time].index[0]           
#        return self.weather['Rn'][index]
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
#        return 0
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]          
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]         
           
    def get_CO2_A1(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns measured CO2 concentration in ring A1 (ambient) [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_A1'][index]
    def get_CO2_A2(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns measured CO2 concentration in ring A2 (ambient) [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_A2'][index]
    def get_CO2_A3(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns measured CO2 concentration in ring A3 (ambient) [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_A3'][index]
    def get_CO2_E1(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns measured CO2 concentration in ring E1 (elevated) [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_E1'][index]
    def get_CO2_E2(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns measured CO2 concentration in ring E2 (elevated) [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_E2'][index]
    def get_CO2_E3(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns measured CO2 concentration in ring E3 (elevated) [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_E3'][index]


class Atmosphere_Ring1_nCO2:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace_A1E1.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        #self.np_weather = np.genfromtxt(self.fpath,names=True,delimiter='\t',dtype=[('Date', '<S10'), ('Rain_mmday', '<f8'), ('Tmax_degC', '<f8'), ('Tmin_degC', '<f8'), ('rHmean_', '<f8'), ('sunshine_', '<f8'), ('Windspeed_ms', '<f8')])
        #self.datum = self.weather['Date']        
        #self.datum = self.weather['Date']
        self.tmax = self.weather['Tmax_C']
        self.tmin = self.weather['Tmin_C']
        self.rain = self.weather['Rain_mm']
        self.tmean = (self.tmax/self.tmin)/2.
        self.Rs = self.weather['RS_MJ_qm*d']
        self.Rn = self.weather['Rn_MJ_qm*d']
#        self.sunshine = self.weather['Sunshine_h']
        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
                
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]  
        #return self.tmin[self.datum == time]         
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
        #return self.tmax[self.datum == time] 
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
    def get_Rn(self,time, albedo, daily=True):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]           
#        return self.weather['Rn'][index]
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
#        return 0
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]          
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]            
    def get_CO2_measured(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns CO2 concentration [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_ambient'][index]

################ RING 2 ################### RING 2 ########################### RING 2 ####################### RING 2 ###     
class Atmosphere_Ring2_nCO2:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace_A2E2.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        #self.np_weather = np.genfromtxt(self.fpath,names=True,delimiter='\t',dtype=[('Date', '<S10'), ('Rain_mmday', '<f8'), ('Tmax_degC', '<f8'), ('Tmin_degC', '<f8'), ('rHmean_', '<f8'), ('sunshine_', '<f8'), ('Windspeed_ms', '<f8')])
        #self.datum = self.weather['Date']        
        #self.datum = self.weather['Date']
        self.tmax = self.weather['Tmax_C']
        self.tmin = self.weather['Tmin_C']
        self.rain = self.weather['Rain_mm']
        self.tmean = (self.tmax/self.tmin)/2.
        self.Rs = self.weather['RS_MJ_qm*d']
        self.Rn = self.weather['Rn_MJ_qm*d']
#        self.sunshine = self.weather['Sunshine_h']
        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
        
        
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]  
        #return self.tmin[self.datum == time]         
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
        #return self.tmax[self.datum == time] 
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
    def get_Rn(self,time, albedo, daily=True):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]           
#        return self.weather['Rn'][index]
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
#        return 0
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]        
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]           
    def get_CO2_measured(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns CO2 concentration [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_ambient'][index]               

################ RING 2 ################### RING 2 ########################### RING 2 ####################### RING 2 ###    
class Atmosphere_Ring3_nCO2:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace_A3E3.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        self.tmax = self.weather['Tmax_C']
        self.tmin = self.weather['Tmin_C']
        self.rain = self.weather['Rain_mm']
        self.tmean = (self.tmax/self.tmin)/2.
        self.Rs = self.weather['RS_MJ_qm*d']
        self.Rn = self.weather['Rn_MJ_qm*d']
#        self.sunshine = self.weather['Sunshine_h']
        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
        
        
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]        
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
    def get_Rn(self,time, albedo, daily=True):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]           
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]               
    def get_CO2_measured(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns CO2 concentration [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_ambient'][index]        
 
 
class Atmosphere_Ring1_eCO2:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace_A1E1.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        #self.np_weather = np.genfromtxt(self.fpath,names=True,delimiter='\t',dtype=[('Date', '<S10'), ('Rain_mmday', '<f8'), ('Tmax_degC', '<f8'), ('Tmin_degC', '<f8'), ('rHmean_', '<f8'), ('sunshine_', '<f8'), ('Windspeed_ms', '<f8')])
        #self.datum = self.weather['Date']        
        #self.datum = self.weather['Date']
        self.tmax = self.weather['Tmax_C']
        self.tmin = self.weather['Tmin_C']
        self.rain = self.weather['Rain_mm']
        self.tmean = (self.tmax/self.tmin)/2.
        self.Rs = self.weather['RS_MJ_qm*d']
        self.Rn = self.weather['Rn_MJ_qm*d']
#        self.sunshine = self.weather['Sunshine_h']
        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
        
        
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]  
        #return self.tmin[self.datum == time]         
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
        #return self.tmax[self.datum == time] 
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
    def get_Rn(self,time, albedo, daily=True):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]           
#        return self.weather['Rn'][index]
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
#        return 0
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]          
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]             
    def get_CO2_measured(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns CO2 concentration [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_elevated'][index]

################ RING 2 ################### RING 2 ########################### RING 2 ####################### RING 2 ###     
class Atmosphere_Ring2_eCO2:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace_A2E2.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        #self.np_weather = np.genfromtxt(self.fpath,names=True,delimiter='\t',dtype=[('Date', '<S10'), ('Rain_mmday', '<f8'), ('Tmax_degC', '<f8'), ('Tmin_degC', '<f8'), ('rHmean_', '<f8'), ('sunshine_', '<f8'), ('Windspeed_ms', '<f8')])
        #self.datum = self.weather['Date']        
        #self.datum = self.weather['Date']
        self.tmax = self.weather['Tmax_C']
        self.tmin = self.weather['Tmin_C']
        self.rain = self.weather['Rain_mm']
        self.tmean = (self.tmax/self.tmin)/2.
        self.Rs = self.weather['RS_MJ_qm*d']
        self.Rn = self.weather['Rn_MJ_qm*d']
#        self.sunshine = self.weather['Sunshine_h']
        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
        
        
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]  
        #return self.tmin[self.datum == time]         
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
        #return self.tmax[self.datum == time] 
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
    def get_Rn(self,time, albedo, daily=True):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]           
#        return self.weather['Rn'][index]
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
#        return 0
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]        
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]            
    def get_CO2_measured(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns CO2 concentration [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_elevated'][index]               

################ RING 2 ################### RING 2 ########################### RING 2 ####################### RING 2 ###    
class Atmosphere_Ring3_eCO2:
    #das hier ist der Constructor. Alles was hier drin steht wird nur ein Mal durchgeführt
    #alles was danach in den def's kommt, wird bei jedem Zeitschritt abgefragt
    def __init__(self,fpath='ClimateDataFace_A3E3.csv'):
        self.fpath = fpath
        self.weather = pd.read_table(self.fpath, sep=';')
        self.tmax = self.weather['Tmax_C']
        self.tmin = self.weather['Tmin_C']
        self.rain = self.weather['Rain_mm']
        self.tmean = (self.tmax/self.tmin)/2.
        self.Rs = self.weather['RS_MJ_qm*d']
        self.Rn = self.weather['Rn_MJ_qm*d']
#        self.sunshine = self.weather['Sunshine_h']
        self.wind = self.weather['Windspeed_m_s']

        self.datum = pd.to_datetime(self.weather['Date'], format = '%Y-%m-%d')
        
        
    def get_tmean(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]   
        return self.weather['Tmean_C'][index]  
#        return ((self.weather['Tmax_C'][self.weather[self.datum == time].index[0]] + self.weather['Tmin_C'][self.weather[self.datum==time].index[0]])/2)                
    def get_tmin(self,time):
      #  """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]                
        return self.weather['Tmin_C'][index]        
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Tmax_C'][index]  
    def get_Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_MJ_qm*d'][index]
    def get_Rn(self,time, albedo, daily=True):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns net radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]           
        return self.weather['Rn_MJ_qm*d'][index]
    def get_Rs_clearsky(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns clear sky solar radiation in [MJ m-2]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['RS_clearsky_MJ_qm*d'][index]       
    def get_ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Ea'][index]
    def get_es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Es'][index]
    def get_windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
        index = self.weather[self.datum==time].index[0]    
        return self.weather['Windspeed_m_s'][index]
    def get_rainfall(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns rainfall in [mm/d]"""
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Rain_mm'][index]
    def get_daylength(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns day length in [h] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['Daylength_h'][index]              
    def get_CO2_measured(self,time):
        """  Time as datetime instance: datetime(JJJJ,MM,DD); Returns CO2 concentration [ppm] """
        index = self.weather[self.datum==time].index[0] 
        return self.weather['CO2_elevated'][index]        
 