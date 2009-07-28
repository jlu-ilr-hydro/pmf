from CG_plant import *
from CG_tools import *
from CG_environment import *
from pylab import *

plant=Plant()
sim=Simulation()
soil=Soil()
atmosphere=Atmosphere()

atmosphere=Atmosphere() #Class with etp,tmax and tmin
atmosphere.default_values() #List for etp,tmax and tmin with static values

soil=Soil()
for depth in arange(10.,210.,10.): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,0.05,400.) # lowerlimit,bulkdensity,wetness,nutrients,pressurehead
for horizon in soil:
    if horizon.lower_limit>45and horizon.lower_limit<80:horizon.bulkdensity=1.8

#160,1665
development=[[160,208,421,659,901,1174,1556,1665],['Emergence','Leaf development','Tillering','Stem elongation','Anthesis','Seed fill','Dough stage','Maturity complete']]
critical_pressurehead=[0.,1.,500.,16000.]
Plant_drymass=[]
Plant_thermaltime=[]


def run(time_act,time_period,time_step,sowing_date):
    run_end=time_act+time_period
    while time_act<=run_end:
        if time_act>=sowing_date:
            plant(time_act,time_step.days,1000,0.05,0.5,0.3,0.7,5.0,development,soil,atmosphere,critical_pressurehead)
        sim.result(Plant_drymass, plant.Wp_total)
        sim.result(Plant_thermaltime,plant.stage.total_thermaltime)
        time_act+=time_step

run(datetime(2009,1,1),timedelta(365),timedelta(1),datetime(2009,1,1))





