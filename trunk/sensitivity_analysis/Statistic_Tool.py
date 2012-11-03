# -*- coding: utf-8 -*-
"""
Statisitc Tool: 
This tool holds functions for statistic analaysis. It takes Phton-lists and
returns the parameter of interest:

@author: Tobias

@version: 0.1 (31.08.2012)
"""

import numpy as np


def Bias(Gemessen,Berechnet):
    """
    Bias
    
    Bias =1/N * Sum[i=1/N](  D_i  )       
    with D_i = Measured_i - Calculated_i 
    """    
    if len(Gemessen)==len(Berechnet):
    
        Bias_values=[]
        
        for i in range(len(Gemessen)):
            if Gemessen[i] == -99999:
                '''
                Cleans out No Data values
                '''
                print 'Wrong Results! Clean out No Data Values'                 
                pass
             
            else:            
                Bias_values.append(float(Berechnet[i]) - float(Gemessen[i]))
        
              
        Bias_sum = np.sum(Bias_values[0:len(Bias_values)])
        
        Bias = Bias_sum/len(Bias_values)
        
        return Bias
    
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."
    
def Nash_Sutcliff(Gemessen,Berechnet):
    
    """
    Nash–Sutcliffe model efficiency coefficient
    
    EF = 1 - Sum[N/i=1](   Measured_i - Calculated_i  )**2    /    Sum[N/i=1](  Measured_i - mean(Measured)  )**2
    """
    
    if len(Gemessen)==len(Berechnet):
        
        Nash_Sutcliff_Zaehler=[]
        Nash_Sutcliff_Nenner=[]
        Messwerte_umgeformt=[]        
        for i in range(len(Gemessen)):
            Messwerte_umgeformt.append(float(Gemessen[i]))            
            Nash_Sutcliff_Zaehler.append((float(Gemessen[i])-float(Berechnet[i]))**2)
            Nash_Sutcliff_Nenner.append((float(Gemessen[i])-np.mean(Messwerte_umgeformt))**2) 
        
        Nash_Sutcliff = 1 - (np.sum(Nash_Sutcliff_Zaehler)/np.sum(Nash_Sutcliff_Nenner))
        
        return Nash_Sutcliff
        
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."

    
def Corelation_Coefficient(Gemessen,Berechnet):
    """
    Corelation Coefficient
    
    r= Sum[N/i=1](  (Measured_i-mean(Measured)) * (Calculated_i-mean(Calculated))  )  /  
       sqrt(  Sum[N/i=1](   Measured_i - mean(Measured)²  )  *  Sum[N/i=1](   Calculated_i-mean(Calculated)²   )  )
    """
    if len(Gemessen)==len(Berechnet):
        Corelation_Coefficient = np.corrcoef(Gemessen,Berechnet)[0,1]
#        This Calculation has a mistake
#        r_Zaehler_values=[]
#        r_Nenner_part1_values=[]
#        r_Nenner_part2_values=[]        
#        for i in range(len(Gemessen)):
#            r_Zaehler_values.append((Gemessen[i]-np.mean(Gemessen))*(Berechnet[i]-np.mean(Berechnet)))
#            r_Nenner_part1_values.append((Gemessen[i]-np.mean(Gemessen))**2)
#            r_Nenner_part2_values.append((Berechnet[i]-np.mean(Berechnet))**2)
#        r_Zaehler = np.sum(r_Zaehler_values)
#        r_Nenner = np.sqrt((np.sum(r_Nenner_part1_values))*(np.sum(r_Nenner_part2_values)))
#        
#        r=r_Zaehler/r_Nenner
        return Corelation_Coefficient
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."
  
  
def R_squared(Gemessen,Berechnet):
    """
    Coefficient of Determination
    
    R=r²
    """
    if len(Gemessen)==len(Berechnet):
        return Corelation_Coefficient(Gemessen,Berechnet)**2
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."
        

def MSE(Gemessen,Berechnet):
    """
    Mean Squared Error
    
    MSE=(1/N)  *  Sum[N/i=1](  D_i  )²
    with D_i = Measured_i - Calculated_i   
    """
    if len(Gemessen)==len(Berechnet):
        
        MSE_values=[]
                
        for i in range(len(Gemessen)):
            MSE_values.append((Berechnet[i] - Gemessen[i])**2)        
        
        MSE_sum = np.sum(MSE_values[0:len(Gemessen)])
        
        MSE=MSE_sum/(len(Gemessen))
        return MSE
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."

def RMSE(Gemessen,Berechnet):
    """
    Root Mean Squared Error
    
    RMSE = sqrt(MSE)
    """
    if len(Gemessen)==len(Berechnet):
        return np.sqrt(MSE(Gemessen,Berechnet))
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."    


