from pylab import *
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
        self.uptake=Uptake()
    def __call__(self,time_act,time_step,W_max,growth_factor,root_verticalgrowth,root_percent,shoot_percent,tbase,development,soil,atmosphere,h_plant):
        """
        Description:
    
        Parameter:
        
        Returns:
        """
        self.stage(time_step,atmosphere.get_tmin(time_act),atmosphere.get_tmax(time_act),tbase,development)#calculates total_thermaltime and stage 
        if self.stage.total_thermaltime>=development[0][0] and self.stage.total_thermaltime<=development[0][-1]:#restrict growth due to the development 
            self.uptake(self.root.depth,atmosphere.get_etp(time_act),self.nutrient_demand(),h_plant,10.,soil)
            Wp_potential=self.assimilate(self.Wp_total, W_max, growth_factor)
            Wp_actual=Wp_potential*1.#self.stress_response(T_p, S_h)
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
    def perspire(self,T_p):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        return T_p
    def nutrient_demand(self):
        """
        Description: 
        
        Parameter: time_step
        
        Returns:
        """
        return 100.
    def stress_response(self):
        pass
    
class Uptake():
    def __init__(self):
        self.p_a=[]
        self.a_a=[]
        self.s_h=[]
    def __call__(self,Z_r,T_p,R_p,h_plant,depth_step,soil,c_max=1.,K_m=0.,c_min=0.):
        """
        Description: Calculates the root water and nutrient uptake for a given timestep
                     in the root zone.
    
        Parameter: Z_r = Total rootingdepth at t, T_p = Potential transpiration,
                   R_p = Potential root nutrient uptake, h_plant = critical pressurehead of
                   plant for soil water extraction, depth_step = layer thickness for pressure-
                   head and nutrient_c request, soil = Soil-Instance, c_max = maximal allowed 
                   nutrient concentration,Mechaelis-Menten constant, c_min = minimum concetration 
                   at which no net influx occurs.
        
        Returns: Set p_a = Passive nutrient uptake per timestep, a_a = active nutrient uptake
                 per timestep, s_h = root extractable soil water
        """
        s_h_list=[];p_a_list=[];a_a_list=[]
        s_p=self.water_extractionrate(T_p, Z_r)#s_p = root water extraction rate
        for depth in arange(0.,Z_r,depth_step):
            alpha=self.sink_therm(soil.get_pressurehead(depth+depth_step), h_plant)#sink_therm alpha
            if depth+depth_step<=Z_r:s_h=s_p*alpha*depth_step#uptake from each layer, which are completely penetrated
            else: s_h=alpha*s_p*(Z_r-depth)##uptake from layer which are partly penetrated
            s_h_list.append(s_h)
            p_a=self.passive_nutrientuptake(s_h, soil.get_nutrients(depth+depth_step),c_max)
            p_a_list.append(p_a)
        P_a=sum(p_a_list)
        A_p=max(R_p-P_a,0)#A_p = Potential acitve nutrient uptake
        a_p=A_p/Z_r#a_p = Potential acitve nutrient uptake from soil layer
        for depth in arange(0.,Z_r,depth_step):
            nutrient_c=soil.get_nutrients(depth+depth_step)
            if depth+depth_step<=Z_r:a_a=a_p*self.michaelis_menten(nutrient_c, K_m, c_min)*depth_step
            else: a_a=a_p*self.michaelis_menten(nutrient_c, K_m, c_min)*(Z_r-depth)
            a_a_list.append(a_a)
        A_a=sum(a_a_list)#A_a = Actual acitve nutrient uptake
        R_a=P_a+A_a#R_a = Actual root nutrient uptake
        self.a_a.append(a_a_list)
        self.p_a.append(p_a_list)
        self.s_h.append(s_h_list)
    def water_extractionrate(self,T_p,Z_r): 
        """
        Description:Calculates the maximum possible root water extraction rate over the rootingdepth.
        
        Parameter:T_p = potential transpiration, Z_r = total rootingdepth
            
        Returns:s_p = root water extraction rate
        """
        return T_p/Z_r
    def sink_therm(self,h_soil,h_plant): 
        """
        Description: Calculates alpha(h): a dimensionless prescribed function of soil water pressure head,
                     with values between or equal zero and one.
    
        Parameter:h_soil = pressure head in soil compartment, 
                           h_plant = list with critical pressureheads for the plant
        
        Returns: sink_therm alpha
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err
    def passive_nutrientuptake(self,s_p,c_nutrient,c_max):
        """
        Description: Calculates the passive uptake with water uptake. c_max is hte maximum allowed
                     solution concetration that can be taken up by plant roots during passive uptake.
        
    
        Parameter: s_p = root water extraction rate, c_nutrient = nutrient concentration in soil layer,
                   c_max = maximal allowed nutrient concentration.
        
        Returns: p_a = actual passive nutrient uptake from soil layer.
        """
        return s_p*min(c_nutrient,c_max)
    def michaelis_menten(self,nutrient_c,K_m,c_min):
        """
        Description: Calculates the uptake kinetics wit hthe michaelis menton function.
    
        Parameter: nutrient_c = soillayer nutrient concentration ,K_m = Mechaelis-Menten constant,
                   c_min = minimum concetration at which no net influx occurs.
        
        Returns: I_n = Relationship bewteen ion influx (uptake per unit root and unit time) and its
                 concetration at the root surface (nurient_c).
        """
        return (nutrient_c-c_min)/(K_m+nutrient_c-c_min)
    
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
    

