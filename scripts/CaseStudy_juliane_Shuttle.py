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

from pylab import *
from datetime import datetime, date, time, timedelta
sys.path.insert(0,'..')
import PMF

def run(t,res,plant,i):
                                                                                
    if t.day==1 and t.month==3:
        
        plant = PMF.connect(PMF.PlantBuildingSet.createPlant_c4grass(),soil,atmosphere)              #
        plant.nitrogen.Km = 27 * 62e-6
        plant.nitrogen.NO3min = 0.1e-3
        

    if t.day==1 and t.month==8:
        plant =  None
    #Let grow
    if plant: 
        
        plant(t,'day',1.)  



    ETc_adj = sum(plant.Wateruptake)+plant.et.Evaporation_pot_SW if plant else baresoil.evaporation
    evaporation = plant.et.Evaporation_pot_SW if plant else baresoil.evaporation
    rainfall = atmosphere.get_rainfall(t)

    Zr = plant.root.depth/100. if plant else 0.
    soil(ETc_adj,evaporation,rainfall,Zr)
    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
    
    
    #atmosphere
    res.temperature.append(atmosphere.get_tmean(t))
    res.temperature_min.append(atmosphere.get_tmin(t))
    res.temperature_max.append(atmosphere.get_tmax(t)) 
    res.e_s.append(atmosphere.get_es(t))
    res.e_a.append(atmosphere.get_ea(t)) 
    res.rain.append(atmosphere.get_rainfall(t))
    res.radiation.append(atmosphere.get_Rs(t))  
    res.windspeed.append(atmosphere.get_windspeed(t))
    res.daylength.append(atmosphere.get_daylength(t))    
    res.Rn.append(plant.net_radiation.Rn) if plant else res.Rn.append(0)
    
    
    #plant parameter
    res.vegheight.append(plant.shoot.stem.height) if plant else res.vegheight.append(0)
    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0)
    res.rooting_depth.append(plant.root.depth) if plant else res.rooting_depth.append(0) 
    res.potential_depth.append(plant.root.potential_depth) if plant else res.potential_depth.append(0)
            #development
    res.photo.append(plant.developmentstage.photo) if plant else res.photo.append(0)
    res.verna_factor.append(plant.developmentstage.verna_factor) if plant else res.verna_factor.append(0)
    res.verna_sum.append(plant.developmentstage.verna_sum) if plant else res.verna_sum.append(0)    
    res.tt.append(plant.developmentstage.Thermaltime) if plant else res.tt.append(0)
    res.rate.append(plant.developmentstage.rate) if plant else res.rate.append(0)
            #biomass
    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0)
    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0)
    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0)
    res.leaf.append(plant.shoot.leaf.Wtot if plant else 0.)
    res.stem.append(plant.shoot.stem.Wtot if plant else 0.)
    res.storage.append(plant.shoot.storage_organs.Wtot if plant else 0.)
    
    
    #water and soil
    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append([0])
    res.TAW.append(plant.water.TAW if plant else 0.)
    res.RAW.append(plant.water.RAW if plant else 0.)   
    res.stress.append(plant.water_stress if plant else 0.)
    res.water_stress.append(plant.water_stress) if plant else res.water_stress.append(0)
    res.Dr.append(soil.Dr)

    
    #evapotranspiration
    res.transpiration_PM.append(plant.et.Tpot_PenmanMonteith) if plant else res.transpiration_PM.append(0)
    res.evaporation_PM.append(plant.et.Epot_PenmanMonteith) if plant else  res.evaporation_PM.append(0)    
    res.transpiration_SW.append(plant.et.Transpiration_pot_SW) if plant else res.transpiration_SW.append(0)
    res.evaporation_SW.append(plant.et.Evaporation_pot_SW) if plant else  res.evaporation_SW.append(0)
    
    return plant

class Res(object):
    def __init__(self):
        self.DAS = []
        
        self.temperature = []
        self.temperature_min = []
        self.temperature_max = []        
        self.e_s = []
        self.e_a = []  
        self.rain = []
        self.radiation = []
        self.windspeed = []
        self.daylength = []
        self.Rn = []  
        
        self.vegheight = []
        self.lai = []     
        self.rooting_depth=[]
        self.potential_depth=[]        
        self.photo = []
        self.verna_factor = []
        self.verna_sum = []   
        self.tt = []        
        self.rate = []
        self.biomass = []
        self.root_biomass = []
        self.shoot_biomass = []
        self.leaf=[]
        self.stem=[]
        self.storage=[]       
        self.Wtot = []
        
        self.water_uptake = []
        self.TAW=[]
        self.RAW=[]
        self.stress=[]
        self.water_stress=[]
        self.Dr=[]
       
        self.transpiration_PM = []
        self.evaporation_PM = [] 
        self.transpiration_SW = []
        self.evaporation_SW = []

        
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])

if __name__=='__main__':
     

#######################################
### Setup script   

    import PMF.interface_Jul
    atmosphere = PMF.interface_Jul.Atmosphere_Ring1_eCO2()
    soil = PMF.ProcessLibrary.SWC()
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
        #set management
    sowingdate = set(datetime(i,3,1) for i in range(1999,2009))
    harvestdate = set(datetime(i,8,1) for i in range(1999,2009))
        #Simulation period
    start = datetime(1999,01,01)
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

#######################################
### Plot results
#    
    subplot(211)
    plot(res.vegheight,'k',label='vegheight')
    ylabel('[g m-2]')
    legend(loc=0)
#    ylim(0,1200)

    subplot(212)
    plot(res.stem,'r',label='stembiomass')
    ylabel('Biomass [g m-2]')  #
    legend(loc=0)
    ##legend(loc=0)
    ##show()

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

def writedat(ET, x, y, xprecision=4, yprecision=4):
    with open(ET,'w') as f:
        for X, Y in zip(x, y):
            print >> f, "%.*g\t%.*g" % (xprecision, X, yprecision, Y)  
            

#ET_FAO = 'ET_VegH_VegH.txt'
#x = res.vegheight
#y = res.vegheight
#writedat(ET_FAO,x,y)

