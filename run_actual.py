from pylab import *
from environment import *
from simulation import *
from plant import *

atmosphere=Atmosphere() #Class with etp,tmax and tmin
atmosphere.default_values() #List for etp,tmax and tmin with static values

soil=Soil()
for depth in arange(10,210,10): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,1) # lowerlimit,bulkdensity,wetness,nutrients
    
plant=Plant(soil,atmosphere)#shootpercent=0.7,leaf_appearance=1,rootpercent=0.3,root_elongation=0.5,tb=5.,growth_factor=0.05,W_max=1000
plant.growingseason.__setitem__(0,'Emergence',160) #GDD in Celisus
plant.growingseason.__setitem__(1,'Leaf development',208)
plant.growingseason.__setitem__(2,'Tillering',421)
plant.growingseason.__setitem__(3,'Stem elongation',659)
plant.growingseason.__setitem__(4,'Anthesis',901)
plant.growingseason.__setitem__(5,'Seed fill',1174)
plant.growingseason.__setitem__(6,'Dough stage',1556)
plant.growingseason.__setitem__(7,'Maturity complete',1665)

sim=Simulation(sowing=datetime(2009,3,1))#start=datetime(2009,1,1),end=datetime(2009,12,31),step=timedelta(1)
GDD=[] # List for results
W_tot=[] # List for results
while sim.act_time<=sim.end: #1.1.2009 till 31.12.2009
    if sim.act_time>=sim.sowing and plant.gdd<plant.growingseason.stage[-1].gdd: #Condition for Growth start and end
        GDD_rate = plant.growingseason.thermaltime(atmosphere.get_tmin(sim.act_time),atmosphere.get_tmax(sim.act_time),plant.tb)#Thermal time
        plant.gdd+=GDD_rate#Total Thermal time
        plant.W_tot+=1# test
    sim.result(GDD,plant.gdd)#results
    sim.result(W_tot,plant.W_tot)#results
    sim.act_time+=sim.step

sim.graph(1)#number of rows in window, pot results







