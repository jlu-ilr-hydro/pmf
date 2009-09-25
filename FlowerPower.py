from pylab import *
class Plant:
    Count=0.
    """
    call signature:
    
        Plant()
        
    Create plant class instance. Plant for itselft implements shoot and
    root class.
    
    To start the growth process for a given timstep root must be 
    called with the grow() method:
    
        grow(time_act,time_step,W_max,growth_factor,root_growth,root_percent,
             shoot_percent,tbase,development,soil,atmosphere,h_plant,plant_N)
              
    Grow call several methods from plant and the growth functions from root
    and shoot. At the end of every time step Wttot and Rtot are updated.    
    """
    def __init__(self,soil,atmosphere,stage,root_fraction,shoot_fraction,leaf_fraction,stem_fraction,
                 storage_fraction,tbase=0.,Wmax=1000.,growth=0.05,
                 rootability_thresholds=[1.5,0.5,16000.,.0,0.0,0.0],pressure_threshold=[0.,1.,500.,16000.],
                 plant_N=[[160.,0.43],[1174.,0.16]],leaf_specific_weight=45.,root_growth=1.2,K_m=0.,c_min=0.):
        Plant.Count+=1
        self.biomass=Biomass(self,3.,.5)
        self.Wtot=1.
        self.Rtot=0.
        self.thermaltime=0.
        self.soil=soil
        self.atmosphere=atmosphere
        self.water=Water_MatrixPotentialApproach(self)
        self.ET=ET_FAO(self)
        self.plant_N=plant_N
        self.K_m=K_m
        self.c_min=c_min
        self.tbase=tbase
        self.Wmax=Wmax
        self.growth=growth
        self.stage=Stage(self,stage)
        self.root=Root(self,root_fraction,rootability_thresholds,root_growth,self.soil.get_profile())
        self.shoot=Shoot(self,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction,leaf_specific_weight)
        self.pressure_threshold=pressure_threshold
        self.Wact=0.
        self.Wpot=0.
        self.stress=1.
        self.R_a=0.
        self.R_p=0.
        self.s_p=[]
    @property
    def Isgerminated(self):
        return self.stage.is_growingseason(self.thermaltime)
    def __del__(self):
        Plant.Count-=1
    def step(self,step,interval):
        if step=='day':
            return 1.*interval
        elif step=='hour':
            return 1./24.*interval
    def __call__(self,time_act,step,interval):
        """
        call signature:
        
            __call__(time_act,time_step,W_max,growth_factor,root_growth,root_percent,
                 shoot_percent,tbase,development,soil,atmosphere,h_plant,plant_N)   
        
        The method calls the functions develop() from the stage class and hte grow()
        functions from root and shoot. To calclute the plant growth the functions
        assimilate(), uptake(), N_demand(), N_content, stress_response and respire()
        are used. At the end of every time_step the plant object variables Wtot and 
        Rtot are updated.
        
        Growth occurs if the thermaltime is between emergence and maturity. This 
        threshold are defined in the development parameter.
        
        The required paramter time_act and time_step are float values and define the
        the start and the duration of the growth process (both float values).
        W_max,growth_factor,root_growth,root_percent, shoot_percent and tbase are crop
        specific coeficiants (all float-values). Development, h_plant and plant_N are
        lists with crop specific parameters. Development is explained in the Stage class.
        h_plant is a list with four values with the criticall pressurehead for water
        uptake, e.g. [0.,100.,500.,16000.](float-values). plant_N is a list with four values with crop
        coefficiants for the phenological depending decline of the biomass nitrogen
        content, e.g. [100,0.43,1000,0.16].
        """ 
        time_step=self.step(step,interval)
        self.root.zone(self.root.depth)
        self.thermaltime += self.develop(self.atmosphere.get_tmin(time_act), self.atmosphere.get_tmax(time_act), self.tbase)
        if self.Wtot>=1.:
        #Compute ET
            self.ET(self.atmosphere.get_Rn(time_act,0.12,True),self.atmosphere.get_tmean(time_act)
                                   ,self.atmosphere.get_es(time_act),self.atmosphere.get_ea(time_act)
                                   ,self.atmosphere.get_windspeed(time_act),vegH=self.Wtot/900.+0.01
                                   ,LAI=self.shoot.leaf.LAI,stomatal_resistance=self.shoot.leaf.stomatal_resistance)
        
        #Compute water uptake
            self.water([self.ET.reference/self.root.depth * l.penetration for l in self.root.zone]
                         ,[self.soil.get_pressurehead(l.center) for l in self.root.zone],self.pressure_threshold)
        if self.stage.is_growingseason(self.thermaltime):
            ''' Potential growth  '''
            self.biomass(self.atmosphere.get_Rs(time_act),self.shoot.leaf.LAI)
            Wpot = self.assimilate(self.Wtot, self.Wmax, self.growth)
            
            
            
            ''' Nutrient uptake '''
            self.R_p=self.nitrogen_demand(Wpot, self.nitrogen_content(self.plant_N, self.thermaltime))
            nitrogen=[self.soil.get_nutrients(l.center) for l in self.root.zone]
            self.R_a=self.nutrientuptake(self.root.depth, 
                                         nitrogen, 
                                         self.water.Uptake, self.R_p, [l.penetration for l in self.root.zone], 
                                         self.c_min, self.K_m)
            self.stress=self.stress_response(sum(self.water.Uptake), self.ET.reference, self.R_a, self.R_p)*1.
            Wact=Wpot*self.stress
            self.Wtot = self.Wtot + Wact*time_step
            self.Rtot = self.respire(0.5,Wact,0.5,self.Wtot)               
            ''' root and shoot growth '''
            self.root(time_step,Wact,self.get_fgi(sum(self.water.Uptake), self.ET.reference, self.R_a, self.R_p, 
                                            [nitrogen[i] if l.penetration>0. else 0. for i,l in enumerate(self.root.zone)],
                                            [self.water.stress[i] if l.penetration>0. else 0. for i,l in enumerate(self.root.zone)]))
            self.shoot(time_step,Wact)
    def get_fgi(self,s_h,ETp,R_a,R_p,nitrogen_distribution,water_distribution):
        w=1-s_h/ETp
        n=1-(R_a/R_p) if R_p>0. else 0.
        if  w >= n:
            return [w/sum(water_distribution) for w in water_distribution]
        else:
            return [n/sum(nitrogen_distribution) for n in nitrogen_distribution]
    def nutrientuptake(self,rooting_depth,nutrient_conc,water_uptake,R_p,layer_penetration,c_min,K_m):
        P_a = [w*nutrient_conc[i] for i,w in enumerate(water_uptake)]
        A_p = max(R_p-sum(P_a),0.)
        a_p = A_p/rooting_depth
        michaelis_menten = [(n-c_min)/(K_m+n-c_min) for n in nutrient_conc]
        A_a = [a_p*michaelis_menten[i]*l for i,l in enumerate(layer_penetration)]
        return sum(P_a) + sum(A_a)     
    def develop(self,tmin,tmax,tbase):
        """
        call signature:
        
            thermaltime(tmin,tmax,tbase)
        
        Compute thermaltime and is called in the stage.development() method. 
        
        The parameter tmin, tmax, tbase and tmin are float-values. Tmin and tmax must
        be get from the atmosphere interface. Tbase is a crop specific paramter and
        set by plant.
            
        """
        if tmax < tbase or tmin < tbase:
            return 0
        else:
            return ((tmax+tmin)/2.0-tbase)
    def assimilate(self,Wtot,Wmax,growth_factor):
        """
        call signature:
            
            assimilate(Wtot,Wmax,growth_factor)
        
        assimilate() calculates the additional biomass for a given
        timestep.
        
        Wtot, Wmax and growth_factor are float values. Wtot is given by
        the plant class object variable Wtot. Wmax and growth_factor are
        crop specific parameters.        
        """
        return growth_factor*Wtot*(1.0-Wtot/Wmax)
    def respire(self,resp_growth,Wact,resp_maintenance,Wtot):
        """
        call signature:
            
            respire(a,Wact,b,Wtot)
        
        respire() calcultes growth and maintenance respiration.
        
        Wact,resp_growth,resp_maintenance and Wtot are float values. Wtot is given by
        the plant class object variable Wtot, Wact is the additional
        biomass from plant in every timestep. a and b are adjustment 
        parameter.
        """
        return resp_growth*Wact+resp_maintenance*Wtot
    def nitrogen_content(self,plant_N,thermal_time):
        """
        call signature:
        
            nitrogen_content(plant_N,thermal_time)
        
        nitrogen_content() calculates the actual nitrogen content
        of plant depending on specific crop coefficiants and 
        phenology. For values below plant_N[0] it is set equal
        to plant_N[1]. For values above plant_N[2] it set to 
        plant_N[3]. For values between this range a relative value
        to plant_N[0] and [2] is computed. thermal_time is definded by
        the stage class from plant. 
        
        plant_N is a list with four values with crop coefficiants 
        for the phenological depending decline of the biomass nitrogen
        content, e.g. [[160.,0.43],[1174.,0.16]]. 
        """
        if thermal_time<=plant_N[0][0]: return plant_N[0][1]
        elif thermal_time>=plant_N[1][0]: return plant_N[1][1]
        else: return plant_N[0][1]+(plant_N[1][1]-plant_N[0][1])/(plant_N[1][0]-plant_N[0][0])*(thermal_time-plant_N[0][0])
    def nitrogen_demand(self,Wpot,N_content):
        """
        call signature:
        
            nitrogen_demand(Wpot,N_content)
        
        nitrogen_demand() calculats the nutrient demand.
        
        Wpot and N_content are float values. Wpot must be taken 
        from plant, N_content is given by the corresponding function.
        """
        return Wpot*N_content
    def stress_response(self,S_h,T_p,R_a,R_p):
        """
        call signature:
        
            stress_response(T_p,S_h,R_p,R_a)
        
        stress_response calculates a stress factor which
        can limit the plant growth. The minimal value
        for stress is zero.
        
        T_p,S_h,R_p and R_a are float values. T_p is given by
        perspire(). S_h,R_p and R_a is given by uptake().
        """
        return min(S_h/T_p,R_a/R_p,1.)
    def passive_nutrientuptake(self,s_p,c_nutrient,c_max):
        """
        call signature:
        
            passive_nutrientuptake(s_p,c_nutrient,c_max)
        
        
        Calculates the passive uptake with water uptake. c_max is the 
        maximum allowed solution concetration that can be taken up by 
        plant roots during passive uptake.
        
    
        s_p = root water extraction rate, c_nutrient = nutrient concentration
        in soil layer and  c_max = maximal allowed nutrient concentration
        are flaot values. s_p can be calulated with water_extraction(), 
        c_nutrient must be get from the soil interface, c_max is a
        adjustment coefficiant, defined from the user.
        """
        return s_p*min(c_nutrient,c_max)
    def michaelis_menten(self,c_nutrient,K_m,c_min):
        """
        call signature:
        
            michaelis_menten(c_nutrient,K_m,c_min)
        
        Calculates the uptake kinetics with the michaelis menton function for
        active nutrient uptake. It returns the relationship bewteen 
        ion influx (uptake per unit root and unit time) and its concetration 
        at the root surface (c_nutrient).
    
        c_nutrient = soillayer nutrient concentration ,K_m = Mechaelis-Menten constant,
        and c_min = minimum concetration at which no net influx occurs are float
        values. nutrient_c is given from the soil interface, K_m and c_min are
        crop specific coefficiants.
        """
        return (c_nutrient-c_min)/(K_m+c_nutrient-c_min)
    def vernalisation(self,tmean,plant_vern):
        """call signature:
        
            vernalisation(self,tmean,plant_vernalisation)
        
        Calculates the relative vernalisation based on mean
        temperature and crop specific parameters.
        
        Tmean (float) is the mean temperature in time step.
        plant_vernalisation is a list with the vernalisation threesholds,
        e.g. [-1.,3.,20.]
        """
        if tmean<plant_vern[0] or tmean>plant_vern[2]: return 0.
        elif tmean>=plant_vern[0] and tmean<=plant_vern[1]: return 1.0
        else: return (plant_vern[-1]-tmean)/(plant_vern[-1]-plant_vern[-2])    
    def photoperiod(self,daylength,plant_photoperiod,plant_type):
        """call signature:
        
            photoperiod(daylength,plant_photoperiod,plant_type)
        
        Calculates the plant response to daylength.
        
        Daylenth must be tanken from the environment interface.
        plant_photoperiod is alist with critical values and plant_type
        is a string ('longday' or 'shortday').     
        """  
        if plant_type=='longday':
            if daylength<=plant_photoperiod[0] or daylength>=plant_photoperiod[-1]: 
                return 0.
            elif daylength>plant_photoperiod[1] and daylength<plant_photoperiod[2]: 
                return 1.0
            else: 
                return (plant_photoperiod[1]-daylength)/(plant_photoperiod[1]-plant_photoperiod[0])
        else:
            if daylength<=plant_photoperiod[0] or daylength>=plant_photoperiod[-1]: return 0.
            elif daylength>plant_photoperiod[0] and daylength<plant_photoperiod[1]: return 1.0
            else: return (plant_photoperiod[-1]-daylength)/(plant_photoperiod[-1]-plant_photoperiod[-2])

