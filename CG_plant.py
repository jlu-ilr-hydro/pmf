class Plant:
    """
    Description:
    
    Parameter:
        
    Returns:
    """
    def __init__(self):
        self.Wp_total=1.
        self.R=0.
        self.stage=Stage()
        self.root=Root()
        self.shoot=Shoot()
    def __call__(self,time_act,time_step,W_max,growth_factor,root_verticalgrowth,root_percent,shoot_percent,tbase,development,soil,atmosphere):
        """
        Description:
    
        Parameter:
        
        Returns:
        """
        
        self.stage(time_step,atmosphere.get_tmin(time_act),atmosphere.get_tmax(time_act),tbase,development)   #time_step,tmax,tmin,tbase,development 
        if self.stage.total_thermaltime>=development[0][0] and self.stage.total_thermaltime<=development[0][-1]: 
            Wp_potential=self.assimilate(self.Wp_total, W_max, growth_factor)
            Wp_actual=Wp_potential*1.
            self.R=self.respire(0.5,Wp_actual,0.5,self.Wp_total)
            self.root(time_step,root_verticalgrowth,Wp_actual,root_percent,soil.get_bulkdensity(self.root.depth))
            self.shoot(time_step,Wp_actual,shoot_percent)
            self.Wp_total=self.Wp_total+Wp_actual*time_step
    def assimilate(self,Wp_total,Wp_max,growth_factor):
        """
        Description: The process of assimilation is simulated by a logistic growth function:
                     dW/dt = rW(1-W/K),where the amount of drymass in every time step(dW/dt)[g] 
                     depends on a growth  coefficiant(r)[-]and the whole drymass (W)[g]. The
                     amount of whole drymass is limited by a capacity limit (K)[g].
        
        Parameter: W_total,W_max,growth_factor
            
        Returns: W_actual
        """
        return growth_factor*Wp_total*(1.0-Wp_total/Wp_max)
    def respire(self,a,Wp_actual,b,Wp_total):
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
        return a*Wp_actual+b*Wp_total

class Root:
    """
    Description: Root is part from plant and cannot stand alone. It represents the under-
    ground drymass and the rooting depth.
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.depth=0.
        self.Wr_total=0.
    def __call__(self,time_step,root_verticalgrowth,Wp_actual,root_percent,BD_rootingdepth):
        """
        Description: Computes the root growth. Three steps:
                     a) Vertical growth (rooting depth),
                     b) Root-drymass-partitioning (root drymass) and
                     c) Branchning and drymass allocation (distribution over rootindepth) --> not implemented.
        
        Parameter: time_step, pot_vertical_growth [cm/step], plant_growthrate [g/step] , root_percent [fraction]
        
        Returns: set root depth [cm], drymass [g]
        """
        self.depth=self.depth+self.vertical_growth(self.physical_constraints(BD_rootingdepth), root_verticalgrowth)
        self.Wr_total=self.Wr_total+self.root_partitioning(root_percent, Wp_actual)*time_step
    def vertical_growth(self,physical_constraints,root_verticalgrowth):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        return root_verticalgrowth-physical_constraints*root_verticalgrowth
    def physical_constraints(self,BD_rootingdepth):
        """
        Description: Computes resistance against soil penetration (physical_stress) from
                     the most restricting factor of mechanical impendance, water stress
                     and oxygen deficiency.
        
        Parameter: bulkdensity [g/cm^3], pressurehead [cm]
        
        Returns: Most restricting factor; value between zero (no stres) and one (no penetration possible)
        """
        if BD_rootingdepth > 1.5: mechanical_impendance=0.5
        else: mechanical_impendance=0.
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
    
class Shoot:
    """
    Description: Shoot is part from plant and cannot stand alone. It represents the above-
    ground drymass and the respiration. Shoot owns leaf, storage organs and stem.
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.Ws_total=0.
        self.respiration=0.
        self.leaf=Leaf()
        self.stem=Stem()
        self.storage_organs=Storage_Organs()
    def __call__(self,time_step,Wp_actual,shoot_percent):
        """
        Description: Computes the additional root drymass as fraction from the plant growthrate
                     and the respiration.
        
        Parameter: time_step, plant_act_growthrate [drymass/step] , Shoot_percent [fraction]
        
        Returns: set shoot_drymass [g]
        """
        Ws_actual=self.shoot_partitioning(shoot_percent, Wp_actual)
        self.respiration=self.respire(self.Ws_total, Ws_actual, 1., 1.)
        self.Ws_total=self.Ws_total+Ws_actual*time_step
    def shoot_partitioning(self,shoot_percent,Wp_actual):
        """
        Description: Computes the additional shoot drymass as fraction from the plant growthrate.
        
        Parameter: plant_growthrate [drymass/step] , shoot_percent [fraction]
        
        Returns: Shoot_growthrate [g]
        """
        return shoot_percent*Wp_actual
    def respire(self,Ws_total,Ws_actual,a,b):
        """
        Description: Respiration is computed from the actual growth rate (growth respiration) and
                     the total dry mass (maintenance respiration) with two constants a and b with the
                     following equation: R = a(dW/dt)+bW, where a [g CO2 (kg drymass)-1] and b a 
                     [g CO2 (kg drymass)-1] are constants, R is respiration [g CO2], Wtotal [g] the 
                     total drymatter at timestep and Wactual the actual growthrate.
        
        Parameter: plant_growthrate [drymass/step] , shoot_percent [fraction]
        
        Returns: Shoot_growthrate [g]
        """
        return a*Ws_actual+b*Ws_total

class Stem:
    """
    Description: Storage_Organs is part from shoot and cannot stand alone. 
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.W_total=0.
    def __call__(self,time_step):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
    def grow(self):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        pass
    
class Storage_Organs:
    """
    Description: Storage_Organs is part from shoot and cannot stand alone. 
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.W_total=0.
    def __call__(self,time_step):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
    def grow(self):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        pass
    
class Leaf:
    """
    Description: Root is part from shoot and cannot stand alone. 
    
    Parameter:  The required paramerters are named in the __call__ method.
        
    Returns: ---
    """
    def __init__(self):
        self.W_total=0.
        self.leafarea=0.
    def __call__(self,time_step):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
    def grow(self):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        pass
    
class Stage:
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
    
        Parameter: developmet [list with two lists:[thermaltime],[names]],
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
        """
        Description: get_stage computes the actual plant stage 
        
        Parameter: total_thermaltime, list with development stages
        
        Returns: Plant Stage (String)
        """
        for stage in development[0]:
            if total_thermaltime<=stage:
                return development[1][development[0].index(stage)]
                break
    

