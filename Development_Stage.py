class Development_Stage:
    """
    Description: Development_Stage is part from plant and cannot stand alone. 
                 Development depends on daily temperature (tmax, tmin) and 
                 a crop associated base temperature (tb) over which development 
                 can occur. A development stage is defined by the cumulative sum 
                 of GDD (Growing Degree Day)
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
     
    def __init__(self):
        self.total_thermaltime=0.
        self.stage=0
    def __call__(self,time_step,tmax,tmin,tbase,development):
        """
        Description: Computes the development of the plant bases on thermaltime and
                     plant specific accumulated thermaltime for each development stage.
    
        Parameter: developmet [list with deveolment stages in accumulated thermaltime],
                   tmax [Celsius], tmin [Celsius], tbase [Celsius]
        
        Returns: set total_thermaltime [Celsius]
        """
        self.total_thermaltime=self.total_thermaltime+self.thermaltime(tmin, tmax, tbase)*time_step
        self.stage=self.get_stage(self.total_thermaltime,development)
    def thermaltime(self,tmin,tmax,tbase):
        """
        Description: Thermaltime computes the additional thermal time per timestep.
                     The parameters tmin and tmax are given from the atmosphere-interface
                     and tbase from the plant class.
    
        Parameter: tmin [Celsius], tmax [Celsius], tbase [Celsius]
        
        Returns: Additional thermaltime [Celsius]
        """
        if tmax < tbase or tmin < tbase:
            return 0
        else:
            return ((tmax+tmin)/2.0-tbase)
    def get_stage(self,total_thermaltime,development):
        for stage in development:
            if total_thermaltime<=stage:
                break
        return development.index(stage)

        
        