def MAE(Gemessen,Berechnet):
    """
    Mean Absolute Error
    
    MAE = (1/N) * Sum[N/i=1](  |D_i|  )    
    with D_i = Measured_i - Calculated_i   
    """
    if len(Gemessen)==len(Berechnet):
        
        MAE_values=[]
                
        for i in range(len(Gemessen)):
            MAE_values.append(np.abs(Berechnet[i] - Gemessen[i]))        
        
        MAE_sum = np.sum(MAE_values[0:len(Gemessen)])
        
        MAE = MAE_sum/(len(Gemessen))
        
        return MAE
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."    


def RRMSE(Gemessen,Berechnet):
    """
    Relative Root Mean Squared Error
    
    RRMSE = RMSE / mean(Calculated)    
    """
    
    if len(Gemessen)==len(Berechnet):

        RRMSE = RMSE(Gemessen,Berechnet)/np.mean(Berechnet)
        return RRMSE
        
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."    
    

def RMAE(Gemessen,Berechnet):
    """
    Relative Mean Absolute Error
    
    RMAE = (1/N) * Sum[N/i=1](  |Measured_i-Calculated_i|  /  mean(|Gemessen|)  )
    """
    if len(Gemessen)==len(Berechnet):
        
        RMAE_values =[]
        
        for i in range(len(Gemessen)):
            RMAE_values.append(np.abs(Gemessen[i]-Berechnet[i])/np.abs(Gemessen[i]))
        
        RMAE_sum = np.sum(RMAE_values[0:len(Gemessen)])
        RMAE = RMAE_sum/len(Gemessen)        
        return RMAE
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."    
    
        
def Agreement_index(Gemessen,Berechnet):
    """
    Agreement Index
    
    index = 1 - (  Sum[N/i=1](  Gemessen_i - Berechnet_i  )²  )  /  
                (Sum[N/i=1](  |Berechnet_i - mean(Berechnet)| + |Gemessen_i - mean(Gemessen|  )  )²)
    """
    if len(Gemessen)==len(Berechnet):
        
        Agreement_index_Zaehler_values = []
        Agreement_index_Nenner_values = []         
        
        for i in range(len(Gemessen)):
            Agreement_index_Zaehler_values.append((Gemessen[i]-Berechnet[i])**2)
            Agreement_index_Nenner_values.append((np.abs(Berechnet[i]-np.mean(Gemessen))+np.abs(Gemessen[i]-np.mean(Gemessen)))**2)
        
        Agreement_index_Zaehler_Summe = np.sum(Agreement_index_Zaehler_values)
        Agreement_index_Nenner_Summe = np.sum(Agreement_index_Nenner_values)
        
        Agreement_index = 1 - (Agreement_index_Zaehler_Summe/Agreement_index_Nenner_Summe)
        
        return Agreement_index
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."    
    

def Variance(Messdaten):
    """
    Variance
    
    sigma² = 1/N * Sum[N/i=1](  Messdaten - Mean(Messdaten)  )
    """
    Variance_values = []    
    for i in range(len(Messdaten)):
        Variance_values.append((Messdaten[i]-np.mean(Messdaten))**2)            
    Variance = np.sum(Variance_values)/len(Messdaten) 
    return Variance
    

def Covariance(Gemessen,Berechnet):
    """
    Covariance
    
    sigma(x,y) = 1/N * Sum[N/i=1](  ( Gemessen_i - mean(Gemessen) ) * ( Berechnet_i - mean(Berechnet) )  )
    """
    if len(Gemessen)==len(Berechnet):
        Covariance_values = []
        
        for i in range(len(Gemessen)):
            Covariance_values.append((Gemessen[i]-np.mean(Gemessen))*(Berechnet[i]-np.mean(Berechnet)))
            
        Covariance = np.sum(Covariance_values)/(len(Gemessen))
        return Covariance
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."  

def Standard_deviation(Messdaten):
    """
    Standard Derivation
    
    sigma = sqrt(Variance)
    """
    
    return np.sqrt(Variance(Messdaten))


def Decomposed_MSE(Gemessen,Berechnet):
    """
    Decomposed MSE (Kobayashi and Salam (2000))
    
    MSE = (Bias)² + SDSD + LCS
    
    with
    SDSD = (sigma_Gemessen - sigma_Berechnet)²
     LCS = 2 * sigma_Gemessen * sigma_Berechnet * (1 - r)
    """
    
    if len(Gemessen)==len(Berechnet):
        
        Decomposed_MSE = str(round((Bias(Gemessen,Berechnet))**2,2))+'(Bias**2) + '+str(round((Standard_deviation(Gemessen)-Standard_deviation(Berechnet))**2,2))+'(SDSD) + '+str(round(2*Standard_deviation(Gemessen)*Standard_deviation(Berechnet)*(1-Corelation_Coefficient(Gemessen,Berechnet)),2))+'(LCS)'         
        
        return Decomposed_MSE
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."  



def Default(Gemessen,Berechnet):
    """

    """
    if len(Gemessen)==len(Berechnet):
        return None
    else:
        return "Error: Gemessene und Berechnete Wertelisten sind nicht gleichlang."    
    


