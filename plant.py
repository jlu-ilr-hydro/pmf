class Plant:
    """
    Description:
    
    Parameter:
        
    Returns:
    """
    def __init__(self):
        self.W_total=1.
        self.R=0.
    def __call__(self,time_step,W_max,growth_factor):
        """
        Description:
    
        Parameter:
        
        Returns:
        """
        W_potential=self.assimilate(self.W_total, W_max, growth_factor)
        W_actual=W_potential*1.
        self.R=self.respire(1,W_actual,1,self.W_total)
        self.W_total=self.W_total+W_actual*time_step
    def assimilate(self,W_total,W_max,growth_factor):
        """
        Description: The process of assimilation is simulated by a logistic growth function:
                     dW/dt = rW(1-W/K),where the amount of drymass in every time step(dW/dt)[g] 
                     depends on a growth  coefficiant(r)[-]and the whole drymass (W)[g]. The
                     amount of whole drymass is limited by a capacity limit (K)[g].
        
        Parameter: W_total,W_max,growth_factor
            
        Returns: W_actual
        """
        return growth_factor*W_total*(1.0-W_total/W_max)
    def respire(self,a,W_actual,b,W_total):
        """
        Description:Respiration is computed from the actual growth rate (growth respiration) and
                    the total dry mass (maintenance respiration) with two constants a and b with the
                    following equation: Repiration: R = a(dW/dt)+bW, where a [g CO2 (kg drymass)-1] 
                    and b a [g CO2 (kg drymass)-1] are constants, R is respiration [g CO2], 
                    Wtotaranspiration_ratel [g] the total drymatter at timestep and Wactual 
                    the actual growthrate
    
        Parameter: a,W_actual,b,W_total
        
        Returns: Respiration
        """
        return a*W_actual+b*W_total
    
from datetime import *
p=Plant()
p(timedelta(1).days,1000,0.05)
print p.W_total,p.R