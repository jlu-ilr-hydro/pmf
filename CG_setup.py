from cg_plant import *
from cg_tools import *
from pylab import *
from datetime import *

def set_development(growinseason):
    for stage in growingseason[0]:
        plant.stage.__setitem__(stage,growingseason[1][growingseason[0].index(stage)])

def set_event(events,count):
    plant.phenological_event.__setitem__(events[0][2])
    for event in events:
        plant.phenological_event[count].__setitem__(event[2],event[0],event[1])

def grow(time_act,time_step,soil,atmosphere):
    plant(time_act,time_step,soil,atmosphere)
    
    
def graph(list):
    g=Graph()
    for item in list:
        g.__setitem__(item[0],item[1])
    g.plot()

#Parameter development:
growingseason=[[160.,208.,421.,659.,901.,1174.,1556.,1665.],
               ['Emergence','Leaf development','Tillering','Stem elongation','Anthesis','Seed fill','Dough stage','Maturity']]

#Parameter partitioning:
event1=[[160.,1.,'root'],[901.,0.5,'root'],[1665.,0.,'root']]
event2=[[160.,0.,'shoot'],[901.,0.5,'shoot'],[1665.,1.,'shoot']]
event3=[[160.,0.,'leaf'],[901.,0.5,'leaf'],[1174.,0.375,'leaf'],[1665.,0.,'leaf']]
event4=[[160.,0.,'stem'],[901.,0.5,'stem'],[1174.,0.375,'stem'],[1665.,0.,'stem']]
event5=[[160.,0.,'storage'],[901.,0.0,'storage'],[1174.,0.25,'storage'],[1665.,1.,'storage']]

#Create plant with default values
plant=Plant()

#Create development and partitioning parameter
set_development(growingseason) #set development
set_event(event1,0) #set root part
set_event(event2,1) #set shoot part
set_event(event3,2) #set leaf part
set_event(event4,3) #set stem part
set_event(event5,4) #set storage organs part
