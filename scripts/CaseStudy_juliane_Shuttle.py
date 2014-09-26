# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:00:12 2013

@author: kellner-j
"""

# -*- coding: utf-8 -*-
"""
Case Study II: Water balance - Single layer Storage approach
The Case Study represents a summer wheat setup of PMF and with the
SoilWaterContainer (SWC) as water balance model:

Weather     : Muencheberg,

Soil texture: Silt

Soil        : SWC,

Atmosphere  : cmf1d,      

Simulation  : 1.1.1980 - 31.12.1980 and 

Management  : Sowing - 1.3.JJJJ, Harvest - 8.1.JJJJ.


@author: Sebastian Multsch

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
import numpy as np
#import pandas as pd
#from dateutil.parser import parse
from pylab import *
from datetime import datetime, date, time, timedelta
sys.path.insert(0,'..')
import PMF
    
def run(t,res,plant,i):
                                                                                # daylength = atmosphere.get_daylength(t)   
    if t.day==1 and t.month==3:
        
        plant = PMF.connect(PMF.PlantBuildingSet.createPlant_SWC_Soltani_Shuttleworth(),soil,atmosphere)              #daylength
        plant.nitrogen.Km = 27 * 62e-6
        plant.nitrogen.NO3min = 0.1e-3
        

    if t.day==1 and t.month==8:
        plant =  None
    #Let grow
    if plant: 
        
        plant(t,'day',1.)  
    
#    #Calculates evaporation for bare soil conditions
#    if plant:
#        data[i]['Root'] =   plant.root.Wtot 
#        
#    else:
#        data[i]['Root'] = 0 
   
#    ETc_adj = sum(plant.Wateruptake)+plant.et.evaporation if plant else baresoil.evaporation
#    evaporation = plant.et.evaporation if plant else baresoil.evaporation
    ETc_adj = sum(plant.Wateruptake)+plant.et.Evaporation_pot_SW if plant else baresoil.evaporation
    evaporation = plant.et.Evaporation_pot_SW if plant else baresoil.evaporation
    rainfall = atmosphere.get_rainfall(t)
###### N E W ####### N E W ############ N E W ######################### N E W 
#    daylength = atmosphere.get_daylength(t)    
############################################################################
    Zr = plant.root.depth/100. if plant else 0.
    soil(ETc_adj,evaporation,rainfall,Zr)
    
    res.tt.append(plant.developmentstage.Thermaltime) if plant else res.tt.append(0)
###### N E W ####### N E W ############ N E W ######################### N E W ###### N E W ####### N E W ############ N E W ######################### N E W 
    res.vegheight.append(plant.shoot.stem.height) if plant else res.vegheight.append(0)
########################################################################################################################################################    
    res.rate.append(plant.developmentstage.rate) if plant else res.rate.append(0)
    
    res.water_stress.append(plant.water_stress) if plant else res.water_stress.append(0)
    res.potential_depth.append(plant.root.potential_depth) if plant else res.potential_depth.append(0)
    res.rooting_depth.append(plant.root.depth) if plant else res.rooting_depth.append(0)
    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append([0])
#    res.transpiration.append(plant.et.transpiration) if plant else res.transpiration.append(0)
#    res.evaporation.append(plant.et.evaporation) if plant else  res.evaporation.append(0)
    res.transpiration_PM.append(plant.et.Tpot_PenmanMonteith) if plant else res.transpiration_PM.append(0)
    res.evaporation_PM.append(plant.et.Epot_PenmanMonteith) if plant else  res.evaporation_PM.append(0)    
    res.transpiration_SW.append(plant.et.Transpiration_pot_SW) if plant else res.transpiration_SW.append(0)
    res.evaporation_SW.append(plant.et.Evaporation_pot_SW) if plant else  res.evaporation_SW.append(0)
    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0)
    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0)
    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0)
    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0)
#    res.ETo.append(plant.et.Reference) if plant else res.ETo.append(0)
#    res.ETc.append(plant.et.Cropspecific) if plant else res.ETc.append(0)
    res.rain.append(atmosphere.get_rainfall(t))
    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
    res.temperature.append(atmosphere.get_tmean(t))
    res.temperature_min.append(atmosphere.get_tmin(t))
    res.temperature_max.append(atmosphere.get_tmax(t)) 
