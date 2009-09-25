class Leaf():
    def __init(self,specific_weight):
        self.specific_weight=specific_weight
        self.lai=0.
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
    
