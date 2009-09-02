from datetime import *
from pylab import *
from CG_plant import *
from cmf import *


from cmf_setup import cmf1d
import cmf
# Create a soil column
c=cmf1d(sand=60,silt=30,clay=10,c_org=2.0,layercount=50,layerthickness=0.1)

#Load meteo data
import cmf.cmfDWD as dwd
# Load meteoroligical stations
MeteoStations=dwd.GetMeteorology(c.project,'dwddaten/kl_bestand_abgabe440_1','dwddaten/kl_satz_abgabe440_1','dwddaten/kl_dat_abgabe440_1',cmf.Time(1,1,1980),cmf.Time(1,1,2006))
# Load rainfall stations
rainfall=dwd.get_rainfall('dwddaten/rr_dat_abgabe440')

# Set Giessen as actual meteo station
c.cell.meteorology=cmf.MeteoStationReference( MeteoStations['02609'],c.cell)
# Set Giessen as rainfall station
c.cell.rain.flux=rainfall['76148']

# Set intial conditions
c.cell.saturated_depth=2.5


#Import flower power

#Parameter for development:
stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
               ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]]

#Parameter for partitioning:
root_fraction=[[160.,1.],[901.,0.5],[1665.,0.]]
shoot_fraction=[[160.,0.],[901.,0.5,],[1665.,1.,]]
leaf_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
stem_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
storage_fraction=[[160.,0.],[901.,0.0],[1174.,0.25],[1665.,1.]]

#Create plant with default values
plant=Plant(stage,root_fraction,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction)

# Inferface flowerpower - cmf
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
    def get_soilprofile(self):
        """ Returns a list with the lower limits of the
            layers in the soilprofile in cm.
        """
        return [l.boundary[1]*100 for l in self.cmf1d.cell.layers]

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
        return 20.

                
""" call
#Import cmf,flowerpower,cmf1d and interface
cd d:\pyxy\src
from cg_interface import *
from datetime import *
from pylab import *

#Model time and list for results
thermaltime=[];biomass=[];stress=[]
wetness=[];matrix_potential=[];flux=[]
time_act=datetime(2000,1,1)
time_end=datetime(2000,12,31)
time_step=timedelta(1)

#Initialise interfaces
soil=Soil(c)
atmosphere=Atmosphere(c)

while time_act<time_end:
    #FlowerPower run
    plant(time_act,timedelta(1),soil,atmosphere)
    #Water flux from cmf to FlowerPower
    #CMF run
    c.run(cmf.day)
    #Time step
    time_act+=time_step
    #Results
    thermaltime.append(plant.thermaltime);biomass.append(plant.Wtot);stress.append(plant.stress)
    wetness.append(c.wetness);matrix_potential.append(c.matrix_potential);flux.append(c.flux)
    time_act, plant.s_h
    
hold=0
fig=figure()
fig.add_subplot(621)
plot(thermaltime,label='thermaltime')
legend(loc=0)
ylabel('GDD')

fig.add_subplot(622)
plot(biomass,label='biomass')
legend(loc=0)
ylabel('biomass in g')

fig.add_subplot(623)
plot(stress,label='stress')
ylim(0,1)
legend(loc=0)
ylabel('fraction')

fig.add_subplot(624)
imshow(transpose(wetness),cmap=cm.RdYlBu)
ylabel('wetness')

fig.add_subplot(625)
imshow(transpose(matrix_potential),cmap=cm.RdYlBu)
xlabel('Time in days')
ylabel('matrix_potential')

fig.add_subplot(626)
imshow(transpose(flux),cmap=cm.RdYlBu)
xlabel('Time in days')
ylabel('flux')   
"""