class Root:
    """
    call signature:
    
        Root(plant)
        
    Create root class instance. Root is part from the plant class 
    and is created automatically whenever implementing plant class.
    
    To start the growth process for a given timstep root must be 
    called with the grow() method, which is done by the plant class:
    
        grow(time_step,root_growth,Wp_actual,root_percent,BD_rootingdepth)
              
    The method calls the functions vertical_growth(), physical_constraints(),
    root_paritioning() and calculate the object variables depth and Wtot. 
    """
    def __init__(self,plant,root_fraction,rootability_thresholds,root_growth,soil_profile):
        self.plant=plant
        self.rootability_thresholds=rootability_thresholds
        self.root_growth=root_growth
        self.fraction=Fraction(root_fraction)
        self.depth=1.
        self.Wtot=0.
        self.zone=SoilLayer()
        self.zone.get_rootingzone(soil_profile)
        self.distribution=[0. for l in self.zone]
        self.fgi=[]
    @property
    def Fraction(self):
        return self.fraction(self.plant.thermaltime)
    def __call__(self,time_step,Wact,feeling_good_index):
        """
        call signature:
        
            __call__(time_step,root_growth,Wact,root_percent,bulkdensity,h,rootability_thresholds)
            
        The method calls the functions elongation(), physical_constraints(),
        root_paritioning() and calculate the object variables depth and Wtot. 
        
        Root_growth,Wact,root_percent, bulkdensity and h are float-values.        
        The parameter time_step  set the duration of the growth process.
        """
        self.fgi=feeling_good_index
        self.depth=self.depth+self.elongation(self.physical_constraints(self.plant.soil.get_bulkdensity(self.depth),self.plant.soil.get_pressurehead(self.depth),self.rootability_thresholds),self.root_growth)*self.plant.stress*time_step
        Wact_root=self.root_partitioning(self.fraction(self.plant.thermaltime), Wact)
        self.Wtot=self.Wtot+Wact_root*time_step
        self.distribution=self.allocate_biomass(self.distribution, Wact_root, feeling_good_index)
    def allocate_biomass(self,distribution,Wact_root,feeling_good_index):
        return [b+(Wact_root*feeling_good_index[i]) for i,b in enumerate(distribution)]
    def elongation(self,physical_constraints,root_growth):
        """
        call signature:
            
            elongation(physical_constraints,root_growth)
        
        The method calculates vertical growth.
        
        The parameter physical_constraints and root_growth are float values.
        Physical_constraints can be calculated with the corresponding function.
        Root growth is a crop specific parameter.            
        """
        return root_growth-physical_constraints*root_growth
    def physical_constraints(self,bulkdensity,h,rootability_thresholds):
        """
        call signature: 
        
            physical_constraints(bulkdensity,h,rootability_thresholds)
            
        Physical_constraints() calculates the soil resistance against root
        penetration and returns the most restricting parameter.
        
        Bulkdensity and h (pressurehead) must be tanken form the soil interface.
        rootability_thresholds is a list with six values, e.g.
        [meachanical_impendance threshold, physical_contrain through physical_constraint, 
        water_stress threshold, physical_contrain through water stress,
        oxygen_deficiency threshold, physical_contrain through oxygen_deficiency]
        """
        if bulkdensity>=rootability_thresholds[0]: mechanical_impendance=rootability_thresholds[1]
        else: mechanical_impendance=0.
        
        if h>=rootability_thresholds[2]:water_stress=rootability_thresholds[3]
        else: water_stress=0.
        
        if h<=rootability_thresholds[4]:oxygen_deficiency=rootability_thresholds[5]
        else: oxygen_deficiency=0.
        return max(mechanical_impendance,water_stress,oxygen_deficiency)
    def root_partitioning(self,Wact,root_percent):
        """
        call signature:
        
            grow(Wact,root_percent)
            
        Let the root object grow.
        
        The parameter Wact is actual growthrate from the plant class and
        root_percent a crop specific coefficiant. Both are double values.        
        """
        return root_percent*Wact
