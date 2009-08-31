import CG_setup as cg
from datetime import *
import env
from pylab import *


# Inferface from FlowerPower for soil interaction
class Soil:
    """call siganture:
    
        Soil(cmf1d)
        
    Soil implements the interface for the interactions between
    cmf1d and the crop growth model.
    
    Cmf1d must be implementated from the corresponding class.
    """
    def __init__(self,cmf1d):
        self.cmf1d=cmf1d
    def get_pressurehead(self,depth):
        """ Depth in cm; Returns the capillary suction in cm for a given depth."""
        layer=self.cmf1d.layer(depth/100)
        if self.cmf1d.matrix_potential[layer]*100>0:
            return 0
        else: return -self.cmf1d.matrix_potential[layer]*100 
    def get_porosity(self,depth):
        """ Depth in cm; Returns the porosity in m3/m3 of the soil in the given depth."""
        layer=self.cmf1d.layer(depth/100)
        return self.cmf1d.get_porosity(layer)
    def get_nutrients(self,depth):
        """ Depth in cm; Returns 0.5"""
        return 0.5
    def get_bulkdensity(self,depth):
        """ Depth in cm; Returns 1.5"""
        return 1.5

# Inferface from FlowerPower for atmosphere interaction
class Atmosphere:
    """call siganture:
    
        Atmosphere(cmf1d)
        
    Atmosphere implements the interface for the interactions between
    cmf1d and the crop growth model.
    
    Cmf1d must be implementated from the corresponding class.
    """
    def __init__(self,cmf1d):
        self.cmf1d=cmf1d
    def get_tmin(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal Temperature at time """
        return self.cmf1d.cell.get_weather(time).Tmin
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal Temperature at time """
        return self.cmf1d.cell.get_weather(time).Tmax
    def get_etp(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns 5.0 """
        return 5.

#Methods for plant water extraction from soil

class Water_extraction():
    """ Water_extraction must be implemented with cmf1d instance and
        functioning as interface for the water flux from the soil
        into plant. 
        
        At first depth profile from FlowerPower must be converted into
        cmf1d soil layer; in the second step the water flux is calclulated
        from the root water uptake for each layer.
    """
    def __init__(self,cmf1d):
        self.cmf1d=cmf1d
    def waterloss_flux(self,rooted_layer,water_uptake):
        """ Water_uptake must be taken from plant.s_h; rooted layer
            must be calculated with the corresponding function.
            Returns a list with fluxes for each root penetrated layer
            in mm/day.
        """
        try:
            return [water_uptake[rooted_layer.index(l)] for l in rooted_layer]
        except IndexError:
            return []
    def rooted_layer(self,rooting_depth,depth_step=10.):
        """ Depth_step in cm, must be equal to plant.uptake depth_step
            Returns a list with the penetrated root zone from cmf1d in
            therms of cmf1d layer concept.        
        """
        return [self.cmf1d.layer(depth) for depth in arange(0.,rooting_depth/100.,depth_step/100.)]                
                
""" call
#import cmf
cd d:\pyxy\src\env
import cmf
import cmf_example as example
from datetime import *

#import cg_plant and cg_interface
cd d:\pyxy\src
import CG_setup as cg #import flowerpower
import CG_interface as interface #import atmosphere interface flowerpower_cmf_weather

#Model time amd lsit for results
thermaltime=[];biomass=[];stress=[]
wetness=[];matrix_potential=[];flux=[]
time_act=datetime(2000,1,1)
time_end=datetime(2000,12,31)
time_step=timedelta(1)

#Implement interfaces
soil=interface.Soil(example.c)
atmosphere=interface.Atmosphere(example.c)
water=interface.Water_extraction(example.c)

while time_act<time_end:
    #PLANT
    cg.grow(time_act,timedelta(1),soil,atmosphere)
    thermaltime.append(cg.plant.thermaltime);biomass.append(cg.plant.Wtot)
    stress.append(cg.plant.stress)
    
    #CMF
    example.c.flux=water.waterloss_flux(water.rooted_layer(cg.plant.root.depth),cg.plant.s_h)
    example.c.run(cmf.day)
    wetness.append(example.c.wetness);matrix_potential.append(example.c.matrix_potential);flux.append(example.c.flux)
    
    #TIME
    time_act+=time_step

hold=0
fig=figure()
fig.add_subplot(621)
plot(thermaltime,label='thermaltime')
legend(loc=0)
xlabel('Time in days')
ylabel('GDD in C')
fig.add_subplot(622)
plot(biomass,label='biomass')
legend(loc=0)
xlabel('Time in days')
ylabel('biomass in g')
fig.add_subplot(623)
plot(stress,label='stress')
ylim(0,1)
legend(loc=0)
xlabel('Time in days')
ylabel('fraction')
fig.add_subplot(624)
imshow(transpose(wetness),cmap=cm.RdYlBu)
xlabel('Time in days')
ylabel('Depth in m')
fig.add_subplot(625)
imshow(transpose(matrix_potential),cmap=cm.RdYlBu)
xlabel('Time in days')
ylabel('Depth in m')
fig.add_subplot(626)
imshow(transpose(flux),cmap=cm.RdYlBu)
xlabel('Time in days')
ylabel('Depth in m')

    
    
"""
