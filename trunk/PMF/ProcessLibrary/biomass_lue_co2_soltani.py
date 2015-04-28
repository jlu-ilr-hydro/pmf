# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: kellner-j
'''
import math
import PMF

class Biomass_LUE_CO2_Soltani:
    """
    Calculates biomass growth with the radiation use efficiency concept.
    
    Calculates the daily biomass grwoth from a crop specific
    radiation use efficiency (RUE) and the daily incoming absorbed
    photosynthetic active radiation (aPAR). aPAR depends on the
    plant leaf area index and a dimensionless extinction
    coefficiant. RUE varies with change in the atmospheric CO2 concentration.
    The underlying equation for RUE is extracted from Soltani and Sinclair 2012, p.123.
    
    Implementation
    ==============
    Biomass_LUE must be implemented with the crop specific paramters
    for the LUE-concept.
    
    Call signature
    ==============
    Plant must be calles with crop and environmental factors.
    
    """

    
    def __init__(self,RUE,C_0,factor_b,CO2_ring):
        """
        Returns a Biomass_LUE instance.
        
        :type RUE: double
        :param RUE: Radiation use efficiency [g m-1 day-1]
        :type C_0: double
        :param C_0: reference CO2 concentration (=350 µmol/mol)
        :type factor_b: double
        :param factor_b: coefficient that adapt RUE to C4 (factor_b=0.4) or C3 (factor_b=0.8) plants [-]   
        :rtype: biomass_lue
        :return: Biomass_LUE instance
        """
        #Constant variables
        self.rue_0=RUE
        self.C_0=C_0
        self.factor_b= factor_b
        self.CO2_ring = CO2_ring
   
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
        :return: Potential growth in [g dry matter m-2 day-1].
        """ 
        return self.growthrate
    @property
    def ActualGrowth(self):
        """
        Return actual growth influenced by water and nitorgen stress.
        
        :rtype: double
        :return: Actual growth in [g dry matter m-2 day-1].
        """ 
        return self.growthrate * (1-self.stress)
    @property
    def Total(self):
        """
        Returns produced total amount of dry matter including stress and senescence.
        
        :rtype: double
        :return: Biomass [g dry matter m-2].
        """ 
        return self.total
        
    @property
    def Rue_soltani(self):
        return self.rue_sol

    @property
    def PAR_absorbed(self):
        return self.par_absorbed


    def __call__(self,step,stress,Rs,interception,LAI,CO2_measured,senesced_leaf):  
        """
        Calculates the stressed and unstressed growth of the plant.
        
        :type step: double
        :param step: Time step in [days].
        :type Rs: double
        :param Rs: total solar radiation [MJ m-2 day-1].
        :type stress: double
        :param stress: Parameter for water and nitrogen stress between 0 - 1. [-].
        :type LAI: double
        :param LAI: Leaf area index of the plant in [m2 m-2].
        :type CO2_measured: double
        :param CO2_measured: atmospheric CO2 concentration in rings [ppm].
        """
        
        self.stress = stress
        self.rue_sol = self.rue_soltani(self.rue_0,self.C_0,self.factor_b,CO2_measured)
        self.par_absorbed = self.PAR_a(Rs, interception)
        self.growthrate = self.par_absorbed * self.rue_sol
        self.total = self.total - senesced_leaf + self.growthrate * (1-self.stress) * step         
        self.pot_total = self.pot_total + self.growthrate
        
    
    def rue_soltani(self,rue_0,C_0,factor_b,C_measured):
        """
        Returns radiation use efficiency affected by CO2 concentration [g/MJ]
        
        This approach is taken from Soltani and Sinclair (2012) and based on 
        Penning de Vries 1989.
        
        :type rue_0: double
        :param rue_0: radiation use efficiency at the reference CO2 concentration (350 µmol/mol) [g/MJ]
        :type C_0: double
        :param C_0: reference CO2 concentration (=350 µmol/mol)
        :type factor_b: double
        :param factor_b: coefficient that adapt RUE to C4 (factor_b=0.4) or C3 (factor_b=0.8) plants [-]
        :type C_measured: double
        :param C_measured: target CO2 concentration [µmol/mol] 
        """
        return rue_0*(1+factor_b*math.log(C_measured/C_0)) 
        

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
        

    def measured_CO2(self,atmosphere,time_act):
        """
        Returns a method to interfere with the atmosphere interface over the 
        plant instance.
        
        :type atmosphere: atmosphere
        :param atmosphere: Atmosphere object from the plant interface soil.
        :type time_act: datetime
        :param time_act: Actual time in [DD,MM,JJJ].
        :rtype: method
        :return: Function for getting elevated CO2 concentration
        """
        if self.CO2_ring == 1.1:
            CO2_measured = atmosphere.get_CO2_A1(time_act) 
        elif self.CO2_ring == 1.2:
            CO2_measured = atmosphere.get_CO2_A2(time_act) 
        elif self.CO2_ring == 1.3:
            CO2_measured = atmosphere.get_CO2_A3(time_act) 
        elif self.CO2_ring == 2.1:
            CO2_measured = atmosphere.get_CO2_E1(time_act) 
        elif self.CO2_ring == 2.2:
            CO2_measured = atmosphere.get_CO2_E2(time_act) 
        else: CO2_measured = atmosphere.get_CO2_E3(time_act)
#        return atmosphere.get_CO2_measured(time_act)
        return CO2_measured
