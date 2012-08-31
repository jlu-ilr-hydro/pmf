# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:39:17 2012

@author: Pooder
"""
import numpy as np


def Bias(Gemessen,Berechnet):
    
    if len(Gemessen)==len(Berechnet):
        
        """
        Bias =1/N * Sum[i=1/N](D_i)
        
        with D_i = Measured_i - Calculated_i 
        """
    
        Bias_values=[]
                
        for i in range(len(Gemessen)):
            Bias_values.append(float(Berechnet[i]) - float(Gemessen[i]))
                
        Bias_sum = np.sum(Bias_values[0:len(Gemessen)])
        
        Bias = Bias_sum/len(Gemessen)
        
        return Bias
    
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."
    
def Nash_Sutcliff(Gemessen,Berechnet):
    
    """
    Nash–Sutcliffe model efficiency coefficient
    
    EF = 1 - (Sum[N/i=1](Measured_i - Calculated_i)**2  / Sum[N/i=1](Measured_i - mean(Measured))**2)
    """
    
    if len(Gemessen)==len(Berechnet):
        
        Nash_Sutcliff_Zaehler=[]
        Nash_Sutcliff_Nenner=[]
        Messwerte_umgeformt=[]        
        for i in range(len(Gemessen)):
            Messwerte_umgeformt.append(float(Gemessen[i]))            
                
        for i in range(len(Gemessen)):
            Nash_Sutcliff_Zaehler.append((float(Gemessen[i])-float(Berechnet[i]))**2)
            Nash_Sutcliff_Nenner.append((float(Gemessen[i])-np.mean(Messwerte_umgeformt))**2) 
        
        Nash_Sutcliff = 1 - (np.sum(Nash_Sutcliff_Zaehler)/np.sum(Nash_Sutcliff_Nenner))
        
        return Nash_Sutcliff
        
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."

    
def Corelation_Coefficient(Gemessen,Berechnet):
    if len(Gemessen)==len(Berechnet):
        Corelation_Coefficient = np.corrcoef(Gemessen,Berechnet)[0,1]
        return Corelation_Coefficient
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."
  
  
def R_squared(Gemessen,Berechnet):
    if len(Gemessen)==len(Berechnet):
        return Corelation_Coefficient(Gemessen,Berechnet)**2
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."
    


