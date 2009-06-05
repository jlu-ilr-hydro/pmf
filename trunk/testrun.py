from pylab import *
from SimpleGrowth import *
from standalone import *



p = Plant() 

#development data
v=Vegetationperiod(p)
v.addstage('Emergence',500)
v.addstage('Anthesis', 1000)
v.addstage('Maturity',3000)



###################################################
###################################################
#RUN


plotgrowth = []
plotrootgrowth = []
plotshootgrowth = []
plotrootelongation = []
plotlai = []
plottt=[]
plotplantrespiration=[]
plotrootrespiration=[]
plotshootrespiration=[]

time = arange(0,364)
for doy in time:
        soil_water_content=0
        for horizon in s:
            horizon.wetness=data_wetness[doy]
            soil_water_content+=horizon.wetness
        print p.root.water_uptake(20)
        p.vegetationperiod.tmax=data_tmax[doy]
        p.vegetationperiod.tmin = data_tmin[doy]
        plotgrowth.append(p.grow())
        plotrootgrowth.append(p.root.drymass)
        p.root.resistance = s.getresistance(p.root.rootingdepth)
        plotrootelongation.append(p.root.rootingdepth*-1)
        plotshootgrowth.append(p.shoot.drymass)
        plotlai.append(p.shoot.leaf.lai)
        plotplantrespiration.append(p.respire())
        plotrootrespiration.append(p.root.respiration)
        plotshootrespiration.append(p.shoot.respiration)
        plottt.append(p.vegetationperiod.tt)   
        if  v.getstage(p.vegetationperiod.tt) <= v[-1].cdd:
            break

#Dry mass in each horizon: 
rootdensity = p.root.drymass/p.root.rootingdepth

s.horizonvalues()

for horizon in s:
    if horizon.upperlimit < p.root.rootingdepth:
        if horizon.lowerlimit > p.root.rootingdepth:
            dlength = p.root.rootingdepth - horizon.upperlimit
            horizon.drymass = dlength * rootdensity
        else:
            horizon.drymass = horizon.length * rootdensity

for horizon in s:
    print horizon.drymass
    
print p.root.drymass

#####################################################
#PLOTTING
fig = figure()
fig.add_subplot(611)
plot(plotgrowth, label='Plant')
plot(plotshootgrowth, label='Shoot')
plot(plotrootgrowth, label='Root')
legend(loc=0)
ylabel('DM[t/ha]')
xlim(0,365)
fig.add_subplot(612)
plot(plotrootelongation, label='RootLength')
legend(loc=0)
ylabel('Length[cm]')
xlim(0,365)
legend(loc=0)
fig.add_subplot(613)    
plot(plotlai, label='LeafAreaIndex')
legend(loc=0)
ylabel('LAI[m2/m2]')
xlim(0,365)
fig.add_subplot(614)
plot(data_tmax, label='tmax')
plot(data_tmin, label='tmin')
xlim(0,365)
ylim(0,40)
legend(loc=0)
xlabel('DOY')
ylabel('Celsius')
fig.add_subplot(615)
plot(plottt, label='ThermalTime')
xlim(0,365)
legend(loc=0)
ylabel('DegreeDays')
fig.add_subplot(616)
plot(plotplantrespiration, label='Plant')
plot(plotshootrespiration, label='Shoot')
plot(plotrootrespiration, label='Root')
xlim(0,365)
legend(loc=0)
xlabel('DOY')
ylabel('kgCO2/day')
show()

