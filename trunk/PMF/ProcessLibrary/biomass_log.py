# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: S. Multsch
'''

class Biomass_LOG:
    """
    Calculates plant growth based on a logistical growth function.
    
    Growth is simulated with a logistic growth function. The amount of biomass 
    in gram per time step depends on a crop specific growth coefficiant
    multiplied with the total biomass. A capacity limit retricts growth.
    The growthrate for a timestep is given by the following equation.
    
    Implementation
    ==============
    Biomass_LOG must be implemented with specific values
    for limiting maximal biomass and a growthfactor.
    
    Call signature
    ==============
    Biomass_LOG must be called with the actual time step and stress
    coefficiant.
    
    :see: [J.H.M. Thornley & Johnson 1990]
    """
    def __init__(self,capacitylimit,growthfactor):
        """
        Returns a Biomass_LOG instance.
        
        :type capacitylimit: double
        :param capacitylimit: Maximal plant biomass in [g]. 
        :type growthfactor: double
        :param growthfactor: Growth facor of the plant in [g biomass day-1].
        :rtype: biomass_log
        :return: Biomass_LOG instance
        """
        #Constant variables
        self.capacitylimit=capacitylimit
        self.growthfactor=growthfactor
        #State variables
        self.total=1.
        self.stress=0.
    @property
    def PotentialGrowth(self):
        """
        Return potential growth without stress.
        
        :rtype: double
        :return: Potential growth in [g biomass day-1].
        """ 
        return self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit)
    @property
    def ActualGrowth(self):
        """
        Return actual growth influenced by water and nitorgen stress.
        
        :rtype: double
        :return: Actual growth in [g biomass day-1].
        """ 
        return self.PotentialGrowth * self.stress
    @property
    def Total(self):
        """
        Return total biomass.
        
        :rtype: double
        :return: Total biomass in [g].
        """ 
        return self.total
    def __call__(self,stress,step):
        """
        Calculates total plant biomass under stressed conditions.
        
        :type stress: double
        :param stress: Parameter for water and nitrogen stress between 0 - 1
        in [-].
        :type step: double
        :param step: Time of the actual intervall.
        :return: -
        """
        self.stress=stress
        self.total = self.total + self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit) * stress * step
    def logarithmic_growth(self,total_biomass,growthfactor,capacitylimit):
        """
        Return growthrate from a logarithmic growht function.
        
        Calculates the growthrare of a logarithmic growth function.
        
        :type total_biomass: double
        :param total_biomass: Total bioamss of the plant in [g].
        :type capacitylimit: double
        :param capacitylimit: Maximal plant biomass in [g]. 
        :type growthfactor: double
        :param growthfactor: Growth facor of the plant in [g biomass day-1].
        :rtype: double
        :return: Growhtrate in [g biomass day-1].
        """
        return total_biomass * growthfactor * (1- total_biomass / capacitylimit)
    def atmosphere_values(self,atmosphere,time_act):
        """
        Biomass_LOG need no atmosphere values.
        """
        pass