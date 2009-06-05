from datetime import *
from pylab import *

class Plant:
    def __init__(self):
        self.total_drymass=1 # Gesamte Trochenmasse in [kg]
        self.actual_growth=0 # Wachstumsrate pro Zeiteinheit [kg/Tag], oder [kg/Schritt]
    def grow(self,step): #Wachstumsfunktion, die alle anderen Funktionen von Pflanze aufruft
        self.actual_growth=self.assimilate(self.total_drymass,1000,0.05)
        self.total_drymass=self.total_drymass+self.actual_growth*step
        #self.wateruptake ...
        #self.nutrientuptkae...
        #self.stress ...
        #self.root.grow(self.soil.get_bulkdensity(depth)--> soll hier der Boden abgefragt werden oder in Hauptschleife?
    def assimilate(self,W_total,K,r): #Logistisches Wacshtum
        return r*W_total*(1.0-W_total/K)


class Simulation:
    def __init__(self,start=datetime(2009,1,1),end=datetime(2009,12,31),step=timedelta(1)):
        self.start=start
        self.end=end
        self.step=step
        self.time=self.start
    def run(self): # könnte die Schleife steuern
        pass 
    def grafics(self): # Methode für die Aufbereitung der Ergebnisse in Grafikeb
        pass
    def results(self): # SollErgebnisse irgendwie Aufbereiten
        pass

s=Simulation()
p=Plant()#an dieser Stelle wird im richtigen Modul Boden und Atmospäre übergeben: p=Plant(Soil,Atmosphere)
total_harvest=[]
harvest=datetime(2009,9,30)
while s.time < s.end:
    total_harvest.append(p.total_drymass)
    p.grow(s.step.days)
    s.time+=s.step
    if s.time == harvest:
        break
    
    
    
plot(total_harvest)
show()
  


