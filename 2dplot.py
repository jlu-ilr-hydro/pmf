from pylab import *
from datetime import *

time_act=datetime(2009,1,1)
time_step=timedelta(1)
depth=87.

water=[]

for days in range(4):    
    water.append([])
    for depth in arange(0.,depth,1.):
        water[time_act.day-1].append(depth)
    time_act+=time_step  

print water
print datetime(2009,1,9)

