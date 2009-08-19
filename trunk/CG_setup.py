from CG_plant import *
from CG_tools import *
from CG_environment import *
from pylab import *

#Parametrisation environment
soil=Soil()
atmosphere=Atmosphere()
atmosphere.default_values() #List for etp,tmax and tmin with static values
soil=Soil()
for depth in arange(10.,210.,10.): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,1.,400.) # lowerlimit,bulkdensity,wetness,nutrients,pressurehead

#Parametrisation plant
plant=Plant(soil,atmosphere,5.,1000.,0.05)

#Parametrisation plant: Development
plant.stage.__setitem__(160.,'Emergence');plant.stage.__setitem__(208.,'Leaf development');plant.stage.__setitem__(421.,'Tillering');plant.stage.__setitem__(659.,'Stem elongation')
plant.stage.__setitem__(901.,'Anthesis');plant.stage.__setitem__(1174.,'Seed fill');plant.stage.__setitem__(1556.,'Dough stage');plant.stage.__setitem__(1665.,'Maturity')

#Parametrisation plant: development depending partitioning
plant.phenological_event.__setitem__(); plant.phenological_event[0].__setitem__(160.,1.); plant.phenological_event[0].__setitem__(901.,0.5);plant.phenological_event[0].__setitem__(1665.,0.)
plant.phenological_event.__setitem__(); plant.phenological_event[1].__setitem__(160.,0.); plant.phenological_event[1].__setitem__(901.,0.5); plant.phenological_event[1].__setitem__(1665.,1.)
plant.phenological_event.__setitem__(); plant.phenological_event[2].__setitem__(160.,0.); plant.phenological_event[2].__setitem__(901,0.5); plant.phenological_event[2].__setitem__(1174,0.375); plant.phenological_event[2].__setitem__(1665.,0.)
plant.phenological_event.__setitem__(); plant.phenological_event[3].__setitem__(160.,0.); plant.phenological_event[3].__setitem__(901,0.5); plant.phenological_event[3].__setitem__(1174,0.375); plant.phenological_event[3].__setitem__(1665.,0.)
plant.phenological_event.__setitem__(); plant.phenological_event[4].__setitem__(160.,0.); plant.phenological_event[4].__setitem__(901,0.0); plant.phenological_event[4].__setitem__(1174,0.25); plant.phenological_event[4].__setitem__(1665.,0.)
rootability_thresholds=[1.5,0.5,16000,0.9,0.0,0.0]

h_plant=[0.,1.,500.,16000.]
plant_N=[[160.,0.43],[1174.,0.16]]
lai_conversion=1.


thermaltime=[];plant_biomass=[];root=[];shoot=[];leaf=[];stem=[];storage_organs=[]
root_elongation=[];water_uptake=[];nutrient_uptake=[]
def run(time_act,time_period,time_step,sowing_date):
    run_end=time_act+time_period
    while time_act<=run_end:
        if time_act>=sowing_date:
            plant(time_act,time_step.days,0.5,0.5,h_plant,plant_N,lai_conversion,rootability_thresholds)
        thermaltime.append(plant.thermaltime);plant_biomass.append(plant.Wtot); root.append(plant.root.Wtot);shoot.append(plant.shoot.Wtot);leaf.append(plant.shoot.leaf.Wtot);stem.append(plant.shoot.stem.Wtot);storage_organs.append(plant.shoot.storage_organs.Wtot)
        time_act+=time_step
run(datetime(2009,1,1),timedelta(365),timedelta(1.),datetime(2009,1,1))
graph=Graph()
graph.__setitem__('Thermaltime',thermaltime,'doy','GDD');graph.__setitem__('Plant', plant_biomass, 'doy', 'biomass')
graph.__setitem__('root', root, 'doy', 'biomass');graph.__setitem__('shoot', shoot, 'doy', 'biomass')
graph.__setitem__('leaf', leaf, 'doy', 'biomass');graph.__setitem__('stem', stem, 'doy', 'biomass')
graph.__setitem__('storage_organs', storage_organs, 'doy', 'biomass')
graph.plot()





