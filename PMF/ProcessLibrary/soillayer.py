# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

@author: kellner-j
'''
class SoilLayer:
    """
    SoilLayer is the framework for the rooting zone.
    
    Soillayer holds values for the geometrical description
    of the rootingzone. It is divided into layers which can
    be penetrated from the plant root.

    Implementation
    ==============
    Soillayer is implemented without values. With the
    function get_rootingzone() a rootingzone can be created.
    
    Call signature
    ==============
    Call Soillayer calculates the actual rootingzone, depending
    on the depth of the plant root. For that the root penetration for 
    each layer is calculated.
    """
    def __init__(self,lower=0.,upper=0.,center=0.,thickness=0.,penetration=0.,soilprofile=[]):
        """
        Returns a soillayer instance with zero values for all attributes.
        
        To create a rootingzone get_rootingzone() must be called.
        
        @type lower: double
        @param lower: Lower limit of the soil layer relative to ground 
        surface level in [cm].
        @type upper: double
        @param upper: Upper limit of the soil layer relative to ground 
        surface level in [cm].
        @type center: double
        @param center: Center of the soil layer relative to ground 
        surface level in [cm].
        @type thickness: double
        @param thickness: Thickness of the layer in [cm].
        @type penetration: double 
        @param penetration: Root penetrated fraction of the layer in [cm].
        @rtype: soillayer
        @return: soillayer instance
        """
        self.lower=lower
        self.upper=upper
        self.center=center
        self.thickness=thickness
        self.rootingzone=[]
        self.get_rootingzone(soilprofile)
        self.penetration=penetration
    def __getitem__(self,index):
        return self.rootingzone[index]
    def __iter__(self):
        for horizon in self.rootingzone:
            yield horizon
    def __len__(self):
        return len(self.rootingzone)
    def get_rootingzone(self,soilprofile):
        """ Returns a rootingzone.
        
        @type soilprofile: list
        @param soilprofile: List with the lower limits of the layers in the 
        soilprofile in [cm].
        @rtype: soilprofile
        @return: Soilprofile which defines the actual rootingzone.
        """
        #Create soillayer for each layer in soilprofile
        for i,layer in enumerate(soilprofile):
            #Each layer is a soillayer instance
            self.rootingzone.append(SoilLayer())
            #set lower limit
            self.rootingzone[i].lower=layer
            #first layer upper limit = 0.
            if i == 0: 
                self.rootingzone[i].upper = 0.
            #all other layers upper limit = lower limit of the above layer
            else: 
                self.rootingzone[i].upper = (soilprofile[i-1])
            #Center and thickness of each layer
            self.rootingzone[i].center = (self.rootingzone[i].lower + self.rootingzone[i].upper) / 2.
            self.rootingzone[i].thickness = self.rootingzone[i].lower - self.rootingzone[i].upper
    def __call__(self,Zr):
        """
        Calculates the penetration depth for each soillayer in the rootingzone.
        
        @type Zr: double
        @param: Rootingdepth in [cm].
        @return: -
        """
        #For each layer in rootingzone
        for layer in self.rootingzone:
            #If lower limit <= rootingdepth, the soillayer is full penetrated
            if layer.lower <= Zr:
                layer.penetration = layer.thickness
            #If upperlimit above rootingdepth, layer is not penetrated
            elif layer.upper>Zr:
                layer_penetration = 0.
            #If only a part from the layer is penetrated, the value is rootingdepth minus upperlimit
            else: 
                layer.penetration = Zr - layer.upper