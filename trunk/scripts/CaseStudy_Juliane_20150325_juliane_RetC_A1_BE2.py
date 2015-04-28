# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:00:12 2013

@author: kellner-j
"""

# -*- coding: utf-8 -*-
"""
Case Study Grass: Water balance - Single layer Storage approach
The Case Study represents a grassland setup of PMF and with the
SoilWaterContainer (SWC) as water balance model:

Weather     : Leihgestern (Gießen),

Soil texture: Silt

Soil        : SWC,

Atmosphere  : cmf1d,      

Simulation  : 1.1.1999 - 31.12.2009 and 

Management  : Sowing - 1.3.JJJJ, Harvest - 8.1.JJJJ.

im
@author: Juliane Kellner

@version: 0.1 (26.10.2010)

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
"""
#######################################
#######################################
### Runtime Loop

import pandas as pd
from pylab import *
from datetime import datetime, date, time, timedelta
sys.path.insert(0,'..')
import PMF





def run(groundwaterlevel,porosity_1,porosity_2,porosity_3,res_weather,res_pmf,res_soilmoisture,res_soilmoisture10,
        res_pressurehead,res_wateruptake,res_branching,
        i_parameterset,day_of_simulation,t,plant,
        tt_of_leaf_development_start,first_simulation_year):  
##### new year
    # at beginning of new year thermal time is set to leaf development
            
    time = mdates.date2num(t)
        
    if t.day==1 and t.month==1 and t.year==first_simulation_year:
        plant.shoot.Wtot = 20.0
        plant.shoot.storage_organs.Wtot = 0.
        plant.shoot.stem.Wtot = 10.  # [g m-2]
#        plant.shoot.stem.vertical_stem_growth = 0.04  #[m]
        plant.shoot.leaf.Wtot = 10.
        plant.shoot.leaf.leafarea = 0.7
        
        
    if t.day==1 and t.month==1 and t.year>=first_simulation_year:      
        plant.developmentstage.tt = tt_of_leaf_development_start

##### harvest
    # reset biomass and thermal time
    if np.any(HarvestDate== t):         
##        #root biomass continues growing
        plant.shoot.Wtot =  20.0 #g m-2
        plant.shoot.storage_organs.Wtot = 0.
        plant.shoot.stem.Wtot = 10. # g m-2
#        plant.shoot.stem.vertical_stem_growth = 0.04  #[m]
        # leave biomass
        # assuming: vegheight =0.04m --> LAI=24*vegheight= 0.96 according to FAO
        # with LAI= 0.96 [m²/m²] and spec_leaf_weight = 40 [g/m²]
        # Wtot = LAI * spec_leaf_weight = 0.96 * 40 = 38.4 [g/m²] after harvest
        plant.shoot.leaf.Wtot = 10.
        plant.shoot.leaf.leafarea = 0.7
        plant.developmentstage.tt = tt_of_leaf_development_start   #with tt=160 ends the emergence phase
    else: pass   
        
    #Let grow
    if plant:         
        plant(day_of_simulation,t,'day',1.)  
    
    if plant:
        res_pmf[i_parameterset,day_of_simulation,0] = plant.biomass.total
        res_pmf[i_parameterset,day_of_simulation,1] = plant.root.Wtot
        res_pmf[i_parameterset,day_of_simulation,2] = plant.shoot.Wtot
        res_pmf[i_parameterset,day_of_simulation,3] = plant.shoot.leaf.Wtot
        res_pmf[i_parameterset,day_of_simulation,4] = plant.shoot.stem.Wtot 
        res_pmf[i_parameterset,day_of_simulation,5] = plant.shoot.storage_organs.Wtot            
        res_pmf[i_parameterset,day_of_simulation,6] = plant.shoot.stem.height
        res_pmf[i_parameterset,day_of_simulation,7] = plant.shoot.leaf.LAI
        res_pmf[i_parameterset,day_of_simulation,8] = plant.root.depth
        res_pmf[i_parameterset,day_of_simulation,9] = plant.developmentstage.verna_factor  
        res_pmf[i_parameterset,day_of_simulation,10] = plant.developmentstage.photo
        res_pmf[i_parameterset,day_of_simulation,11] = plant.developmentstage.Thermaltime
        res_pmf[i_parameterset,day_of_simulation,12] = plant.developmentstage.rate          
        res_pmf[i_parameterset,day_of_simulation,13] = plant.et.Transpiration_pot_SW
        res_pmf[i_parameterset,day_of_simulation,14] = plant.et.Evaporation_pot_SW      
        res_pmf[i_parameterset,day_of_simulation,15] = plant.et.Evapotranspiration_pot_SW
        res_pmf[i_parameterset,day_of_simulation,17] = plant.interception.NetRainfall
        res_pmf[i_parameterset,day_of_simulation,18] = plant.interception.PET0 
        res_pmf[i_parameterset,day_of_simulation,19] = plant.et.T_PM
        res_pmf[i_parameterset,day_of_simulation,20] = plant.et.E_PM
        res_pmf[i_parameterset,day_of_simulation,21] = plant.et.R_c_s
#        res_pmf[i_parameterset,day_of_simulation,22] = atmosphere.Kr()
        res_pmf[i_parameterset,day_of_simulation,23] = plant.et.Evaporation_pot_SW*(0.25*atmosphere.Kr()[0]+0.25*atmosphere.Kr()[1]+0.25*atmosphere.Kr()[2]+0.25*atmosphere.Kr()[3])
        res_pmf[i_parameterset,day_of_simulation,24] = plant.biomass.Rue_soltani
        res_pmf[i_parameterset,day_of_simulation,25] = plant.biomass.par_absorbed
        res_pmf[i_parameterset,day_of_simulation,26] = plant.biomass.ActualGrowth
        res_pmf[i_parameterset,day_of_simulation,27] = time

    res_pmf[i_parameterset,day_of_simulation,16] = atmosphere.get_rainfall(t)
    res_pmf.flush()
    
    for d in range(4): # 0-10cm
        kr_factor = atmosphere.Kr()[d]
#        print kr_factor, d
        res_kr[i_parameterset,day_of_simulation,d,0] = time
        res_kr[i_parameterset,day_of_simulation,d,1] = kr_factor
    res_kr.flush()     
#    for d in range(4):
#        evapo_actual = plant.et.Evaporation_pot_SW*(0.25*atmosphere.Kr()[0]+0.25*atmosphere.Kr()[1]+0.25*atmosphere.Kr()[2]+0.25*atmosphere.Kr()[3])
        
    
    
    res_weather[i_parameterset,day_of_simulation,0] = plant.net_radiation.Rn 
    res_weather[i_parameterset,day_of_simulation,1] = atmosphere.get_tmean(t)
    res_weather[i_parameterset,day_of_simulation,2] = atmosphere.get_tmax(t) 
    res_weather[i_parameterset,day_of_simulation,3] = atmosphere.get_tmin(t)
    res_weather[i_parameterset,day_of_simulation,4] = atmosphere.get_es(t)
    res_weather[i_parameterset,day_of_simulation,5] = atmosphere.get_ea(t)
    res_weather[i_parameterset,day_of_simulation,6] = atmosphere.get_daylength(t)
    res_weather[i_parameterset,day_of_simulation,7] = atmosphere.get_rainfall(t)
    res_weather[i_parameterset,day_of_simulation,8] = atmosphere.get_windspeed(t)    
    res_weather[i_parameterset,day_of_simulation,9] = atmosphere.get_CO2_A1(t)
    res_weather[i_parameterset,day_of_simulation,10] = atmosphere.get_CO2_A2(t)
    res_weather[i_parameterset,day_of_simulation,11] = atmosphere.get_CO2_A3(t)
    res_weather[i_parameterset,day_of_simulation,12] = atmosphere.get_CO2_E1(t)
    res_weather[i_parameterset,day_of_simulation,13] = atmosphere.get_CO2_E2(t)
    res_weather[i_parameterset,day_of_simulation,14] = atmosphere.get_CO2_E3(t)
    res_weather[i_parameterset,day_of_simulation,15] = atmosphere.get_Rs(t)
    res_weather[i_parameterset,day_of_simulation,16] = time
    res_weather[i_parameterset,day_of_simulation,17] = groundwaterlevel
#    print atmosphere.get_ea(t)
    res_weather.flush()           
        
    

    for d,depth in enumerate(atmosphere.soilprofile()):             # m3 water per m3 pores          
        if depth<12.:
            wetness = min(porosity_1, atmosphere.get_wetness(depth) *porosity_1)
            saturation = min(1.,atmosphere.get_wetness(depth))
        if depth>22.:
            wetness = min(porosity_3, atmosphere.get_wetness(depth) *porosity_3) 
            saturation = min(1.,atmosphere.get_wetness(depth))
        else:
            wetness = min(porosity_2, atmosphere.get_wetness(depth) *porosity_2) 
            saturation = min(1.,atmosphere.get_wetness(depth))                          
        res_soilmoisture[i_parameterset,day_of_simulation,d,1] = wetness                        #soil moisture = m3 water per m3 soil
        res_soilmoisture[i_parameterset,day_of_simulation,d,0] = time
        res_soilmoisture[i_parameterset,day_of_simulation,d,2] = depth      
        res_soilmoisture[i_parameterset,day_of_simulation,d,3] = saturation  #saturation = cm3 water per cm3 pore volume
    res_soilmoisture.flush()   
    
    for d,depth in enumerate(atmosphere.soilprofile()):
        wetness1 = atmosphere.get_wetness(1)*porosity_1
        wetness2 = atmosphere.get_wetness(2)*porosity_1
        wetness3 = atmosphere.get_wetness(3)*porosity_1
        wetness4 = atmosphere.get_wetness(4)*porosity_1
        wetness_10cm = mean((wetness1,wetness2,wetness3,wetness4))           
        res_soilmoisture10[i_parameterset,day_of_simulation,1] = wetness_10cm #m3 water per m3 soil
        res_soilmoisture10[i_parameterset,day_of_simulation,0] = time
    res_soilmoisture10.flush()    
    
        
    for d,depth in enumerate(atmosphere.soilprofile()):
        pressurehead = atmosphere.get_pressurehead(depth)
        res_pressurehead[i_parameterset,day_of_simulation,d,1] = pressurehead 
        res_pressurehead[i_parameterset,day_of_simulation,d,0] = time 
    res_pressurehead.flush()        


    for d,depth in enumerate(atmosphere.soilprofile()):
        res_wateruptake[i_parameterset,day_of_simulation,d,1] = plant.Wateruptake[d]    # water uptake through plants [mm]
        res_wateruptake[i_parameterset,day_of_simulation,d,0] = time 
    res_wateruptake.flush()   
    
    for d,depth in enumerate(atmosphere.soilprofile()):
        res_branching[i_parameterset,day_of_simulation,d,1] = plant.root.branching[d] 
        res_branching[i_parameterset,day_of_simulation,d,0] = time
    res_branching.flush()   
    
    return plant
     
    

if __name__=='__main__':
     
################################################################################################
################################################################################################
### Setup script   

    
    import PMF
    import cmf
    from cmf_setup_JK_A1_BE2_RetC import cmf1d                ### ADAPT SCRIPT!!!!!!!!!!!!!!!!
    from cmf_fp_interface_JK import cmf_fp_interface
    import os
    from Load_Data import load_data
    import numpy as np
    import matplotlib.dates as mdates
    
    
    
    project = '_A1_BE2_RetC'
####### external data
   
    # meteorological data
    fpath =     'D:\Daten\Documents\Code\pmf\scripts\Data\ClimateDataFace.csv'
 #   stationname='D:\Daten_fletcher\data\Juliane\pmf\scripts\Data\ClimateDataFace2.csv' #D:\Daten_fletcher\data\Juliane\pmf\scripts\Data\
    Datenstart=datetime(1998,05,20)    
    
    # harvest dates
    Name_of_HarvestFile = 'D:\Daten\Documents\Code\pmf\scripts\Data\Harvestdate.csv'
    read_HarvestFile = pd.read_table(Name_of_HarvestFile, sep=';')
    HarvestDate = pd.to_datetime(read_HarvestFile['Harvestdate'], format = '%Y-%m-%d')   

    fpath_sm = 'D:\Daten\Documents\Code\pmf\scripts\Data\SoilMoisture.csv'

    
###### cmf - soil parameter

    layercount=18
    #layerthickness=0.05
    tracertext=''
    

####### pmf

    tt_of_leaf_development_start = 161.    

##### #
    #Simulation period
    start = datetime(1999,01,01)
    end = datetime(2009,12,31)
    
    first_simulation_year = start.year
    time_period_days = end-start
    
    amount_simulation_days = time_period_days.days+ 1.
    DataStart_gw= datetime(1993,03,24)
    DataEnd_gw = datetime(2012,12,21)  
    
    

    
    #create result files for pmf, weather, soilmoisture, pressurehead, water uptake, branching results
    mode = 'w+'
    if os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_pmf'+project+'.dat'):    
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_pmf'+project+'.dat')
        res_pmf = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_pmf'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,30))
    else:
        res_pmf = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_pmf'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,30))

    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_weather'+project+'.dat'):          
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_weather'+project+'.dat')      
        res_weather = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_weather'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,20))  
    else:    
        res_weather = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_weather'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,20))  
         
    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture'+project+'.dat'):     
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture'+project+'.dat')
        res_soilmoisture = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,4))
    else:
        res_soilmoisture = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,4))
    
    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture15'+project+'.dat'):
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture15_'+project+'.dat') 
        res_soilmoisture10 = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture15'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,2))
    else:
        res_soilmoisture10 = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_soilmoisture15'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,2))
        
    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_pressurehead'+project+'.dat'):
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_pressurehead'+project+'.dat')
        res_pressurehead = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_pressurehead'+project+'', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))
    else:
        res_pressurehead = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_pressurehead'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))
   
    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_wateruptake'+project+'.dat'):
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_wateruptake'+project+'.dat') 
        res_wateruptake = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_wateruptake'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))
    else:
       res_wateruptake = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_wateruptake'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))     
       
    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_branching'+project+'.dat'):
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_branching'+project+'.dat')
        res_branching = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_branching'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))
    else:
        res_branching = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_branching'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))

    if  os.path.exists(r'D:\Daten\Documents\Code\pmf\scripts\results_kr'+project+'.dat'):
        os.remove(r'D:\Daten\Documents\Code\pmf\scripts\results_kr'+project+'.dat')
        res_kr = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_kr'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))
    else:
        res_kr = np.memmap(r'D:\Daten\Documents\Code\pmf\scripts\results_kr'+project+'.dat', dtype=('<f4'), mode=mode, shape=(5,amount_simulation_days,layercount,2))
       

    # load the file with calculated parametersets   
#    parametersets = np.load("parametersets_soil1.npy")
    parametersets = [(1.,0.6,0.28,1.18)] #(1.,0.6,0.28,1.18),(0.1944,0.09,0.04,1.2)
    #(Ksat, porosity, alpha, n)
    #    Ksat = saturated conductivity [m d-1]        
    #    porosity = pore volume per soil volume [m³ m-³]
    #    alpha = inverse of the air entry potential [cm-1]
    #    n = shape parameter of retention curve [-]
    
    
###### Simulation  ##########################################################################################  
    
    #log-Datei
    log_errors = ""    
    
    error = False    
    
    
    #for every parameterset
    error_count = 0
    i = 0 
    count = len(parametersets)
    while i < count:
        print "parameter set",i+1,count,error_count
        
        if error_count <=2:
                
            i_parameterset = i
            params = [i]
            
    #        print 'new parameterset', i_parameterset, params
            Ksat_1= 1.2744
            porosity_1= 0.66409
            alpha_1= 0.20448
            n_1= 1.127
            
            Ksat_2 = 0.2207
            porosity_2= 0.54962
            alpha_2= 0.73246
            n_2= 1.07365
            
            Ksat_3 =0.0738
            porosity_3= 0.44863
            alpha_3= 0.00401
            n_3= 1.12969


            
         #create a cmf cell and load the meteorological data  and groundwater data
            loader = load_data(start,DataStart_gw,DataEnd_gw)   #groundwater data
            cmf_cell = cmf1d(DataStart_gw,DataEnd_gw,loader,Datenstart,Ksat_1,Ksat_2,Ksat_3,porosity_1,porosity_2,porosity_3,alpha_1,alpha_2,alpha_3,
                             n_1,n_2,n_3,layercount)  #,layerthickness
            cmf_cell.t = start
            cmf_cell.load_meteo(Datenstart,start,fpath)  
              
            
         #use the interface to get soil and atmosphere data  
            soil        = cmf_fp_interface(Datenstart,cmf_cell,fpath)   
            atmosphere  = cmf_fp_interface(Datenstart,cmf_cell,fpath) 
         
         
            step =datetime(2000,1,29) - datetime(2000,1,28)
            print "Run ... "  
            time = start
            day_of_simulation=0.
         
    
         #create a plant (a c3 grass)
            'create new plant'
            plant = PMF.connect(PMF.PlantBuildingSet.createPlant_c3grass_CMF(),soil,atmosphere)          
            plant.nitrogen.Km = 27 * 62e-6
            plant.nitrogen.NO3min = 0.1e-3   
    
            print ''
            print ''
            print '#######################################'
    
    
    ##  #CMF1d groundwater  
            piezometer          = 'P7'    
            gw_array            = loader.groundwater(piezometer)
            gw = cmf_cell.project.NewOutlet('groundwater',x=0,y=0,z=-1.1)
            gw.potential = -.5 #IMPORTANT 
            gw.is_source=True
            gw_flux=cmf.Richards(cmf_cell.cell.layers[-1],gw)
            
            FACEring     = 'A1'
            soimoi_array = loader.soil_moisture(FACEring)
    
           
            ####
            try:        

                while time <= end: 
                    '''groundwater data'''
                    rundays=(DataEnd_gw-DataStart_gw).days            
                    cmf.Richards(cmf_cell.cell.layers[-1],gw)
                    if gw_array['Date'].__contains__(time)==True:
                        Gw_Index=np.where(gw_array['Date']==time)               
                        gw.potential=gw_array[piezometer][Gw_Index] 
                    groundwaterlevel = gw.potential
                    
                    '''run the model'''    
                    run_model = run(groundwaterlevel,porosity_1,porosity_2,porosity_3,res_weather,res_pmf,res_soilmoisture,
                                    res_soilmoisture10,res_pressurehead,res_wateruptake,res_branching,
                                    i_parameterset,day_of_simulation,time,plant,tt_of_leaf_development_start,first_simulation_year)
                    if time.day == 31. and time.month == 12.:               
                        print '#####',time, '######'
        
                   
                    #Calculates evaporation for bare soil conditions
                   
                    flux = [uptake*-1. for uptake in plant.Wateruptake]
                    flux[0] -= plant.et.Evaporation_pot_SW*atmosphere.Kr()[0]*0.1
                    flux[1] -= plant.et.Evaporation_pot_SW*atmosphere.Kr()[1]*0.2
                    flux[2] -= plant.et.Evaporation_pot_SW*atmosphere.Kr()[2]*0.3
                    flux[3] -= plant.et.Evaporation_pot_SW*atmosphere.Kr()[3]*0.4
                    
                    
                    
                    cmf_cell.flux=flux
                    
                    time = time + step
                    cmf_cell.run(cmf.day)
                    day_of_simulation+=1.
                    
                   
#                    error_cmf = True                    
#                    while error_cmf:
#                        try:
#                            '''go one day further'''          
#                            cmf_cell.run(cmf.day)
#                            error_cmf = False
#                        except RuntimeError:
#                            print 'x'
#                            pass
               
#                        day_of_simulation+=1.
                    
                i+=1
            except RuntimeError:
                
                print "ERROR", time, sum(plant.Wateruptake)
                log_errors += str(time)
                error_count+=1
                break
#                pass
        else:
            error_count = 0
            i+=1
            

               
    f = open(r"D:\Daten\Documents\Code\pmf\scripts\log_errors.txt","wb")
    f.write(log_errors)
    f.close()
    del f

#######################################
### Plot results
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import datetime as dt
import matplotlib
#from datetime import datetime, date, time, timedelta
import datetime

project = project


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

     
parameterset_number=0

date1 = dt.datetime(1999,01,01)
date2 = dt.datetime(2010,01,01)
xlims = []
for result in perdelta(date1,date2,dt.timedelta(days=1)):
    xlims.append(result)
x_lims = mdates.date2num(xlims)

start = dt.datetime(1999,01,01)
end = dt.datetime(2009,12,31)
time_period_days = end-start
amount_simulation_days = time_period_days.days+ 1.
layercount = 18

firstyear =  range(0,12*365,365)
lastyear =  range(365,12*365,365)


pmf =  np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_pmf"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,30))           
weather = np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_weather"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,20))   
soilmoi = np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_soilmoisture"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,layercount,4))
wateruptake = np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_wateruptake"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,layercount,2))
branching = np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_branching"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,layercount,2))            
soilmoi10 = np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_soilmoisture15"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,2))
kr_factor = np.memmap("D:/Daten/Documents/Code/pmf/scripts/results_kr"+project+".dat", dtype=('<f4'), mode='r', shape=(5,amount_simulation_days,layercount,2))

wateruptake_daily =[]
for i in range(11*365):
    wu_daily = sum(wateruptake[parameterset_number,i,:layercount,1])
    wateruptake_daily.append(wu_daily)

f = lambda d: 0.005*(d+1)**2 - 0.005*(d+1)
depths = map(f,range(0,19))
depths_formatted = [ '%.2f' % elem for elem in depths ]

def altElement(a):
    return a[::2]

depth_ylim = altElement(depths_formatted)


measured_shoot_biomass_a1 = [543.9, 768.8, 686.5, 682.8, 556.9, 633, 657, 561, 541.1, 499.7, 559.9]


#=====================================================================================================
''' PLOTS '''

fig = plt.figure(1)

'''wateruptake'''
plt.subplot(615).set_title('wateruptake [mm]')
plt.subplot(615).set_ylabel('soil depth \n [m]')
plt.subplot(615).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),4, dtype=int)[0], 'k--', linewidth=1.3)
plt.subplot(615).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),6, dtype=int)[0], 'k--', linewidth=1.3)
y_lims = [0,18]
img413 = plt.subplot(615).imshow(np.transpose(wateruptake[parameterset_number,:,:layercount,1]),cmap=cm.Blues, aspect='auto',
          extent = [pmf[parameterset_number,:,27][0], pmf[parameterset_number,:,27][-1],  y_lims[-1], 0.])
plt.subplot(615).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(615).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(615).xaxis.set_major_formatter(date_format)
plt.subplot(615).set_yticks(np.arange(0,19,2))
plt.subplot(615).set_yticklabels([str(i) for i in depth_ylim])
plt.colorbar(img413)


'''soil moisture'''
plt.subplot(616).set_title('soil moisture [cm3 cm-3]')
plt.subplot(616).set_ylabel('soil depth \n [m]')
plt.subplot(616).set_xlabel('time')
plt.subplot(616).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),4, dtype=int)[0], 'k--', linewidth=1.3)
plt.subplot(616).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),6, dtype=int)[0], 'k--', linewidth=1.3)
plt.subplot(616).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),12, dtype=int)[0], 'w--', linewidth=0.5)            
y_lims = [0,18]
img414 =plt.subplot(616).imshow(np.transpose(soilmoi[parameterset_number,:,:layercount,3]),cmap=cm.jet_r, aspect='auto',
          extent = [pmf[parameterset_number,:,27][0], pmf[parameterset_number,:,27][-1],  y_lims[-1], y_lims[0]])
plt.subplot(616).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(616).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(616).xaxis.set_major_formatter(date_format)
plt.subplot(616).set_yticks(np.arange(0,19,2))
plt.subplot(616).set_yticklabels([str(i) for i in depth_ylim])
plt.colorbar(img414)


'''precipitation'''
plt.subplot(611).set_title('precipitation [mm]')
plt.subplot(611).set_ylabel('precipitation \n [mm]')
plt.subplot(611).plot(pmf[parameterset_number,:,27], weather[parameterset_number,:,7], 'k', label='precipitation')   #rain
plt.subplot(611).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(611).xaxis_date()
plt.subplot(611).invert_yaxis()
date_format = mdates.DateFormatter('%Y')
plt.subplot(611).xaxis.set_major_formatter(date_format)
plt.colorbar(img414)


'''shoot_biomass'''
plt.subplot(612).set_title('shoot biomass [g m-2]')
plt.subplot(612).set_ylabel('shoot biomass \n [g m-2]')
plt.subplot(612).plot(pmf[parameterset_number,:,27], pmf[parameterset_number,:,2], 'g', label='precipitation')   #shoot biomass
plt.subplot(612).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(612).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(612).xaxis.set_major_formatter(date_format)
plt.colorbar(img414)

'''branching'''
plt.subplot(613).set_title('branching [g]')
plt.subplot(613).set_ylabel('soil depth \n [m]')
y_lims = [0,18]
img512 = plt.subplot(613).imshow(np.transpose(branching[parameterset_number,:,:layercount,1]),cmap=cm.YlOrBr, aspect='auto',
          extent = [pmf[parameterset_number,:,27][0], pmf[parameterset_number,:,27][-1],  y_lims[-1], 0.])
plt.subplot(613).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(613).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(613).xaxis.set_major_formatter(date_format)
plt.subplot(613).set_yticks(np.arange(0,19,2))
plt.subplot(613).set_yticklabels([str(i) for i in depth_ylim])
plt.colorbar(img512)

'''ET_act'''
plt.subplot(614).set_title('ET_act [mm]')
plt.subplot(614).set_ylabel('ET_act \n [mm]')
plt.subplot(614).plot(pmf[parameterset_number,:,27], pmf[parameterset_number,:,23], 'b', label='evaporation')   #E_act
wateruptake_daily =[]
for i in range(len(pmf[parameterset_number,:,27])):
    wu_daily = sum(wateruptake[parameterset_number,i,:layercount,1])
    wateruptake_daily.append(wu_daily)
plt.subplot(614).plot(pmf[parameterset_number,:,27], wateruptake_daily, 'g-', linewidth =.5, label='transpiration')   #T_act
#plt.legend()
plt.subplot(614).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(614).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(614).xaxis.set_major_formatter(date_format)
plt.subplot(614).set_ylim([0,5])
plt.colorbar(img414)


fig.subplots_adjust(bottom=0.5, top=0.9, hspace=0.7)
fig.autofmt_xdate()
show()


fig = plt.figure(2)

'''precipitation'''
plt.subplot(311).set_title('precipitation [mm]')
plt.subplot(311).set_ylabel('precipitation \n [mm]')
plt.subplot(311).plot(pmf[parameterset_number,:,27], weather[parameterset_number,:,7], 'k', label='precipitation')   #rain
plt.subplot(311).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
plt.subplot(311).xaxis_date()
plt.subplot(311).invert_yaxis()
date_format = mdates.DateFormatter('%Y')
plt.subplot(311).xaxis.set_major_formatter(date_format)
plt.colorbar(img414)

'''shoot_biomass'''
plt.subplot(312).set_title('shoot biomass [g/m$^2$]')
plt.subplot(312).set_ylabel('shoot biomass \n [g/m$^2$]')
plt.subplot(312).plot(pmf[parameterset_number,:,27], pmf[parameterset_number,:,2], 'g', label='shoot biomass')   #rain
plt.subplot(312).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(312).xaxis.set_major_formatter(date_format)
plt.colorbar(img414)

'''LAI'''
plt.subplot(313).set_title('LAI [m/m$^2$]')
plt.subplot(313).set_ylabel('LAI \n [m/m$^2$]')
plt.subplot(313).plot(pmf[parameterset_number,:,27], pmf[parameterset_number,:,7], 'g', label='leaf area index')   
plt.subplot(313).xaxis_date()
date_format = mdates.DateFormatter('%Y')
plt.subplot(313).xaxis.set_major_formatter(date_format)
plt.colorbar(img414)

show()





#================================================
'''using soil depth..doesn't work'''
#================================================
#
#fig = plt.figure(2)
##
#'''wateruptake'''
#plt.subplot(413).set_title('wateruptake [mm]')
#plt.subplot(413).set_ylabel('soil depth [cm]')
#y_lims =list(soilmoi[parameterset_number,:,:layercount,2][0]) 
#plt.subplot(413).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),y_lims[3], dtype=int)[0], 'k--', linewidth=1.3)
#plt.subplot(413).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),y_lims[5], dtype=int)[0], 'k--', linewidth=1.3)
#img413 = plt.subplot(413).imshow(np.transpose(wateruptake[parameterset_number,:,:layercount,1]),cmap=cm.Blues, aspect='auto',
#          extent = [pmf[parameterset_number,:,27][0], pmf[parameterset_number,:,27][-1],  y_lims[-1], 0.])
#plt.subplot(413).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
#plt.subplot(413).xaxis_date()
#date_format = mdates.DateFormatter('%Y')
#plt.subplot(413).xaxis.set_major_formatter(date_format)
#plt.colorbar(img413)
#
#
#'''soil moisture'''
#plt.subplot(414).set_title('soil moisture [cm3 cm-3]')
#plt.subplot(414).set_ylabel('soil depth [cm]')
#y_lims =list(soilmoi[parameterset_number,:,:layercount,2][0]) 
#plt.subplot(414).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),y_lims[3], dtype=int)[0], 'k--', linewidth=1.3)
#plt.subplot(414).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),y_lims[5], dtype=int)[0], 'k--', linewidth=1.3)
#gw_levels_cm = (-100)*np.array(weather[parameterset_number,:-1,17])
#plt.subplot(414).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            gw_levels_cm, 'k-',linewidth=1.3)
#img414 = plt.subplot(414).imshow(np.transpose(soilmoi[parameterset_number,:,:layercount,1]),cmap=cm.jet_r, aspect='auto',
#          extent = [pmf[parameterset_number,:,27][0], pmf[parameterset_number,:,27][-1],  y_lims[-1], 0.])
#plt.subplot(414).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
#plt.subplot(414).xaxis_date()
#date_format = mdates.DateFormatter('%Y')
#plt.subplot(414).xaxis.set_major_formatter(date_format)
#plt.colorbar(img414)
#
#
#'''precipitation'''
#plt.subplot(411).set_title('precipitation [mm]')
#plt.subplot(411).set_ylabel('precipitation [mm]')
#plt.subplot(411).plot(pmf[parameterset_number,:,27], weather[parameterset_number,:,7], 'b')   #rain
#plt.subplot(411).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
#plt.subplot(411).xaxis_date()
#date_format = mdates.DateFormatter('%Y')
#plt.subplot(411).xaxis.set_major_formatter(date_format)
#plt.colorbar(img414)
#
#fig.subplots_adjust(bottom=0.5, top=0.9, hspace=0.7)
#fig.autofmt_xdate()
#show()


#====================================
'''soil moisture in each layer'''
#====================================

#fig = plt.figure(3)
#'''soil moisture'''
#fig = figure()
#plt.subplot(414).set_title('soil moisture [cm3 cm-3]')
#plt.subplot(414).set_ylabel('soil layer')
#plt.subplot(414).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),4, dtype=int)[0], 'k--', linewidth=1.3)
#plt.subplot(414).plot(arange(pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]),
#            np.full((1,pmf[parameterset_number,:,27][-1]-pmf[parameterset_number,:,27][0]),6, dtype=int)[0], 'k--', linewidth=1.3)
#y_lims = [0,18]
#img414 =plt.subplot(414).imshow(np.transpose(soilmoi[parameterset_number,:,:layercount,1]),cmap=cm.jet_r, aspect='auto',
#          extent = [pmf[parameterset_number,:,27][0], pmf[parameterset_number,:,27][-1],  y_lims[-1], y_lims[0]])
#plt.subplot(414).set_xlim([pmf[parameterset_number,:,27][0],pmf[parameterset_number,:,27][-1]])
#plt.subplot(414).xaxis_date()
#date_format = mdates.DateFormatter('%Y')
#plt.subplot(414).xaxis.set_major_formatter(date_format)
#plt.colorbar(img414)


'''no dates at x-axis'''
#subplot(311)
#title('plant water uptake [mm]')
#plt.yticks(np.arange(0,18,2.))
#plt.xticks(np.arange(0,11*365+1,365.))
#imshow(np.transpose(wateruptake[parameterset_number,:,:layercount,1]),cmap=cm.Blues, aspect='auto')
#xaxis_date()
#plt.plot(arange(11*365),np.full((1,11*365),4, dtype=int)[0], 'k--', linewidth=1.3)
#plt.plot(arange(11*365),np.full((1,11*365),6, dtype=int)[0], 'k--', linewidth=1.3)
#ylabel('layer number')
#colorbar()
#
#subplot(312)
#title('soil moisture [cm^3 cm^-3]')
#plt.yticks(np.arange(0,18,2.))
#plt.xticks(np.arange(0,11*365+1,365.))
#imshow(np.transpose(soilmoi[parameterset_number,:,:layercount,1]),cmap=cm.jet_r,vmin=0., vmax=.6, aspect='auto')
#plt.plot(arange(11*365),np.full((1,11*365),4, dtype=int)[0], 'k--', linewidth=1.3)
#plt.plot(arange(11*365),np.full((1,11*365),6, dtype=int)[0], 'k--', linewidth=1.3)
#ylabel('layer number')
#colorbar()
#
#subplot(313)
#title('precipitation [mm]')
#plt.yticks(np.arange(min(weather[parameterset_number,:,7]), max(weather[parameterset_number,:,7])+1,10.))
#plt.xticks(np.arange(0,11*365+1,365.))
#plt.plot(weather[parameterset_number,:,7], 'b')   #rain
#ylabel('precipitation[mm]')
#plt.axis([0,11*365,0,60])
#plt.gca().invert_yaxis()
#xlabel('time [days]')
#colorbar()
#show()
#fig.tight_layout()





#######old way to the figures

#timeline=drange(date1,date2,timedelta(1))

#ax1=subplot(411)
##plt.plot(pmf[parameterset_number,:,13], 'g-') # Trans_SW
##plt.plot(pmf[parameterset_number,:,14], 'b-') #E_SW
#plt.yticks(np.arange(0,18,2.))
#title('root biomass [g/m^2]')
##imshow(np.transpose(wateruptake[parameterset_number,:,:layercount]),cmap=cm.Blues, aspect='auto')
#imshow(np.transpose(branching[parameterset_number,:,:layercount]),cmap=cm.YlOrBr, aspect='auto')
#ylabel('layer number')
#xlabel('time [days]')
##imshow(np.transpose(soilmoi[parameterset_number,:,:10]),cmap=cm.jet_r,vmin=0.3, vmax=1, aspect='auto')
##plt.axis([0,11*365,-1,0])
##plt.title('Plant water uptake')
##plt.ylim(20,0,2)
##plt.legend(['Transpiration','Evaporation'], bbox_to_anchor=(1.05, 1), loc=2 ) #borderaxespad=0.
#colorbar()

#subplot(311)
##imshow(np.transpose(wateruptake[parameterset_number,:,:20]),cmap=cm.Blues, aspect='auto')
#plt.yticks(np.arange(0,18,2.))
#plt.xticks(np.arange(0,11*365+1,365.))
#title('soil moisture [cm^3 cm^-3]')
#imshow(np.transpose(soilmoi[parameterset_number,:,:layercount]),cmap=cm.jet_r,vmin=0., vmax=.6, aspect='auto')
#plt.plot(arange(11*365),np.full((1,11*365),4, dtype=int)[0], 'w--', linewidth=3.0)
#plt.plot(arange(11*365),np.full((1,11*365),6, dtype=int)[0], 'w--', linewidth=3.0)
#ylabel('layer number')
##xlabel('time [days]')
##plt.title('Soil moisture [m³/m³]')
#colorbar()
#.jet_r
#plt.plot(pmf[parameterset_number,:,2], 'b-')      #shoot biomass
#plt.axis([0,2*365,0,200])
#plt.plot(pmf[parameterset_number,:,1], 'r-')
#plot(atmosphere.get_CO2_A1)
#plt.plot(weather[parameterset_number,:,0], 'r-')  #net radiation
#plt.plot(weather[parameterset_number,:,1], 'b-') #tmean
#plt.plot(weather[parameterset_number,:,2], 'g-') #tmax
#plt.plot(weather[parameterset_number,:,3], 'r-') #tmin
#plt.plot(weather[parameterset_number,:,4], 'g-')
#plt.plot(weather[parameterset_number,:,5], 'b-')
#plt.plot(weather[parameterset_number,:,6], 'r-')
#plt.plot(weather[parameterset_number,:,7], 'b-') #rain
#plt.plot(weather[parameterset_number,:,8], 'g-') #wind
#plt.plot(weather[parameterset_number,:,9], 'y-')
#plt.plot(weather[parameterset_number,:,10], 'b-')
#plt.plot(weather[parameterset_number,:,11], 'r-')
#plt.plot(weather[parameterset_number,:,12], 'k-')
#plt.plot(pmf[parameterset_number,:,13], 'g-') # Trans_SW
#plt.plot(pmf[parameterset_number,:,14], 'b-') #E_SW
#plt.plot(weather[parameterset_number,:,15], 'b--') # ET_SW
#plt.axis([0,2*365,0,5])
#colorbar()
#plt.plot(pmf[parameterset_number,:,19], 'g-')

#
#subplot(312)
##imshow(np.transpose(soilmoi[parameterset_number,:,:20]),cmap=cm.jet_r,vmin=0.3, vmax=1, aspect='auto')
##plt.plot(pmf[parameterset_number,:,13], 'g-') # Trans_SW
##plt.plot(pmf[parameterset_number,:,14], 'b-') #E_SW
##plt.plot(pmf[parameterset_number,:,19], 'g-') # T_PM
##plt.plot(pmf[parameterset_number,:,20], 'b-') #E_PM
##plt.plot(pmf[parameterset_number,:,2], 'b-')      #shoot biomass
##plt.plot(pmf[parameterset_number,:,6], 'k-')      #stem height
##plt.plot(pmf[parameterset_number,:,3], 'g-')      #leaf biomass
###plt.plot(pmf[parameterset_number,:,4], 'b-')      #stem biomass
##plt.plot(pmf[parameterset_number,:,7], 'g-')      #LAI
##plt.plot(pmf[parameterset_number,:,24], 'g-')      #rue soltani
##plt.plot(weather[parameterset_number,:,1], 'r')   #mean temp
#title('precipitation [mm]')
#plt.plot(weather[parameterset_number,:,7], 'b')   #rain
#ylabel('precipitation[mm]')
##xlabel('time [days]')
##plt.plot(weather[parameterset_number,:,1], 'r-') #tmean
##plt.plot(pmf[parameterset_number,:,13], 'b-')
#plt.yticks(np.arange(min(weather[parameterset_number,:,7]), max(weather[parameterset_number,:,7])+1,10.))
#plt.xticks(np.arange(0,11*365+1,365.))
#plt.axis([0,11*365,0,60])
#plt.gca().invert_yaxis()
##show()
##plt.axis([0,2*365,0,200])
#colorbar()
#
#subplot(313)
#title('plant water uptake [mm]')
#plt.yticks(np.arange(0,18,2.))
#plt.xticks(np.arange(0,11*365+1,365.))
#imshow(np.transpose(wateruptake[parameterset_number,:,:layercount]),cmap=cm.Blues, aspect='auto')
#ylabel('layer number')
#xlabel('time [days]')
##plt.plot(pmf[parameterset_number,:,2], 'g-')      #shoot biomass
##plt.plot(pmf[parameterset_number,:,25], 'g-')      #PAR_a
##plt.plot(weather[parameterset_number,:,1], 'b-') #tmean
##plt.plot(weather[parameterset_number,:,2], 'g-') #tmax
##plt.plot(weather[parameterset_number,:,3], 'r-') #tmin
##plt.plot(weather[parameterset_number,:,5], 'r-') #ea
##plt.plot(weather[parameterset_number,:,15], 'r-') #Rs
##plt.plot(pmf[parameterset_number,:,26], 'r-') #actualGrowth
##imshow(np.transpose(soilmoi[parameterset_number,:,:20]),cmap=cm.jet_r,vmin=0.3, vmax=1, aspect='auto')
##plt.plot(pmf[parameterset_number,:,13], 'g-') # Trans_SW
##plt.plot(pmf[parameterset_number,:,14], 'b-') # Evapo_SW
##plt.plot(wateruptake[0,:,:], 'g-')
##plt.plot(pmf[0,:,23], 'b-')
##plt.yticks(np.arange(0,1300,100.))
##plt.xticks(np.arange(0,11*365+1,365.))
##plt.axis([0,11*365,0,1300])
#colorbar()
#show()

########################################
'''Data of Climate Data'''
########################################
#rad_solar   = [np.mean(weather[0,i:j,15]) for i,j in zip(firstyear,lastyear)]
#print 'rad_solar', rad_solar
#rad_net     = [np.mean(weather[0,i:j,0]) for i,j in zip(firstyear,lastyear)]
#print 'rad_net', rad_net
#tmean       = [np.mean(weather[0,i:j,1]) for i,j in zip(firstyear,lastyear)]
#print 'tmean', tmean
#tmax        = [np.mean(weather[0,i:j,2]) for i,j in zip(firstyear,lastyear)]
#print 'tmax', tmax
#tmin        = [np.mean(weather[0,i:j,3]) for i,j in zip(firstyear,lastyear)]
#print 'tmin', tmin
#es          = [np.mean(weather[0,i:j,4]) for i,j in zip(firstyear,lastyear)]
#print 'es', es
#ea          = [np.mean(weather[0,i:j,5]) for i,j in zip(firstyear,lastyear)]
#print 'ea', ea
#daylength   = [np.mean(weather[0,i:j,6]) for i,j in zip(firstyear,lastyear)]
#print 'daylength', daylength
#rain        = [np.sum(weather[0,i:j,7]) for i,j in zip(firstyear,lastyear)]
#print 'rain', rain
#wind        = [np.mean(weather[0,i:j,8]) for i,j in zip(firstyear,lastyear)]
#print 'wind', wind
#Co2_a1      = [np.mean(weather[0,i:j,9]) for i,j in zip(firstyear,lastyear)]
#print 'Co2_a1', Co2_a1
#Co2_a2      = [np.mean(weather[0,i:j,10]) for i,j in zip(firstyear,lastyear)]
#print 'Co2_a2', Co2_a2
#Co2_a3      = [np.mean(weather[0,i:j,11]) for i,j in zip(firstyear,lastyear)]
#print 'Co2_a3', Co2_a3
#Co2_e1      = [np.mean(weather[0,i:j,12]) for i,j in zip(firstyear,lastyear)]
#print 'Co2_e1', Co2_e1
#Co2_e2      = [np.mean(weather[0,i:j,13]) for i,j in zip(firstyear,lastyear)]
#print 'Co2_e2', Co2_e2
#Co2_e3      = [np.mean(weather[0,i:j,14]) for i,j in zip(firstyear,lastyear)]
#print 'Co2_e3', Co2_e3
##print 'Rn', weather[0,100:365,0]
##print 'tmean', weather[0,0:365,1]
##print 'tmax', weather[0,0:365,2]    #passt
##print 'es', weather[0,100:365,4]    #passt
##print 'ea', weather[0,100:365,5]      #passt
##print 'daylength', weather[0,0:365,6] #passt
##print 'rain', weather[0,100:365,7]  #passt
##print 'wind', weather[0,100:365,8]  #passt
##print 'Co2_a1', weather[0,100:365,9]#passt
##print 'Co2_a2', weather[0,100:365,10] #passt
##print 'Co2_a3', weather[0,100:365,11]#passt
##print 'Co2_e1', weather[0,100:365,12]#passt
##print 'Co2_e2', weather[0,100:365,13] #passt
##print 'Co2_e3', weather[0,100:365,14]#passt
##print 'Rs', weather[0,100:365,15] #passt
#
#def writedat_2(Biom, a, k, l, m, n, o, q, r, s, t, u, v, w, x, y, z):
#    with open(Biom,'w') as f:
#        for A, K, L, M, N, O, Q, R, S, T, U, V, W, X, Y, Z in zip(a, k, l, m, n, o, q, r, s, t, u, v, w, x, y, z):
#            print >> f, "%r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r" % (A, K, L, M, N, O, Q, R, S, T, U, V, W, X, Y, Z)
#
#waterbalance = 'Climate_Input.txt'
#a = rad_solar
#k = rad_net
#l = tmean
#m = tmax
#n = tmin
#o = es
#q = ea
#r = daylength
#s = rain
#t = wind
#u = Co2_a1
#v = Co2_a2
#w = Co2_a3
#x = Co2_e1
#y = Co2_e2
#z = Co2_e3
#writedat_2(waterbalance, a, k, l, m, n, o, q, r, s, t, u, v, w, x, y, z)



########################################
'''water balance '''
########################################
#rain            = [weather[0,i:j,7].sum() for i,j in zip(firstyear,lastyear)]
rain            = [np.sum(weather[0,i:j,7]) for i,j in zip(firstyear,lastyear)]
print 'rain', rain
evapo_pot       = [np.sum(pmf[0,i:j,14]) for i,j in zip(firstyear,lastyear)]
print 'evapo_pot', evapo_pot
trans_pot       = [np.sum(pmf[0,i:j,13]) for i,j in zip(firstyear,lastyear)]
print 'trans_pot', trans_pot
evapotran_pot   = [np.sum(pmf[0,i:j,15]) for i,j in zip(firstyear,lastyear)]
print 'evapotran_pot', evapotran_pot
evapo_act       = [np.sum(pmf[0,i:j,23]) for i,j in zip(firstyear,lastyear)]
print 'evapo_act', evapo_act
trans_act       = [np.sum(wateruptake[0,i:j,:,1]) for i,j in zip(firstyear,lastyear)]
print 'trans_act', trans_act

def writedat_1(Biom, q, r, s, t, u, v):
    with open(Biom,'w') as f:
        for Q, R, S, T, U, V in zip( q, r, s, t, u, v):
            print >> f, "%r %r %r %r %r %r" % (Q, R, S, T, U, V)

waterbalance = 'waterbalance'+project+'.txt'
q = rain
r = evapo_pot
s = trans_pot
t = evapotran_pot
u = evapo_act
v = trans_act
writedat_1(waterbalance,q,r,s,t,u,v)




###########################################
'''soil moisture 0-10cm'''
###########################################
soilmoi_10       = soilmoi10[0,:,1]
print 'soilmoi_10', soilmoi_10

def writedat_7(Biom, q):
    with open(Biom,'w') as f:
        for Q in zip( q):
            print >> f, "%r " % (Q)

waterbalance = 'soilmoi_10'+project+'.txt'
q = soilmoi_10
writedat_7(waterbalance,q)



###########################################
'''shoot biomass and LAI'''
###########################################
shootbiomass    = pmf[0,:,2] 
lai             = pmf[0,:,7]

def writedat_8(Biom, q,r):
    with open(Biom,'w') as f:
        for Q,R in zip( q,r):
            print >> f, "%r %r" % (Q,R)

waterbalance = 'shoot_LAI'+project+'.txt'
q = shootbiomass     #shoot biomass
r = lai    # LAI
writedat_8(waterbalance,q,r)




########################################
'''biomass components'''
########################################
firstyear_firstpeak =  range(0,11*365,365)      #because of two harvest dates are there two maxima in biomass
lastyear_firstpeak =  range(181,11*365,365)
firstyear_secondpeak =  range(182,11*365,365)
lastyear_secondpeak =  range(365,12*365,365)

biomass_1peak     = [np.sum(pmf[0,i:j,1]) for i,j in zip(firstyear_firstpeak,lastyear_firstpeak)]
print 'biomass_1peak', biomass_1peak
biomass_2peak     = [np.sum(pmf[0,i:j,1]) for i,j in zip(firstyear_secondpeak,lastyear_secondpeak)]
print 'biomass_2peak', biomass_2peak
shoot_1peak       = [np.max(pmf[0,i:j,2]) for i,j in zip(firstyear_firstpeak,lastyear_firstpeak)]
print 'shoot_1peak', shoot_1peak
shoot_2peak       = [np.max(pmf[0,i:j,2]) for i,j in zip(firstyear_secondpeak,lastyear_secondpeak)]
print 'shoot_2peak', shoot_2peak
stem_1peak        = [np.max(pmf[0,i:j,4]) for i,j in zip(firstyear_firstpeak,lastyear_firstpeak)]
print 'stem_1peak', stem_1peak
stem_2peak        = [np.max(pmf[0,i:j,4]) for i,j in zip(firstyear_secondpeak,lastyear_secondpeak)]
print 'stem_2peak', stem_2peak
leaf_1peak        = [np.max(pmf[0,i:j,3]) for i,j in zip(firstyear_firstpeak,lastyear_firstpeak)]
print 'leaf_1peak', leaf_1peak
leaf_2peak        = [np.max(pmf[0,i:j,3]) for i,j in zip(firstyear_secondpeak,lastyear_secondpeak)]
print 'leaf_2peak', leaf_2peak
storage_org_1peak = [np.max(pmf[0,i:j,5]) for i,j in zip(firstyear_firstpeak,lastyear_firstpeak)]
print 'storage_org_1peak', storage_org_1peak
storage_org_2peak = [np.max(pmf[0,i:j,5]) for i,j in zip(firstyear_secondpeak,lastyear_secondpeak)]
print 'storage_org_2peak', storage_org_2peak
root        = [np.max(pmf[0,i:j,1]) for i,j in zip(firstyear,lastyear)]
print 'root', root

def writedat_4(Biom, o, q, r, s, t, u, v, w, x, y, z):
    with open(Biom,'w') as f:
        for O, Q, R, S, T, U, V, W, X, Y, Z in zip(o, q, r, s, t, u, v, w, x, y, z):
            print >> f, "%r %r %r %r %r %r %r %r %r %r %r" % ( O, Q, R, S, T, U, V, W, X, Y, Z)

waterbalance = 'biomass_components'+project+'.txt'
o = biomass_1peak
q = biomass_2peak
r = shoot_1peak
s = shoot_2peak
t = stem_1peak
u = stem_2peak
v = leaf_1peak
w = leaf_2peak
x = storage_org_1peak
y = storage_org_2peak
z = root
writedat_4(waterbalance, o, q, r, s, t, u, v, w, x, y, z)



####################
'''plant parameter '''
####################

#actualgrowth = [pmf[0,i:j,26].mean() for i,j in zip(firstyear,lastyear)]    #with N and H2O stress, but without senescence
#print 'Actual Growth', actualgrowth
#actualgr_sum = [pmf[0,i:j,26].sum() for i,j in zip(firstyear,lastyear)]
#print 'Actual Growth SUM', actualgr_sum
#rue_co2     = [pmf[0,i:j,24].mean() for i,j in zip(firstyear,lastyear)]
#print 'rue', rue_co2
#par_a       = [pmf[0,i:j,25].mean() for i,j in zip(firstyear,lastyear)]
#print 'PAR_a', par_a
#lai_min         = [pmf[0,i:j,7].min() for i,j in zip(firstyear,lastyear)]
#print 'lai_min', lai_min
#lai_max         = [np.max(pmf[0,i:j,7]) for i,j in zip(firstyear,lastyear)]
#print 'lai_max', lai_max
#lai_mean         = [pmf[0,i:j,7].mean() for i,j in zip(firstyear,lastyear)]
#print 'lai_mean', lai_mean
#height_min     = [pmf[0,i:j,6].min() for i,j in zip(firstyear,lastyear)]
#print 'height_min', height_min
#height_max     = [pmf[0,i:j,6].max() for i,j in zip(firstyear,lastyear)]
#print 'height_max', height_max
#height_mean     = [pmf[0,i:j,6].mean() for i,j in zip(firstyear,lastyear)]
#print 'height_mean', height_mean
#thermaltime = [pmf[0,i:j,11].sum() for i,j in zip(firstyear,lastyear)] 
#print 'thermaltime', thermaltime
#devel_stage = [pmf[0,i:j,12].sum() for i,j in zip(firstyear,lastyear)] 
#print 'devel_stage', devel_stage
#
#
#####################
#'''further parameter'''
#####################
#r_c_s_min   = [pmf[0,i:j,21].min() for i,j in zip(firstyear,lastyear)] 
#r_c_s_max   = [pmf[0,i:j,21].max() for i,j in zip(firstyear,lastyear)] 
#r_c_s_mean  = [pmf[0,i:j,21].mean() for i,j in zip(firstyear,lastyear)] 
#print 'r_c_s_min', r_c_s_min
#print 'r_c_s_max', r_c_s_max
#print 'r_c_s_mean', r_c_s_mean
#Kr_value_min= [pmf[0,i:j,22].min() for i,j in zip(firstyear,lastyear)] 
#Kr_value_max= [pmf[0,i:j,22].max() for i,j in zip(firstyear,lastyear)] 
#Kr_value_mean= [pmf[0,i:j,22].mean() for i,j in zip(firstyear,lastyear)] 
#print 'Kr_value_min', Kr_value_min
#print 'Kr_value_max', Kr_value_max
#print 'Kr_value_mean', Kr_value_mean    


#
#
##[::-1] numpy slicing
#
##np.std(r)
#
#x= [2,3,4,5]
#y= [3,4,5,6]
#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.plot(x,y)
##plt.plot(soilmoi15[parameterset_number,:])
##ax1.plot(SoiMoi_File['A1'])
#plt.tight_layout()

##ax1.colorbar()
#
#ax2 = fig.add_subplot(312)
#ax2.imshow(np.transpose(wateruptake[parameterset_number,:,:10]),cmap=cm.Blues, aspect='auto')
##ax2.colorbar()
#
#ax3 = fig.add_subplot(313)
#ax3.imshow(np.transpose(soilmoi[parameterset_number,:,:10]),cmap=cm.jet_r,vmin=0, vmax=1, aspect='auto')
##ax3.colorbar()



#subplot(312)
#plot(pmf[parameterset_number,:,16])
#colorbar()

##leaf biomass
#plot(pmf[0,:,3])
#plot(pmf[1,:,3])
#plot(pmf[2,:,3])
#plot(pmf[3,:,3])
#plot(pmf[4,:,3])
#
##storage organs biomass
#plot(pmf[0,:,5])
#plot(pmf[1,:,5])
#plot(pmf[2,:,5])
#plot(pmf[3,:,5])
#plot(pmf[4,:,5])

##pot ET SW
#plot(pmf[0,:,15])
#plot(pmf[1,:,15])
#plot(pmf[2,:,15])
#plot(pmf[3,:,15])
#plot(pmf[4,:,15])





##vegheight
#    plt.plot(res.tt, res.vegheight, 'b.')
#    plt.legend(('vegheight'),loc=2)

#rain
#    plt.plot(res.rain, 'b.', res.netrainfall, 'r.')
#    plt.legend(('rain', 'net rain'),loc=2)
#    
#    plt.plot(res.interceptedrain, 'y')
##    plt.legend(('intercepted rain'),loc=2)
#    plt.xlabel('days')
#    plt.ylabel('amount of rain not reaching the soil surface [mm d-1]')    
    
    
#evaporation
#    plt.plot(res.evaporation_SW, 'b-',res.transpiration_SW, 'b--',res.evapotranspiration_SW, 'k', res.intercep_PET0,'y-',res.intercep_ET0,'y--')
##    plt.axis([120,150,0,2])
#    plt.xlabel('days')
#    plt.ylabel('evaporation [mm d-1]')
#    plt.legend(('E_SW', 'T_SW', 'ET_SW', 'PET0', 'ET0'), loc=2)
##evaporation nur Epot and Tpot
#    plt.plot(res.evaporation_SW, 'b-',res.transpiration_SW, 'b--',res.evapotranspiration_SW, 'k')
##    plt.axis([120,150,0,2])
#    plt.xlabel('days')
#    plt.ylabel('evaporation [mm d-1]')
#    plt.legend(('E_SW', 'T_SW', 'ET_SW'), loc=2)
#    plt.plot(res.lai, 'b-',res.biomass, 'b--',res.leaf, 'k')
#    plt.plot(res.tt)
##biomass depending on thermal time
#    plt.plot(res.tt,res.leaf, 'g-',res.tt, res.stem, 'g--',res.tt, res.storage,'y',res.tt, res.shoot_biomass, 'k')
#    plt.axis([0,1660,0,10])
#    plt.xlabel('temperature sum [degree C]')
#    plt.ylabel('biomass [g m-2]')
#    plt.legend(('leaf', 'stem', 'storage', 'shoot'), loc=2)
##biomass over time
#    plt.plot(res.array[0,1:365,3])#, 'g-', res.stem, 'g--', res.storage,'y', res.shoot_biomass, 'k')
##    plt.axis([0,1660,0,10])
#    plt.xlabel('time [days]')
#    plt.ylabel('biomass [g m-2]')
#    plt.legend(('leaf', 'stem', 'storage', 'shoot'), loc=2)    
###biomass over time
#    plt.plot(res.biomass, 'g-', res.shoot_biomass, 'g--', res.root_biomass,'y')
##    plt.axis([0,1660,0,10])
#    plt.xlabel('time [days]')
#    plt.ylabel('biomass [g m-2]')
#    plt.legend(('biomass', 'shoot', 'root'), loc=2)      
#    
#    subplot(211)
##    plot(res.intercep_PET0,'k',label='PET0')
#    plot(res.intercep_ET0,'r',label='ET0')
#    ylabel('[g m-2]')
#    legend(loc=0)
##    ylim(0,1200)
#
#    subplot(212)
#    plot(res.rain, 'b', label ='Rain')
#    plot(res.netrainfall, 'y', label ='Net Rain')    
#    ylabel('Biomass [g m-2]')  
#    legend(loc=0)
#    ##legend(loc=0)
#    ##show()

#    plot(res.leaf, 'g', label ='Leaf')
#    plot(res.stem,'k', label ='Stem')    
#    plot(res.storage, 'r', label ='Storage')
#    plot(res.tt, '--', label = 'ThermalTime')

##########################################
# putting results into a text file


def writedat(ET, x, y, xprecision=4, yprecision=4):
    with open(ET,'w') as f:
        for X, Y in zip(x, y):
            print >> f, "%.*g\t%.*g" % (xprecision, X, yprecision, Y)  

def writedat_1(Biom, q, s, t, u):
    with open(Biom,'w') as f:
        for Q, S, T, U in zip( q, s, t, u):
            print >> f, "%r %r %r %r" % (Q, S, T, U)

def writedat_2(Biom, q):
    with open(Biom,'w') as f:
        for Q in zip( q):
            print >> f, "%r" % (Q)
#prior_results = 'ET_pot_Results_20150304.txt'
#q = rain
#s = Tpot
#t = Epot
#u = ETpot
#writedat_1(prior_results, q, s, t, u)

#prior_results2 = 'T_act_Results_20150303.txt'
#q = Tact
#writedat_2(prior_results2, q)


#prior_results2 = 'ET_act_Results_Rootbiom_20150303.txt'
#q = Tact
#s = Eact
#t = ETact
#u = root_biom
#writedat_1(prior_results2, q, s, t, u)
#
#
#prior_results3 = 'Biomass_Results_20150303.txt'
#q = shoot_biom
#s = stem_biom
#t = leaf_biom
#u = storage_org_biom
#writedat_1(prior_results3, q, s, t, u)

#ET_FAO = 'ET_VegH_VegH.txt'
#x = res.vegheight
#y = res.vegheight
#writedat(ET_FAO,x,y)
            
#Biomass = 'Ring1_eCO2_tot-root-shoot-leaf-evap-transpi.txt'
#print "With CO2"
#w = res.tt
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#g = res.stem
#h = res.storage
#i = res.lai
#writedat_1(Biomass,w,x,y,z,g,h,i)           

'''Test ob die meteorologischen Daten richtig eingelesen werden'''
#Meteodata = 'Meteodata.txt'
#print "Read meteorol data"
#w = res.temperature_min
#x = res.temperature_max
#y = res.e_s
#z = res.e_a
#g = res.rain
#h = res.windspeed
#i = res.daylength
#writedat_1(Meteodata,w,x,y,z,g,h,i)         
#
#CO2Data = 'CO2Data.txt'
#print "Read meteorol data"
#w = res.CO2_A1
#x = res.CO2_A2
#y = res.CO2_A3
#z = res.CO2_E1
#g = res.CO2_E2
#h = res.CO2_E3
#i = res.biomass
#writedat_1(CO2Data,w,x,y,z,g,h,i)             

def writedat(ET, x, y, xprecision=4, yprecision=4):
    with open(ET,'w') as f:
        for X, Y in zip(x, y):
            print >> f, "%.*g\t%.*g" % (xprecision, X, yprecision, Y)  
            
#ET_FAO = 'ET_VegH_VegH.txt'
#x = res.vegheight
#y = res.vegheight
#writedat(ET_FAO,x,y)
#
#Leaf_biomass = 'leaf_biomass.txt'
#x = res.tt
#y = res.leaf
#writedat(Leaf_biomass,x,y)
