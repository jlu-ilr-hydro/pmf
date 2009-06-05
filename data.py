from sebi_enviroment import *
from pylab import *
###Weather
#tmin,tmax,tp

#weatherdata:
data_tmax  = arange(0,364)
data_tmin  = arange(0,364)
data_tmax[0:364] = 10
data_tmin[0:364] = 5
data_tmax[91:240] = 30
data_tmin[91:240] = 20

data_etp=arange(0,364)
data_etp[0:364]=10
data_etp[200:250]=10

#soildata:
soil=Soil()
soil.addhorizon(30,0.9,2,1)
soil.addhorizon(100,0.5,5,1)
soil.addhorizon(200,0.2,3,1)
for horizon in soil:
    horizon.nutrient=10
a=arange(0,364)
b=arange(0,364)
c=arange(0,364)
a[0:364]=1
b[0:364]=5
c[0:364]=4
data_wetness=[a,b,c]

atmosphere=Atmosphere(data_etp, data_tmin,data_tmax)



