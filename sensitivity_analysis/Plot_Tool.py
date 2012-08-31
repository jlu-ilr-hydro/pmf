# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:31:36 2012

@author: Pooder
"""


import numpy as np
import matplotlib.pyplot as plt
import Statistic_Tool as stat
from datetime import *
import math


#class Measured(object):
#    def __init__(self):
#        self.Water0_30cm=[]
#        self.Water30_60cm=[]
#        self.Water60_90cm=[]
#
#class Calculated(object):
#    def __init__(self):
#        self.date=[]
#        self.year=[]
#        self.month=[]
#        self.day=[]
#        self.Water0_30cm=[]
#        self.Water30_60cm=[]
#        self.Water60_90cm=[]
        
        
#def load_measured_values():
#    measured_file=file(get_Plotfiles(Plot)[0]) 
#    measured_file.readline()
#    for line in measured_file:
#        columns = line.split(';')     
#        Meas.Water0_30cm.append(columns[6])
#        Meas.Water30_60cm.append(columns[7])
#        Meas.Water60_90cm.append(columns[8])

#def load_calculated_values():
#    calculated_file=file(get_Plotfiles(Plot)[1]) 
#    calculated_file.readline()
#    for line in calculated_file:
#        columns = line.split(',')
#        Calc.year.append(columns[0])
#        Calc.month.append(columns[1])
#        Calc.day.append(columns[2])
#        Calc.Water0_30cm.append(columns[3])
#        Calc.Water30_60cm.append(columns[4])
#        Calc.Water60_90cm.append(columns[5])


#def get_Plotfiles(Plot):
#    if Plot==1:
#        Messwerte='Measured_Water_content_Plot1.csv'
#        Ergebnisse='Calculated_Watercontent_Plot = 1 and RUE = '+str(RUE)+'.csv'
#    if Plot==2:
#        Messwerte='Measured_Water_content_Plot2.csv'
#        Ergebnisse='Calculated_Watercontent_Plot = 2 and RUE = '+str(RUE)+'.csv'
#    if Plot==3:
#        Messwerte='Measured_Water_content_Plot3.csv'
#        Ergebnisse='Calculated_Watercontent_Plot = 3 and RUE = '+str(RUE)+'.csv'
#    return Messwerte,Ergebnisse


#def load_measured_values():
#    measured_file=file(get_Plotfiles(Plot)[0]) 
#    measured_file.readline()
#    for line in measured_file:
#        columns = line.split(';')     
#        Meas.stem_and_leaf.append(columns[4])
#
#    
#def load_calculated_values():
#    calculated_file=file(get_Plotfiles(Plot)[1]) 
#    calculated_file.readline()
#    for line in calculated_file:
#        columns = line.split(',')
#        Calc.year.append(columns[0])
#        Calc.month.append(columns[1])
#        Calc.day.append(columns[2])
#        Calc.stem_and_leaf.append(columns[5])

#class Analysis:
#    def __init__(self,model,runtimeloop,evaluationData,modelData,ForcingData):
#        self.model=model
#        self.runtimeloop=runtimeloop
#        self.evaluationData=evaluationData
#        self.modelData=modelData # Numpy structured array 
#    
#    @property
#    def corr_coeff(self,par='Wetness_30cm'):
#        model_data = self.modelData
#        evaluation_data = self.evaluationData
#        cc =   np.corrcoef(model_data,evaluation_data)[0,1]
#        return cc
#        
#    @property
#    def r_squared(self,par):
#        return self.corr_coeff(par)**2
#        
#    @property
#    def NashSutcliffe(self,par):
#        return None
#        
#    @property
#    def Bias(self,par):
#        return 1
#        
#    def __call__(self,start,end):
#        step=1
#        time_actual=start
#        while time_actual < (end-start):
#            self.runtimeloop(step,self.model,self.modelData)
#            step+=1
#            
#            
#        print 'finish'
#        return True
#        
#class RuntimeLoop:
#    def __init__(self):
#        None
#    def __call__(step,model,modelData):
#        model.run(step)
#        modelData.append(np.sum(model.wetness[:6]))
#        
#        
#model = None#cmf1D()
#runtimeloop=RuntimeLoop()
#
#evaluationData=[]
#
#
#
#
#sensI = Analysis(model=model,runtimeloop=runtimeloop,evaluationData=evaluationData,modelData=[],ForcingData=[])


           #RUE=4
          #r = np.load(get_Plotfiles(1)[0]).view(np.recarray)
#        load_measured_values()
#        load_calculated_values()
     
    
        
        
        #cc0_30cm = np.corrcoef(Meas.Water0_30cm,Calc.Water0_30cm)[0,1]
        #cc30_60cm = np.corrcoef(Meas.Water30_60cm,Calc.Water30_60cm)[0,1]
        #cc60_90cm = np.corrcoef(Meas.Water60_90cm,Calc.Water60_90cm)[0,1]
        
        #cc_stem_and_leaf = np.corrcoef(Meas.stem_and_leaf,Calc.stem_and_leaf)[0,1]

#        
#        Bias_values=[]
#        
#        for i in range(len(Calc.stem_and_leaf)):
#            Bias_values.append(float(Calc.stem_and_leaf[i]) - float(Meas.stem_and_leaf[i]))
#        
#        Bias_Summe.append(np.sum(Bias_values[0:len(Calc.stem_and_leaf)]))
        
        #########################
        
        
#        Datum=[]
#        for i in range(len(Calc.year)):
#            Datum.append(datetime(int(Calc.year[i]),int(Calc.month[i]),int(Calc.day[i])))
           
        #######Plot############## 
        
    
    
#        Bias_Mittelwert = Bias_Summe[Plotnumber]/6
#        print Bias_Mittelwert
#        
#        Nash_Sutcliff_Zaehler=[]
#        Nash_Sutcliff_Nenner=[]
#        Nash_Sutcliff_Summe=[]
#        for i in range(len(Calc.year)):
#            float(Meas.stem_and_leaf[i])            
#        
#        for i in range(len(Calc.year)):
#            Nash_Sutcliff_Zaehler.append((float(Meas.stem_and_leaf[i])-float(Calc.stem_and_leaf[i])**2))
#            Nash_Sutcliff_Nenner.append((float(Meas.stem_and_leaf[i])-np.sum(Nash_Sutcliff_Summe))**2)#!! np.sum muss floats bekommen 
#
#        Nash_Sutcliff_values = []
#        for i in range(len(Calc.year)):            
#            Nash_Sutcliff_values.append(Nash_Sutcliff_Zaehler[i]/Nash_Sutcliff_Nenner[i])
#        
#        Nash_Sutcliff=[]
#        Nash_Sutcliff.append(np.sum(Nash_Sutcliff_values))
       
#        fig = plt.figure()
#        ax = fig.add_subplot(111)
#        plt.text(13, 3, 'r='+str(round(cc,4)), size=20,
#             ha="center", va="center",
#             bbox = dict(boxstyle="round",
#                         ec=(1., 0.5, 0.5),
#                         fc=(1., 0.8, 0.8),
#                         )
#             )
        #if Plot==1:
        #x = linspace(0,24,24)
        
#===============Results stem and leaf==========================================
        
#            
#            if Plot ==1:
#                #ax1.set_ylim(0,35,1)
#                ax1.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
#                ax1.set_ylim(0,8000)
#                #ax1.plot(Datum,Calc.Water0_30cm,'b--')
#                ax1.plot(Datum,Calc.stem_and_leaf,'bo', ms=4,label='PMF')
#                #ax1.plot(Datum,Meas.Water0_30cm,'g--')
#                ax1.plot(Datum,Meas.stem_and_leaf,'go', ms=4,label='Kersebaum')
#                ax1.legend(loc=2, bbox_to_anchor = (0.77, 0.4),scatterpoints=0)
#                ax1.set_title('Stem and leaf [kg/ha] Plot '+str(Plot)+' with r= '+str(round(cc_stem_and_leaf,4))+' and Bias = '+str(round(Bias_Summe[Plot-1]/len(Calc.stem_and_leaf),2)))
#                ax1.grid()    
#                ax1.set_xlabel('Date')
#                ax1.set_ylabel('Stem and Leaf [kg/ha]')
#                ax1.fill_between(Datum,Calc.stem_and_leaf,Meas.stem_and_leaf,facecolor='red', alpha=0.5)    
#    
#            if Plot ==2:
#                #ax1.set_ylim(0,35,1)
#                ax2.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
#                ax2.set_ylim(0,8000)
#                #ax1.plot(Datum,Calc.Water0_30cm,'b--')
#                ax2.plot(Datum,Calc.stem_and_leaf,'bo', ms=4,label='PMF')
#                #ax1.plot(Datum,Meas.Water0_30cm,'g--')
#                ax2.plot(Datum,Meas.stem_and_leaf,'go', ms=4,label='Kersebaum')
#                #ax2.legend(loc=2, bbox_to_anchor = (0.77, 1.4),scatterpoints=0)
#                ax2.set_title('Stem and leaf [kg/ha] Plot '+str(Plot)+' with r= '+str(round(cc_stem_and_leaf,4))+' and Bias = '+str(round(Bias_Summe[Plot-1]/len(Calc.stem_and_leaf),2)))
#                ax2.grid()    
#                ax2.set_xlabel('Date')
#                ax2.set_ylabel('Stem and Leaf [kg/ha]')
#                ax2.fill_between(Datum,Calc.stem_and_leaf,Meas.stem_and_leaf,facecolor='red', alpha=0.5)    
#    
#            if Plot ==3:
#                #ax1.set_ylim(0,35,1)
#                ax3.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
#                ax3.set_ylim(0,8000)
#                #ax1.plot(Datum,Calc.Water0_30cm,'b--')
#                ax3.plot(Datum,Calc.stem_and_leaf,'bo', ms=4,label='PMF')
#                #ax1.plot(Datum,Meas.Water0_30cm,'g--')
#                ax3.plot(Datum,Meas.stem_and_leaf,'go', ms=4,label='Kersebaum')
#                #ax3.legend(loc=2, bbox_to_anchor = (0.77, 1.4),scatterpoints=0)
#                ax3.set_title('Stem and leaf [kg/ha] Plot '+str(Plot)+' with r= '+str(round(cc_stem_and_leaf,4))+' and Bias = '+str(round(Bias_Summe[Plot-1]/len(Calc.stem_and_leaf),2)))
#                ax3.grid()    
#                ax3.set_xlabel('Date')
#                ax3.set_ylabel('Stem and Leaf [kg/ha]')
#                ax3.fill_between(Datum,Calc.stem_and_leaf,Meas.stem_and_leaf,facecolor='red', alpha=0.5)    
#                
#                
#        #legend(bbox_to_anchor=(0., 3.40, 1., 2.102), loc=0,
#        #       ncol=2, mode="expand", borderaxespad=0.)
#        plt.tight_layout()
#        plt.draw()
#        plt.savefig('Stem_and_leaf for all plots and RUE = '+str(RUE), dpi=400)    
#        plt.close()            
#        
#        
#        
    
    
    
    
    
#=================Results watercontent=========================================
#        ax1 = plt.subplot(311)
#        ax2 = plt.subplot(312)
#        ax3 = plt.subplot(313)
#        
#        ax1.set_ylim(0,35,1)
#        ax1.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
#        #ax1.plot(Datum,Calc.Water0_30cm,'b--')
#        ax1.plot(Datum,Calc.Water0_30cm,'bo', ms=4,label='CMF')
#        #ax1.plot(Datum,Meas.Water0_30cm,'g--')
#        ax1.plot(Datum,Meas.Water0_30cm,'go', ms=4,label='Kersebaum')
#        ax1.legend(loc=2, bbox_to_anchor = (0.77, 1.4),scatterpoints=0)
#        ax1.set_title('Watercontent 0-30cm with r= '+str(round(cc0_30cm,4)))
#        ax1.grid()    
#        ax1.set_xlabel('Date')
#        ax1.set_ylabel('Water Content [%]')
#        ax1.fill_between(Datum,Calc.Water0_30cm,Meas.Water0_30cm,facecolor='red', alpha=0.5)    
#        
#        
#        ax2.set_ylim(0,35,1)
#        ax2.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
#        #ax2.plot(Datum,Calc.Water30_60cm,'b--')
#        ax2.plot(Datum,Calc.Water30_60cm,'bo',ms=4,label='Calculated (CMF)')
#        #ax2.plot(Datum,Meas.Water30_60cm,'g--')
#        ax2.plot(Datum,Meas.Water30_60cm,'go',ms=4,label='Measured (Kersebaum) ')
#        #ax2.legend()
#        ax2.set_title('Watercontent 30-60cm with r= '+str(round(cc30_60cm,4)))
#        ax2.grid()    
#        ax2.set_xlabel('Date')
#        ax2.set_ylabel('Water Content [%]')
#        ax2.fill_between(Datum,Calc.Water30_60cm,Meas.Water30_60cm,facecolor='red', alpha=0.5)     
#            
#        ax3.set_ylim(0,35,1)
#        ax3.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
#        #ax3.plot(Datum,Calc.Water60_90cm,'b--')
#        ax3.plot(Datum,Calc.Water60_90cm,'bo',ms=4,label='Calculated (CMF)')
#        #ax3.plot(Datum,Meas.Water60_90cm,'g--')
#        ax3.plot(Datum,Meas.Water60_90cm,'go',ms=4,label='Measured (Kersebaum) ')
#        #ax3.legend()
#        ax3.set_title('Watercontent 60-90cm with r= '+str(round(cc60_90cm,4)))
#        ax3.grid()    
#        ax3.set_xlabel('Date')
#        ax3.set_ylabel('Water Content [%]')
#        ax3.fill_between(Datum,Calc.Water60_90cm,Meas.Water60_90cm,facecolor='red', alpha=0.5)     
#        
#        #legend(bbox_to_anchor=(0., 3.40, 1., 2.102), loc=0,
#        #       ncol=2, mode="expand", borderaxespad=0.)
#        plt.tight_layout()
#        plt.draw()
#        plt.savefig('Watercontent for Plot '+str(Plot)+' and RUE = '+str(RUE), dpi=400)    
#        plt.close()

            


def load_data(Plot,value,Position_Messwerte,Position_Ergebnisse):
    Measured_datafile='Measured_'+value+'_Plot'+str(Plot)+'.csv'
    Calculated_datafile='Calculated_'+value+'_Plot = '+str(Plot)+' and RUE = '+str(RUE)+'.csv'
    
    measured_file=file(Measured_datafile)
    measured_file.readline()
    for line in measured_file:
        line = line.strip() 
        columns = line.split(';')     
        Meas.Messwerte.append(float(columns[Position_Messwerte]))
        
    calculated_file=file(Calculated_datafile) 
    calculated_file.readline()
    for line in calculated_file:
        line = line.strip() 
        columns = line.split(',')
        Calc.year.append(columns[0])
        Calc.month.append(columns[1])
        Calc.day.append(columns[2])
        Calc.Ergebnisse.append(float(columns[Position_Ergebnisse]))



class Measured(object):
    def __init__(self):
        self.Messwerte=[]


class Calculated(object):
    def __init__(self):
        self.date=[]
        self.year=[]
        self.month=[]
        self.day=[]
        self.Ergebnisse=[]
    
        

if __name__=='__main__':

    """
    Setup:
    """    
    Parameter = 'stem_and_leaf'
    Parameter_unit = ' [kg/ha] '    
    Position_Messwerte = 4
    Position_Ergebnisse = 5

    """
    Runtimeloop:
    """    
    Values = []
    for RUE_Faktor in range(10):
        RUE=RUE_Faktor+1
        
        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312)
        ax3 = plt.subplot(313)
        plt.title(Parameter+Parameter_unit)
        
        for Plotnumber in range(3):
           
            Plot = Plotnumber+1
            
           
            Meas=Measured()
            Calc=Calculated()
            
            
            
            load_data(Plot,Parameter,Position_Messwerte,Position_Ergebnisse)
            
            Datum=[]
            for i in range(len(Calc.year)):
                Datum.append(datetime(int(Calc.year[i]),int(Calc.month[i]),int(Calc.day[i])))
             
            Bias = stat.Bias(Meas.Messwerte,Calc.Ergebnisse)
            
            Nash_Sutcliff = stat.Nash_Sutcliff(Meas.Messwerte,Calc.Ergebnisse)

            cc = stat.Corelation_Coefficient(Meas.Messwerte,Calc.Ergebnisse)

            cc_squared = stat.R_squared(Meas.Messwerte,Calc.Ergebnisse)
            
            
            Values.append(Meas.Messwerte)
            Values.append(Calc.Ergebnisse)            
            
            #Biggest_value = math.ceil(np.max(Values))
            #print Biggest_value
    
         
            """
            Plot:
            """
        
        
            
            if Plot ==1:
                #ax1.set_ylim(0,35,1)
                ax1.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
                ax1.set_ylim(0,math.ceil(np.max(Values)))
                #ax1.plot(Datum,Calc.Water0_30cm,'b--')
                ax1.plot(Datum,Calc.Ergebnisse,'bo', ms=4,label='PMF')
                #ax1.plot(Datum,Meas.Water0_30cm,'g--')
                ax1.plot(Datum,Meas.Messwerte,'go', ms=4,label='Kersebaum')
                ax1.legend(loc=2, bbox_to_anchor = (0.77, 0.4),scatterpoints=0)
                ax1.set_title('Plot '+str(Plot)+' with r='+str(round(cc,4))+', Bias='+str(round(Bias,2))+' and EF='+str(round(Nash_Sutcliff,2)))
                ax1.grid()    
                ax1.set_xlabel('Date')
                ax1.set_ylabel(Parameter+Parameter_unit)
                ax1.fill_between(Datum,Calc.Ergebnisse,Meas.Messwerte,facecolor='red', alpha=0.5)    
    
            if Plot ==2:
                #ax2.set_ylim(0,35,1)
                ax2.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
                ax2.set_ylim(0,math.ceil(np.max(Values)))
                #ax2.plot(Datum,Calc.Water0_30cm,'b--')
                ax2.plot(Datum,Calc.Ergebnisse,'bo', ms=4,label='PMF')
                #ax2.plot(Datum,Meas.Water0_30cm,'g--')
                ax2.plot(Datum,Meas.Messwerte,'go', ms=4,label='Kersebaum')
                #ax2.legend(loc=2, bbox_to_anchor = (0.77, 0.4),scatterpoints=0)
                ax2.set_title('Plot '+str(Plot)+' with r='+str(round(cc,4))+', Bias='+str(round(Bias,2))+' and EF='+str(round(Nash_Sutcliff,2)))
                ax2.grid()    
                ax2.set_xlabel('Date')
                ax2.set_ylabel(Parameter+Parameter_unit)
                ax2.fill_between(Datum,Calc.Ergebnisse,Meas.Messwerte,facecolor='red', alpha=0.5)   
            if Plot ==3:
                #ax3.set_ylim(0,35,1)
                ax3.set_xlim(datetime(1993,1,1),datetime(1999,1,1))
                ax3.set_ylim(0,math.ceil(np.max(Values)))
                #ax3.plot(Datum,Calc.Water0_30cm,'b--')
                ax3.plot(Datum,Calc.Ergebnisse,'bo', ms=4,label='PMF')
                #ax3.plot(Datum,Meas.Water0_30cm,'g--')
                ax3.plot(Datum,Meas.Messwerte,'go', ms=4,label='Kersebaum')
                #ax3.legend(loc=2, bbox_to_anchor = (0.77, 0.4),scatterpoints=0)
                ax3.set_title('Plot '+str(Plot)+' with r='+str(round(cc,4))+', Bias='+str(round(Bias,2))+' and EF='+str(round(Nash_Sutcliff,2)))
                ax3.grid()    
                ax3.set_xlabel('Date')
                ax3.set_ylabel(Parameter+Parameter_unit)
                ax3.fill_between(Datum,Calc.Ergebnisse,Meas.Messwerte,facecolor='red', alpha=0.5)   
                
        #legend(bbox_to_anchor=(0., 3.40, 1., 2.102), loc=0,
        #       ncol=2, mode="expand", borderaxespad=0.)
        plt.tight_layout()
        plt.draw()
        plt.savefig(Parameter+' for all plots and RUE = '+str(RUE), dpi=400)    
        plt.close()     




 

  