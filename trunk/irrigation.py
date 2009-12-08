# -*- coding:utf-8 -*-
"""
Created on 07.12.2009

Application of FlowerPower with two waterbalance models as Irrigation management
tool.

Irrigation planing:
By calculating the soil water balance of the root zone on a daily basis 
(Equation 85), the timing and the depth of future irrigations can be planned. 
To avoid crop water stress, irrigations should be applied before or at the 
moment when the readily available soil water is depleted (Dr, i £ RAW). To 
avoid deep percolation losses that may leach relevant nutrients out of the 
root zone, the net irrigation depth should be smaller than or equal to the 
root zone depletion (Ii £ Dr, i).
@author: sebi
"""

def run(t,res,plant):
    #Management
    if t.day==1 and t.month==3:
        plant_swc = FlowerPower.connect(FlowerPower.createPlant_SWC(),swc_fp,cmf_fp)
        plant_cmf = FlowerPower.connect(FlowerPower.createPlant_CMF(),cmf_fp,cmf_fp)
        plant = [plant_swc,plant_cmf]
    if t.day==1 and t.month==8:
        plant = None  
        
    #Calculates evaporation for bare soil conditions
    baresoil(c.Kr(),0.,c.get_Rn(t, 0.12, True),c.get_tmean(t),c.get_es(t),c.get_ea(t), c.get_windspeed(t),0.,RHmin=30.,h=1.)    
    
    #plant growth
    if plant: [p(t,'day',1.) for p in plant]
    
    #swc_fp_interaction
    ETc_adj = sum(plant[0].Wateruptake)+plant[0].et.evaporation if plant else baresoil.evaporation
    evaporation = plant[0].et.evaporation if plant else baresoil.evaporation
    rainfall =c.cell.rain(t)
    Zr = plant[0].root.depth/100. if plant else 0.
    swc_fp(ETc_adj,evaporation,rainfall,Zr)
        
    #cmf_fp_interaction
    flux = [uptake*-1. for uptake in plant[1].Wateruptake] if plant  else zeros(c.cell.layer_count())
    flux[0] -= plant[1].et.evaporation if plant else baresoil.evaporation
    c.flux=flux
    
   
        
    res[1].Dr.append(c.wetness)
    res[0].Dr.append(swc_fp.Dr)
    res[0].rain.append(c.cell.rain(t)) 
    #Results
    if plant:
        res[0].TAW.append(plant[0].water.TAW)
        res[0].RAW.append(plant[0].water.RAW)
        res[0].rootdepth.append(-plant[0].root.depth)
        res[1].rootdepth.append(plant[1].root.branching)
        for i,p in enumerate(plant):
            res[i].W_shoot.append(p.shoot.Wtot)
            res[i].W_root.append(p.root.Wtot)
            res[i].LAI.append(p.shoot.leaf.LAI)
            res[i].Sh.append(p.Wateruptake)
            res[i].T.append(p.et.transpiration)
            res[i].E.append(p.et.evaporation)
            res[i].stress.append(p.water_stress)            
    else:
        res[0].TAW.append(0.)
        res[0].RAW.append(0.)
        res[0].rootdepth.append(0)
        res[1].rootdepth.append(zeros(c.cell.layer_count()))
        for r in res:
            r.W_shoot.append(0.)
            r.W_root.append(0.)
            r.LAI.append(0.)
            r.Sh.append(0.)
            r.T.append(0.)
            r.E.append(0.)
            r.stress.append(0.)
            
    c.run(cmf.day)
    return plant


class Res():
    def __init__(self):
        self.W_shoot=[]
        self.W_root=[]
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
    def __repr__(self):
        return "Shoot = %gg, Root =% gg, LAI = %gm2/m2, Wateruptake =% gmm, T = %gmm, E = %gmm, Stress = %g" % (self.W_shoot[-1],self.W_root[-1],self.LAI[-1],sum(self.Sh[-1]),self.T[-1],self.E[-1],self.stress[-1])



if __name__=='__main__':
    from pylab import *
    from datetime import *
    import FlowerPower
    import cmf
    from cmf_setup import cmf1d
    from cmf_fp_interface import cmf_fp_interface
    import psyco
    psyco.full()
    
    r1=Res()
    r2=Res()
    res = [r1,r2]
    
    #Create Evaporation modul
    baresoil = FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    
    #Create cmf cell    
    c=cmf1d(sand=20,silt=60,clay=20,c_org=2.0,bedrock_K=0.01,layercount=20,layerthickness=0.1)
    c.load_meteo(rain_factor=1.)
    cmf_fp = cmf_fp_interface(c.cell)
    c.cell.saturated_depth=5.
    
    #Create Soilwater container
    swc_fp = FlowerPower.SWC()
    
    #Create management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1980,1,1)
    end = datetime(1984,12,31)
    
    plant = None
    #Runtime loop
    c.t = start
    while c.t<end:
        plant=run(c.t,res,plant)
        print c.t

    def graph_plot(max,column,number,data,label,**kwargs):
        subplot(max,column,number)
        plot(data,label=label,**kwargs)
        legend(loc=0)
        grid()
        
    def graph_image(max,column,number,data,**kwargs):
        subplot(max,column,number)
        imshow(transpose(data),aspect='auto',interpolation='nearest',extent=[0,350,200,0],**kwargs)
        ylim(100,0)
        grid()
    
     
    #Fieldcapacity-concept
    figtext(.2, .96,'Fieldcapacity based approach - FAO')
    figtext(.2, .94,('Shoot %4.2f, Root %4.2f, LAI %4.2f')%(filter(lambda res: res>0,res[0].W_shoot)[-1],filter(lambda res: res>0,res[0].W_root)[-1],filter(lambda res: res>0,res[0].LAI)[-1]))
    graph_plot(4,2,1,res[0].rootdepth,'Rootdepth')
    graph_plot(4,2,3,res[0].stress,label='Stress',color='r')
    graph_plot(4,2,5,[sum(r)for r in res[0].Sh],label='Wateruptake')
    #graph_plot(4,2,7,res[0].Dr,label='Dr')
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
    graph_plot(4,2,6,[sum(w) for w in res[1].Sh],label='Wateruptake')  
    graph_image(4,2,8,res[1].Dr,cmap=cm.RdYlBu)
    show()
    """
    timeline = drange(start,end,timedelta(1))
    
    subplot(311)
    plot_date(timeline,res[0].W_shoot,'b',label='FAO - biomass')
    plot_date(timeline,res[1].W_shoot,'r',label='CMF - biomass')
    legend(loc=0)
    title('Crop growth')
    ylabel('[g/m2]')
    
    subplot(312)
    plot_date(timeline,res[0].stress,'b',label='FAO - Droughtstress')
    plot_date(timeline,res[1].stress,'r',label='CMF - Droughtstress')
    legend(loc=0)
    title('Stress influence')
    ylabel('[-]')
    ylim(0,1)
    
    subplot(313)
    plot_date(timeline,[sum(w) for w in res[0].Sh],'b',label='FAO - Wateruptake')
    plot_date(timeline,[sum(w) for w in res[1].Sh],'r',label='CMF - Wateruptake')
    legend(loc=0)
    title('Plant-Soil-Interaction')
    ylabel('[mm]')
    
    show()
     
    """    
        
        
        
        
        
        
        
        
        
        
        
        
        