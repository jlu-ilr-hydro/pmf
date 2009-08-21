from datetime import *
from pylab import *

class Graph():
    def __init__(self,name='',values=[]):
        self.graphs=[]
        self.values=values
        self.name=name
    def __setitem__(self,name,values):
        self.graphs.append(Graph(name,values))
    def __getitem__(self,index):
        return self.graphs[index]
    def __iter__(self):
        for graph in self.graphs:
            yield graph
    def __call__(self,name,values):
        self.__setitem__(name,values)
    def plot(self):
        fig=figure()
        for graph in self.graphs:
            fig.add_subplot(len(self.graphs),1,self.graphs.index(graph)+1)
            plot(graph.values,label=graph.name)
            legend(loc=0)
            xlim(0,365)
        show()


    
   