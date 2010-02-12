# -*- coding: utf-8 -*-
"""
Case Study I: Water balance - Single layer Storage approach
The Case Study represents a summer wheat setup of PMF and with the
SoilWaterContainer (SWC) as water balance model:

Weather     : Giessen,

Soil texture: Silt

Soil        : SWC,

Atmosphere  : cmf1d,      

Simulation  : 1.1.1980 - 31.12.1980 and 

Management  : Sowing - 1.3.JJJJ, Harvest - 8.1.JJJJ.


@author: Sebastian Multsch

@version: 0.1 (01.02.2010)

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

def run(t,res,plant):
    if t.day==1 and t.month==3:
        plant = PMF.connect(PMF.createPlant_SWC(),soil,atmosphere)
        plant.nitrogen.Km = 27 * 62e-6
        plant.nitrogen.NO3min = 0.1e-3

    if t.day==1 and t.month==8:
        plant =  None
    #Let grow
    if plant: 
        plant(t,'day',1.)
     
    
    #Calculates evaporation for bare soil conditions
   
    ETc_adj = sum(plant.Wateruptake)+plant.et.evaporation if plant else baresoil.evaporation
    evaporation = plant.et.evaporation if plant else baresoil.evaporation
    rainfall = atmosphere.cell.rain(t)
    Zr = plant.root.depth/100. if plant else 0.
    soil(ETc_adj,evaporation,rainfall,Zr)
    
    res.water_stress.append(plant.water_stress) if plant else res.water_stress.append(0)
    res.potential_depth.append(plant.root.potential_depth) if plant else res.potential_depth.append(0)
    res.rooting_depth.append(plant.root.depth) if plant else res.rooting_depth.append(0)
    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append([0])
    res.transpiration.append(plant.et.transpiration) if plant else res.transpiration.append(0)
    res.evaporation.append(plant.et.evaporation) if plant else  res.evaporation.append(0)
    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0)
    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0)
    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0)
    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0)
    res.ETo.append(plant.et.Reference) if plant else res.ETo.append(0)
    res.ETc.append(plant.et.Cropspecific) if plant else res.ETc.append(0)
    res.rain.append(atmosphere.cell.rain(t))
    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
    res.temperature.append(atmosphere.get_tmean(t))
    res.radiation.append(atmosphere.get_Rs(t))
    res.stress.append(plant.water_stress if plant else 0.)
    res.leaf.append(plant.shoot.leaf.Wtot if plant else 0.)
    res.stem.append(plant.shoot.stem.Wtot if plant else 0.)
    res.storage.append(plant.shoot.storage_organs.Wtot if plant else 0.)
    res.Dr.append(soil.Dr)
    res.TAW.append(plant.water.TAW if plant else 0.)
    res.RAW.append(plant.water.RAW if plant else 0.)
    atmosphere.run(cmf.day) 
    return plant

class Res(object):
    def __init__(self):
        self.water_uptake = []
        self.transpiration = []
        self.evaporation = []
        self.biomass = []
        self.root_biomass = []
        self.shoot_biomass = []
        self.lai = []
        self.ETo = []
        self.ETc = []
        self.rain = []
        self.temperature = []
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
        
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])
if __name__=='__main__':
#######################################
#######################################
### Setup script   
    import os ####### MOVIE !!!
    from pylab import *
    from datetime import *
    import PMF
    import cmf
    from cmf_setup import cmf1d
    
    class Movie: ####### MOVIE !!!
        def __init__(self,figure):
            """
            Creates a figure wtih one subplot
            """
            ion()
            self.files = []
            self.fig =  figure
            self.ax1 = self.fig.add_subplot(211)
            self.ax2 = self.fig.add_subplot(212)
            
            
        def __call__(self,data,i):
            self.ax1.cla()
            ylim(0,20)
            self.ax1.plot(data[0],label='Precipitation')
            
            legend(loc=1)
            
            self.ax2.cla()
            self.ax2.plot(data[1],'r--',label='Dr')
            self.ax2.plot(data[2],'k',label='RAW')
            ylim(0,150)
            legend(loc=1)
            
            
            
            fname = '_%03d.png'%i
            print 'Saving frame', fname
            self.fig.savefig(fname)
            self.files.append(fname)
        def makeMovie(self,fps=5,name='Movie'):
            """
            Makes a .mpg movie with the .png - files in the same folder.
            The mencoder.exe must be included to the file-folder.
            """
            import os
            os.system("mencoder mf://*.png -mf type=png:fps="+str(fps)+" -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o "+name+".mpg")
    
    
    #Create cmf cell    
    atmosphere=cmf1d()
    atmosphere.load_meteo(rain_factor=1)
    
    soil = PMF.ProcessLibrary.SWC()
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    #set management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1980,3,1)
    end = datetime(1980,8,31)
   
    #Simulation
    res = Res()
    plant = None
    print "Run ... "    
    start_time = datetime.now()
    atmosphere.t = start
    i=0 ####### MOVIE !!!
    
    rain=zeros(185)####### MOVIE !!!
    dr=zeros(185)####### MOVIE !!!
    raw=zeros(185)
    movie = Movie(figure()) ####### MOVIE !!!
    
    
    while atmosphere.t<end:
        rain[i]+=atmosphere.cell.rain(atmosphere.t)####### MOVIE !!!
        dr[i]+=soil.Dr####### MOVIE !!!
        raw[i]+=res.RAW[-1] if sum(res.RAW) >1 else 0.####### MOVIE !!!
        
        movie([rain,dr,raw],i) ####### MOVIE !!!
        plant=run(atmosphere.t,res,plant)
        print atmosphere.t
        i+=1 ####### MOVIE !!!
movie.makeMovie()####### MOVIE !!!



"""
#######################################
#######################################
### Show results
import pylab
params = {'backend': 'ps',
          'axes.labelsize': 20,
          'text.fontsize': 20,
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          'legend.fontsize': 18,
          'font.family' : 'Arial',
          'font.style' : 'normal',
          'font.variant' : 'normal',
          'font.weight' : 'normal',
          'font.stretch' : 'normal',
          'font.size' : 'large',}

pylab.rcParams.update(params)

timeline=drange(start,end,timedelta(1))


fig = figure()
fig.subplots_adjust(left=0.2, wspace=0.6)
labelx = -0.05  # axes coords
fig.patch.set_alpha(0.5)

ax1 = fig.add_subplot(311)
ax1.plot_date(timeline,res.RAW,'k',label='Readily available water')
ax1.plot_date(timeline,res.Dr,'r--',label='Depletion')
ax1.legend(loc=0)
ax1.set_ylabel('Water balance [mm]')
ax1.yaxis.set_label_coords(labelx, 0.5)


  
ax2 = fig.add_subplot(312)
ax2.plot_date(timeline,res.water_stress,'b',label='Drought stress')
ax2.set_ylabel('Stress index [-]')
ax2.set_ylim(0,1)
ax2.legend(loc=0)
ax2.yaxis.set_label_coords(labelx, 0.5)

ax3 = fig.add_subplot(313)
ax3.plot_date(timeline,[-r for r in res.rooting_depth],'g',label='Actual')
ax3.plot_date(timeline,[-r for r in res.potential_depth],'k--',label='Potential')
ax3.set_ylabel('Rooting depth [cm]')
ax3.legend(loc=4)
ax3.yaxis.set_label_coords(labelx, 0.5)

show()
""" 
    
    
    
    
   
    
    