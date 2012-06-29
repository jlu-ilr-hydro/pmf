# -*- coding: utf-8 -*-
"""
Case Study III: Drought event
The Case Study represents a summer wheat setup of PMF and with the
Catchment Modeling Framework (CMF) in the version cmf1d.

Weather     : Giessen,

Soil texture: Silt

Soil        : cmf1d

Atmosphere  : cmf1d,      

Simulation  : 1.1.1980 - 31.12.1980 and 

Management  : Sowing - 1.3.JJJJ, Harvest - 8.1.JJJJ.

Changing conditions: The upper soil layers dry out in the early growing season.
                    This effect is represented through increased water fluxes
                    from the upper three soil layers between 1.4.JJ And 1.5.JJ.


@author: Sebastian Multsch

@version: 1.0 (01.10.2009)

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
    #Management
    if t.day==1 and t.month==3:
        plant_swc = PMF.connect(PMF.createPlant_SWC(),swc_fp,cmf_fp)
        plant_cmf = PMF.connect(PMF.createPlant_CMF(),cmf_fp,cmf_fp)
        plant = [plant_swc,plant_cmf]
    if t.day==1 and t.month==8:           
        plant = None  
        
    #Calculates evaporation for bare soil conditions
    baresoil(c.Kr(),0.,c.get_Rn(t, 0.12, True),c.get_tmean(t),c.get_es(t),c.get_ea(t), c.get_windspeed(t),0.,RHmin=30.,h=1.)    
    
    #plant growth
    if plant: [p(t,'day',1.) for p in plant]
    
    #swc_fp_interaction
    Wateruptake = sum(plant[0].Wateruptake) if plant else 0.
    evaporation = plant[0].et.evaporation if plant else baresoil.evaporation
    rainfall =c.cell.rain(t)
    Zr = plant[0].root.depth/100. if plant else 0.
    ETc_adj = Wateruptake + evaporation
    swc_fp(ETc_adj,evaporation,rainfall,Zr)
        
    #cmf_fp_interaction
    flux = [uptake*-1. for uptake in plant[1].Wateruptake] if plant  else zeros(c.cell.layer_count())
    flux[0] -= plant[1].et.evaporation if plant else baresoil.evaporation
    
    #influences through lateral flow
    if t.day>=1  and t.month==4 or t.month==5:
        flux[0]-=1
        flux[1]-=1
        flux[2]-=1
  
    c.flux=flux
    
   
        
    res[1].Dr.append(c.wetness)
    res[0].Dr.append(swc_fp.Dr)
    res[0].rain.append(c.cell.rain(t)) 
    res[0].radiation.append(c.get_Rn(t, 0.12, True))
    #Results
    if plant:
        res[0].TAW.append(plant[0].water.TAW)
        res[0].RAW.append(plant[0].water.RAW)
        res[0].rootdepth.append(plant[0].root.depth)
        res[1].rootdepth.append(plant[1].root.branching)
        res[1].root_growth.append(plant[1].root.actual_distribution)
        
        for i,p in enumerate(plant):
            res[i].W_shoot.append(p.shoot.Wtot)
            res[i].W_root.append(p.root.Wtot)
            res[i].LAI.append(p.shoot.leaf.LAI)
            res[i].Sh.append(p.Wateruptake)
            res[i].T.append(p.et.transpiration)
            res[i].E.append(p.et.evaporation)
            res[i].stress.append(p.water_stress)
            res[i].W_potential.append(p.biomass.pot_total)
            res[i].rootdepth_pot.append(p.root.potential_depth)
            res[i].W_leaf.append(p.shoot.leaf.Wtot)
            res[i].W_stem.append(p.shoot.stem.Wtot)
            res[i].W_storage.append(p.shoot.storage_organs.Wtot)
           
    else:
        res[0].TAW.append(0.)
        res[0].RAW.append(0.)
        res[0].rootdepth.append(0)
        res[1].rootdepth.append(zeros(c.cell.layer_count()))
        res[1].root_growth.append(zeros(c.cell.layer_count()))
        res[0].Sh.append(0.)
        res[1].Sh.append(zeros(c.cell.layer_count()))
        for r in res:
            r.W_shoot.append(0.)
            r.W_root.append(0.)
            r.LAI.append(0.)
            
            r.T.append(0.)
            r.E.append(0.)
            r.stress.append(0.)
            r.W_potential.append(0.)
            r.rootdepth_pot.append(0.)
            r.W_leaf.append(0.)
            r.W_stem.append(0.)
            r.W_storage.append(0.)
 
    c.run(cmf.day)
    return plant


class Results():
    def __init__(self):
        self.W_shoot=[]
        self.W_root=[]
        self.W_leaf=[]
        self.W_stem=[]
        self.W_storage=[]
        self.rootdepth=[]
        self.LAI=[]
        self.Sh=[]
        self.T=[]
        self.E=[]
        self.stress=[]
        self.TAW=[]
        self.RAW=[]
        self.Dr=[]
        self.rain=[]
        self.W_potential=[]
        self.rootdepth_pot=[]
        self.radiation=[]
        self.root_growth=[]
        
        
    def __repr__(self):
        return "Shoot = %gg, Root =% gg, LAI = %gm2/m2, Wateruptake =% gmm, T = %gmm, E = %gmm, Stress = %g" % (self.W_shoot[-1],self.W_root[-1],self.LAI[-1],sum(self.Sh[-1]),self.T[-1],self.E[-1],self.stress[-1])

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
    import psyco
    import time
    psyco.full()
    
    r1=Results()
    r2=Results()
    res = [r1,r2]
    
    #Create Evaporation modul
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    
    #Create cmf cell    
    c=cmf1d()
    c.load_meteo(rain_factor=.75)
    cmf_fp = cmf_fp_interface(c.cell)
    c.cell.saturated_depth=5.
    
    #Create Soilwater container
    swc_fp = PMF.SWC()
    
    #Create management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1980,3,1)
    end = datetime(1980,12,31)
    
    plant = None
    c.t = start
    while c.t<end:
        plant=run(c.t,res,plant)
        
        #shoot_data[i] += res[0].W_shoot[-1]
        #shoot_line = make_show(shoot_line,shoot_data)
        #i+=1
        
        print c.t

   
#######################################
#######################################
### Show results    


subplot(311)
title('Root biomass in each soil layer [g]')
imshow(transpose([r[:20] for r in res[1].rootdepth]),cmap=cm.Greens,aspect='auto',interpolation='nearest',extent=[60,200,100,0])
ylabel('Depth [cm]')
colorbar()
subplot(312)
title('Root growth in each soil layer [g]')
imshow(transpose([r[:20] for r in res[1].root_growth]),cmap=cm.Greens,aspect='auto',interpolation='nearest',extent=[60,200,100,0])
ylabel('Depth [cm]')
colorbar()
subplot(313)
title('Wetness [m3 m-3]')
imshow(transpose([r[:20] for r in res[1].Sh]),cmap=cm.Blues,aspect='auto',interpolation='nearest',extent=[60,200,100,0])
ylabel('Depth [cm]')
xlabel('Day of year')
colorbar()

"""




