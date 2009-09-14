from CG_plant import *
from CG_tools import *
from pylab import *
from datetime import *

def grow(time_act,time_step,soil,atmosphere):
    plant(time_act,time_step,soil,atmosphere)
        
    
    
def graph(list):
    g=Graph()
    for item in list:
        g.__setitem__(item[0],item[1])
    g.plot()

#Parameter development:
stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
               ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]]

#Parameter partitioning:
penetrated_layer=[[160.,1.],[901.,0.5],[1665.,0.]]
shoot_fraction=[[160.,0.],[901.,0.5,],[1665.,1.,]]
leaf_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
stem_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
storage_fraction=[[160.,0.],[901.,0.0],[1174.,0.25],[1665.,1.]]

#Create plant with default values
plant=Plant(stage,penetrated_layer,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction)
