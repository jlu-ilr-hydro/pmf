# -*- coding: utf-8 -*-

"""

"""

def run(t,res,plant):
    if t.day==1 and t.month==3:
        plant = FlowerPower.connect(FlowerPower.createPlant_SWC(),soil,atmosphere)
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
        self.stress=[]
        self.fc=[]
        self.wp=[]
        
        
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])
if __name__=='__main__':
    
    from pylab import *
    from datetime import *
    import FlowerPower
    import cmf
    from cmf_setup import cmf1d
    import psyco
    psyco.full()
    
    #Create cmf cell    
    atmosphere=cmf1d()
    atmosphere.load_meteo(rain_factor=1)
    
    soil = FlowerPower.SWC()
    baresoil = FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    #set management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1980,3,1)
    end = datetime(1980,8,1)
    #Simulation
    res = Res()
    plant = None
    print "Run ... "    
    start_time = datetime.now()
    atmosphere.t = start
    while atmosphere.t<end:
        plant=run(atmosphere.t,res,plant)
       
    print 'Duration:',datetime.now()-start_time
    def showit(a,pos,posmax,**kwargs):
        subplot(posmax,1,pos)
        imshow(transpose(a),aspect='auto',interpolation='nearest',**kwargs)
        colorbar()
    #Calculates DAS for each development stage
    stages = FlowerPower.make_plant.CropCoefficiants().stage
    #Days after sowing (DAS) unit maturity
    DAS = filter(lambda res: res!=0,res.DAS)[-1]
    #Fraction of each development stage from maturity 
    relStages = [s[1] / stages[-1][1] for s in stages]
    #DAS for each stage
    DAS = [DAS.days * s for s in relStages]
    figtext(.01, .97, ('Rain %4.2f, Radiation %4.2f, Temperature: %4.2f') % (sum(res.rain),sum(res.radiation),sum(res.temperature)))
    figtext(.01, .95, ('ETo %4.2f, ETc %4.2f, transpiration %4.2f, evaporation %4.2f') % (sum(res.ETo),sum(res.ETc),sum(res.transpiration),sum(res.evaporation)))
    figtext(.01, .93, ('Plant biomass %4.2f, Root biomass %4.2f, Shoot biomass %4.2f, LAI %4.2f, Water uptake: %4.2f') % (filter(lambda res: res>0,res.biomass)[-1], filter(lambda res: res>0,res.root_biomass)[-1], filter(lambda res: res>0,res.shoot_biomass)[-1], filter(lambda res: res>0,res.lai)[-1],sum(res.water_uptake)))
    figtext(.01, .91, ('Emergence %4.2f,Leaf development %4.2f,  Tillering %4.2f, Stem elongation %4.2f, Anthesis %4.2f, Seed fill %4.2f, Dough stage %4.2f, Maturity %4.2f') % (DAS[0],DAS[1],DAS[2],DAS[3],DAS[4],DAS[5],DAS[6],DAS[7]))   
    subplot(311)
    plot(res.root_biomass,label="Root")
    plot(res.shoot_biomass,label="Shoot")
    plot(res.leaf,label="Leaf")
    plot(res.stem,label="Stem")
    plot(res.storage,label="Storage")
    legend(loc=0)
    grid()
    subplot(312)
    plot(res.Dr,label="Depletion")
    plot(res.TAW,label="Total available soil water")
    plot(res.water_uptake,label='Wateruptake')
    legend(loc=0)
    grid()
    subplot(313)
    plot(res.ETc,label='ETc')
    plot(res.ETo,label='ETo')
    plot(res.evaporation,label='Evaporation')
    plot(res.transpiration,label='Transpiration')
    legend(loc=0)
    show()
    