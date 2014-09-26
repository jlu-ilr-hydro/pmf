# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

@author: kellner-j
'''
import math
import pylab as pylab
class Nitrogen:
    """
    Calculates nitrogen uptake from the soil.
    
    The root nitrogen uptake is divided into active and passive uptake. 
    Aktive uptake will occure, if passive uptake cannot satisfy 
    the demand. The passive uptake in each soil layer pa depends 
    on the soil water extraction sh and a maximum allowed solution 
    concetration cmax which can be taken up by plant roots. Low 
    values or zero inhibit passive nitrogen uptake. This can be 
    important for other nutrients which can be taken up only active.
    
    The potential active uptake from each soil layer is calculated with 
    the Michaelis-Menten function. This function descirbes the relationship 
    between influx and its concentration at the root surface.
    
    Implementation
    ==============
    Nitrogen must be implemeted with the paramter
    for the michaelis menten equation.
    
    Call signature
    ==============
    Must be calles with water uptake, the plant nitrogen demand  
    and the nitrogen concentration in the soil.
    
    @see: [Simunek & Hopmans 2009]
    """
    def __init__(self,Km=0.1,NO3_min=0.,max_passive_uptake=1e300,layercount=41):
        """
        Returns a Biomass_LOG instance.
        
        @type Km: double
        @param Km: Half saturation concentration in umol/l  27. * 14e-6
        @type NO3_min: double
        @param NO3_min: Residual N concentration
        @type layercount: double
        @param layercount: Count of the layer in the soil profile.
        @type max_passive_uptake: double
        @param max_passive_uptake: ...
        
        
        @rtype: nitrogen
        @return: Nitrogen instance
        
        @todo: Define units for all parameters. 
        """
        self.layercount=layercount
        #Constant variables
        self.Km=Km
        self.NO3min=NO3_min
        self.max_passive_uptake=max_passive_uptake
        #State variables
        self.Pa=[0. for l in range(self.layercount)]
        self.Aa=[0. for l in range(self.layercount)]
    @property
    def Active(self):
        """
        Returns active nitrogen uptake.
        
        @rtype: double
        @return: Active nitrogen uptake.
        """
        return self.Aa
    @property
    def Passive(self):
        """
        Returns passive nitrogen uptake.
        
        @rtype: double
        @return: Passive nitrogen uptake.
        """
        return self.Pa
    @property
    def Total(self):
        """
        Returns total nitrogen uptake.
        
        @rtype: double
        @return: Total nitrogen uptake.
        """
        return [pa + self.Aa[i] for i,pa in enumerate(self.Pa)]
    def __call__(self,NO3_conc,Sh,Rp,root_fraction):
        """
        Calculates active and passive nitrogen uptake.
        
        @type NO3_conc: list
        @param NO3_conc: NO3 concnetrations in rootzone.
        @type Sh: list
        @param Sh: Plant water uptake from the rootzone in [mm].
        @type Rp: list
        @param Rp: Potential nutrient demand of the plant in [g].
        @type root_fraction: list
        @param root_fraction: Root biomass fraction form whole biomass for each layer in the soil profile in [-].
        @todo: Check Passive uptake
        @return: -
        """
        
        #Passive uptake
        self.Pa = [max(0,w*min(NO3_conc[i],self.max_passive_uptake)) for i,w in enumerate(Sh)]
        #Residual demand
        Ap = max(Rp-sum(self.Pa),0.)
        #Michelis-menten values for each layer
        michaelis_menten = [(NO3-self.NO3min)/(self.Km+NO3-self.NO3min) if NO3>self.NO3min else 0.0 for NO3 in NO3_conc]
        #Active uptake
        self.Aa = [Ap * michaelis_menten[i] * fraction for i,fraction in enumerate(root_fraction)]
        if min(self.Pa)<0 or min(self.Aa)<0:
            a=2