class Shoot:
    """
    call signature:
    
        Shoot(plant)
        
    Create shoot class instance. Shoot is part from the plant class 
    and is created automatically whenever implementing plant class.
    Further more call shoot implements leaf, stem and storage_organs
    classes.
    
    To start the growth process for a given timstep shoot must be 
    called with the grow() method, which is done by the plant class:
    
         __call__(time_step,Wact,shoot_percent)
        
    The method calls the function shoot_partitioning() and update
    the object variable Wtot.
    """
    def __init__(self,plant,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction,lai_conversion):
        self.plant=plant
        self.fraction=Fraction(shoot_fraction)
        self.Wtot=0.
        self.leaf=Leaf(self,leaf_fraction,lai_conversion)
        self.stem=Stem(self,stem_fraction)
        self.storage_organs=Storage_Organs(self,storage_fraction)
    @property
    def Fraction(self):
        return self.fraction(self.plant.thermaltime)
    def __call__(self,time_step,Wact):
        """
        call signature:
        
            grow(time_step,Wact,shoot_percent)
            
        Let the shoot object grow with the shoot_partitioning()
        function.
        
        The parameter Wact is actual growthrate from the plant class and
        shoot_percent a crop specific coefficiant. Both are double values.        
        The parameter time_step set the duration of the growth process.
        """
        Wact_shoot=self.shoot_partitioning(self.fraction(self.plant.thermaltime), Wact)
        self.Wtot=self.Wtot+Wact_shoot*time_step
        self.leaf(time_step,Wact_shoot)
        self.stem(time_step,Wact_shoot)
        self.storage_organs(time_step,Wact_shoot)
    def shoot_partitioning(self,shoot_fraction,Wact):
        """
        call signature:
        
            shoot_partitioning(self,shoot_fraction,Wact):
            
        Allocates biomass to shoot biomass.
        
        The parameter Wact is actual growthrate from the plant class and
        shoot_fraction a crop specific coefficiant. Both are double values.        
        """
        return shoot_fraction*Wact
    
