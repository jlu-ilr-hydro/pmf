# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: kellner-j
'''
import math
import pylab as pylab

class Waterstress_FAO:
    """
    Simple water uptake model which computes water uptake under stressed
    conditions.
    
    The model calculates plant water uptake under water stress
    conditions. Plant water demand equals the potential transpiration.
    If the soil cannot satisfy these demand, stress occurs and 
    the potential transpiration is reduced to the actual water uptake.
    The reduction factor through water stress is computed in relation
    to "Crop evapotranspiration - Guidelines for computing crop 
    water requirements - FAO Irrigation and drainage paper 56".
    All equations and concepts implemented in this class are taken 
    from these approach.
    
    Implementation
    ==============
    WAter_FAO must be implemented with a crop specific stress
    coefficiant, which can be taken from the guidelines.
    
    Call signature
    ==============
    Waterstress_FAO calculates the wateruptake under stressed 
    conditions for a given rootingzone.
    
    :see: [Allen et al, 1998]
    """
    def __init__(self,waterbalance=None,plant=None,average_available_soilwater=0.5):
        """
        Returns a Waterstress_FAO instance.
        
        :type average_available_soilwater: double
        :param average_available_soilwater:  fraction of TAW that a crop 
        can extract from the root zone without suffering water stress in [-].
        
        :rtype: water_fao
        :return: Water_FAO instance
        """
        self.waterbalance=waterbalance
        self.plant=plant
        #Constant variables
        self.p = average_available_soilwater
        #State variables
        self.TAW=0.
        self.RAW=0.
        self.Ks=0.
    def __call__(self,rootzone):
        """
        Calculates water stress values for each layer in the rooting zone.
        
        :type rootzone: list
        :param rootzone: List with middle depth of each layer in [cm].
        :rtype: list
        :return: Stress values for each layer in rootzone in [-].
        """
        TAW = self.calc_TAW(self.waterbalance.fc, self.waterbalance.wp, self.plant.root.depth/100.)
        RAW = TAW * self.p
        Ks = [self.calc_Ks(TAW, self.waterbalance.Dr, RAW, self.p) for z in rootzone]
        
        self.TAW=TAW
        self.RAW=RAW
        self.Ks=Ks
        return Ks
    def calc_Ks(self,TAW,Dr,RAW,p):
        """ 
        Calculates transpiration reduction factor.
        
        Potential transpiration is reducees, if the depletion exceeds the
        readily available soil water. When the root zone depletion is smaller 
        than RAW, Ks = 1.
        
        :type TAW: double
        :param TAW: Total available soil water in the root zone in [mm].
        :type Dr: double
        :param Dr: Root zone depletion in [mm].
        :type RAW: double
        :param RAW: Readily available soil water in the root zone in [mm].
        :type p: double
        :param p: Fraction of TAW that a crop can extract from the root zone 
        without suffering water stress in [-].
        :rtype: double
        :return: Transpiration reduction factor dependent on available soil
        water in [-].       
        """
        Ks = (TAW-Dr)/((1-p)*TAW) if Dr > RAW else 1.
        return max(Ks,0.)
    def adjust_p(self,p_table,ETc):
        """ 
        Adjust extractable soil water without stress.
        
        p is Fraction of TAW that a crop can extract from the root zone without 
        suffering water stress. The values for p apply for ETc 5 mm/day can be 
        adjusted with the daily ETc. 
    
        :type p_table: double
        :param p_table: Fraction of TAW that a crop can extract from the root 
        zone without suffering water stress in [-].
        :type ETc: double
        :param ETc: Crop specific evapotranspiration in [mm].
        :rtype: double
        :return: Adjusted extractable soil water in [-].
        """
        return p_table + 0.04*(5-ETc)
    def calc_TAW(self,FC,WP,Zr):
        """ 
        Returns total available water in the root zone.
        
        The total available water in the root zone is the difference 
        between the water content at field capacity and wilting point.
        TAW is the amount of water that a crop can extract from its root zone,
        and its magnitude depends on the type of soil and the rooting depth
        
        :type FC: double 
        :param FC: Water content at field capacity in [m3 m-3].
        :type WP: double 
        :param WP: Water content at wilting point in [m3 m-3].
        :type Zr: double 
        :param Zr: Rooting depth in [m] 
        
        :rtype: double
        :return: Total available soil water in the root zone in [mm].
        """
        return 1000*(FC-WP)*Zr