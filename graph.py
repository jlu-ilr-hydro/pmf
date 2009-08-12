from pylab import *
from time import *

"""
Probleme:
    - die Abbildungen sollen sich gleichzeitig aktualisieren
    - die Axen sollen fest sein, von Anfang an (habs mit axes() und anderen befeheln ausprobiert
      geht nicht, weil dann immer ein extra plot mit den festen axen erstellt wird 
    - habe einfach listen mit nullen gefuellt, is aber irgendwie gemogelt
"""

Wtot=1.
GDD=0.
grow = lambda Wtot: Wtot*0.05*(1.-Wtot/1000)
develope = lambda tmax,tmin: (tmax-tmin)/2.
drymass=zeros(365)
development=zeros(365)

ion()
hold(False)
fig=figure()


for i in range(300):
    Wtot=Wtot+grow(Wtot)
    drymass[i]+=Wtot
    fig.add_subplot(211)
    plot(drymass)
    GDD=GDD+develope(25.,10.)
    development[i]+=GDD
    fig.add_subplot(212)
    plot(development)
    sleep(0.)
    

