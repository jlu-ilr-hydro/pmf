# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: kellner-j
'''

class Waterstress_Feddes:
    """
    Water uptake model based on soil matrixpotential and a crop specific 
    uptake function.
    
    The water uptake is limited througt a sink therm variable alpha.
    This value vary with the water pressure head in the soil layer. 
    Alpha is a dimensonless factor between zero and one. The factor 
    limits water uptake due to the wilting point and oxygen dificiency.
    Alpha is determinded with four threshold values for the pressure head
    (h1-oxygen deficiency,h-4 wiliting point, h2 and h3 -optimal conditons). 
    Values for the parameters vary with the crop.  
    
    Water stress in a soil layer can bee compensated from other soil layer.
    This compensation is a empirical distribution from stressed soil layer
    in less stressed soil layers. Compensation is limited to the actual 
    uptake multiplied with the maxcomp parameter. Maxcomp is a user value.
    
    
    Implementation
    ==============
    Waterstress_Feddes must be implementeed with the maxcom parameter,
    which is defined from the user.
    
    Call signature
    ==============
    Water_feddes calculates the water uptake under stress conditions
    and calculates the compensation therm.    
    
    @see: [Feddes et al, 1978, Feddes & Raats 2004]
    """
    def __init__(self,waterbalance=None,plant=None,maxcomp=2.,layercount=41):
        """
        Returns a Waterstress_Feddes instance.
        
        :type maxcomp: double
        :param maxcomp: Maximal compensation capacity factor in [-].
        :type layercount: double
        :param layercount: Count of the layer in the soil profile.
        
        :rtype: water_feddes
        :return: Waterstress_Feddes instance
        """
        self.waterbalance=waterbalance
        self.plant=plant
        self.layercount=layercount
        #Constant variables
        self.max_compensation_capacity=maxcomp
        #State variables
        self.Sh=[0. for l in range(self.layercount)]
        self.alpha=[0. for l in range(self.layercount)]
        self.compensation=[0. for l in range(self.layercount)]
        self.Shcomp=[0. for l in range(self.layercount)]
    def __call__(self,rootzone):
        """
        Calculates water uptake under stressed conditions.
    
        :type rootzone: list
        :param rootzone: List with middle depth of each layer in  [cm].
        :rtype: list
        :return: Stress values for each layer in rootzone in [-].
        """
        return [self.sink_term(self.waterbalance.get_pressurehead(z), self.plant.pressure_threshold)for z in rootzone]
    def compensate(self,Sh,Sp,pressurehead,alpha,maxopth,maxcomp):
        """
        Calculates compensation factors for each layer in the rootingzone.
        
        Compensation capacity = (Actual uptake-Potential uptake)*maxcom
        
        :type s_p: list
        :param s_p: List with the potential water uptake for each soillayer in
        rootingzone in [mm].
        :type s_h: list
        :param s_h: List with the actual water uptake for each soillayer in
        rootingzone in [mm].
        :type pressurehead: list
        :param pressurehead: List with the soil pressurehead for each soillayer
        in rootingzone in [cm].
        :type alpha: list
        :param alpha: Prescribed crop specific function of soil water pressure
        head with values between or equal zero and one in [-].
        :type maxcomp: double
        :param maxcomp: Maximal compensation capacity factor in [-].
        :type maxopth: double
        :param maxopth: Plant pressure head until water uptake can occur without
        stress in [cm water column].
        :rtype: list
        :return: List with the compensated uptake in [mm].
        """
        #Remaining alpha of the less stress soil layer
        remaining_alpha= [max(1-(m/maxopth),0.) for i,m in enumerate(pressurehead)] 
        #Remaining uptake capacity of the soillayer
        remaining_uptake=sum(Sp)-sum(Sh)
        #Returns list with the compensation values in mm
        return [min(r/sum(remaining_alpha)*remaining_uptake,maxcomp*Sh[i])for i,r in enumerate(remaining_alpha)]     
    def sink_term(self,h_soil,h_plant): 
        """
        Computes sink term alpha.
        
        The water uptake is limited througt a sink therm variable alpha. 
        This value vary with the water pressure head in the soil layer. 
        Alpha is a dimensonless factor between zero and one. The factor 
        limits water uptake due to the wilting point and oxygen dificiency. 
        After alpha is determinded with four threshold values for the pressure 
        head (h1-oxygen deficiency,h-4 wiliting point, h2 and
        h3 -optimal conditons). Values for the parameters vary with the crop. 
        H3 also varies with the transpiration.
        
        :type h_soil: list
        :param h_soil: List with soil pressurehead for each layer in 
        [cm water column].
        :type h_plant: list
        :param h_plant: List with soil pressurehead. These conditions limiting 
        water uptake in. [cm water column].
        :rtype: list
        :return: Prescribed crop specific function of soil water pressure head 
        with values between or equal zero and one in [-].
        
        :see: [Feddes and Raats, 2004]
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err