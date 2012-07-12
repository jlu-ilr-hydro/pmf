# -*- coding: utf-8 -*-
"""
Case Study I: Water balance - Multi layer Richards approach
The Case Study represents a summer wheat setup of PMF and with the
Catchment Modeling Framework (CMF) in the version cmf1d:

Weather     : Muenchenberg,

Soil texture: Various Sand,

Soil        : cmf1d,

Atmosphere  : cmf1d,      

Simulation  : 1.1.1980 - 31.12.1980 and 

Management  : Sowing - 1.3.JJJJ, Harvest - 8.1.JJJJ.


@author: Tobias

@version: 0.1 (29.06.2012)

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
    if t.day==1 and t.month==3: #check sowing
        plant = PMF.createPlant_CMF() #create a plant instance without interfaces
        plant = PMF.connect(plant,cmf_fp,cmf_fp) #connect the plant with soil and atmosphere interface
    if t.day==1 and t.month==8: #check harvest
        plant =  None #delete plant instance
    if plant: #check, if plant exists
        plant(t,'day',1.) #run plant, daily time step, timeperiod: 1.             
    #calculate evaporation from bare soil
    baresoil(cmf_fp.Kr(),0.,cmf_fp.get_Rn(t, 0.12, True),cmf_fp.get_tmean(t),cmf_fp.get_es(t),cmf_fp.get_ea(t), cmf_fp.get_windspeed(t),0.,RHmin=30.,h=1.)    
    #get plant water uptake   
    flux = [uptake*-1. for uptake in plant.Wateruptake] if plant  else zeros(c.cell.layer_count())    
    #get evaporation from bare soil or plant model    
    flux[0] -= plant.et.evaporation if plant else baresoil.evaporation
    # set water flux of each soil layer from cmf   
    c.flux=flux
    # run cmf
    c.run(cmf.day)        
    #get status variables of cmf
    res.waterstorage.append(c.cell.layers.volume) #water content of each layer in [mm/day] (list with 40 soil layers)
    res.flux.append(c.flux) #water flux of each layer in [mm/day] (list with 40 soil layers)
    res.wetness.append(c.wetness) #wetness/water content of each layer in [%/day] (list with 40 soil layers)
    res.deep_percolation.append(c.groundwater.waterbalance(t)) #water flux to groundwater [mm/day]
    res.rain.append(c.cell.get_rainfall(t)) #rainfall in [mm/day]
    #get baresoil evaporation [mm/day]
    res.baresoil_evaporation.append(0.0) if plant else  res.baresoil_evaporation.append(baresoil.evaporation)       
    #get status variables of pmf
    #biomass status
    res.PotentialGrowth.append(plant.biomass.PotentialGrowth) if plant else res.PotentialGrowth.append(0) #[g/m2/day]
    res.ActualGrowth.append(plant.biomass.ActualGrowth) if plant else res.ActualGrowth.append(0) #[g/m2/day]
    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0) #[g/m2]
    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0) #[g/m2]
    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0) #[g/m2]
    res.leaf.append(plant.shoot.leaf.Wtot) if plant else res.leaf.append(0) #[g/m2]
    res.stem.append(plant.shoot.stem.Wtot) if plant else res.stem.append(0) #[g/m2]
    res.storage.append(plant.shoot.storage_organs.Wtot) if plant else res.storage.append(0) #[g/m2]   
    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0) #[m2/m2]
    #development    
    res.developmentstage.append(plant.developmentstage.Stage[0]) if plant else res.developmentstage.append("")
    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
    if plant:       
        if plant.developmentstage.Stage[0] != "D": 
            res.developmentindex.append(plant.developmentstage.StageIndex) if plant else res.developmentindex.append("")
        else:
            res.developmentindex.append("")
    else:
        res.developmentindex.append("")    
    #plant water balance [mm/day]
    res.ETo.append(plant.et.Reference) if plant else res.ETo.append(0)
    res.ETc.append(plant.et.Cropspecific) if plant else res.ETc.append(0)
    #transpiration is not equal to water uptake! transpiration is calculated without stress and wateruptake with stress!!!
    res.transpiration.append(plant.et.transpiration) if plant else res.transpiration.append(0) 
    res.evaporation.append(plant.et.evaporation) if plant else  res.evaporation.append(0)
    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append(zeros(c.cell.layer_count())) #(list with 40 layers)    
    res.stress.append((plant.water_stress, plant.nutrition_stress) if plant else (0,0)) # dimensionsless stress index (0-->no stress; 1-->full stress)    
    #root growth
    res.potential_depth.append(plant.root.potential_depth) if plant else res.potential_depth.append(0) #[cm]
    res.rooting_depth.append(plant.root.depth) if plant else res.rooting_depth.append(0) #[cm]
    res.branching.append(plant.root.branching) if plant else res.branching.append(zeros(c.cell.layer_count())) # growth RATE in each layer per day [g/day](list with 40 layers)
    res.root_growth.append(plant.root.actual_distribution) if plant else  res.root_growth.append(zeros(c.cell.layer_count())) # total root biomass in each layer [g/layer]
    res.time.append(t)
    return plant

class Res(object):
    def __init__(self):
        self.flux=[]
        self.water_uptake = []
        self.branching = []
        self.transpiration = []
        self.evaporation = []
        self.biomass = []
        self.root_biomass = []
        self.shoot_biomass = []
        self.lai = []
        self.root_growth = []
        self.ETo = []
        self.ETc = []
        self.wetness = []
        self.rain = []
        self.temperature = []
        self.DAS = []
        self.stress = []
        self.leaf=[]
        self.stem=[]
        self.storage=[]
        self.potential_depth=[]
        self.rooting_depth=[]
        self.time = []
        self.developmentstage = []
        self.PotentialGrowth = []
        self.ActualGrowth = []
        self.developmentindex=[]
        self.deep_percolation=[]
        self.baresoil_evaporation=[]
        self.waterstorage=[]
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])

#######################################
#######################################
### Setup script

if __name__=='__main__':
    
    from pylab import *
    from datetime import *
    import PMF
    import cmf
    from cmf_setup import cmf1d
    from cmf_fp_interface import cmf_fp_interface
    #from Atmosphere import ClimateStation
#    import psyco
#    psyco.full()
    
    #Create cmf cell    

    
#########Plot1 Kersebaum#########
#########Bodenschichten##########
    #c=cmf1d(sand=[90.,90.,80.,92.,94.,96.],silt=[3.,5.,8.,4.,3.,2.],clay=[7.,5.,12.,4.,3.,2.],c_org=[.66,.16,.08,0.,0.,0.],bedrock_K=0.01,layercount=6,layerthickness=[.3,.3,.3,.3,.3,.75],tracertext='')
#################################
#################################

#########Plot2 Kersebaum#########
#########Bodenschichten##########
    c=cmf1d(sand=[85.,90.,80.,80.,90.,90],silt=[10.,5.,8.,10.,5.,5.],clay=[5.,5.,12.,10.,5.,5.],c_org=[.58,.13,0.,0.,0.,0.],bedrock_K=0.01,layercount=6,layerthickness=[.3,.6,.4,.4,.1,.45],tracertext='')
#################################
#################################

#########Plot3 Kersebaum#########
#########Bodenschichten##########
    #c=cmf1d(sand=[85.,90.,81.,80.],silt=[9.,5.,6.,9],clay=[6.,5.,13.,11.],c_org=[.62,.13,0.,0.],bedrock_K=0.01,layercount=4,layerthickness=[.3,.7,.1,1.15],tracertext='')
#################################
#################################

 
    print "cmf is setup"
    
    #Station1_Giessen = meteo() #!!!
    #Station1_Giessen.load_weather('climate_giessen.csv') #!!!
    c.load_meteo(rain_factor=1.)
    print "meteo loaded"
    cmf_fp = cmf_fp_interface(c.cell)
    cmf_fp.default_Nconc = .3
    #cmf_fp.default_Nconc = .1
    
    
    print "Interface to PMF"
    c.cell.saturated_depth=5.
    #Create evapotranspiration instance or bare soil conditions
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    
    #set management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1992,1,1)
    end = datetime(1992,12,31)
    #Simulation
    res = Res()
    plant = None
    print "Run ... "    
    start_time = datetime.now()
    c.t = start
    start_content = np.sum(c.cell.layers.volume)
    while c.t<end:
        plant=run(c.t,res,plant)

    P = np.sum(res.rain) # precipitation
    E = np.sum(res.evaporation)+np.sum(res.baresoil_evaporation) # evaporation from baresoil and covered soil
    T = np.sum(np.sum(res.water_uptake)) # actual transpiration
    DP = np.sum(res.deep_percolation) # deep percolation (groundwater losses)
    storage =np.sum(c.cell.layers.volume)- start_content 
    print '\n################################\n' + '################################\n' + 'Water balance'
    print  "%gmm (P) = %gmm (E) +  %gmm (T) + %gmm (DP) + %gmm (delta)" % (P,E,T,DP,storage)
    print  "Water content according to water balance: %gmm \nActual water content of soil: %gmm" % ((start_content + P-DP-T-E),np.sum(c.cell.layers.volume))

    
    
    ######
    # groundwater.waterbalance -> der Fluß ist nicht in flux mit drin!!!
######################################
######################################
## Show results
timeline=drange(start,end,timedelta(1))
subplot(311)
imshow(transpose([r[:20] for r in res.wetness]),cmap=cm.Blues,aspect='auto',interpolation='nearest',extent=[0,len(timeline),100,0],vmin=0.3,vmax=1.0)
ylabel('Depth [cm]')
xlabel('Day of year')
subplot(312)
plot_date(timeline,[i[0] for i in res.stress],'b',label='Drought stress')
ylabel('Stress index [-]')
ylim(0,1)
legend(loc=0)
subplot(313)
plot_date(timeline,[-r for r in res.rooting_depth],'g',label='Actual')
plot_date(timeline,[-r for r in res.potential_depth],'k--',label='Potential')
ylabel('Rooting depth [mm]')
legend(loc=0)
show()

#===============================================================================
# import csv, codecs, cStringIO
# 
# with open('cmf1D.csv', 'wb') as f:    
#     writer = csv.writer(f,delimiter='\t', quotechar='"',quoting=csv.QUOTE_ALL)
#     writer.writerow(['Year','Month','Day','Rainfall','Temperature','Radiation','Wetness','Stage','StageIndex','Transpiration','Evaporation','Wateruptake','Root biomass','Shoot biomass','PotentialGrowth','ActualGrowht','LAI','RootingDepth','Stress'])
#     for i,day in enumerate(res.time):
#         writer.writerow([day.year,day.month,day.day,
#                          res.rain[i],res.temperature[i],res.radiation[i],sum(res.wetness[i]),
#                          res.developmentstage[i],res.developmentindex[i],res.transpiration[i],res.evaporation[i],sum(res.water_uptake[i]),res.root_biomass[i],res.shoot_biomass[i],res.PotentialGrowth[i],res.ActualGrowth[i],res.lai[i],res.rooting_depth[i],res.stress[i][0]])
#===============================================================================

