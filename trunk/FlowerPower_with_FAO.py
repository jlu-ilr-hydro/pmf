# -*- coding:utf-8 -*-
"""
Created on 11.11.2009

@author: sebi
"""
def run(t,res,plant):
    if t.day==1 and t.month==3:
        plant = FlowerPower.connect(FlowerPower.createPlant_SWC(),swc,meteo)
    if t.day==1 and t.month==8:
        plant =  None
    #Let grow
    if plant: 
        plant(t,'day',1.)
    #Calculates evaporation for bare soil conditions
    swc_baresoil(swc.Kr(),0.,meteo.get_Rn(t, 0.12, True),meteo.get_tmean(t),meteo.get_es(t),meteo.get_ea(t), meteo.get_windspeed(t),0.,RHmin=30.,h=1.)    
    #SWC
    ETc = plant.et.Cropspecific if plant else 0. 
    evaporation = plant.et.evaporation if plant else swc_baresoil.evaporation
    rainfall = meteo.cell.rain(t)
    Zr = plant.root.depth/100. if plant else 0.
    swc(ETc,evaporation,rainfall,Zr,runoff=0.,irrigation=0.,capillarrise=0.)
    
    
    res.biomass.append(plant.biomass.Total if plant else 0.)
    res.LAI.append(plant.shoot.leaf.LAI if plant else 0.)
    res.root.append(plant.root.Wtot if plant else 0.)
    res.shoot.append(plant.shoot.Wtot if plant else 0.)
    res.wateruptake.append(sum(plant.water.Uptake) if plant else 0.)
    res.ETo.append(plant.et.Reference if plant else 0.)
    res.ETc.append(plant.et.Cropspecific if plant else 0.)
    res.evaporation.append(plant.et.evaporation if plant else 0.)
    res.transpiration.append(plant.et.transpiration if plant else 0.)
    res.rain.append(meteo.cell.rain(t))
    meteo.run(cmf.day)
    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
    res.temperature.append(meteo.get_tmean(t))
    res.radiation.append(meteo.get_Rs(t))
    res.rootingdepth.append(plant.root.depth if plant else 0.)
    res.stress.append((plant.water_stress, plant.nutrition_stress) if plant else (0,0))
    res.Ks.append(plant.water.Ks if plant else 0.)
    res.TAW.append(swc.TAW)
    res.Dr.append(swc.Dr)
    return plant
class Res:
    def __init__(self):
        self.LAI=[]
        self.biomass=[]
        self.root=[]
        self.shoot=[]
        self.wateruptake=[]
        self.ETo=[]
        self.ETc=[]
        self.evaporation=[]
        self.transpiration=[]
        self.rain=[]
        self.DAS=[]
        self.temperature = []
        self.radiation = []
        self.rootingdepth=[]
        self.stress=[]
        self.Ks=[]
        self.TAW=[]
        self.Dr=[]
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, LAI = %gm2m-2, Wateruptake=%gmm,Stress=%s, Rootingdepth=%gcm" % (self.shoot[-1],self.root[-1],self.LAI[-1],sum(self.wateruptake[-1]),self.stress[-1],self.rootingdepth[-1])

if __name__=='__main__':
    from pylab import *
    from datetime import *
    import FlowerPower
    import cmf
    from cmf_setup import cmf1d
    #Create cmf cell    
    meteo=cmf1d()
    meteo.load_meteo(rain_factor=1)
    #Create swc
    swc=FlowerPower.SWC()
    #evaporation module
    swc_baresoil = FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    #set management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1980,1,1)
    end = datetime(1980,12,31)
    meteo.t = start
    res=Res()
    plant=None
    while meteo.t<end:
        plant=run(meteo.t,res,plant)
        print meteo.t,res


    #Calculates DAS for each development stage
    stages = FlowerPower.make_plant.CropCoefficiants().stage
    #Days after sowing (DAS) unit maturity
    DAS = filter(lambda res: res!=0,res.DAS)[-1]
    #Fraction of each development stage from maturity 
    relStages = [s[1] / stages[-1][1] for s in stages]
    #DAS for each stage
    DAS = [DAS.days * s for s in relStages]
    #figtext(.01, .97, ('Rain %4.2f, Radiation %4.2f, Temperature: %4.2f') % (sum(res.rain),sum(res.radiation),sum(res.temperature)))
    #figtext(.01, .95, ('ETo %4.2f, ETc %4.2f, transpiration %4.2f, evaporation %4.2f') % (sum(res.ETo),sum(res.ETc),sum(res.transpiration),sum(res.evaporation)))
    #figtext(.01, .93, ('Plant biomass %4.2f, Root biomass %4.2f, Shoot biomass %4.2f, LAI %4.2f, Water uptake: %4.2f') % (filter(lambda res: res>0,res.biomass)[-1], filter(lambda res: res>0,res.root)[-1], filter(lambda res: res>0,res.shoot)[-1], filter(lambda res: res>0,res.LAI)[-1],sum(res.wateruptake)))
    #figtext(.01, .91, ('Emergence %4.2f,Leaf development %4.2f,  Tillering %4.2f, Stem elongation %4.2f, Anthesis %4.2f, Seed fill %4.2f, Dough stage %4.2f, Maturity %4.2f') % (DAS[0],DAS[1],DAS[2],DAS[3],DAS[4],DAS[5],DAS[6],DAS[7]))
    
    subplot(411)
    plot(res.root,label='Root')
    plot(res.shoot,label='Shoot')
    twinx()
    plot(res.rootingdepth,label='Rootingdepth')
    legend(loc=0)
    subplot(412)
    plot(res.transpiration,label='Transpiration')
    plot(res.ETo,label='ETo')
    plot(res.ETc,label='ETc')
    plot(res.wateruptake,label='Wateruptake')
    legend(loc=0)
    subplot(413)
    plot(res.Ks,label='Ks')
    legend(loc=0)
    subplot(414)
    plot(res.TAW,label='Total available water')
    plot(res.Dr,label='Depletion')
    legend(loc=0)

    show()
    