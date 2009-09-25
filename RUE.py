from pylab import *
class Biomass:
    def __init__(self,RUE,k):
        self.RUE=RUE
        self.k=k
        self.total=0.
        self.growthrate=0.
    @property
    def GrowthRate(self):
        return self.growthrate
    @property
    def Total(self):
        return self.total
    def __call__(self,Rs,LAI):
        self.growthrate = self.grow(self.PAR_a(Rs, self.intercept(LAI, self.k)), self.RUE)
        self.total += self.growthrate
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
    def intercept(self,LAI,k):
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
    def grow(self,PARa,RUE):
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
class Leaf:
    def __init__(self,specific_weight):
        self.specific_weight=specific_weight
        self.lai=1.
    @property
    def LAI(self):
        return self.lai
    def __call__(self,biomass):
        self.lai+=self.convert(biomass, self.specific_weight)
    def convert(self,biomass,specific_weight):
        """ Calculates LAI [ha/ha]:
        
        The growth of leaf area is related to growth in leaf weight.
        The specific leaf weight of new leaves change with crop age.
        Leaf area is determined by dividing the weight of
        live leaves by the specific leaf weight
        
        biomass - biomass of the leafs[kg/ha]
        specific_weight - dry weight of leaves (no reserves,
        only structural dry matter) with a total one-sided 
        leaf area of one hectare [kg/ha]
        """
        return biomass/specific_weight
    def get_specific_weight(self,thermaltime,fixed_specific_weight):
        """
        The specific leaf weight of new leaves is calculated by
        multiplying the specific leaf weight constant with a factor that depends on the
        development stage of the crop.
        """
        weight_factor=1.
        return weight_factor*fixed_specific_weight
     
plant=Biomass(3.,0.5)
leaf=Leaf(40.)
day=1
res=[]
Rs=12


while day<=100:
    plant(Rs,leaf.LAI)
    fraction=.5 if day<50 and day>15 else 0.
    leaf(plant.GrowthRate*0.75*fraction)
    res.append(plant.Total)
    print 'growthrate g/m2 %4.2f, biomass g/m2 %4.2f, PAR MJ/m2 %4.2f, LAI m2/m2 %4.2f' % (plant.GrowthRate,plant.Total,plant.PAR_a(Rs, plant.intercept(leaf.LAI, plant.k)),leaf.LAI)
    day+=1











