from CG_plant import *
from pylab import *
from datetime import *
from CG_tools import *

# Inferface from FlowerPower for soil interaction
class Soil:
    def __init__(self):
        pass
    def get_pressurehead(self,depth):
        return 400.
    def get_nutrients(self,depth):
        return 10
    def get_bulkdensity(self,depth):
        return 1.5
    def get_profile(self):
        return [i*10. for i in range(1,21)]

class Atmosphere:
    def __init__(self):
        pass
    def get_tmin(self,time):
        return 10.
    def get_tmax(self,time):
        return 25.
    def get_etp(self,time):
        return 5.

#Parameter development:
stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
               ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',2000.]]#'Maturity',1665.

#Parameter partitioning:
root_fraction=[[160.,1.],[901.,0.5],[1665.,0.]]
shoot_fraction=[[160.,0.],[901.,0.5,],[1665.,1.,]]
leaf_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
stem_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
storage_fraction=[[160.,0.],[901.,0.0],[1174.,0.25],[1665.,1.]]

#Create plant with default values
plant=Plant(stage,root_fraction,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction)

#Model time amd lsit for results
thermaltime=[];biomass=[];shoot=[];root=[];stem=[];leaf=[];storage=[];root_depth=[];water_profile=[]
time_act=datetime(2000,1,1)
time_end=datetime(2000,12,31)
time_step=timedelta(1)#daily

#Interfaces
soil=Soil()
atmosphere=Atmosphere()

while time_act<time_end:
    plant(time_act,'day',time_step.days,soil,atmosphere)
    thermaltime.append(plant.thermaltime);biomass.append(plant.Wtot)
    shoot.append(plant.shoot.Wtot);root.append(plant.root.Wtot)
    root_depth.append(plant.root.depth)
    leaf.append(plant.shoot.leaf.Wtot);stem.append(plant.shoot.stem.Wtot);storage.append(plant.shoot.storage_organs.Wtot)
    time_act+=time_step
    if plant.uptake!=[]:print plant.uptake[-1][5]

    
results=([['thermaltime',thermaltime],['plant',biomass],['shoot',shoot],['root',root],['leaf',leaf],['stem',stem],['storage',storage],['root_depth',root_depth]])
graph=Graph()
for r in results:
    graph(r[0],r[1])                  
graph.plot()



    
    
    