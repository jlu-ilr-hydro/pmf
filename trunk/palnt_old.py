class Plant:
    """    
    Default values:
    shootpercent=0.7,leaf_appearance=1,rootpercent=0.3,tb=5.,growth_factor=0.05,maxdrymass=1000 
    """
    def __init__(self,Soil,Atmosphere,shootpercent=0.7,leaf_appearance=1,rootpercent=0.3,tb=0.,growth_factor=0.05,W_max=1000):
        self.shoot=Shoot(shootpercent,leaf_appearance,self)
        self.root=Root(rootpercent,self)
        self.growingseason=Growingseason(self)
        self.soil=Soil
        self.atmosphere=Atmosphere
        self.tb=tb
        self.W_max=W_max
        self.growth_factor=growth_factor
        self.gdd=0
        self.W_tot=1
    def shoot_root_ratio(self):
        pass
        #irgnedewas ausdenken
    def assimilate(self,W_tot,K,r):
        """
        The process of assimilation is simulated by a logistic growth function as follows:
        
        Logistic function: dW/dt = rW(1-W/K),
        
        where the amount of drymass in every time step (dW/dt) [g] depends on a growth 
        coefficiant(r)[-]and the whole drymass (W)[g]. The amount of whole drymass is 
        limited by a capacity limit (K)[g].
        """
        return r*W_tot*(1.0-W_tot/K)
    def respire(self,W_tot,W_act,a,b):
        """
        Respiration is computed from the actual growth rate (growth respiration) and
        the total dry mass (maintenance respiration) with two constants a and b with the
        following equation:
        
        Repiration: R = a(dW/dt)+bW,
        
        where a [g CO2 (kg drymass)-1] and b a [g CO2 (kg drymass)-1] are constants,
        R is respiration [g CO2], Wtotaranspiration_ratel [g] the total drymatter at timestep and Wactual 
        the actual growthrate.
        """
        return a*W_act+b*W_tot
    def perspire(self,transpiration_rate):
        """ Transpiration is not calculated by the model for itself.
        """
        return transpiration_rate
    def nutrientdemand(self,W_pot,nutrient_fraction):
        """
        Nutrient demand (only Nitrogen) is calculated from dry mass with a nutrientfraction.
        This factor is the fractional nitrogen content of the dry mass.
        
        Nutrientdemand = W_potential * Nutrient_fraction,
        
        where Nutrientfraction [g N * W-1] is the nitrogen content of the drymass
        and Nutrientdemand [g] is the nutrient demand in this time step.
        """
        return nutrient_fraction*W_pot
    def harvest(self,drymass,harvest_index):
        """
        Harvest returns the Yield as product from Wtotal and a harvest_index
        
        Yield = Wtotal * harvest_index,
        
        with Yield [g] and Wtotal [g] and a harvest_index [-]
        """
        return drymass*harvest_index
    def stress_response(self,water_uptake,water_demand,nutrient_uptake,nutrient_demand):
        """
        Less nutrient or water uptake can limit potential growth, but only the most limiting factor reduces the growth.
        
        stress = 1-min(water_uptake/water_demand,nutrient_uptake/nutrient_demand),
        
        where stress response [-] is a dimensionless coefficient between zero (no stress) and one (fully stressed). 
        """
        
        return 1-min(water_uptake/water_demand,nutrient_uptake/nutrient_demand)                        
    def nutrientuptake(self,nutrient_demand,water_uptake,nutrient_conc,nutrient_content):
        """
        Total nutrient uptake depends on active and passive uptake. Passive uptake is proportitional to wateruptake.
        Can passive uptake don't satify the plant nutrient demand, active uptake will occur. The total uptake is limited by
        the soil nitrogen content and the rooting depth.
        
        [...]
        
        where Nutrientactive,passive, total [g] are the total and the components of uptake from the soil compartments.
        """
        nutrient_passive=min(water_uptake*nutrient_conc,nutrient_demand,nutrient_content)
        nutrient_active=min(max(nutrient_demand-nutrient_passive,0),nutrient_content-nutrient_passive)
        nutrient_total=nutrient_active+nutrient_passive
        return nutrient_total
    
