from simple_growth import *
from enviroment import *
from pylab import *

########################################################################################################
########################################################################################################
#### Soil and atmosphere interface
soil=Soil()
soil.default_values()
atmosphere=Atmosphere()
atmosphere.default_values()
########################################################################################################
########################################################################################################
#### Plant implementation
p=Plant(soil,atmosphere)
p.growingseason.__setitem__(0,'Emergence',500)
p.growingseason.__setitem__(1,'Maturity',5000)

########################################################################################################
########################################################################################################
#### Time variables
total_thermaltime=0.
total_drymass=1.
root_total_drymass=0.
shoot_total_drymass=0
total_respiration=0.
root_total_respiration=0.
shoot_total_respiration=0.
total_depth=0.
total_leafs=0.

########################################################################################################
########################################################################################################
#### Plot variables
plot_nutrient_demand=[]
plot_water_demand=[]
plot_water_uptake=[]
plot_nutrient_uptake=[]
plot_stress_factor=[]
plot_total_thermaltime=[]
plot_total_drymass=[]
plot_root_total_drymass=[]
plot_shoot_total_drymass=[]
plot_total_respiration=[]
plot_root_total_respiration=[]
plot_shoot_total_respiration=[]
plot_root_total_drymass=[]
plot_total_rootingdepth=[]
plot_total_leafs=[]
plot_tmin=[]
plot_tmax=[]
plot_etp=[]
plot_wetness=[]
plot_nutrient_conc=[]
plot_bulkdensity=[]

########################################################################################################
########################################################################################################
#### Growing season (1 year)
time = arange(364)
for doy in time:
    ########################################################################################################
    ########################################################################################################
    #### Model calculations
    thermaltime=p.growingseason.thermaltime(p.atmosphere.get_tmin(doy),p.atmosphere.get_tmax(doy),p.tb)
    total_thermaltime+=thermaltime
    stage=p.growingseason.getstage(total_thermaltime)
    potential_growthrate=p.assimilate(total_drymass, p.W_max, p.growth_factor)
    water_demand=p.perspire(p.atmosphere.get_etp(doy))
    nutrient_demand=p.nutrientdemand(potential_growthrate, 0.01)
    wetness=[]
    nutrients=[]
    profile=arange(1,total_depth,1)#vorrausgesetzt, wetness gibt die feucht pro cm an
    
    for depth in profile:
        wetness.append(p.soil.get_wetness(depth))
        nutrients.append(p.soil.get_nutrients(depth))
    water_content=sum(wetness)
    water_uptake=p.wateruptake(water_demand, water_content)
    w=array(wetness)
    n=array(nutrients)
    nutrient_content=sum(w*n)
    nutrient_conc=sum(n)/n.size
    
    nutrient_uptake=p.nutrientuptake(nutrient_demand, water_uptake, nutrient_conc, nutrient_content)
    stress_factor=p.stress(water_uptake, water_demand, nutrient_uptake, nutrient_demand)
    actual_growthrate=potential_growthrate-potential_growthrate*stress_factor
    
    respirationrate=p.respire(total_drymass,actual_growthrate, 0.05, 0.5)
    #total_respiration+=respirationrate
    #root_growthrate=p.root.partitioninggrowth(actual_growthrate,p.root.rootpercent)
    #root_total_drymass+=root_growthrate
    #root_respirationrate=p.root.respire(root_total_drymass,root_growthrate, 0.05, 0.5)
    #root_total_respiration+=root_respirationrate
    #rootingrate=p.root.elongation(soil.get_bulkdensity(total_depth),p.root.elongation_factor)
    #total_depth+=rootingrate
    #shoot_growthrate=p.shoot.partitioninggrowth(actual_growthrate,p.shoot.shootpercent)
    #shoot_total_drymass+=shoot_growthrate
    #shoot_respirationrate=p.shoot.respire(shoot_total_drymass,shoot_growthrate, 0.05, 0.5)
    #shoot_total_respiration+=shoot_respirationrate
    #leafrate=p.shoot.leaf.grow(p.shoot.leaf.appearance_rate)
    #total_leafs+=leafrate
    total_drymass+=actual_growthrate
    ########################################################################################################
    ########################################################################################################
    #### Plotting  
    plot_total_thermaltime.append(total_thermaltime)
    plot_nutrient_demand.append(nutrient_demand)
    plot_water_demand.append(water_demand)
    plot_water_uptake.append(water_uptake)
    plot_nutrient_uptake.append(nutrient_uptake)
    plot_stress_factor.append(stress_factor)
    plot_total_drymass.append(total_drymass)
    plot_total_respiration.append(total_respiration)
    plot_root_total_drymass.append(root_total_drymass) 
    plot_root_total_respiration.append(root_total_respiration)
    plot_total_rootingdepth.append(total_depth)
    plot_shoot_total_drymass.append(shoot_total_drymass)
    plot_shoot_total_respiration.append(shoot_total_respiration)
    plot_total_leafs.append(total_leafs)
    plot_tmin.append(p.atmosphere.get_tmin(doy))
    plot_tmax.append(p.atmosphere.get_tmax(doy))
    plot_etp.append(p.atmosphere.get_etp(doy))
    plot_bulkdensity.append(soil.get_bulkdensity(total_depth))
    plot_wetness.append(soil.get_wetness(total_depth))
    plot_nutrient_conc.append(soil.get_nutrients(total_depth))

