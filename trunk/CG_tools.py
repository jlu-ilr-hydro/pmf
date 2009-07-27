from datetime import *
from pylab import *

class Simulation:
    def __init__(self,sowing=datetime(2009,1,1),start=datetime(2009,1,1),end=datetime(2009,12,31),time_step=timedelta(1)):
        self.start=start
        self.end=end
        self.time_step=time_step
        self.time_act=self.start
        self.sowing=sowing
        self.results=[]         
    def result(self,name,value):
        try:
            self.results[self.results.index(name)].append(value)
        except ValueError:
            self.results.append(name)
            self.results[self.results.index(name)].append(value)
    def graph(self,rows):
        fig=figure()
        for result in self.results:
            fig.add_subplot(len(self.results),rows,self.results.index(result)+1)
            plot(result)
        show()
        
