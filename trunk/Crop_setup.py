from plant import *
from WaterBalance import *
from cmf_setup import *
import cmf
class Field:
    def __init__(self,soil,atmosphere):
        self.soil=soil
        self.atmosphere=atmosphere
        self.soilwater=Water_MatrixPotentialApproach()
        self.plant=Plant(self.soil,self.atmosphere,self.soilwater,self.ET)
        self.ET=ET_FAO()
    def harvest(self):
        return self.plant.Wtot
    def __call__(self,time_act,step,interval):
        #Compute ET
        self.ET(self.atmosphere.get_Rn(time_act,0.12,True),self.atmosphere.get_tmean(time_act)
                                   ,self.atmosphere.get_es(time_act),self.atmosphere.get_ea(time_act)
                                   ,self.atmosphere.get_windspeed(time_act),vegH=self.plant.Wtot/900.+0.01
                                   ,LAI=1+3*self.plant.shoot.plant.Wtot/900.,stomatal_resistance=self.plant.shoot.leaf.stomatal_resistance)
        #Compute water uptake
        self.soilwater([self.ET.reference/self.plant.root.depth * l.penetration for l in self.plant.root.zone]
                         ,[self.soil.get_pressurehead(l.center) for l in self.root.zone],self.plant.pressure_threshold)
        self.plant(time_act,step,interval)
    
class Management:
    def __init__(self):
        self.sowing_date=self.set_management()[0]
        self.harvest_date=self.set_management()[1]
        self.total_harvest=[]
        self.dict_of_plants={}
    def isharvest(self,time_act):
        for date in self.harvest_date:
            if time_act==date:
                return True
                break
    def issowing(self,time_act):
        for date in self.sowing_date:
            if time_act==date:
                return True
                break
    def set_management(self):
        sowing_date=[t.datetime(1991,3,1),t.datetime(1992,3,1),t.datetime(1993,3,1),t.datetime(1994,3,1),t.datetime(1995,3,1)
                      ,t.datetime(1996,3,1),t.datetime(1997,3,1),t.datetime(1998,3,1),t.datetime(1999,3,1),t.datetime(2000,3,1)
                      ,t.datetime(1980,3,1),t.datetime(1981,3,1),t.datetime(1982,3,1),t.datetime(1983,3,1),t.datetime(1984,3,1)
                      ,t.datetime(1985,3,1),t.datetime(1986,3,1),t.datetime(1987,3,1),t.datetime(1988,3,1),t.datetime(1989,3,1)
                      ,t.datetime(1990,3,1)]
        harvest_date=[t.datetime(1991,9,30),t.datetime(1992,9,30),t.datetime(1993,9,30),t.datetime(1994,9,30),t.datetime(1995,9,30)
                      ,t.datetime(1996,9,30),t.datetime(1997,9,30),t.datetime(1998,9,30),t.datetime(1999,9,30),t.datetime(2000,9,30)
                      ,t.datetime(1980,9,30),t.datetime(1981,9,30),t.datetime(1982,9,30),t.datetime(1983,9,30),t.datetime(1984,9,30)
                      ,t.datetime(1985,9,30),t.datetime(1986,9,30),t.datetime(1987,9,30),t.datetime(1988,9,30),t.datetime(1989,9,30)
                      ,t.datetime(1990,9,30)]
        return [sowing_date,harvest_date]
    def __call__(self,time_act):
        if self.issowing(time_act) == True:
            return True
        elif self.isharvest(time_act) == True:
            return True   
        
if __name__=='__main__':
    import datetime as t
    import time
    c=cmf1d(sand=60,silt=30,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    load_meteo(c.project,stationname='Giessen')
    management=Management()
    field=Field(c,c)
    time_act=t.datetime(1980,1,1)
    time_step=t.timedelta(1)
    c.t=time_act
    i=0
    start = time.time()
    while time_act<t.datetime(1980,9,30):
        i+=1
        if management.issowing(time_act) == True:
            wheat=field.plant
        if management.isharvest(time_act) == True:
            del field.plant
        if field.plant.Count>=1:
            field(time_act,'day',1.)
            c.flux=[s_h*-1. for s_h in plant.water.uptake]
        else:
            c.flux=[0]*50
        if i%1==0:
            if Plant.Count>=1:
                print time_act, 'ET %4.2f, sh %4.2f,comp %4.2f, sh_comp %4.2f' % (plant.ET.reference,sum(plant.water.uptake),sum(plant.water.compensation),sum(plant.water.s_h_compensated))
                #print time_act ,'fgi',['%4.2f' %  a for a in plant.root.fgi][:10],sum(plant.root.fgi)
                #print time_act,'pF',['%4.2f' % a for a in c.pF][:10]
                #print time_act, 's_p', ['%4.2f' % u for u in plant.s_p]
                #print time_act, 's_h', ['%4.2f' % u for u in plant.water.uptake]
                #print time_act, 'alpha', ['%4.2f' % u for u in plant.water.alpha]#[:10]
                #print time_act, 's_h_comp', ['%4.2f' % u for u in plant.water.uptake_comp]#[:10]
                #print time_act, 'flux',['%4.2f' % f for f in c.flux][:10]
            else:
                print 'No plant'
        c.run(cmf.day)
        time_act+=time_step
    elapsed = (time.time() - start)

print elapsed