class Stem:
    """
    call signature:
    
        Stem(shoot)
        
    Create stem class instance. Stem is part from the Shoot class 
    and is created automatically whenever implementing shoot class.
    
    To start the growth process for a given timstep Stem must be 
    called with the grow() method, which is done by the shoot class:
    
        grow(time_step,stem_ratio,Wact_shoot)
        
    The method calculates the stem class variable Wtot.
    """
    def __init__(self,shoot,stem_fraction):
        self.shoot=shoot
        self.fraction=Fraction(stem_fraction)
        self.Wtot=0.
    @property
    def Fraction(self):
        return self.fraction(self.shoot.plant.thermaltime)
    def  __call__(self,time_step,Wact_shoot):
        """
        call signature:
        
             __call__(time_step,stem_fraction,Wact_shoot)
            
        Let the stem object grow. For that, Wtot is updated
        in every step.
        
        The parameter time_step set the duration of the growth process.stem_fraction
        the fraction from shoot, which is allocated to stem
        """
        self.Wtot=self.Wtot+self.stem_partitioning(self.fraction(self.shoot.plant.thermaltime), Wact_shoot)*time_step
    def stem_partitioning(self,stem_ratio,Wact_shoot):
        """
        call signature:
        
            stem_partitioning(self,stem_fraction,Wact):
            
        Allocates biomass to stem biomass.
        
        The parameter Wact is actual growthrate from the shoot class and
        stem_fraction a crop specific coefficiant. Both are double values.        
        """
        return stem_ratio*Wact_shoot
    
