# -*- coding: utf-8 -*-
'''
Created on 02.11.2009

@author: philkraf
'''
import psyco
psyco.full()
import cmf
import DECOMP
from cmf_DECOMP import DECOMPcmf
from cmf_fp_interface import cmf_fp_interface
from datetime import datetime
from time import clock
import PMF
import pylab
import numpy as np
from cmf_setup import cmf1d
c1=cmf1d(sand=200,silt=60,clay=20,c_org=2.0,bedrock_K=0.1,layercount=20,layerthickness=0.1,tracertext='N DOC')
print "cmf is setup"
c1.load_meteo(rain_factor=0.5)
print "meteo loaded"
N,DOC = c1.project.solutes
cmf_fp = cmf_fp_interface(c1.cell, N)
print "Interface to PMF"
DECOMPcell=DECOMPcmf(c1.cell)
print "DECOMP layers ok"
def fertilize(kgN_ha):
    """Adds to the SOM of the first layer easily decomposable SOM components 
    with a C/N ratio of 10
    @type kgN_ha: Amount of fertilizer in kg N per ha. 
    """
    gN = kgN_ha * 1e3 * c1.cell.area * 1e-4
    DECOMPcell.DECOMPlayers[0] += DECOMP.SOM(gN,10 * gN)
fertilize(50)
c1.cell.saturated_depth=5.0
#set management
sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
#Simulation period
start = datetime(1980,1,1)
end = datetime(1980,12,31)

#Create evapotranspiration instance or bare soil conditions
baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
plant=None
class Res(object):
    def __init__(self):        
        self.shoot_biomass=[]
        self.root_biomass=[]
        self.water_uptake=[]
        self.matrix_potential=[]
        self.cN=[]
        self.cDOC=[]
        self.Nflux_fp=[]
        self.Nflux=[]
        self.Ndemand=[]
        self.Nuptake=[]
        self.transpiration=[]
    def __repr__(self):
        return ("biomass=%gg, root biomass=%gg, " + \
               "avg[N]=%g, Nuptake=%gg Ndemand=%gg, " + \
               "Tact= %gmm, Tpot= %gmm, Mpot=%gm")  % \
               (self.shoot_biomass[-1],
                sum(self.root_biomass[-1]),
                np.mean(self.cN[-1]),self.Nuptake[-1],self.Ndemand[-1], sum(self.water_uptake[-1]),
                self.transpiration[-1], self.matrix_potential[-1][0])

c1.t = start

def run_step(t,res,plant):
    if t.day==1 and t.month==3:
        plant=PMF.connect(PMF.createPlant_CMF(),cmf_fp,cmf_fp)
    if t.day==1 and t.month==8:
        DECOMPcell.depose_litter((plant.shoot.leaf.Wtot + plant.shoot.stem.Wtot) * c1.cell.area ,0.0)
        DECOMPcell.set_root_litter(plant.root.branching)
        plant=None
    if plant:
        plant(t,'day',1.)
    #Water flux from soil to plant
    flux = [-uptake for uptake in plant.water.Uptake] if plant else [0]* c1.cell.layer_count()
    flux[0] -= plant.et.evaporation if plant else baresoil.evaporation
    c1.flux = flux
    T=c1.get_tmean(t)
    DECOMPcell.run(T,1.)
    if plant:
        for i,l in enumerate(c1.cell.layers):
            l.Solute(N).source -= plant.nitrogen.Active[i] * c1.cell.area
    c1.run(cmf.day)
    res.shoot_biomass.append(plant.shoot.Wtot if plant else 0.0)
    res.root_biomass.append(plant.root.branching if plant else [0.0] * c1.cell.layer_count())
    res.water_uptake.append(plant.water.Uptake if plant else [0.0] * c1.cell.layer_count())
    res.matrix_potential.append(c1.matrix_potential)
    res.cN.append([l.conc(N) for l in c1.cell.layers])
    res.cDOC.append([l.conc(DOC) for l in c1.cell.layers])
    res.Nflux_fp.append(plant.nitrogen.Active if plant else [0.0] * c1.cell.layer_count())
    res.Nflux.append([l.Solute(N).source for l in c1.cell.layers])
    res.Ndemand.append(plant.Rp if plant else 0.0)
    res.Nuptake.append(sum(plant.nitrogen.Total) if plant else 0.0)
    res.transpiration.append(plant.et.transpiration if plant else 0.0)
    return plant
res=Res()
print "Run..."
start_t=clock()
i=0
while c1.t<end:
    plant=run_step(c1.t,res,plant)
    i+=1
    if i % 1==0:
        print c1.t,res
        
print cmf.sec* (clock() - start_t)
def showit(a,name,pos,posmax,**kwargs):
    pylab.subplot(posmax,1,pos)
    pylab.imshow(np.transpose(a),interpolation='nearest',**kwargs)
    pylab.ylabel(name)
    pylab.colorbar()
pylab.subplot(711)
#plot(res.shoot_biomass,hold=0)
pylab.plot(res.Ndemand,label='Ndemand')
pylab.plot(res.Nuptake,label='NUptake')
pylab.legend(loc=0)
showit(res.root_biomass,"Root biomass",2,7,cmap=pylab.cm.Greens)
showit(res.water_uptake,"Water uptake",3,7,cmap=pylab.cm.Blues)
showit(res.matrix_potential,"M_Pot",4,7,cmap=pylab.cm.RdYlBu,vmin=-9)
showit(res.cN,"[N]",5,7,cmap=pylab.cm.jet)
showit(res.Nflux_fp,"Nflux to flower power",6,7,cmap=pylab.cm.jet)
showit(res.Nflux,"Nflux total",7,7,cmap=pylab.cm.jet)
pylab.show()