##### N E W ####### N E W ############ N E W ######################### N E W 
    res.daylength.append(atmosphere.get_daylength(t))
    res.photo.append(plant.developmentstage.photo) if plant else res.photo.append(0)
    res.verna_factor.append(plant.developmentstage.verna_factor) if plant else res.verna_factor.append(0)
    res.verna_sum.append(plant.developmentstage.verna_sum) if plant else res.verna_sum.append(0)
#    res.senesced_leaf(plant.shoot.leaf.sen_mass) if plant else res.senesced_leaf.append(0)
    res.e_s.append(atmosphere.get_es(t))
    res.e_a.append(atmosphere.get_ea(t)) 
    res.Rn.append(plant.net_radiation.Rn) if plant else res.Rn.append(0)
#    res.r_b.append(plant.et.R_b) if plant else res.r_b.append(0)
#    res.r_a_a.append(plant.et.R_a_a) if plant else res.r_a_a.append(0)
#    res.r_c_a.append(plant.et.R_c_a) if plant else res.r_c_a.append(0)
#    res.r_c_s.append(plant.et.R_c_s) if plant else res.r_c_s.append(0)
#    res.r_s_a.append(plant.et.R_s_a) if plant else res.r_s_a.append(0)
#    res.r_s_s.append(plant.et.R_s_s) if plant else res.r_s_s.append(0)
############################################################################
    res.radiation.append(atmosphere.get_Rs(t))  
    res.stress.append(plant.water_stress if plant else 0.)
    res.leaf.append(plant.shoot.leaf.Wtot if plant else 0.)
    res.stem.append(plant.shoot.stem.Wtot if plant else 0.)
    res.storage.append(plant.shoot.storage_organs.Wtot if plant else 0.)
    res.Dr.append(soil.Dr)
    res.TAW.append(plant.water.TAW if plant else 0.)
    res.RAW.append(plant.water.RAW if plant else 0.)
    res.windspeed.append(atmosphere.get_windspeed(t))
   
    
    return plant

class Res(object):
    def __init__(self):
        self.rate = []
        self.tt = []
##### N E W ####### N E W ############ N E W ######################### N E W 
        self.vegheight = []
##########################################################################
        self.Wtot = []
        self.water_uptake = []
#        self.transpiration = []
#        self.evaporation = []
        self.transpiration_PM = []
        self.evaporation_PM = [] 
        self.transpiration_SW = []
        self.evaporation_SW = []
        self.biomass = []
        self.root_biomass = []
        self.shoot_biomass = []
        self.lai = []
        self.ETo = []
        self.ETc = []
        self.rain = []
        self.temperature = []
        self.temperature_min = []
        self.temperature_max = []
##### N E W ####### N E W ############ N E W ######################### N E W 
        self.photo = []
        self.daylength = []
        self.verna_factor = []
        self.verna_sum = []
        self.senesced_leaf = []
        self.e_s = []
        self.e_a = []
        self.Rn = []
        self.r_b = []
        self.r_a_a = []
        self.r_c_a = []
        self.r_c_s = []
        self.r_s_a = []
        self.r_s_s = []
###########################################################################
        self.radiation = []
        self.DAS = []
        self.leaf=[]
        self.stem=[]
        self.storage=[]
        self.Dr=[]
        self.TAW=[]
        self.RAW=[]
        self.stress=[]
        self.fc=[]
        self.wp=[]
        self.rooting_depth=[]
        self.potential_depth=[]
        self.water_stress=[]
        self.windspeed = []
        
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])

if __name__=='__main__':
    

#    data = np.empty([365],dtype=[('Root',np.single),('Shoot',np.single)])    
    
    
    
