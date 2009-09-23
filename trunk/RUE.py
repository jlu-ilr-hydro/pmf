class GrainYield:
    def __init__(self):
        pass
    def PAR_a(self,Rs,interception):
        """ The PARa can be calculated from the fraction 
            of solar radiation at the top of the canopy, which 
            is transmitted to the ground (I/I0)/->interception
            
            RS - total solar radiation (MJ/m2 d)
            0.5- fraction of total solar energy, which is 
                 photosynthetically active
            interception - fraction of total solar radiation
                 flux, which is intercepted by the crop
            0.9-fraction of radiation absorbed by the crop 
                allowing for a 6 percent albedo and for inactive 
                radiation absorption
        """
        
        
        return Rs*0.5*0.9*(1-interception)
    def intercept(self,LAI,k=0.5):
        """ The relationship between I/I0 and LAI fits a
        negative exponential (similar to the Beer Lambert Law).
        
        LAI-Leaf area index (m2/m2)
        k - canopy extinction coefficien
        
        canopy extinction coefficient in wheat crops ranges
        from 0.3 to 0.7 and is highly dependent on leaf angle
        (low K for erect leaves). From equation 3, it can be calculated that
        95 percent PAR interception requires a LAI as high as 7.5 for erect 
        leaves but a LAI of only about 4.0 for more horizontal leaves
        """
        return exp(-k*LAI)
    def grow(self,PARa,RUE=3.0):
        """ total canopy net photosynthesis is linearly related to PARA and so is 
        crop growth rate (CGR, g/m2 d), which is the net accumulation of dry weight
        
        RUE - radiation use efficiency (g/m2 d)
        
        Measured values of RUE in a wheat crop are close to 3.0 
        g/MJ PARA when roots are included
        """
        return RUE * PARa
    def grain_yield(self,KNO,KW=0.041):#KW for wheat
        """ Return GY
        
        KNO is established in the period between 20 and 30 days 
        before flowering and ten days after anthesis.
        
        GY - grain yield (g/m2)
        KNO - the kernel number (m-2)
        KW - the kernel weight (g)
        """
        return KNO*KW
    def harvest(self,GrainYield,HarvestIndex=1.):
        return GrainYield*HarvestIndex
    
    def kernel_number(self,spike_dryweight):
        """ Spike dry weight appears to be a major determinant of KNO
        """
        pass
    
    
    
    
    
    
    
    