class Growingseason:
    """
    Development depends on daily temperature (tmax, tmin) and a crop associated base temperature (tb)
    over which development can occur. A development stage is defined by the cumulative sum of GDD (Growing Degree Day)
    """    
    def __init__(self,plant):
        self.stage=[]
        self.plant=Plant
    def __setitem__(self,index,name,tt):
        self.stage.append(Stage(name,tt))
    def __getitem__(self,index):
        return self.stage[index]
    def __iter__(self):
        for s in self.stage:
            yield s
    def thermaltime(self,tmin,tmax,tb):
        """
        GDD = (tmax+tmin)/2.0-tb),
        
        where GGD [Celsius] is the difference between daily mean temperature [Celsius]  and tbase [Celsius].
        For tmax or tmin < tb, GDD is set to zero. 
        """
        if tmax < tb or tmin < tb:
            return 0
        else:
            return ((tmax+tmin)/2.0-tb)
    def getstage(self,gdd):
        """
        Returns the actual stage depending on the actual amounbt of GDD.
        """
        for stage in self.stage:
            if gdd <= stage.gdd:
                return stage.name
                break        

class Stage:
    """
    The stage class definese deveopment stages with name and accumulated GDDs.
    """
    def __init__(self,name,gdd):
        self.name=name
        self.gdd=gdd
         
class Root:
    def __init__(self,rootpercent,Plant):
        self.rootpercent=rootpercent
        self.W_tot=0
        self.depth=0
        self.plant=Plant
    def grow(self,drymass):
        pass
    def partitioning(self,W_act,rootpercent):
        """
        The root drymass is calculated as fraction from the Wactual.
        """
        return W_act*rootpercent
    def elongation(self,bulkdensity,rooting_rate):
        return bulkdensity*rooting_rate
    def respire(self,W_total,W_actual,a,b):
        """
        Respiration is computed from the actual growth rate (growth respiration) and
        the total dry mass (maintenance respiration) with two constants a and b with the
        following equation:
        
        Repiration: R = a(dW/dt)+bW,
        
        where a [g CO2 (kg drymass)-1] and b a [g CO2 (kg drymass)-1] are constants,
        R is respiration [g CO2], Wtotal [g] the total drymatter at timestep and Wactual 
        the actual growthrate.
        """
        return a*W_actual+b*W_total
    def sink_therm_alpha(h):#calculates sink therm alpha depending on h=soil water pressure head(cm)
        return 1 # later fuzzy set
    def wateruptake_homogeneous(self,T_p,Z_r):
        """
        T_P=potential transpiration (cm*d^-1), Z_r=root-zone depth (cm)
        """
        return T_p/Z_r 
    def wateruptake_heterogeneous(self,T_p,Z_r,z):
        """
        T_P=potential transpiration (cm*d^-1), Z_r=root-zone depth (cm), z=depth (cm)
        """
        return 2*T_p/Z_r*(1-z/Z_r)
    def wateruptake_nonhomogeneous(self,T_p,L_r,l_r,z):
        """
        T_P=potential transpiration (cm*d^-1), L_r=root mass or the root length density(cm cm-3),z=depth(cm)
        """
        return l_r/L_r*T_p

class Shoot:
    def __init__(self,shootpercent,leaf_appearance,Plant):
        self.shootpercent=shootpercent
        self.plant=Plant
        self.W_tot=0
        self.leaf=Leaf(leaf_appearance,self)
    def grow(self,drymass):
        pass
    def partitioning(self,W_act,shootpercent):
        """Shoot dry mass [g] is proportional to the plant dry mass"""
        return W_act*shootpercent
    def respire(self,W_total,W_actual,a,b):
        """
        Respiration is computed from the actual growth rate (growth respiration) and
        the total dry mass (maintenance respiration) with two constants a and b with the
        following equation:
        
        Repiration: R = a(dW/dt)+bW,
        
        where a [g CO2 (kg drymass)-1] and b a [g CO2 (kg drymass)-1] are constants,
        R is respiration [g CO2], Wtotal [g] the total drymatter at timestep and Wactual 
        the actual growthrate.
        """
        return a*W_actual+b*W_total

class Leaf:
    def __init__(self,leaf_appearance,Shoot):
        self.appearance_rate=leaf_appearance
        self.shoot=Shoot
    def grow(self,appearance_rate):
        return appearance_rate