#######################################
#######################################
### Setup script   
   
       # import cmf
      #  from cmf_setup import cmf1d
        
        
        #Create cmf cell    
    #    atmosphere=cmf1d()
     #   atmosphere.load_meteo(rain_factor=1)
        
        #atmodphere = Atmoshper_Juliane()    
    
    import PMF.interface_Jul
    atmosphere = PMF.interface_Jul.Atmosphere_Ring1_eCO2()
    soil = PMF.ProcessLibrary.SWC()
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
        #set management
    sowingdate = set(datetime(i,3,1) for i in range(1992,2009))
    harvestdate = set(datetime(i,8,1) for i in range(1992,2009))
        #Simulation period
    #start = datetime(1995,04,07)
    start = datetime(1999,01,01)
        
    #end = datetime(2009,12,31)
    end = datetime(2009,12,31)
        #Simulation
    res = Res()
    plant = None
    step = datetime(2000,1,29) - datetime(2000,1,28)
    print step
    print "Run ... "  
    print "Atmosphere_Ring1_eCO2"
        #start_time = datetime.now()
    time = start
    i=0
    while time < end:
        plant = run(time,res,plant,i)
        time = time + step
        i+=1
       #print "time: %s" % time
    
#######################################
#######################################
### Show results
#    
    subplot(211)
    plot(res.vegheight,'k',label='vegheight')
    ylabel('[g m-2]')
    legend(loc=0)
#    ylim(0,1200)
#
#
#    subplot(211)
#    plot(res.root_biomass,'b',label='root_biomass')
#    ylabel('Biomass [g m-2]')
#    legend(loc=0)
#    ylim(0,1200)
#
#    subplot(211)
#    plot(res.shoot_biomass,'r',label='shoot_biomass')
#    ylabel('Biomass [g m-2]')
#    legend(loc=0)    
#    ylim(0,1200)
#
    subplot(212)
    plot(res.stem,'r',label='stembiomass')
    ylabel('Biomass [g m-2]')  #
    legend(loc=0)
#    ylim(0,1200)
#
#    subplot(212)
#    plot(res.stem,'m',label='stem')
#    ylabel('Biomass [g m-2]')    #
#    legend(loc=0)
#    ylim(0,1200)
#    
#    subplot(212)
#    plot(res.storage,'c',label='storage')
#    ylabel('Biomass [g m-2]')    #
#    legend(loc=0)
#    ylim(0,1200)
#    
#    subplot(212)
#    plot(res.leaf,'g',label='leaf')
#    ylabel('Biomass [g m-2]')    #
#    legend(loc=0)
#    ylim(0,1200)
#       
#    subplot(212)
#    plot(res.evaporation_PM,'k',label='Epot')
#    ylabel('[mm d-1]')    #
#    legend(loc=0)

###########################################
## for writing the lists as strings into the text file
#f = open('TPOT.txt', 'w')
##t = str(np.array(res.transpiration))
#e = str(zip(res.transpiration,res.evaporation,res.biomass))
#f.write(e)
#f.close()

##########################################
##########################################
# putting results into a text file

def writedat_1(Biom, w, x, y, z, g, h, i):
    with open(Biom,'w') as f:
        for W, X, Y, Z, G, H, I in zip(w, x, y, z, g, h, i):
            print >> f, "%r %r %r %r %r %r %r" % (W, X, Y, Z, G, H, I)
#            
#Biomass = 'Ring1_eCO2_tot-root-shoot-leaf-evap-transpi.txt'
#print "With CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#g = res.stem
#h = res.storage
#i = res.lai
#writedat_1(Biomass,w,x,y,z,g,h,i)           
#      
#Biomass = 'Ring1_tot-root-shoot-leaf-evap-transpi.txt'
#print "Without CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#g = res.stem
#h = res.storage
#i = res.lai
#writedat_1(Biomass,w,x,y,z,g,h,i)   
            
            
#Biomass = 'Bioma1_shoot-stem-storage-leaf-.txt'
#print "Without CO2"
#w = res.shoot_biomass
#x = res.stem
#y = res.storage
#z = res.leaf
#writedat_1(Biomass,w,x,y,z)        


#Biomass = 'Bioma_A2E2-2_tot-root-shoot-leaf-.txt'
#print "Without CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#writedat_1(Biomass,w,x,y,z) 
#
#Biomass = 'Bioma_A3E3-2_tot-root-shoot-leaf-.txt'
#print "Without CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#writedat_1(Biomass,w,x,y,z) 
#
#Biomass = 'Bioma_A1E1_tot-root-shoot-leaf-.txt'
#print "With CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#writedat_1(Biomass,w,x,y,z) 
#
#Biomass = 'Bioma_A2E2_tot-root-shoot-leaf-.txt'
#print "With CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#writedat_1(Biomass,w,x,y,z) 
#
#Biomass = 'Bioma_A3E3-3_tot-root-shoot-leaf-.txt'
#print "With CO2"
#w = res.biomass
#x = res.root_biomass
#y = res.shoot_biomass
#z = res.leaf
#writedat_1(Biomass,w,x,y,z) 








