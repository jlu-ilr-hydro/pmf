from pylab import *
grow = lambda Wtot: Wtot*0.05*(1.-Wtot/1000)
Wtot=1.
ion()
x = range(365)
biomass = zeros(365)
line, = plot(x,biomass)
ylim(0,1000)
print len(x)
for i in range(365):
    Wtot+=grow(Wtot)
    biomass[i]+=Wtot
    line.set_ydata(biomass)
    draw()
