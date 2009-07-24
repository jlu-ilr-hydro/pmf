from pylab import *
from environment import *
from simulation import *
from plant import *
from Fuzzy import *

sink_therm=FuzzySet([0.,1.,500.,16000.])

atmosphere=Atmosphere() #Class with etp,tmax and tmin
atmosphere.default_values() #List for etp,tmax and tmin with static values

soil=Soil()
for depth in arange(10,210,10): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,0.05,400) # lowerlimit,bulkdensity,wetness,nutrients


plant=Plant(soil,atmosphere)#shootpercent=0.7,leaf_appearance=1,rootpercent=0.3,tb=5.,growth_factor=0.05,W_max=1000
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
water_S_p=[]
water_S_h=[]
while sim.act_time<=sim.end: #1.1.2009 till 31.12.2009
    if sim.act_time>=sim.sowing and plant.gdd<plant.growingseason.stage[-1].gdd: #Condition for Growth start and end
        GDD_rate = plant.growingseason.thermaltime(atmosphere.get_tmin(sim.act_time),atmosphere.get_tmax(sim.act_time),plant.tb)#Thermal time
        plant.gdd+=GDD_rate#Total Thermal time
        W_pot=plant.assimilate(plant.W_tot, plant.W_max, plant.growth_factor)#drymass assimilation with logistic growth func
        T_p=plant.perspire(plant.atmosphere.get_etp(sim.act_time))
        Z_r=plant.root.depth
        for horizon in soil:
            if horizon.upper_limit<plant.root.depth: #no compensation, water uptake is limited to water pressure head above wilting point and oxygen dificiency
                if horizon.lower_limit<=plant.root.depth:
                    z=horizon.lower_limit
                    S_p.append(plant.root.wateruptake_homogeneous(T_p,Z_r)*horizon.depth)
                    h=horizon.pressure_head
                    alpha=sink_therm(h)
                    S_h.append(plant.root.wateruptake_homogeneous(T_p,Z_r)*horizon.depth*alpha)
                else:
                    residual_depth=plant.root.depth-horizon.upper_limit
                    z=plant.root.depth
                    S_p.append(plant.root.wateruptake_homogeneous(T_p,Z_r)*residual_depth)
                    h=horizon.pressure_head
                    alpha=sink_therm(h)
                    S_h.append(plant.root.wateruptake_homogeneous(T_p,Z_r)*residual_depth*alpha)         
        stress=0
        W_act=W_pot-W_pot*stress
        plant.shoot.W_tot=plant.shoot.W_tot+plant.shoot.partitioning(W_act,plant.shoot.shootpercent)*sim.step.days #aboveground dry matter
        plant.root.W_tot=plant.root.W_tot+plant.root.partitioning(W_act,plant.root.rootpercent)*sim.step.days #belowground dry matter
        plant.root.depth+=plant.root.elongation(1,1)
        plant.W_tot=plant.W_tot+W_act*sim.step.days # total dry matter
    sim.act_time+=sim.step
    