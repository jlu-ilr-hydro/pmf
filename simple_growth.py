from pylab import *

class Plant:
    """
    The plant class must be implemented wit ha soil and a atmosphere interface:
    class Soil:
    def get_wetness(self,depth):
        pass
    def get_nutrients(self,depth):
        pass
    def get_bulkdensity(self,depth):
        pass

    class Atmosphere:
    def get_etp(self,time): 
        pass
    def get_tmax(self,time):
        pass
    def get_tmin(self,time):
        pass 
    
    Default values:
    
    shootpercent=0.7,leaf_appearance=1,rootpercent=0.3,root_elongation=0.5,tb=5.,growth_factor=0.05,maxdrymass=1000 
     
    """
    def __init__(self,Soil,Atmosphere,shootpercent=0.7,leaf_appearance=1,rootpercent=0.3,root_elongation=0.5,tb=5.,growth_factor=0.05,W_max=1000):
        self.shoot=Shoot(shootpercent,leaf_appearance,self)
        self.root=Root(rootpercent,root_elongation,self)
        self.growingseason=Growingseason(self)
        self.soil=Soil
        self.atmosphere=Atmosphere
        self.tb=tb
        self.W_max=W_max
        self.growth_factor=growth_factor
        self.gdd=0
        self.stage=''
        self.W_tot=1
        self.values=[]
    def grow(self,step,act_time):
        gdd_rate=self.growingseason.thermaltime(self.atmosphere.get_tmin(act_time), self.atmosphere.get_tmax(act_time), self.tb)
        self.gdd+=gdd_rate
        self.stage=self.growingseason.getstage(self.gdd)
        W_pot=self.assimilate(self.W_tot,self.W_max,self.growth_factor)
        water_demand=self.perspire(self.atmosphere.get_etp(act_time))
        nutrient_demand=self.nutrientdemand(W_pot, 0.05)
        water_content=10
        water_uptake=self.wateruptake(water_demand, water_content)
        nutrient_conc=0.5
        nutrient_content=water_content*nutrient_conc
        nutrient_uptake=self.nutrientuptake(nutrient_demand, water_uptake, nutrient_conc, nutrient_content)
        stress_factor=self.stress(water_uptake, water_demand, nutrient_uptake, nutrient_demand)
        W_act=W_pot-W_pot*stress_factor
        R=self.respire(self.W_tot, W_act, 0.05, 0.5)
        self.W_tot+=W_act
        self.values=[W_pot,W_act,self.W_tot,gdd_rate,water_demand,nutrient_demand,water_uptake,nutrient_uptake,stress_factor,R]
    def assimilate(self,W_total,K,r):
        """
        The process of assimilation is simulated by a logistic growth function as follows:
        
        Logistic function: dW/dt = rW(1-W/K),
        
        where the amount of drymass in every time step (dW/dt) [g] depends on a growth 
        coefficiant(r)[-]and the whole drymass (W)[g]. The amount of whole drymass is 
        limited by a capacity limit (K)[g].
        """
        return r*W_total*(1.0-W_total/K)
    def respire(self,W_tot,W_act,a,b):
        """
        Respiration is computed from the actual growth rate (growth respiration) and
        the total dry mass (maintenance respiration) with two constants a and b with the
        following equation:
        
        Repiration: R = a(dW/dt)+bW,
        
        where a [g CO2 (kg drymass)-1] and b a [g CO2 (kg drymass)-1] are constants,
        R is respiration [g CO2], Wtotal [g] the total drymatter at timestep and Wactual 
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
    def stress(self,water_uptake,water_demand,nutrient_uptake,nutrient_demand):
        """
        Less nutrient or water uptake can limit potential growth, but only the most limiting factor reduces the growth.
        
        stress = 1-min(water_uptake/water_demand,nutrient_uptake/nutrient_demand),
        
        where stress response [-] is a dimensionless coefficient between zero (no stress) and one (fully stressed). 
        """
        
        return 1-min(water_uptake/water_demand,nutrient_uptake/nutrient_demand)
    def wateruptake(self,water_demand,water_content):
        """
        The remaining wateruptake is computed from the following equation from every soil horizon limited by the rootingdepth:
        
        Wateruptake = min(water_demand,water_content),
        
        where Wateruptake [mm] is the uptake for a time step from a specific depth, Waterdemand [mm]
        is equal to potential transpiration and Watercontent[mm] is the water content of the soil.
        """
        return min(water_demand,water_content)                         
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
    def __init__(self,rootpercent,root_elongation,Plant):
        self.elongation_factor=root_elongation
        self.rootpercent=rootpercent
        self.plant=Plant
    def grow(self,drymass):
        pass
    def partitioninggrowth(self,Wactual,rootpercent):
        """
        The root drymass is calculated as fraction from the Wactual.
        """
        return Wactual*rootpercent
    def elongation(self,bulkdensity,rooting_rate):
        return rooting_rate*bulkdensity
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
class Shoot:
    def __init__(self,shootpercent,leaf_appearance,Plant):
        self.shootpercent=shootpercent
        self.plant=Plant
        self.leaf=Leaf(leaf_appearance,self)
    def grow(self,drymass):
        pass
    def partitioninggrowth(self,drymass,shootpercent):
        """Shoot dry mass [g] is proportional to the plant dry mass"""
        return shootpercent*drymass
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

class Soil:
    def get_wetness(self,depth):
        pass
    def get_nutrients(self,depth):
        pass
    def get_bulkdensity(self,depth):
        pass

class Atmosphere:
    def get_etp(self,time): 
        pass
    def get_tmax(self,time):
        pass
    def get_tmin(self,time):
        pass  