class Storage_Organs:
    """
    call signature:
    
        Storage_organs(shoot)
        
    Create Storage_Organs class instance. Storage_Organs is part from 
    the Shoot class and is created automatically whenever implementing 
    shoot class.
    
    To start the growth process for a given timstep Storage_Organs must 
    be called with the growt() method, which is done by the shoot class:
    
         __call__(time_step,storage_organs_ratio,Wact_shoot)
        
    The method calculates the Storage_Organs class variable Wtot.
    """
    def __init__(self,shoot,storage_fraction):
        self.shoot=shoot
        self.fraction=Fraction(storage_fraction)
        self.Wtot=0.
    @property
    def Fraction(self):
        return self.fraction(self.shoot.plant.thermaltime)
    def  __call__(self,time_step,Wact_shoot):
        """
        call signature:
        
            grow(time_step,storage_organs_fraction,Wact_shoot)
            
        Let the storage_organs object grow. For that, Wtot is updated
        in every step. storage_organs_fraction is the part from shoot biomass,
        which is allocated to storage_organs.
        
        The parameter time_step set the duration of the growth process.
        """
        self.Wtot=self.Wtot+self.storage_organs_partitioning(self.fraction(self.shoot.plant.thermaltime),Wact_shoot)*time_step
    def storage_organs_partitioning(self,storage_organs_fraction,Wact_shoot):
        """
        call signature:
        
            storage_organs_partitioning(self,storage_organs_ratio,Wact_shoot):
            
        Allocates biomass to storage_organs biomass.
        
        The parameter Wact is actual growthrate from the plant class and
        storage_organs_fraction a crop specific coefficiant. Both are double values.        
        """
        return storage_organs_fraction*Wact_shoot
    