def graph_plot(a,b,c,data,**kwargs):
    subplot(a,b,c)
    plot(data,**kwargs)
    
    
def graph_image(a,b,c,data,**kwargs):
    subplot(a,b,c)
    imshow(transpose(data),aspect='auto',interpolation='nearest',**kwargs)   
"""
"""
def build_cinema(duration,ymax,**kwargs):
    #hold(False)
    ion()
    line, = plot(zeros(duration),**kwargs)
    ylim(0,ymax)
    return line
def make_show(line, dat):
    line.set_ydata(dat)
    draw()
    return line

duration = end-start
shoot_data = [0.for i in range(duration.days)]
shoot_line=build_cinema(duration.days,1000)
i=0
"""
    
ax1=subplot(311)
ax2=subplot(312)
ax3=subplot(313)

"""
timeline = drange(start,end,timedelta(1))
graph_image(3,1,1,[r[:15] for r in res[1].Dr],cmap=cm.Greys,vmax=1,vmin=0)
ylabel('Depth in [cm]') 
subplot(312)
plot_date(timeline,res[1].stress,label='Droughtstress')
ylabel('Stress index')
legend(loc=0)
graph_image(3,1,3,[r[:15] for r in res[1].rootdepth],cmap=cm.Greys,vmax=10,vmin=0)
ylabel('Depth in [cm]')

