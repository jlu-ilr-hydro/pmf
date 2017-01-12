# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: kellner-j
'''
import math
class Net_Radiation:  
    """
    Calculates net radiation on basis of incoming solar radiation and leaf area index.
    
    Implementation
    ==============
    Leaf is implemented from the plant class.
    
    Call signature
    ==============
    Net_Radiation calculates actual albedo and net radiation (difference between incoming net 
    shortwave radiation Rns and outgoing net longwave radiation Rnl).
    """
    def __init__(self,albedo_m,Cr):            
        """
        Returns the net radiation [MJ m-2 d-1]
        
        :type: leaf
        :param: leaf instance
        :type albedo_m: double
        :param albedo_m: Albedo for a closed grass canopy [-]
        :type Cr: double
        :param Cr: Extinction coefficient of the vegeation [-]
        :rtype: Net_Radiation
        :return: Net_Radiation instance
        """
        
        # crop specific parameter (listet in the CropDatabase)
        self.albedo_m = albedo_m
        self.Cr = Cr
                
        #State variables updated in every timestep
        self.albedo = 0.
        self.interception = 0.
        self.R_n_s = 0. #net shortwave radiation
        self.R_n_l = 0. #net longwave radiation
        self.R_n = 0.   #net radiation
        self.R_s_n = 0  # net radiation that reaches the soil                 
        
    @property
    def Albedo(self):
        """
        Returns acutal albedo on basis of LAI.
        
        :rtype: double
        :return: Albedo [-]
        """
        return self.albedo
        
    @property
    def Rn(self):
        """
        Returns net radiation.
        
        :rtype: double
        :return: Net radiation [MJ m-2 d-1]
        """
        return self.R_n
        
    def  __call__(self,Tmax,Tmin,e_a,Rsolar,Rs_clearsky,LAI):
        """
        Call net_radiation calculates the net radiation (the difference between 
        incoming net shortwave radiation and outgoing net longwave radiation). 
        In addition the acutal albedo on basis of the LAI is calculated.

        The net radiation is calculated considering a change in albedo 
        due to varying LAI over development.

        :type Tmax: double
        :param Tmax: Maximum temperature [K]       
        :type Tmin: double
        :param Tmin: Minimum temperature [K]
        :type e_a: double
        :type e_a: Actual vapour pressure [kPa]  
        :type Rsolar: double
        :param Rsolar: Solar radiation [MJ m-2 d-1]
        :type Rs_clearsky: double
        :type Rs_clearsky: Solar raditaion of a clear sky [MJ m-2 d-1]
        :type LAI: double
        :param LAI: Effective leaf area index [m2 m-2]
        """
        
        self.albedo = self.calc_albedo(LAI,self.albedo_m)  
        self.interception = self.calc_interception(LAI,self.Cr)
        
        self.R_n_s = self.calc_R_n_s(Rsolar, self.albedo)
        self.R_n_l = self.calc_R_n_l(Tmax,Tmin,e_a,Rsolar,Rs_clearsky)
        self.R_n = self.calc_R_n(self.R_n_s,self.R_n_l)
        self.R_s_n = self.calc_R_s_n(self.R_n,self.interception) #[MJ m-2 d-1]

    
    def calc_albedo(self,LAI,albedo_m):
        """ 
        Calculates the albedo depending on LAI.
        
        Albedo is the fraction of solar radiation that is reflected by the surface.
        The equation is taken from Zhou et al. 2006, p. 156.
        
        :type LAI: double
        :param LAI: Effective leaf area index [m2 m-2]
        :type albedo_m: double
        :param albedo_m: Albedo for a closed grass canopy [-]
        :rtype: double
        :return: Albedo [-].        
        """
        albedo_s = 0.1 # albedo for bare wet soil
        return albedo_m - (albedo_m - albedo_s)*math.exp(-0.56*LAI)
    
      
    def calc_R_n_s(self,Rsolar, albedo):     
        """
        Calculates the net shortwave radiation.     
        
        The net shortwave radiation results from the balance between incoming 
        and reflected shortwave radiation. Hence, it is the fraction of solar
        radiation that is not reflected.
        
        :type Rsolar: double
        :param Rsolar: Solar radiation [MJ m-2 d-1]
        :type albedo: double
        :param albedo: Part of the radiation that is reflected []
        :rtype: double
        :return: Net shortwave radiation [MJ m-2 d-1].   
        """
        return ((1.-albedo)*Rsolar)
    
    def calc_R_n_l(self,Tmax,Tmin,e_a,Rsolar,Rs_clearsky):
        """
        Calculates the net longwave radiation.    
    
        :type Tmax: double
        :param Tmax: Maximum temperature [K]       
        :type Tmin: double
        :param Tmin: Minimum temperature [K]
        :type e_a: double
        :param e_a: Actual vapour pressure [kPa]
        :type Rsolar: double
        :param Rsolar: Solar radiation [MJ m-2 d-1]
        :type Rs_clearsky: double
        :param Rs_clearsky: Solar raditaion of a clear sky [MJ m-2 d-1]
        :rtype: double
        :return: Net longwave radiation [MJ m-2 d-1].   
        """
        Tmax_k = Tmax + 273.16     # maximum daily temperature in Kelvin
        Tmin_k = Tmin + 273.16     # minimum daily temperature in Kelvin
        sigma = 4.903*10**(-9)     # [MJ K-4 m-2 d-1] Stefan-Boltzlmann-constant
        return (sigma*((Tmax_k**4. + Tmin_k**4.)/2.)*(0.34 - 0.14*math.sqrt(e_a))*(1.35*Rsolar/Rs_clearsky -0.35))  

    def calc_R_n(self,R_n_s,R_n_l):
        """
        Calculates the net radiation. 
        
        The net radiation is the difference between the incoming net shortwave 
        radiation (R_n_s) and the outgoing longwave radiation (R_n_l).
        
        :type R_n_l: double
        :param R_n_l: Net longwave radiation [MJ m-2 d-1]       
        :type R_n_s: double
        :param R_n_s: Net shortwave radiation [MJ m-2 d-1]
        :rtype: double
        :return: Net radiation [MJ m-2 d-1].   
        """        
        return (R_n_s - R_n_l)

    def calc_interception(self,LAI,Cr):
        """ 
        Calculates fraction of radiation which is intercepted by the crop.
 
        :type LAI: double
        :param LAI: Effective leaf area index [m2 m-2]
        :type Cr: double
        :param Cr: Extinction coefficient of the vegeation [-]
        :rtype: double
        :return: Fraction of total solar radiation flux, which is intercepted by the crop [-].
        """           
        return math.exp(-Cr*LAI)  

    
    def calc_R_s_n(self,R_n,interception):
        """ 
        Calculates radiation which reaches the soil surface.

        To calculate the radation which reaches the soil surface the Beer's 
        law relationship was taken.

        :type R_n: double
        :param R_n: Net radiation [MJ m-2 d-1]   
        :type interception: double
        :param interception: Fraction of total solar radiation flux, which is intercepted by the crop [-]   
        :rtype: double
        :return: Radiation which reaches the soil surface [MJ m-2 d-1].
        """ 
        return R_n * interception  