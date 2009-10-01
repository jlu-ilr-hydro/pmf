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
    def __init__(self,soil,atmosphere,stage,shoot_percent,root_percent,
                leaf_percent,stem_percent,storage_percent,tbase=0.,
                 rootability_thresholds=[1.5,0.5,16000.,.0,0.0,0.0],pressure_threshold=[0.,1.,500.,16000.],
                 plant_N=[[160.,0.43],[1174.,0.16]],leaf_specific_weight=50.,root_growth=1.2,K_m=0.,c_min=0.):
        Plant.Count+=1
        self.soil=soil
        self.atmosphere=atmosphere
        self.water=Stress_Feddes(self)
        self.developmentstage=DevelopmentStage(self,stage)
        
        seasons = [self.developmentstage[0][1],
                   self.developmentstage[3][1]-self.developmentstage[0][1],
                   self.developmentstage[6][1]-self.developmentstage[3][1],
                   self.developmentstage[-1][1]-self.developmentstage[6][1]]
        Kcb_values = [0.15,1.1,0.15]
        self.ET=ET_FAO(self,Kcb_values,seasons)
        
        self.root=Root(self,root_percent,rootability_thresholds,root_growth,self.soil.get_profile())
        self.shoot=Shoot(self,shoot_percent,leaf_percent,stem_percent,storage_percent,leaf_specific_weight,self.developmentstage[4][1],shoot_percent,leaf_percent,stem_percent,storage_percent)
        self.biomass=Biomass_LUE(self,3.0,0.4)
        self.plant_N=plant_N
        self.K_m=K_m
        self.c_min=c_min
        self.tbase=tbase
        self.pressure_threshold=pressure_threshold
        self.R_a=0.
        self.R_p=0.
        self.s_p=[]
    def __del__(self):
        Plant.Count-=1
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
        time_step = 1. * interval if step == 'day' else 1./24. * interval
        self.root.zone(self.root.depth)
        self.developmentstage(time_step,self.atmosphere.get_tmin(time_act), self.atmosphere.get_tmax(time_act), self.tbase)
        
        #Evapotranspiration
        self.ET(self.soil.Kr_cmf(),self.developmentstage.Thermaltime,self.atmosphere.get_Rn(time_act,0.12,True),self.atmosphere.get_tmean(time_act)
                                   ,self.atmosphere.get_es(time_act),self.atmosphere.get_ea(time_act)
                                   ,self.atmosphere.get_windspeed(time_act),vegH=1.
                                   ,LAI=self.shoot.leaf.LAI,stomatal_resistance=self.shoot.leaf.stomatal_resistance,)
        if self.developmentstage.IsGerminated:
        #Water uptake
            transpiration_distribution = [self.ET.Reference/self.root.depth * l.penetration for l in self.root.zone]
            self.water(transpiration_distribution
                         ,[self.water.soil_values(self.soil,l.center) for l in self.root.zone],self.pressure_threshold)
        if self.developmentstage.IsGrowingseason:
            #Nutrient uptake
            self.R_p=self.nitrogen_demand(self.biomass.PotentialGrowth, self.nitrogen_content(self.plant_N, self.developmentstage.Thermaltime))
            nitrogen=[self.soil.get_nutrients(l.center) for l in self.root.zone]
            self.R_a=self.nutrientuptake(self.root.depth, 
                                         nitrogen, 
                                         self.water.Uptake, self.R_p, [l.penetration for l in self.root.zone], 
                                         self.c_min, self.K_m)            
            #Growth
            self.stress=self.stress_response(sum(self.water.Uptake), self.ET.Reference, self.R_a, self.R_p)*1.
            self.biomass(self.stress,time_step,self.biomass.atmosphere_values(self.atmosphere,time_act),self.shoot.leaf.LAI)
            #Partitioning            
            self.root(time_step,self.get_fgi(sum(self.water.Uptake), self.ET.Reference, self.R_a, self.R_p, 
                                            [nitrogen[i] if l.penetration>0. else 0. for i,l in enumerate(self.root.zone)],
                                            [self.water.Alpha[i] if l.penetration>0. else 0. for i,l in enumerate(self.root.zone)]),
                                            (self.root.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                                            self.soil.get_pressurehead(self.root.depth),self.stress)
            self.shoot(time_step,(self.shoot.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.leaf.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.stem.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.storage_organs.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       self.developmentstage.Thermaltime)
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
    def __init__(self,plant,root_percent,rootability_thresholds,root_growth,soil_profile):
        self.plant=plant
        self.rootability_thresholds=rootability_thresholds
        self.root_growth=root_growth
        self.depth=1.
        self.Wtot=0.
        self.zone=SoilLayer()
        self.zone.get_rootingzone(soil_profile)
        self.distribution=[0. for l in self.zone]
        self.fgi=[]
        self.percent=root_percent
    def __call__(self,time_step,feeling_good_index,root_biomass,pressure_head,stress):
        """
        call signature:
        
            __call__(time_step,root_growth,Wact,root_percent,bulkdensity,h,rootability_thresholds)
            
        The method calls the functions elongation(), physical_constraints(),
        root_paritioning() and calculate the object variables depth and Wtot. 
        
        Root_growth,Wact,root_percent, bulkdensity and h are float-values.        
        The parameter time_step  set the duration of the growth process.
        """
        self.fgi=feeling_good_index
        self.depth=self.depth+self.elongation(self.physical_constraints(self.plant.soil.get_bulkdensity(self.depth),pressure_head,self.rootability_thresholds),self.root_growth)*stress*time_step
        self.Wtot=self.Wtot+root_biomass*time_step
        self.distribution=self.allocate_biomass(self.distribution, root_biomass, feeling_good_index)
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
    def __init__(self,plant,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction,lai_conversion,thermaltime_anthesis,shoot_percent,leaf_percent,stem_percent,storage_percent):
        self.plant=plant
        self.Wtot=0.
        self.leaf=Leaf(self,leaf_percent,lai_conversion,thermaltime_anthesis)
        self.stem=Stem(self,stem_percent)
        self.storage_organs=Storage_Organs(self,storage_percent)
        self.percent=shoot_percent
    def __call__(self,time_step,shoot_biomass,leaf_biomass,stem_biomass,storage_biomass,thermaltime):
        """
        call signature:
        
            grow(time_step,Wact,shoot_percent)
            
        Let the shoot object grow with the shoot_partitioning()
        function.
        
        The parameter Wact is actual growthrate from the plant class and
        shoot_percent a crop specific coefficiant. Both are double values.        
        The parameter time_step set the duration of the growth process.
        """
        self.Wtot=self.Wtot+shoot_biomass*time_step
        self.leaf(time_step,leaf_biomass,thermaltime)
        self.stem(time_step,stem_biomass)
        self.storage_organs(time_step,storage_biomass)    
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
    def __init__(self,shoot,stem_percent):
        self.shoot=shoot
        self.Wtot=0.
        self.height=0.
        self.percent=stem_percent
    def  __call__(self,time_step,stem_biomass):
        """
        call signature:
        
             __call__(time_step,stem_fraction,Wact_shoot)
            
        Let the stem object grow. For that, Wtot is updated
        in every step.
        
        The parameter time_step set the duration of the growth process.stem_fraction
        the fraction from shoot, which is allocated to stem
        """
        self.height = self.calc_height()
        self.Wtot=self.Wtot+stem_biomass*time_step
    def calc_height(self):
        pass
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
    def __init__(self,shoot,storage_percent):
        self.shoot=shoot
        self.Wtot=0.
        self.percent=storage_percent
    def  __call__(self,time_step,storage_biomass):
        """
        call signature:
        
            grow(time_step,storage_organs_fraction,Wact_shoot)
            
        Let the storage_organs object grow. For that, Wtot is updated
        in every step. storage_organs_fraction is the part from shoot biomass,
        which is allocated to storage_organs.
        
        The parameter time_step set the duration of the growth process.
        """
        self.Wtot=self.Wtot+storage_biomass*time_step
    def grain_yield(self,KNO,KW=0.041):#KW for wheat
        """ Return GY
        
        KNO is established in the period between 20 and 30 days 
        before flowering and ten days after anthesis.
        
        GY - grain yield (g/m2)
        KNO - the kernel number (m-2)
        KW - the kernel weight (g)
        """
        return KNO*KW
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
    def __init__(self,shoot,leaf_percent,specific_weight,thermaltime_anthesis):
        self.shoot=shoot
        self.stomatal_resistance= 100 if self.shoot.plant.developmentstage.IsGerminated else 300
        self.Wtot=0.
        self.leafarea=0.1
        self.specific_weight=specific_weight
        self.thermaltime_anthesis = thermaltime_anthesis
        self.percent=leaf_percent
    @property
    def LAI(self):
        return self.leafarea
    def  __call__(self,time_step,leaf_biomass,thermaltime):
        """
        call signature:
        
            grow(time_step,leaf_fraction,Wact_shoot)
            
        Let the leaf object grow. For that, two object variables are updated
        in every step: Wtot and leafarea. 
        
        The parameter time_step set the duration of the growth process.
        """
        self.Wtot = self.Wtot + leaf_biomass * time_step
        self.leafarea += self.convert(leaf_biomass, self.adjust_specific_weight(thermaltime, self.thermaltime_anthesis)*self.specific_weight)
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
    def adjust_specific_weight(self,thermaltime,thermaltime_anthesis):
        """
        The specific leaf weight of new leaves is calculated by
        multiplying the specific leaf weight constant with a factor that depends on the
        development stage of the crop.
        """
        return min((thermaltime/thermaltime_anthesis+0.25),1.)
class DevelopmentStage():
    def __init__(self,plant,stage):
        self.plant=plant
        self.stages=[]
        self.thermaltime=0.
        for s in stage:
            self.__setitem__(s)
    @property
    def StageIndex(self):
        return self.stages.index(self.Stage)
    @property
    def IsGrowingseason(self):
        return True if self.thermaltime>=self.stages[0][1] and self.thermaltime< self.stages[-1][1] else False
    @property
    def IsGerminated(self):
        return True if self.thermaltime > self.stages[0][1] else False
    @property
    def Thermaltime(self):
        return self.thermaltime
    @property
    def Stage(self):
        return filter(lambda i:i[1]>=self.thermaltime, self.stages)[0] if self.thermaltime<=self.stages[-1][1] else 'Development finished'
    def __setitem__(self,stage):
        self.stages.append(stage)
    def __getitem__(self,index):
        return self.stages[index]
    def __iter__(self):
        for s in self.stages:
            yield s
    def __call__(self,time_step,tmin,tmax,tbase):
        self.thermaltime = self.thermaltime + self.develop(tmin, tmax, tbase) * time_step
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
    def __init__(self,plant,kcb_values,seasons):
        self.plant=plant
        self.kcb_values=kcb_values
        self.seasons=seasons
        self.eto=0.
        self.kcb=0.
        self.ke=0.
    @property
    def Transpiration(self):
        return self.eto * self.kcb
    @property
    def Evaporation(self):
        return self.eto * self.ke
    @property
    def Reference(self):
        return self.eto
    @property
    def Cropspecific(self):
        return self.eto * (self.kcb+self.ke)
    @property
    def Adjusted(self):
        return self.eto * (self.kcb*self.ks+self.ke)
    def __call__(self,Kr,thermaltime,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,RHmin=30.,h=1.):
        self.eto = self.reference_ET(Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0)

        self.kcb = self.calc_Kcb(thermaltime, self.kcb_values[0], self.kcb_values[1],
                                 self.kcb_values[2], self.seasons[0], self.seasons[1], 
                                 self.seasons[2], self.seasons[3])
        
        kcmax = self.calc_Kcmax(self.kcb, h, windspeed, RHmin)
        fc = self.calc_fc_dynamic(self.kcb, kcmax, h, self.kcb_values[0])
        few = self.calc_few(fc, 1.)
        self.ke = self.calc_Ke(Kr, kcmax, self.kcb, few)
        
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
    def calc_ETc(self,ETo,Kcb,Ke):
        """ Returns ETc in [mm] from basal crop coefficient (Kcb) and 
            and soil evaporation (Ke)
        """
        return ETo * (Kcb+Ke)
    def adjust_Kcb(self,Kcb_tab,windspeed,RHmin,h):
        """ - Kcb (Tab) the value for Kcb mid or Kcb end (if 0.45) taken from Table 17,
            - windspeed the mean value for daily wind speed at 2 m height over grass during the mid or late season growth stage [m s-1]
            - RHmin the mean value for daily minimum relative humidity during the mid- or late season growth stage
            - h the mean plant height during the mid or late season stage [m] (from Table 12)
        """
        return Kcb_tab + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3
    def calc_Kcb(self,day,Kcb_ini,Kcb_mid,Kcb_end,Lini,Ldev,Lmid,Llate):
        """ Constructed basal crop coefficient (Kcb) curve 
            using growth stage lengths.
            Lini - Length of initial season
            Ldev - Length of crop development season
            Lmid - Length of mid season
            Llate - Length of late season
            Kcb_ini - Kcb for initial season
            Kcb_mid - Kcb for mid season
            Kcb_end - Kcb for late season
            day - day
        """
        if day <=Lini: return Kcb_ini
        elif day <=Lini+Ldev: return Kcb_ini+(day-Lini)/Ldev*(Kcb_mid-Kcb_ini)
        elif day <=Lini+Ldev+Lmid: return Kcb_mid
        elif day <= Lini+Ldev+Lmid+Llate: return Kcb_mid+(day-(Lini+Ldev+Lmid))/Llate*(Kcb_end-Kcb_mid)
        else: return Kcb_end
    def calc_Ke(self,Kr,Kcmax,Kcb,few):
        """
        Ke - soil evaporation coefficient,
        Kcb - basal crop coefficient,
        Kcmax - maximum value of Kc following rain or irrigation,
        Kr - dimensionless evaporation reduction coefficient dependent
             on the cumulative depth of water depleted (evaporated) from the topsoil,
        few - fraction of the soil that is both exposed and wetted,
              i.e., the fraction of soil surface from which most evaporation occurs.
        """
        return min(Kr*(Kcmax - Kcb), few*Kcmax,)
    def calc_Kcmax(self,Kcb,h,windspeed,RHmin):
        """ 
        Kc max represents an upper limit on the evaporation
        and transpiration from any cropped surface and is imposed
        to reflect the natural constraints placed on available
        energy represented by the energy balance difference
        Rn - G - H(Equation 1). Kc max ranges from about 1.05
        to 1.30 when using the grass reference ETo.
        - RHmin the mean value for daily minimum relative humidity during the mid- or late season growth stage
        h - mean maximum plant height during the period of calculation
        (initial, development, mid-season, or late-season) [m],
    
        Kcb - basal crop coefficient
        """
        return max((1.2 + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3),Kcb+0.05)
    def calc_TEW(self,qFC,qWP,Ze):
        """
        TEW total evaporable water = maximum depth of water 
        that can be evaporated from the soil when the topsoil
        has been initially completely wetted [mm],
        qFC - soil water content at field capacity [m3 m-3],
        q WP - soil water content at wilting point [m3 m-3],
        Ze - depth of the surface soil layer that is subject to
             drying by way of evaporation [0.10-0.15m].
        """
        return 1000(qFC-0.5*qWP)*Ze
    def calc_Kr(self,De,TEW,REW):
        """
        Kr - dimensionless evaporation reduction coefficient dependent on the soil 
             water depletion (cumulative depth of evaporation) from the topsoil layer
        De - cumulative depth of evaporation (depletion) from the soil surface
                     layer at the end of day i-1 (the previous day) [mm],
        TEW - maximum cumulative depth of evaporation (depletion) from the soil 
              surface layer when Kr = 0 (TEW = total evaporable water) [mm],
        REW - cumulative depth of evaporation (depletion) at the end of stage 1 
              (REW = readily evaporable water) [mm]
        """
        if De > REW:
            return (TEW-De)/(TEW-REW)
        else:
            return 1.
    def calc_few(self,fc,fw=1.):#fw=1. - precipitation
        """
        1 - fc average exposed soil fraction not covered (or shaded) by vegetation [0.01 - 1],
        fw average fraction of soil surface wetted by irrigation or precipitation [0.01 - 1].
        """
        return min(1-fc,fw)
    def calc_fc_dynamic(self,Kcb,Kcmax,h,Kcmin=0.15):#Kcmin=0.15 - annual crops under nearly bare soil condition
        """ 
        !!! This equation should be used with caution and validated from field observations !!!
        fc - the effective fraction of soil surface covered by vegetation [0 - 0.99],
        Kcb - the value for the basal crop coefficient for the particular day or period,
        Kcmin - the minimum Kc for dry bare soil with no ground cover [0.15 - 0.20],
        Kcmax the maximum Kc immediately following wetting (Equation 72),
        h - mean plant height [m].
        """
        return ((Kcb-Kcmin)/(Kcmax-Kcmin))**(1+0.5*h) 
    def calc_fc_static(self,thermaltime,seasons):
        """
        The value for fc is limited to < 0.99. The user should assume appropriate values
        for the various growth stages. Typical values for fc :
        """
        if thermaltime <= seasons[0]: return 0.1 #0.0-0.1
        elif thermaltime <= seasons[0]+seasons[1]: return 0.8#0.1-0.8
        elif thermaltime <= seasons[0]+seasons[1]+seasons[2]:return 1.#0.8-1.
        else: return 0.8#0.2-0.8
class Stress_FAO:
    def __init__(self,average_available_soilwater=0.5):
        self.ks=0.
        self.p = average_available_soilwater
    @property
    def Stress(self):
        return self.ks 
    def __call__(self,ET,TAW,Dr):
        RAW = WAW * self.adjust_p(self.p, ET)
        self.ks = self.calc_Ks(TAW, Dr, RAW, self.p)
    def calc_Ks(self,TAW,Dr,RAW,p):
        """ Water content in me root zone can also be expressed by root zone depletion,
        Dr, i.e., water shortage relative to field capacity. At field capacity, the root 
        zone depletion is zero (Dr = 0). When soil water is extracted by evapotranspiration, 
        the depletion increases and stress will be induced when Dr becomes equal to RAW. After 
        the root zone depletion exceeds RAW (the water content drops below the threshold q t), 
        the root zone depletion is high enough to limit evapotranspiration to less than potential 
        values and the crop evapotranspiration begins to decrease in proportion to the amount of 
        water remaining in the root zone.
        
        Ks - dimensionless transpiration reduction factor dependent on available soil water [0 - 1],
        Dr - root zone depletion [mm],
        TAW- total available soil water in the root zone [mm],
        p  - fraction of TAW that a crop can extract from the root zone without suffering
             water stress [-].
        
        When the root zone depletion is smaller than RAW, Ks = 1
        For Dr > RAW, Ks:
        """
        return (TAW-Dr)/((1-p)*TAW) if Dr > RAW else 1.
    def adjust_p(self,p_table,ETc):
        """ The values for p apply for ETc 5 mm/day can be adjusted. 

        p - fraction and ETc as mm/day. 
        """
        return p_table + 0.04*(5-ETc)
class Stress_Feddes:
    def __init__(self,plant,max_compensation_capacity=2.):
        self.plant=plant
        self.max_compensation_capacity=max_compensation_capacity
        self.s_h=[]
        self.alpha=[]
        self.compensation=[]
        self.s_h_compensated=[]
    @property
    def Stress(self):
        pass
    @property
    def Uptake(self):
        return self.s_h
    @property
    def Compensated_Uptake(self):
        return self.compensation
    @property
    def Alpha(self):
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
    def soil_values(self,soil,depth):
        return soil.get_pressurehead(depth)
class Biomass_LOG:
    def __init__(self,plant,capacitylimit,growthfactor):
        self.plant=plant
        self.capacitylimit=capacitylimit
        self.growthfactor=growthfactor
        self.total=1.
        self.stress=0.
    @property
    def PotentialGrowth(self):
        return self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit)
    @property
    def ActualGrowth(self):
        return self.PotentialGrowth * self.stress
    @property
    def Total(self):
        return self.total
    def __call__(self,stress,time_step):
        self.stress=stress
        self.total = self.total + self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit) * stress * time_step
    def logarithmic_growth(self,total_biomass,growthfactor,capacitylimit):
        return total_biomass * growthfactor * (1- total_biomass / capacitylimit)
    def atmosphere_values(self,atmosphere,time_act):
        pass
    def senescence(self):
        pass
