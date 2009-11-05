# -*- coding: utf-8 -*-
'''
Created on 02.11.2009

@author: philkraf
'''

import cmf
from cmf_DECOMP import DECOMPcmf, DECOMP
from cmf_fp_interface import cmf_fp_interface
from datetime import datetime
import FlowerPower
from pylab import *
from cmf_setup import cmf1d
c1=cmf1d(sand=20,silt=60,clay=20,c_org=2.0,bedrock_K=0.01,layercount=20,layerthickness=0.1,tracertext='N DOC')
print "cmf is setup"
c1.load_meteo()
print "meteo loaded"
N,DOC = c1.project.solutes
cmf_fp = cmf_fp_interface(c1.cell, N)
print "Interface to FlowerPower"
DECOMPcell=DECOMPcmf(c1.cell)
print "DECOMP layers ok"
# G�lle schmeissen
DECOMPcell.DECOMPlayers[0] = DECOMP.SOM(0.1*1e0,1e0)
c1.cell.saturated_depth=2.0
#set management
sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
#Simulation period
start = datetime(1980,1,1)
end = datetime(1980,12,31)

#Create evapotranspiration instance or bare soil conditions
baresoil = FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
plant=None
class Res(object):
    def __init__(self):        
        self.shoot_biomass=[]
        self.root_biomass=[]
        self.water_uptake=[]
        self.wetness=[]
        self.cN=[]
        self.cDOC=[]
        self.Nflux_fp=[]
        self.Nflux=[]
    def __repr__(self):
        return "M=%gg, Mr=%gg, [N]=%g" % (self.shoot_biomass[-1],sum(self.root_biomass[-1]),mean(self.cN[-1]))

c1.t = start

def run_step(t,res,plant):
    if t.day==1 and t.month==3:
        plant=FlowerPower.crconnectCropmf_fp, cmf_fp,"SummerWheat")
    if t.day==1 and t.month==8:
        DECOMPcell.depose_litter(plant.shoot.leaf.Wtot+plant.shoot.stem.Wtot,0.0)
        DECOMPcell.set_root_litter(plant.root.branching)
        plant=None
    if plant:
        plant(t,'day',1.)
    #Water flux from soil to plant
    flux = [-uptake for uptake in plant.water.Uptake] if plant else [0]* c1.cell.layer_count()
    #flux[0] -= plant.et.Evaporation if FlowerPower.Plant.Count >0 else baresoil.Evaporation
    c1.flux=flux
    T=c1.get_tmean(t)
    DECOMPcell.run(T,1.)
    if plant:
        for i,l in enumerate(c1.cell.layers):
            l.Solute(N).source -= plant.nitrogen.Active[i]
    c1.run(cmf.day)
    res.shoot_biomass.append(plant.shoot.Wtot if plant else 0.0)
    res.root_biomass.append(plant.root.branching if plant else [0.0] * c1.cell.layer_count())
    res.water_uptake.append(flux)
    res.wetness.append(c1.wetness)
    res.cN.append([l.conc(N) for l in c1.cell.layers])
    res.cDOC.append([l.conc(DOC) for l in c1.cell.layers])
    res.Nflux_fp.append(plant.nitrogen.Active if plant else [0.0] * c1.cell.layer_count())
    res.Nflux.append([l.Solute(N).source for l in c1.cell.layers])
    return plant
res=Res()
print "Run..."
while c1.t<end:
    plant=run_step(c1.t,res,plant)
    print c1.t,res
def showit(a,pos,posmax,**kwargs):
     subplot(posmax,1,pos)
     imshow(transpose(a),interpolation='nearest',**kwargs)
     colorbar()

showit(res.root_biomass,2,7,cmap=cm.Greens)
showit(res.water_uptake,3,7,cmap=cm.Blues)
showit(res.wetness,4,7,cmap=cm.RdYlBu)
showit(res.cN,5,7,cmap=cm.jet, vmax=1e-4)
showit(res.Nflux_fp,6,7,cmap=cm.jet)
showit(res.Nflux,7,7,cmap=cm.jet)
show()