class Leaf:
    """
    call signature:
    
        Leaf(shoot)
        
    Create Leaf class instance. Leaf is part from the Shoot class and is
    created automatically whenever implementing shoot class.
    
    To start the growth process for a given timstep leaf must be 
    called with the grow() method, which is done by the shoot class:
    
         __call__(time_step)
        
    The method calculates the two leaf class variables leafarea and 
    Wtot.
    """
    def __init__(self,shoot,leaf_fraction,specific_weight):
        self.shoot=shoot
        self.fraction=Fraction(leaf_fraction)
        self.stomatal_resistance= 100 if self.shoot.plant.Isgerminated else 300
        self.Wtot=0.
        self.leafarea=1.
        self.adjusted_leafarea=1.
        self.specific_weight=specific_weight
    @property
    def LAI_adjusted(self):
        return self.adjusted_leafarea
    @property
    def LAI(self):
        return self.leafarea
    @property
    def Dryweight(self):
        return self.Wtot
    @property
    def Fraction(self):
        return self.fraction(self.shoot.plant.thermaltime)
    def  __call__(self,time_step,Wact_shoot):
        """
        call signature:
        
            grow(time_step,leaf_fraction,Wact_shoot)
            
        Let the leaf object grow. For that, two object variables are updated
        in every step: Wtot and leafarea. 
        
        The parameter time_step set the duration of the growth process.
        """
        Wact = self.leaf_partitioning(self.fraction(self.shoot.plant.thermaltime), Wact_shoot)
        self.Wtot = self.Wtot + Wact * time_step
        self.leafarea = self.leafarea + self.convert(Wact, self.specific_weight)* time_step
    def leaf_partitioning(self,leaf_fraction,Wact_shoot):
        """
        call signature:
        
            leaf_partitioning(self,leaf_fraction,Wact_shoot):
            
        Allocates biomass to leaf biomass.
        
        The parameter Wact is actual growthrate from the plant class and
        leaf_fraction a crop specific coefficiant. Both are double values.        
        """
        return leaf_fraction*Wact_shoot
    def convert(self,biomass,specific_weight):
        """ Calculates LAI [ha/ha]:
        
        The growth of leaf area is related to growth in leaf weight.
        The specific leaf weight of new leaves change with crop age.
        Leaf area is determined by dividing the weight of
        live leaves by the specific leaf weight
        
        biomass - biomass of the leafs[kg/ha]
        specific_weight - dry weight of leaves (no reserves,
        only structural dry matter) with a total one-sided 
        leaf area of one hectare [kg/ha]
        """
        return biomass/specific_weight
    def adjust_specific_weight(self,thermaltime,thermaltime_anthesis,fixed_specific_weight):
        """
        The specific leaf weight of new leaves is calculated by
        multiplying the specific leaf weight constant with a factor that depends on the
        development stage of the crop.
        """
        return min((thermaltime/thermaltime_anthesis+0.5)*fixed_specific_weight,1)
class Stage():
    Count = 0
    def __init__(self,plant,stage):
        self.plant=plant
        self.stages=[]
        Stage.Count+=1
        for s in stage:
            self.__setitem__(s)
    def __setitem__(self,stage):
        self.stages.append(stage)
    def __getitem__(self,index):
        return self.stages[index]
    def __iter__(self):
        for s in self.stages:
            yield s
    def __call__(self,thermaltime):
        if thermaltime>self.stages[-1][1]: return 'Development finished'
        else:
            for stage in self.stages:
                if thermaltime<=stage[1]:
                    return stage[0]
                    break
    def __del__(self):
        Stage.Count-=1
    def is_growingseason(self,thermaltime):
        if thermaltime>=self.stages[0][1] and thermaltime< self.stages[-1][1]:
            return True
        else:
            return False
     
class Fraction:
    Count = 0
    """ call siganture:
    
        Fraction(events)
        
    Fraction is a lists with events for partitioning. Each event
    must be definded with a thermaltime threshold as first
    arguement and a fractioning valu as second arguement.
    """
    def __init__(self,events):
        self.events=[]
        for e in events:
            self.__setitem__(e[0],e[1])
        Fraction.Count+=1
    def __setitem__(self,time,value):
        self.events.append(Event(time,value))
    def __getitem__(self,index):
        return self.events[index]
    def __iter__(self):
        for event in self.events:
            yield event
    def __del__(self):
        Fraction.Count-=1
    def __call__(self,thermaltime):
        """call signature:
        
            __call__(thermaltime)
            
        Returns the event, whoch is related to the given
        thermaltime.
        """
        if thermaltime>=self.events[-1].time: 
                return self.events[-1].value
        else:
            for e in self.events:
                if thermaltime<=e.time:
                    return e.value
                    break 

