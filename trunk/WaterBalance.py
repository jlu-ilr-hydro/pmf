class WaterBalance_MatrixPotential:
    def __init__(self,max_compensation_capacity=2.):
        self.max_compensation_capacity=max_compensation_capacity
        self.s_h=[]
        self.alpha=[]
        self.compensation=[]
        self.s_h_compensated=[]
    @property
    def uptake(self):
        return self.s_h
    @property
    def uptake_comp(self):
        return self.compensation
    @property
    def stress(self):
        return self.alpha
    def __call__(self,s_p,matrix_potential,pressure_threshold):
        self.s_h =[s * self.sink_term(matrix_potential[i], pressure_threshold)for i,s in enumerate(s_p)]
        self.alpha = [self.sink_term(m,pressure_threshold)for m in matrix_potential]
        self.compensation = self.compensate(self.s_h,s_p,matrix_potential, self.alpha, pressure_threshold[2],
                                               self.max_compensation_capacity)
        self.s_h_compensated=[s_h + self.compensation[i] for i,s_h in enumerate(self.s_h)]
    def compensate(self,s_h,s_p,matrix_potential,alpha,max_opt_pressure,max_compensation_capacity):
        remaining_alpha= [max(1-(m/max_opt_pressure),0.) for i,m in enumerate(matrix_potential)] 
        remaining_uptake=sum(s_p)-sum(s_h)
        return [min(r/sum(remaining_alpha)*remaining_uptake,max_compensation_capacity*s_h[i])for i,r in enumerate(remaining_alpha)]     
    def sink_term(self,h_soil,h_plant): 
        """
        call signature:
        
            sink_therm(h_soil,h_plant)
        
        Calculates alpha(h): a dimensionless prescribed function of s
        oil water pressure head with values between or equal zero and one.
    
        h_soil = pressure head in soil compartment and h_plant = list 
        with critical pressureheads for the plant. Both variables
        are list with the following structure:
        h_plant is a list with four values with the criticall pressurehead for water
        uptake, e.g. [0.,100.,500.,16000.](float-values). plant_N is a list with four 
        values with crop coefficiants for the phenological depending decline of 
        the biomass nitrogen content, e.g. [100,0.43,1000,0.16].
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err
            
class WaterBalance_ContainerApproach:
    pass

