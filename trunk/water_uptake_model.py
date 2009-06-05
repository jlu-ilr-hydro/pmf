from pylab import *
from enviroment import *

s=Soil()
s.addhorizon(5, 1, 0., 5)
s.addhorizon(60, 1, 15., 5)
s.addhorizon(90, 1, 10., 5)

def water_uptake(wetness,demand):
    return min(wetness,demand)

rooting_depth=10.
water_demand=100.
root_demand=water_demand/rooting_depth
wetness=[]
water=[]
stress=[]
profile=arange(0.,rooting_depth,1.)

for depth in profile:
    wetness.append(s.get_wetness(depth))
for w in wetness:
    water.append(water_uptake(w,root_demand))

        

w=array(wetness)-array(water)
print sum(wetness)
print root_demand
print sum(water)
    

