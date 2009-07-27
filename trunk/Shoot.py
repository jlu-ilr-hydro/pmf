class Shoot:
    """
    Description: Shoot is part from plant and cannot stand alone. It represents the above-
    ground drymass and the respiration. Shoot owns leaf, storage organs and stem.
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.drymass=0.
        self.respiration=0.
        self.leaf=Leaf()
        self.stem=Stem()
        self.Sorage_Organs=Sorage_Organs()
    def __call__(self,time_step,shoot_percent,plant_growthrate):
        """
        Description: Computes the additional root drymass as fraction from the plant growthrate
                     and the respiration.
        
        Parameter: time_step, plant_act_growthrate [drymass/step] , Shoot_percent [fraction]
        
        Returns: set shoot_drymass [g]
        """
        growthrate=self.shoot_partitioning(shoot_percent, plant_growthrate)
        self.respiration=self.respire(self.drymass, growthrate, 1., 1.)
        self.drymass=self.drymass+growthrate*time_step
    def shoot_partitioning(self,shoot_percent,plant_growthrate):
        """
        Description: Computes the additional shoot drymass as fraction from the plant growthrate.
        
        Parameter: plant_growthrate [drymass/step] , shoot_percent [fraction]
        
        Returns: Shoot_growthrate [g]
        """
        return shoot_percent*plant_growthrate
    def respire(self,drymass,growthrate,a,b):
        """
        Description: Respiration is computed from the actual growth rate (growth respiration) and
                     the total dry mass (maintenance respiration) with two constants a and b with the
                     following equation: R = a(dW/dt)+bW, where a [g CO2 (kg drymass)-1] and b a 
                     [g CO2 (kg drymass)-1] are constants, R is respiration [g CO2], Wtotal [g] the 
                     total drymatter at timestep and Wactual the actual growthrate.
        
        Parameter: plant_growthrate [drymass/step] , shoot_percent [fraction]
        
        Returns: Shoot_growthrate [g]
        """
        return a*growthrate+b*drymass
    
s=Shoot()