class Event:
    def __init__(self,time=.0,value=0.):
        self.time=time
        self.value=value
    def __call__(self,time,value):
        self.time=time
        self.value=value

class SoilLayer:
    def __init__(self,lowerlimit=0.,upperlimit=0.,center=0.,thickness=0.,penetration=0.):
        self.lowerlimit=lowerlimit
        self.upperlimit=upperlimit
        self.center=center
        self.thickness=thickness
        self.penetration=penetration
        self.rootingzone=[]
    def __getitem__(self,index):
        return self.rootingzone[index]
    def __iter__(self):
        for horizon in self.rootingzone:
            yield horizon
    def get_rootingzone(self,soil_profile):
        for i,layer in enumerate(soil_profile):
            self.rootingzone.append(SoilLayer())
            self.rootingzone[i].lowerlimit=layer
            if i == 0: 
                self.rootingzone[i].upperlimit = 0.
            else: 
                self.rootingzone[i].upperlimit = (soil_profile[i-1])
            self.rootingzone[i].center = (self.rootingzone[i].lowerlimit + self.rootingzone[i].upperlimit) / 2.
            self.rootingzone[i].depth = self.rootingzone[i].lowerlimit - self.rootingzone[i].upperlimit 
    def __call__(self,rooting_depth):
        for layer in self.rootingzone:
            if layer.lowerlimit <= rooting_depth:
                layer.penetration = layer.depth
            elif layer.upperlimit>rooting_depth:
                layer_penetration = 0.
            else: 
                layer.penetration = rooting_depth - layer.upperlimit

class ET_FAO:
    def __init__(self,plant):
        self.plant=plant
        self.ETo=0.
        self.ETc=0.
        self.ETc_adj=0.
    @property
    def reference(self):
        return self.ETo
    @property
    def cropspecific(self):
        return self.ETc
    @property
    def adjusted(self):
        return self.ETc_adjusted
    def __call__(self,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance):
        self.ETo = self.reference_ET(Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0)
    def reference_ET(self,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0,daily=True):
        """Calculates the potential ET using the famous Penmonteith (FAO 1994) eq.
        daily = if True, the daily average will be calculated, else the hourly
        Rn = Net radiation in MJ/m2
        T = Avg. Temp. for the timespan
        e_s,e_a Sat. vap. press, act. vap. press, Pa
        windspeed = in m/s
        alt = Altitude in m o.s.l.
        vegH = Height of the vegetation in m
        LAI = Leaf area index (both sides) in m2/m2
        stomatal_resistance = Resistance of open stomata against transpiration s/m
        print_steps = if true, some debiug info 
        """
        delta=4098*(0.6108*exp(17.27*T/(T+237.3)))/(T+237.3)**2
        if daily:   G=0
        else : G=(0.5-greater(Rn,0)*0.4)*Rn
        P=101.3*((293-0.0065*alt)/293)**5.253
        c_p=0.001013
        epsilon=0.622
        lat_heat=2.45
        gamma=c_p*P/(lat_heat*epsilon)
        R=0.287
        rho_a=P/(1.01*(T+273)*R)
        d=0.6666667*vegH
        z_om=0.123*vegH
        z_oh=0.1*z_om
        k=0.41
        r_a_u= log((2-d)/z_om)*log((2-d)/z_oh)/k**2
        r_a=r_a_u/windspeed
        r_s=100./(0.5*LAI)
        nominator=(delta+gamma*(1+r_s/r_a))
        ATcoeff=epsilon*3.486*86400/r_a_u/1.01
        #AeroTerm=(rho_a*c_p*(e_s-e_a)/r_a)/nominator
        AeroTerm=gamma/nominator*ATcoeff/(T+273)*windspeed*(e_s-e_a)
        RadTerm=(delta*(Rn-G))/(nominator*lat_heat)
        if printSteps:
           print "ET= %0.2f,AT= %0.2f,RT=   %0.2f" % (AeroTerm+RadTerm,AeroTerm,RadTerm)
           print "Rn= %0.2f,G=  %0.2f,Dlt=  %0.2f" % (Rn,G,delta)
           gamma_star=gamma*(1+r_s/r_a)
           print "gamma*=%0.2f,dl/(dl+gm*)=%0.2f,gm/(dl+gm*)=%0.2f" % (gamma_star,delta/(delta+gamma_star),gamma/(delta+gamma_star))
           print "r_a=%0.2f,r_s=%0.2f,gamma=%0.2f" % (r_a,r_s,gamma)
           print "rho_a=%0.2f,c_p=%0.2f" % (rho_a,c_p)
           print "P=  %0.2f,e_a=%0.2f,e_s=  %0.2f" % (P,e_a,e_s)
        return AeroTerm+RadTerm