class Biomass_LUE:
    def __init__(self,plant,RUE,k):
        self.plant=plant
        self.rue=RUE
        self.k=k
        self.total=0.
        self.growthrate=0.
        self.stress=0.
    @property
    def PotentialGrowth(self):
        return self.growthrate
    @property
    def ActualGrowth(self):
        return self.growthrate * self.stress
    @property
    def Total(self):
        return self.total
    def __call__(self,time_act,stress,Rs,LAI):
        self.stress=stress
        self.growthrate = self.grow(self.PAR_a(Rs, self.intercept(LAI, self.k)), self.rue)
        self.total = self.total + self.growthrate *stress
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
    def harvest(self,Biomass_LUE,HarvestIndex=1.):
        return GrainYield*HarvestIndex
    def kernel_number(self,spike_dryweight):
        """ Spike dry weight appears to be a major determinant of KNO
        """
        pass
    def atmosphere_values(self,atmosphere,time_act):
        return atmosphere.get_Rs(time_act)


class SWC:
    """ SoilWaterContainer (SWC): 
        
        The root zone can be presented by means of a container in
        which the water content may fluctuate. To express the water
        content as root zone depletion is useful. It makes the adding
        and subtracting of losses and gains straightforward as the various
        parameters of the soil water budget are usually expressed in terms
        of water depth. Rainfall, irrigation and capillary rise of groundwater
        towards the root zone add water to the root zone and decrease the root
        zone depletion. Soil evaporation, crop transpiration and percolation
        losses remove water from the root zone and increase the depletion.
    """
    def __ini__(self,sand=.9,clay=.1,initial_Zr=0.1,average_available_soilwater=0.55,Ze=0.1):
        self.sand=sand
        self.clay=clay
        self.silt = max(1-(clay+sand),0.)
        self.soiltype = self.calc_soiltype(self.sand,self.clay,self.silt)
        self.fc=self.calc_soilproperties(self.sand, self.clay)[0]
        self.wp=self.calc_soilproperties(self.sand, self.clay)[1]
        self.dr = self.calc_InitialDepletion(self.fc, average_water_content, initial_Zr)
        self.Ze=Ze
        self.REW = self.calc_REW(soiltype=self.soiltype)
        self.kr=0.
        self.de = 0.
        self.taw = 0.
    @property
    def KR(self):
        return self.kr
    @property
    def taw(self):
        return self.taw
    def Dr(self):
        return self.dr
    def __call__(self,ET,rainfall,Zr,runoff=0.,irrigation=0.,capillarrise=0.):
        
        #Calculta dr and taw for water stress factor Ks
        DP = self.calc_DP(rainfall, runoff, irrigation, ET, self.dr)
        self.dr = self.calc_WaterBalance(self.dr, rainfall, runoff, irrigation, capillarrise, ET, DP)
        self.taw = self.calc_TAW(self.fc, self.wp, Zr)

        
        #Calculate Kr for the evapotranspiration
        TEW = self.calc_TEW(self.fc, self.wp, self.de)
        self.de = self.calc_EvaporationLayer(De, P, RO, I, fw, E, few, DPe, Tew)
        self.kr = self.calc_Kr(self.de, TEW, self.REW)
    def calc_EvaporationLayer(self,De,P,RO,I,fw,E,few,DPe,Tew=0.):
        """
        The estimation of Ke in the calculation procedure requires a 
        daily water balance computation for the surface soil layer for
        the calculation of the cumulative evaporation or depletion from 
        the wet condition. The daily soil water balance equation for the 
        exposed and wetted soil fraction few is:
        
        To initiate water balance for evaporating layer: 
            De = 0. for topsoil near field capacity
            De = TEW for evaporated water has been depleted at beginning
        
        Returns: cumulative depth of evaporation (depletion) following complete wetting 
                 at the end of day i [mm]
                 
        De - cumulative depth of evaporation following complete wetting from 
             the exposed and wetted fraction of the topsoil at the end of day i-1 [mm],
        Pi - precipitation on day i [mm],
        RO - precipitation run off from the soil surface on day i [mm],
        I  - irrigation depth on day i that infiltrates the soil [mm],
        E  - evaporation on day i (i.e., Ei = Ke ETo) [mm],
        T  - depth of transpiration from the exposed and wetted fraction 
             of the soil surface layer on day i [mm],
        DP - deep percolation loss from the topsoil layer on day i if 
             soil water content exceeds field capacity [mm],
        fw - fraction of 
             soil surface wetted by irrigation [0.01 - 1],
        few- exposed and wetted soil fraction [0.01 - 1]
        """
        return De-(P-RO)-(I/fw)+(E/few)+Tew+DPe
    def calc_TAW(self,FC,WP,Zr):
        """ the total available water in the root zone is the difference 
            between the water content at field capacity and wilting point.
            TAW is the amount of water that a crop can extract from its root zone,
            and its magnitude depends on the type of soil and the rooting depth
            
            TAW the total available soil water in the root zone [mm],
            FC - ater content at field capacity [m3 m-3],
            WP - water content at wilting point [m3 m-3],
            Zr - the rooting depth [m].
        """
        return 1000*(FC-WP)*Zr
    def calc_RAW(self,p,TAW):
        """ The fraction of TAW that a crop can extract from the root zone 
            without suffering water stress is the readily available soil water.
            
            RAW- the readily available soil water in the root zone [mm],
            p - average fraction of Total Available Soil Water (TAW) that can be depleted 
            from the root zone before moisture stress (reduction in ET) occurs [0-1].
            
            The factor p differs from one crop to another. The factor p normally varies 
            from 0.30 for shallow rooted plants at high rates of ETc (> 8 mm d-1) to 0.70
            for deep rooted plants at low rates of ETc (< 3 mm d-1). A value of 0.50 for 
            p is commonly used for many crops.
        """
        return p*TAW
    def calc_WaterBalance(self,Dr_previous_day,P,RO,I,CR,ETc,DP):
        """ Returns Dr - root zone depletion at the end of day i [mm]
            
            the root zone can be presented by means of a container in which the water 
            content may fluctuate. To express the water content as root zone depletion 
            is useful. It makes the adding and subtracting of losses and gains straightforward 
            as the various parameters of the soil water budget are usually expressed in terms of 
            water depth. Rainfall, irrigation and capillary rise of groundwater towards the root 
            zone add water to the root zone and decrease the root zone depletion. Soil evaporation, 
            crop transpiration and percolation losses remove water from the root zone and increase 
            the depletion.
            
            Dr_previous_day - water content in the root zone at the end of the previous day, i-1 [mm],
            P  - precipitation on day i [mm],
            RO - runoff from the soil surface on day i [mm],
            I  - net irrigation depth on day i that infiltrates the soil [mm],
            CR - capillary rise from the groundwater table on day i [mm],
            ETc- crop evapotranspiration on day i [mm],
            DP - water loss out of the root zone by deep percolation on day i [mm]
            
            By assuming that the root zone is at field capacity following heavy rain or 
            irrigation, the minimum value for the depletion Dr is zero. At that moment no water is 
            left for evapotranspiration in the root zone, Ks becomes zero, and the root zone 
            depletion has reached its maximum value TAW.
            
            TAW > Dr >= 0
            
            The daily water balance, expressed in terms of depletion at the end of 
            the day is
        """
        return Dr_previous_day - (P-RO) - I - CR + ETc + DP
    def calc_InitialDepletion(self,FC,q,Zr):
        """ To initiate the water balance for the root zone, the initial depletion Dr, i-1 should 
        be estimated. 
        
        where q i-1 is the average soil water content for the effective root zone. Following heavy 
        rain or irrigation, the user can assume that the root zone is near field capacity, 
        i.e., Dr, i-1  0
        
        The initial depletion can be derived from measured soil water content by:
        """
        return 1000*(FC-q)*Zr
    def calc_DP(self,P,RO,I,ETc,Dr_previous_day):
        """ Returns DP
            Following heavy rain or irrigation, the soil water content in the root zone might 
            exceed field capacity. In this simple procedure it is assumed that the soil water content 
            is at q FC within the same day of the wetting event, so that the depletion Dr 
            becomes zero. Therefore, following heavy rain or irrigation.
            
            
            The DP calculated for calc_WaterBalance() is independent of the DP calculted in
            calc_De().As long as the soil water content in the root zone is below field 
            capacity (i.e., Dr, i > 0), the soil will not drain and DPi = 0.
        """
        return max(P - RO + I - ETc - Dr_previous_day,0)
    def calc_soilproperties(self,sand,clay):
        """ Returns volumetric water content theta for fieldcapacity
            and wiltingpoint for  a given fraction of sand and
            clay.
            
            theta_fc     - water content FC [m3/m3]
            theta_wp     - water content WP [m3/m3]
            sand_fraction - sand fraction [fraction]
            clay_fraction - clay fraction [fraction]
            
            
            
        Soil type                    Theta [m3/m3]
                            FC            WP            FC - WP
            sand            0.07 - 0.17 0.02 - 0.07 0.05 - 0.11 
            
        """
        return [0.17,0.07]
    def calc_Kr(self,De,TEW,REW):
        """
        Kr - dimensionless evaporation reduction coefficient dependent on the soil 
             water depletion (cumulative depth of evaporation) from the topsoil layer
        De - cumulative depth of evaporation (depletion) from the soil surface
                     layer at the end of day i-1 (the previous day) [mm],
        TEW - maximum cumulative depth of evaporation (depletion) from the soil 
              surface layer when Kr = 0 (TEW = total evaporable water) [mm],
        REW - cumulative depth of evaporation (depletion) at the end of stage 1 
              (REW = readily evaporable water) [mm]
        """
        if De > REW:
            return (TEW-De)/(TEW-REW)
        else:
            return 1.
    def calc_TEW(self,qFC,qWP,Ze):
            """
            TEW total evaporable water = maximum depth of water 
            that can be evaporated from the soil when the topsoil
            has been initially completely wetted [mm],
            qFC - soil water content at field capacity [m3 m-3],
            q WP - soil water content at wilting point [m3 m-3],
            Ze - depth of the surface soil layer that is subject to
                 drying by way of evaporation [0.10-0.15m].
            """
            return 1000(qFC-0.5*qWP)*Ze   
    def calc_REW(self,soiltype='Sand'):
        """ Return REW cumulative depth of evaporation (depletion) 
            at the end of stage 1 (REW = readily evaporable water) [mm].
        
            The cumulative depth of evaporation, De, at the end of stage 1 
            drying is REW (Readily evaporable water, which is the maximum 
            depth of water that can be evaporated from the topsoil layer 
            without restriction during stage 1). The depth normally ranges
            from 5 to 12 mm and is generally highest for medium and fine 
            textured soils.
        
        """
        return 7. #sand 2-7 mm
    def soiltype(self,sand,clay,silt):
        return 'Sand'



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
        
        