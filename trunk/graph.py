from pylab import *
from datetime import *

time_act=datetime(1980,1,1)


grow = lambda Wtot: Wtot*0.05*(1.-Wtot/1000)
Wtot=1.
ion()
x = range(7670)
biomass = zeros(7670)
line, = plot(x,biomass)
ylim(0,1000)
i=1


res=[]
while time_act <datetime(1984,12,31):
    res.append(1)
    Wtot+=grow(Wtot)
    biomass[i]+=Wtot
    i+=1
    if i%28==0:
        line.set_ydata(biomass)
        draw()
    time_act+=timedelta(1)
print len(res)
show()