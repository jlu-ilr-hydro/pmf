from datetime import *
from pylab import *
from simple_growth import *
from enviroment import *


class Simulation:
    def __init__(self,plant,start=datetime(2009,1,1),end=datetime(2009,12,31),step=timedelta(1)):
        self.start=start
        self.end=end
        self.step=step
        self.act_time=self.start
        self.plant=plant
        self.results=[[],[],[],[],[],[],[],[],[],[]]
    def run(self):
        while self.act_time<self.end:
            self.plant.grow(self.step,self.act_time)
            self.result(self.plant.values)
            self.act_time+=self.step
            
    def result(self,values):
        for i in range(len(values)):
            self.results[i].append(values[i])
    def graph(self):
        names=['W_pot','W_act','self.W_tot','gdd_rate','water_demand','nutrient_demand','water_uptake','nutrient_uptake','stress_factor','R']
        fig=figure()
        for i in range(len(self.results)):
            fig.add_subplot(len(self.results),1,i+1)
            plot(self.results[i],label=names[i])
            legend(loc=0)            
        show()
            

soil=Soil()
soil.default_values()
atmosphere=Atmosphere()
atmosphere.default_values()
plant=Plant(soil,atmosphere)
sim=Simulation(plant)
sim.run()
sim.graph()
  