class Water_MatrixPotentialApproach:
    def __init__(self,plant,max_compensation_capacity=2.):
        self.plant=plant
        self.max_compensation_capacity=max_compensation_capacity
        self.s_h=[]
        self.alpha=[]
        self.compensation=[]
        self.s_h_compensated=[]
    @property
    def Uptake(self):
        return self.s_h
    @property
    def Compensated_Uptake(self):
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

class Biomass:
    def __init__(self,plant,RUE,k):
        self.plant=plant
        self.RUE=RUE
        self.k=k
        self.total=0.
        self.growthrate=0.
    @property
    def CGR(self):
        return self.growthrate
    @property
    def Total(self):
        return self.total
    def __call__(self,Rs,LAI):
        self.growthrate = self.grow(self.PAR_a(Rs, self.intercept(LAI, self.k)), self.RUE)
        self.total += self.growthrate
    def PAR_a(self,Rs,interception):
        """ The PARa can be calculated from the fraction 
            of solar radiation at the top of the canopy, which 
            is transmitted to the ground (I/I0)/->interception
            
            RS - total solar radiation (MJ/m2 d)
            0.5- fraction of total solar energy, which is 
                 photosynthetically active
            interception - fraction of total solar radiation
                 flux, which is intercepted by the crop
            0.9-fraction of radiation absorbed by the crop 
                allowing for a 6 percent albedo and for inactive 
                radiation absorption
        """
        return Rs*0.5*0.9*(1-interception)
    def intercept(self,LAI,k):
        """ The relationship between I/I0 and LAI fits a
        negative exponential (similar to the Beer Lambert Law).
        
        LAI-Leaf area index (m2/m2)
        k - canopy extinction coefficien
        
        canopy extinction coefficient in wheat crops ranges
        from 0.3 to 0.7 and is highly dependent on leaf angle
        (low K for erect leaves). From equation 3, it can be calculated that
        95 percent PAR interception requires a LAI as high as 7.5 for erect 
        leaves but a LAI of only about 4.0 for more horizontal leaves
        """
        return exp(-k*LAI)
    def grow(self,PARa,RUE):
        """ total canopy net photosynthesis is linearly related to PARA and so is 
        crop growth rate (CGR, g/m2 d), which is the net accumulation of dry weight
        
        RUE - radiation use efficiency (g/m2 d)
        
        Measured values of RUE in a wheat crop are close to 3.0 
        g/MJ PARA when roots are included
        """
        return RUE * PARa
    def grain_yield(self,KNO,KW=0.041):#KW for wheat
        """ Return GY
        
        KNO is established in the period between 20 and 30 days 
        before flowering and ten days after anthesis.
        
        GY - grain yield (g/m2)
        KNO - the kernel number (m-2)
        KW - the kernel weight (g)
        """
        return KNO*KW
    def harvest(self,Biomass,HarvestIndex=1.):
        return GrainYield*HarvestIndex
    def kernel_number(self,spike_dryweight):
        """ Spike dry weight appears to be a major determinant of KNO
        """
        pass


''' Plant Interfaces:
        
        Plant requires two interfaces:
        
        1. Soil: Gives information about the soil conditions
                 and must have the folowing functions:
        
        class Soil:
            def get_pressurehead(self,depth):
                """ Depth in cm; Returns the capillary suction in cm for a given depth."""
            def get_wetness(self,depth):
                """ Depth in cm; Returns wetness for a given depth."""
            def get_porosity(self,depth):
                """ Depth in cm; Returns the porosity in m3/m3 of the soil in the given depth.
            def get_nutrients(self,depth):
               """ Depth in cm; Returns 0.5"""
            def get_bulkdensity(self,depth):
               """ Depth in cm; Returns 1.5"""
            def get_profile(self):
                """ Returns a list with the lower limits of the layers in the soilprofile in cm. """
            def layer(self,depth):
        
        1. Atmosphere: Gives information about the soil conditions
                       and must have the folowing functions:
        
        class Atmosphere:
            def get_tmin(self,time):
               """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in Celsius """
            def get_tmax(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in Celsius """
            def get_Rn(self,time,albedo,isdaily):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns radiation """
            def get_Rs(self,time,albedo,isdaily):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns radiation """
            def get_ea(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure"""
            def get_es(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure """
            def get_windspeed(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed """
            def get_tmean(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns tmean """
'''
        
        