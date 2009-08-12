class Plant():
    def __init__(self):
        pass
    def __call__(self,plant_N,thermaltime,Wp_pot,N_uptake):
        return self.N_shortage(self.N_demand(Wp_pot, self.N_content(plant_N, thermaltime)), N_uptake)
    def N_content(self,plant_N,thermaltime):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        if thermaltime<=plant_N[0][0]: return plant_N[0][1]
        elif thermaltime>=plant_N[1][0]: return plant_N[1][1]
        else: return plant_N[0][1]+(plant_N[1][1]-plant_N[0][1])/(plant_N[1][0]-plant_N[0][0])*(thermaltime-plant_N[0][0])
    def N_demand(self,Wp_pot,N_content):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        return Wp_pot*N_content
    def N_shortage(self,N_demand,N_uptake):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        return min(N_uptake/N_demand,1.)

plant_N=[[100,0.43],[1000,0.16]]   
plant=Plant()
print plant(plant_N,1,10,10)