"""


"""
figtext(.2, .96,'Fieldcapacity based approach - FAO')
figtext(.2, .94,('Shoot %4.2f, Root %4.2f, LAI %4.2f')%(filter(lambda res: res>0,res[0].W_shoot)[-1],filter(lambda res: res>0,res[0].W_root)[-1],filter(lambda res: res>0,res[0].LAI)[-1]))
graph_plot(3,2,1,res[0].W_shoot,label='Shoot biomass')
graph_plot(3,2,3,res[0].rootdepth,label='Rootdepth')
subplot(325)
plot(res[0].Dr,label='Depletion')
plot(res[0].TAW,label='TAW')
plot(res[0].RAW,label='RAW')
legend(loc=0)
grid()
figtext(.6, .96,'Matrixpotential based appraoch - CMF')
figtext(.6, .94,('Shoot %4.2f, Root %4.2f, LAI %4.2f')%(filter(lambda res: res>0,res[1].W_shoot)[-1],filter(lambda res: res>0,res[1].W_root)[-1],filter(lambda res: res>0,res[1].LAI)[-1]))
graph_plot(3,2,2,res[1].W_shoot,label='Shoot biomass') 
graph_image(3,2,4,res[1].rootdepth,cmap=cm.Greens) 
graph_image(3,2,6,res[1].Dr,cmap=cm.RdYlBu)
show()
"""

"""
#Fieldcapacity-concept
figtext(.2, .96,'Fieldcapacity based approach - FAO')
figtext(.2, .94,('Shoot %4.2f, Root %4.2f, LAI %4.2f')%(filter(lambda res: res>0,res[0].W_shoot)[-1],filter(lambda res: res>0,res[0].W_root)[-1],filter(lambda res: res>0,res[0].LAI)[-1]))
graph_plot(4,2,1,res[0].rootdepth,'Rootdepth')
graph_plot(4,2,3,res[0].stress,label='Stress',color='r')
ylim(0,1)
#graph_plot(4,2,5,[sum(r)for r in res[0].Sh],label='Wateruptake')
graph_plot(4,2,5,res[0].W_shoot,label='Shoot biomass')
subplot(427)
plot(res[0].Dr,label='Depletion')
plot(res[0].TAW,label='TAW')
plot(res[0].RAW,label='RAW')
legend(loc=0)
grid()
#Matrixpotential-concept
figtext(.6, .96,'Matrixpotential based appraoch - CMF')
figtext(.6, .94,('Shoot %4.2f, Root %4.2f, LAI %4.2f')%(filter(lambda res: res>0,res[1].W_shoot)[-1],filter(lambda res: res>0,res[1].W_root)[-1],filter(lambda res: res>0,res[1].LAI)[-1]))
graph_image(4,2,2,res[1].rootdepth,cmap=cm.Greens)
graph_plot(4,2,4,res[1].stress,label='Stress',color='r') 
ylim(0,1)        
#graph_plot(4,2,6,[sum(w) for w in res[1].Sh],label='Wateruptake')
graph_plot(4,2,6,res[1].W_shoot,label='Shoot biomass')  
graph_image(4,2,8,res[1].Dr,cmap=cm.RdYlBu)
show()
"""


"""

timeline = drange(start,end,timedelta(1))
subplot(311)
plot_date(timeline,[r + res[0].W_root[i] for i,r in enumerate(res[0].W_shoot)],'g',label='Actual')
plot_date(timeline,res[0].W_potential,'k--',label='Potential')
#plot_date(timeline,[r + res[1].W_root[i] for i,r in enumerate(res[1].W_shoot)],'b',label='Actual')
#plot_date(timeline,res[1].W_potential,'k--',label='Potential')
legend(loc=0)
title('Biomass')
ylabel('[g/m2]')

subplot(312)
plot_date(timeline,[-r for r in res[0].rootdepth],'g',label='Actual')
plot_date(timeline,[-r for r in res[0].rootdepth_pot],'k--',label='Potential')
#plot_date(timeline,[-r for r in res[1].rootdepth],'b',label='Actual')
#plot_date(timeline,[-r for r in res[1].rootdepth_pot],'k--',label='Potential')
legend(loc=0)
title('Rooting depth')
ylabel('[cm]')

cumTpotFAO=[0.]
for i,r in enumerate(res[0].T):
    cumTpotFAO.append(cumTpotFAO[-1]+r)

cumTactFAO=[0.]
for i in res[0].Sh:
    cumTactFAO.append(cumTactFAO[-1]+sum(i))
    
cumTpotCMF=[0.]
for i,r in enumerate(res[1].T):
    cumTpotCMF.append(cumTpotCMF[-1]+r)

cumTactCMF=[0.]
for i in res[1].Sh:
    cumTactCMF.append(cumTactCMF[-1]+sum(i))

t = drange(start,end+timedelta(1),timedelta(1))
subplot(313)
plot_date(t,cumTactCMF,'b',label='Actual')
plot_date(t,cumTpotCMF,'k--',label='Potential')

#plot_date(timeline,[sum(w) for w in res[1].Sh],'b',label='Actual')
#plot_date(timeline,res[1].T,'k--',label='Potential')
#plot_date(timeline,[sum(w) for w in res[0].Sh],'g',label='Actual Transpiration')
#plot_date(timeline,res[0].T,'k--',label='Potential')
legend(loc=0)
title('Transpiration')
ylabel('[mm]')
"""
"""
rain=[0.]
for i,r in enumerate(res[0].rain):
    rain.append(rain[-1]+r)

radiation=[0.]
for i in res[0].radiation:
    radiation.append(radiation[-1]+sum(i))
    
    
timeline = drange(start,end,timedelta(1))
t = drange(start,end+timedelta(1),timedelta(1))
subplot(211)
plot_date(t,radiation,'r',label='Radiation')
legend(loc=0)
subplot(212)
plot_date(t,rain,'b',label='Rain')
legend(loc=0)
"""

"""
    #Calculates DAS for each development stage
    stages = PMF.PlantBuildingSet.CropCoefficiants().stage
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
"""
show()  
 
        
        
        
        
        
        
        
        
        
        
        
        
        