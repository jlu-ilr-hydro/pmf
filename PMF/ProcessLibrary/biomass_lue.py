# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: S. Multsch
'''
import math
#import pylab as pylab
import numpy as np

class Biomass_LUE:
    """
    Calculates biomass growth with the radiation use efficiency concept.
    
    Calculates the daily biomass gorwht form a crop specific
    radiatiion use efficiency and the daily incoming absorbed
    photosynthetic active radiation (aPAR). aPAR depends on the
    plant leaf area index and a dimensionless extinction
    coefficiant.
    
    Implementation
    ==============
    Biomass_LUE must be implemented with the crop specific paramters
    for the LUE-concept.
    
    Call signature
    ==============
    Plant must be calles with crop and environmental factors.
    
    """
    def __init__(self,RUE,k):
        """
        Returns a Biomass_LUE instance.
        
        :type RUE: double
        :param RUE: Radiation use efficiency [g m-1 day-1]
        :type k: double
        :param k: Canopy extinction coefficient in [-].
        :rtype: biomass_lue
        :return: Biomass_LUE instance
        """
        #Constant variables
        self.rue=RUE
        self.k=k
        #State variables
        self.total=0.
        self.growthrate=0.
        self.pot_total=0.
        self.stress = 0.
    @property
    def PotentialGrowth(self):
        """
        Return potential growth without stress.
        
        :rtype: double
        :return: Potential growth in [g biomass day-1].
        """ 
        return self.growthrate
    @property
    def ActualGrowth(self):
        """
        Return actual growth influenced by water and nitorgen stress.
        
        :rtype: double
        :return: Actual growth in [g biomass day-1].
        """ 
        return self.growthrate * (1-self.stress)
    @property
    def Total(self):
        """
        Returns total biomass.
        
        :rtype: double
        :return: Biomass in [g biomass day-1].
        """ 
        return self.total
    def __call__(self,step,stress,Rs,LAI):
        """
        Calculates the stressed and unstressed growth of the plant.
        
        :type step: double
        :param step: Time step in [days].
        :type Rs: double
        :param Rs: total solar radiation [MJ m-2 day-1].
        :type stress: double
        :param stress: Parameter for water and nitrogen stress between 0 - 1. 
        in [-].
        :type LAI: double
        :param LAI: Leaf area index of the plant in [m2 m-2].
        :param Rs: total solar radiation [MJ m-2 day-1].
        :type stress: double
        """
        self.stress = stress
        self.growthrate = self.PAR_a(Rs, self.intercept(LAI, self.k))* self.rue
        self.total = self.total + self.growthrate * (1-self.stress) * step
        self.pot_total = self.pot_total + self.growthrate
    def PAR_a(self,Rs,interception):
        """ 
        Returns photosynthetically active absorbed radiation
        
        Canopy photosynthesis is closely related to the photosynthetically 
        active (400 to 700 mm) absorbed radiation (PARa) by green tissue in the 
        canopy. The values 0.5 is the fraction of total solar energy, which is 
        photosynthetically active interception - fraction of total solar 
        radiation flux, which is intercepted by the crop. The value 0.9 is the 
        fraction of radiation absorbed by the crop  allowing for a 6 percent 
        albedo and for inactive radiation absorption.
        
        :type Rs: double
        :param Rs: total solar radiation [MJ m-2 day-1].
        :type interception: double
        :param interception: Fraction of total solar radiation flux, which is 
        intercepted by the crop in [-].
        
        :rtype: double
        :return: Photosynthetically active absorbed radiation in [MJ m-2 day-1].
        """
        return Rs*0.5*0.9*(1-interception)
    def intercept(self,LAI,k):
        """
        Returns crop interception.
        
        anopy extinction coefficient in wheat crops ranges
        from 0.3 to 0.7 and is highly dependent on leaf angle
        (low K for erect leaves). From equation 3, it can be calculated that
        95 percent PAR interception requires a LAI as high as 7.5 for erect 
        leaves but a LAI of only about 4.0 for more horizontal leaves
        
        :type LAI: double
        :param LAI: Leaf area index of the plant in [m2 m-2].
        :type k: double
        :param k: Canopy extinction coefficient in [-].
        """
        return np.exp(-k*LAI)
    def atmosphere_values(self,atmosphere,time_act):
        """
        Returns a method to interfere with the atmosphere interface over the 
        plant instance.
        
        :type atmosphere: atmosphere
        :param atmosphere: Atmosphere object from the plant interface soil. 
        :type time_act: datetime
        :param time_act: Actual time in [DD,MM,JJJ].
        :rtype: method
        :return: Function for getting required atmosphere values.
        """
        return atmosphere.get_Rs(time_act)