fig1=figure()
fig1.add_subplot(511)
plot(plot_total_drymass,label='Plant')
plot(plot_shoot_total_drymass,label='Shoot')
plot(plot_root_total_drymass,label='Root')
legend(loc=0)
ylabel('Drymass[g]')
xlim(0,365)
title('Development and Growth')
fig1.add_subplot(512)
plot(plot_total_respiration,label='Plant')
plot(plot_shoot_total_respiration,label='Shoot')
plot(plot_root_total_respiration,label='Root')
legend(loc=0)
ylabel('Respiration [-]')
xlim(0,365)
fig1.add_subplot(513)
plot(plot_total_rootingdepth,label='Rootingdepth')
legend(loc=0)
ylabel('Depth [cm]')
xlim(0,365)
fig1.add_subplot(514)
plot(plot_total_leafs,label='LAI')
legend(loc=0)
ylabel('Leafs[Leaf]')
xlim(0,365)
fig1.add_subplot(515)
plot(plot_total_thermaltime,label='Thermaltime')
legend(loc=0)
ylabel('GDD')
xlim(0,365)
xlabel('DOY')

fig2=figure()
fig2.add_subplot(311)
plot(plot_water_demand,label='Waterdemand')
plot(plot_water_uptake,label='Wateruptake')
legend(loc=0)
ylabel('[mm]')
xlim(0,365)
ylim(0,50)
title('Water- and Nutrient balance')
fig2.add_subplot(312)
plot(plot_nutrient_demand,label='Nutrientdemand')
plot(plot_nutrient_uptake,label='Nutrientuptake')
legend(loc=0)
ylabel('[g]')
xlim(0,365)
fig2.add_subplot(313)
plot(plot_stress_factor,label='Stressfactor')
legend(loc=0)
ylabel('[-]')
xlim(0,365)
ylim(-0.5,1.5)
xlabel('DOY')

fig3=figure()
fig3.add_subplot(311)
plot(plot_tmin,label='Tmin')
plot(plot_tmax,label='Tmax')
legend(loc=0)
ylabel('[Celsius]')
xlim(0,365)
ylim(-10,30)
title('Enviroment')
fig3.add_subplot(312)
plot(plot_etp,label='ETpot')
legend(loc=0)
ylabel('[mm]')
xlim(0,365)
ylim(0,50)
fig3.add_subplot(313)
plot(plot_wetness,label='Wetness')
plot(plot_nutrient_conc,label='Nutrient_Conc')
plot(plot_bulkdensity,label='Bulkdensity')
legend(loc=0)
ylabel('[-]')
xlim(0,365)
ylim(0,100)
xlabel('DOY')

show()