#ET_FAO = 'Biomass_mitCO2_total-leaf.txt'
#x = res.biomass
#y = res.leaf
#writedat(ET_FAO,x,y)
#
#ET_FAO = 'Biomass_mitCO2_shoot-root.txt'
#x = res.shoot_biomass
#y = res.root_biomass
#writedat(ET_FAO,x,y)

#
##
def writedat(ET, x, y, xprecision=4, yprecision=4):
    with open(ET,'w') as f:
        for X, Y in zip(x, y):
            print >> f, "%.*g\t%.*g" % (xprecision, X, yprecision, Y)  
            
#ET_FAO = 'ET_temp_rb.txt'
#x = res.temperature
#y = res.r_b
#writedat(ET_FAO,x,y)
#
#ET_FAO = 'ET_rcs_lai.txt'
#x = res.r_c_s
#y = res.lai
#writedat(ET_FAO,x,y)
#
#ET_FAO = 'ET_raa_rsa.txt'
#x = res.r_a_a
#y = res.r_s_a
#writedat(ET_FAO,x,y)
#
ET_FAO = 'ET_VegH_VegH.txt'
x = res.vegheight
y = res.vegheight
writedat(ET_FAO,x,y)
#
#ET_FAO = 'ET_rss_Rn.txt'
#x = res.r_s_s
#y = res.Rn
#writedat(ET_FAO,x,y)
#
#ET_FAO = 'ET_es_ea.txt'
#x = res.e_s
#y = res.e_a
#writedat(ET_FAO,x,y)

#ET_FAO = 'ET_TrPM_EvPM.txt'
#x = res.transpiration_PM
#y = res.evaporation_PM
#writedat(ET_FAO,x,y)

#ET_FAO = 'ET_TrSW_EvSW-TEST.txt'
#x = res.transpiration_SW
#y = res.evaporation_SW
#writedat(ET_FAO,x,y)

## txt file with evaporation and transpiration according to ET_FAO  [mm d-1]
#ET_FAO = 'ET_FAO.txt'
#x = res.transpiration
#y = res.evaporation
#writedat(ET_FAO,x,y)

## txt file with evaporation and transpiration similar to PenmanMonteith according to Shuttleworth-Wallace [MJ m-2 d-1]
#ET_SW_PM = 'ET_SW_PM.txt'
#x = res.transpiration_PM
#y = res.evaporation_PM
#writedat(ET_SW_PM,x,y)
## txt file with evaporation and transpiration similar to PenmanMonteith according to Shuttleworth-Wallace [MJ m-2 d-1]
#ET_SW_PM = 'ET_SW_PM_fullcover2.txt'
#x = res.transpiration_PM
#y = res.evaporation_PM
#writedat(ET_SW_PM,x,y)
# txt file with evaporation and transpiration similar to PenmanMonteith according to Shuttleworth-Wallace [MJ m-2 d-1]
#ET_SW_PM = 'ET_SW_PM_baresoil2.txt'
#x = res.transpiration_PM
#y = res.evaporation_PM
#writedat(ET_SW_PM,x,y)

## txt file with evaporation and transpiration according to Shuttleworth Wallace [mm d-1]
#ET_SW = 'ET_SW.txt'
#x = res.transpiration_SW
#y = res.evaporation_SW
#writedat(ET_SW,x,y)    
#    
#
#print res.r_b
#print res.r_a_a
##print res.r_c_a
#print res.r_c_s
#print res.r_s_a
#print res.r_s_s
##print res.transpiration
#print res.evaporation
#print 'LAI'
#print res.lai
#print res.e_a
#print res.e_s

#wenn ich einen Wert aus der Liste (hier Rn) ausgeben will
#sol = atmosphere.get_Rn(datetime(1998,05,05),0.05)    
#print sol


