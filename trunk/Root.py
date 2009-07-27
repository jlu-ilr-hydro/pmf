class Root:
    """
    Description: Root is part from plant and cannot stand alone. It represents the under-
    ground drymass and the rooting depth.
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.depth=0.
        self.drymass=0.
    def __call__(self,time_step,pot_vertical_growth,plant_growthrate,root_percent):
        """
        Description: Computes the root growth. Three steps:
                     a) Vertical growth (rooting depth),
                     b) Root-drymass-partitioning (root drymass) and
                     c) Branchning and drymass allocation (distribution over rootindepth) --> not implemented.
        
        Parameter: time_step, pot_vertical_growth [cm/step], plant_growthrate [g/step] , root_percent [fraction]
        
        Returns: set root depth [cm], drymass [g]
        """
        self.depth=self.depth+pot_vertical_growth-pot_vertical_growth*self.physical_constraints()*time_step
        self.drymass=self.drymass+self.root_partitioning(root_percent, plant_growthrate)*time_step
    def physical_constraints(self):
        """
        Description: Computes resistance against soil penetration (physical_stress) from
                     the most restricting factor of mechanical impendance, water stress
                     and oxygen deficiency.
        
        Parameter: bulkdensity [g/cm^3], matrix_potential [cm]
        
        Returns: Most restricting factor; value between zero (no stres) and one (no penetration possible)
        """
        mechanical_impendance=0.
        water_stress=0.
        oxygen_deficiency=0.
        return max(mechanical_impendance,water_stress,oxygen_deficiency)
    def root_partitioning(self,root_percent,plant_growthrate):
        """
        Description: Computes the additional root drymass as fraction from the plant growthrate.
        
        Parameter: plant_growthrate [drymass/step] , root_percent [fraction]
        
        Returns: Root_growthrate [g]
        """
        return root_percent*plant_growthrate

