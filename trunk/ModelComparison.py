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
    evaporation = plant.et.Evaporation if plant else swc_baresoil.Evaporation
    rainfall = meteo.cell.rain(t)
    Zr = plant.root.depth if plant else 0.
    swc(ETc,evaporation,rainfall,Zr,runoff=0.,irrigation=0.,capillarrise=0.)
    meteo.run(cmf.day)
    res.LAI.append(plant.shoot.leaf.LAI if plant else 0.)
    res.root.append(plant.root.Wtot if plant else 0.)
    res.shoot.append(plant.shoot.Wtot if plant else 0.)
    res.wateruptake.append(sum(plant.water.Uptake) if plant else 0.)
    return plant
class Res:
    def __init__(self):
        self.LAI=[]
        self.root=[]
        self.shoot=[]
        self.wateruptake=[]
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, LAI = %gm2m-2, Wateruptake=%gmm" % (self.shoot[-1],self.root[-1],self.LAI[-1],sum(self.wateruptake[-1]))

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
    #Evaporation module
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
        
    