##    printbegin = datetime(1999,01,01)
##    printend = datetime(2002,12,31)
#    printbegin = 356.*2.
#    printend = 356.*3.
# #   timeline=drange(start,end,timedelta(1))
##    subplot(611)
##    plot(res.rate,'k',label='degree_days rate')
##    ylabel('[degree days]')
##    legend(loc=0)
##    ylim(0,25)
##    
##    subplot(612)
##    plot(res.tt,'k',label='degree_days sum')
##    ylabel('[degree days]')
##    legend(loc=0)
##    ylim(0,1600)
#
#    
#    subplot(511)
#    plot(res.shoot_biomass,'k',label='Wtot')
#    ylabel('Shoot Biomass [g/m^2]')
#    legend(loc=0)
#    xlim(printbegin, printend)
##    ylim(0,10)
#
#    subplot(512)
#    plot(res.lai,'k',label='LAI')
#    ylabel('[m^2/m^2]')
#    legend(loc=0)
#    xlim(printbegin, printend)
#    ylim(0,5)
#    
#    
#    subplot(514)
#    plot(res.transpiration,'k',label='Transpiration')
#    ylabel('[mm]')
#    legend(loc=0)
#    xlim(printbegin, printend)
#    ylim(0,10)    
#    
#    subplot(515)
#    plot(res.evaporation,'k',label='Evaporation')
#    ylabel('[mm]')
#    legend(loc=0)
#    xlim(printbegin, printend)
#    ylim(0,10)    
#    
#    
##    subplot(513)
##    plot(res.verna_factor,'k',label='Vernalization factor')
##    ylabel('[-]')
##    legend(loc=0)
##    ylim(0,1.02)    
##    tt_sum = np.array(res.tt)
##    tt_rate = np.array(res.rate)
##    max_tt = 1665.
###    

#
#    
##    subplot(615)
##    plot(res.photo,'k',label='Photoperiod factor')
##    ylabel('[-]')
##    legend(loc=0)
##    ylim(0,1.02)
##    
#
#
#
##    death_leaf_biomass = death_rate * np.array(res.leaf)
##    leaf_corr = np.array(res.leaf) - death_leaf_biomass     
#    
##    subplot(715)
##    plot(np.array(res.leaf)/40.,'k',label='Leaf corr')
##    ylabel('tt rate')
##    legend(loc=0)
##    ylim(0,2)
##    
##    subplot(716)
##    plot(res.biomass,'k',label='Biomass')
##    ylabel('tt rate')
##    legend(loc=0)
##    ylim(0,650)
##
##    subplot(717)
##    plot(res.shoot_biomass,'k',label='ShootBiomass')
##    ylabel('tt rate')
##    legend(loc=0)
##    ylim(0,650)
#
#    
#
#
#
#
#
##
###plot_date(timeline,res.transpiration,'g',label='Transpiration')
###plot_date(timeline,res.evaporation,'b',label='Evaporation')
##plot_date(timeline,res.rate,'k',label='degree_days')
###plot_date(timeline,res.RAW,'k',label='Readily available Water')
###plot_date(timeline,res.Dr,'r--',label='Depletion')
##ylabel('Evapotranspiration')
##xlim(printbegin, printend)
##legend(loc=0)
###ylabel('Water balance [mm]')   
##subplot(312)
##plot_date(timeline,res.shoot_biomass,'r',label='Shoot Biomass')
###plot_date(timeline,res.temperature,'r',label='Temperature')
###plot_date(timeline,res.temperature_min,'b',label='min_Temperature')
###plot_date(timeline,res.temperature_max,'g',label='max_Temperature')
###plot_date(timeline,res.water_stress,'b',label='Drought stress')
###plot_date(timeline,res.water_stress,'b',label='Drought stress')
##ylabel('Shoot Biomass [g]')
###ylabel('Temperature [°C]')
##xlim(printbegin, printend)
###ylabel('Stress index [-]')
###ylim(0,1)
##legend(loc=0)
##subplot(313)
##plot_date(timeline, res.rain, 'b', label = 'rain')
##ylabel('Rain [mm]')
###plot_date(timeline, res.windspeed, 'b', label = 'windspeed')
###plot_date(timeline,[-r for r in res.rooting_depth],'g',label='Actual')
###plot_date(timeline,[-r for r in res.potential_depth],'k--',label='Potential')
##xlim(printbegin, printend)
###ylabel('Rooting depth [mm]')
###ylabel('Windspeed [mm/s]')
##legend(loc=0)
##show()
