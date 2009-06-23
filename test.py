from pylab import *
from enviroment import *

soil=Soil()
soil.default_values() # soil with static values, defined in modul enviroment
rooting_depth=87 # plant values ...
water_demand=197
nutrient_demand=1000

water_uptake=[]
nutrient_uptake=[]
nutrients=[] #List for daily nutrient_profile
wetness=[] # list for daily wetness_profile
depth=0
depth_step=1 # step for data request
while depth<=rooting_depth:
    if sum(water_uptake) < water_demand: # Condition, if water uptake occurs
        water_uptake.append(soil.get_wetness(depth)*depth_step) #water_uptake: wetness(depth) * depth_step
    else:
        water_uptake.append(0)
    if sum(nutrient_uptake) < nutrient_demand: #Condition, if nutrient uptake occurs
        nutrient_uptake.append(soil.get_wetness(depth)*depth_step*(soil.get_nutrients(depth)))  #passive nutrient_uptake: water_uptake(depth) * nutrient_conc(depth)
    else:
        nutrient_uptake.append(0)        
    depth+=depth_step
print water_uptake
print nutrient_uptake
print sum(nutrient_uptake)
print sum(water_uptake)

