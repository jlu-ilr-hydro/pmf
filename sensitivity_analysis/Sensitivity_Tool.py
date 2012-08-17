# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:31:36 2012

@author: Pooder
"""


import numpy as np

class Measured(object):
    def __init__(self):
        self.Water0_30cm=[]
        self.Water30_60cm=[]
        self.Water60_90cm=[]

class Calculated(object):
    def __init__(self):
        self.date=[]
        self.Water0_30cm=[]
        self.Water30_60cm=[]
        self.Water60_90cm=[]
        
        
def load_measured_values():
    measured_file=file(get_Plotfiles(Plot)[0]) 
    measured_file.readline()
    for line in measured_file:
        columns = line.split(';')     
        Measured.Water0_30cm.append(columns[6])
        Measured.Water30_60cm.append(columns[7])
        Measured.Water60_90cm.append(columns[8])

def load_calculated_values():
    calculated_file=file(get_Plotfiles(Plot)[1]) 
    calculated_file.readline()
    for line in calculated_file:
        columns = line.split(',')
        Calculated.date.append(columns[0])
        Calculated.Water0_30cm.append(columns[1])
        Calculated.Water30_60cm.append(columns[2])
        Calculated.Water60_90cm.append(columns[3])


def get_Plotfiles(Plot):
    if Plot==1:
        Messwerte='Measured_Water_content_Plot1.csv'
        Ergebnisse='Calculated_Watercontent_Plot1.csv'
    if Plot==2:
        Messwerte='Measured_Water_content_Plot2.csv'
        Ergebnisse='Calculated_Watercontent_Plot2.csv'
    if Plot==3:
        Messwerte='Measured_Water_content_Plot3.csv'
        Ergebnisse='Calculated_Watercontent_Plot3.csv'
    return Messwerte,Ergebnisse

        
class Analysis:
    def __init__(self,model,runtimeloop,evaluationData,modelData,ForcingData):
        self.model=model
        self.runtimeloop=runtimeloop
        self.evaluationData=evaluationData
        self.modelData=modelData # Numpy structured array 
    
    @property
    def corr_coeff(self,par='Wetness_30cm'):
        model_data = self.modelData
        evaluation_data = self.evaluationData
        cc =   np.corrcoef(model_data,evaluation_data)[0,1]
        return cc
        
    @property
    def r_squared(self,par):
        return self.corr_coeff(par)**2
        
    @property
    def NashSutcliffe(self,par):
        return None
        
    @property
    def Bias(self,par):
        return None
        
    def __call__(self,start,end):
        step=1
        time_actual=start
        while time_actual < (end-start):
            self.runtimeloop(step,self.model,self.modelData)
            step+=1
            
            
        print 'finish'
        return True
        
class RuntimeLoop:
    def __init__(self):
        None
    def __call__(step,model,modelData):
        model.run(step)
        modelData.append(np.sum(model.wetness[:6]))
        
        
model = None#cmf1D()
runtimeloop=RuntimeLoop()

evaluationData=[]




sensI = Analysis(model=model,runtimeloop=runtimeloop,evaluationData=evaluationData,modelData=[],ForcingData=[])

if __name__=='__main__':
    
    
    Plot=1#select values 1-3 to get differnt plots in Muencheberg
    
    Measured=Measured()
    Calculated=Calculated()
    load_measured_values()
    load_calculated_values()
 
    Messtiefe=Measured.Water0_30cm#select
    Berechnungstiefe=Calculated.Water0_30cm#select  
    
    
    cc =   np.corrcoef(Messtiefe,Berechnungstiefe)[0,1]
       
       
       
       
    #######Plot############## 
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.text(13, 3, 'r='+str(round(cc,4)), size=20,
         ha="center", va="center",
         bbox = dict(boxstyle="round",
                     ec=(1., 0.5, 0.5),
                     fc=(1., 0.8, 0.8),
                     )
         )
    x=Berechnungstiefe
    y=Messtiefe
    plt.plot(x,label='Calculated (CMF)')
    plt.plot(y,label='Measured (Kersebaum) ')
    plt.legend()
    plt.xlim(0,26,1)
    plt.ylim(0,35,1)
    ax.set_xlabel('Number of Measurements')
    ax.set_ylabel('Water Content [%]')    
    plt.draw()    
    plt.show()

  