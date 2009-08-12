from pylab import *
class Plant:
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
    def __init__(self):
        self.Wtot=1.
        self.Rtot=0.
        self.soil_profile=[]
        self.stage=Stage(self)
        self.root=Root(self)
        self.shoot=Shoot(self)
    def grow(self,time_act,time_step,W_max,growth_factor,root_growth,root_percent,shoot_percent,tbase,development,soil,atmosphere,h_plant,plant_N):
        """
        call signature:
        
            grow(time_act,time_step,W_max,growth_factor,root_growth,root_percent,
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
        self.stage.develop(time_step,atmosphere.get_tmin(time_act),atmosphere.get_tmax(time_act),tbase,development)
        if self.stage.thermal_time>=development[0][0] and self.stage.thermal_time<=development[0][-1]:#restrict growth due to the development 
            Wpot=self.assimilate(self.Wtot, W_max, growth_factor)
            self.uptake(self.root.depth,atmosphere.get_etp(time_act),self.nitrogen_demand(Wpot, self.nitrogen_content(plant_N, self.stage.thermal_time)),h_plant,10.,soil)
            Wact=Wpot-Wpot*0.
            self.Rtot=self.respire(0.5,Wact,0.5,self.Wtot)
            self.root.grow(time_step,root_growth,Wact,root_percent,soil.get_bulkdensity(self.root.depth))
            self.shoot.grow(time_step, Wact, shoot_percent)
            self.Wtot=self.Wtot+Wact*time_step
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
    def respire(self,a,Wact,b,Wtot):
        """
        call signature:
            
            respire(a,Wact,b,Wtot)
        
        respire() calcultes growth and maintenance respiration.
        
        Wact,a,b and Wtot are float values. Wtot is given by
        the plant class object variable Wtot, Wact is the additional
        biomass from plant in every timestep. a and b are adjustment 
        parameter.
        """
        return a*Wact+b*Wtot
    def perspire(self,T_p):
        """
        call signature:
        
            perspire(T_p)
        
        perspire() set the potential transiration.
        
        T_p is a float value and taken from the atmosphere interface.
        """
        return T_p
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
        content, e.g. [100,0.43,1000,0.16]. 
        """
        if thermal_time<=plant_N[0][0]: return plant_N[0][1]
        elif thermal_time>=plant_N[1][0]: return plant_N[1][1]
        else: return plant_N[0][1]+(plant_N[1][1]-plant_N[0][1])/(plant_N[1][0]-plant_N[0][0])*(thermal_time-plant_N[0][0])
    def nitrogen_demand(self,Wp_potential,N_content):
        """
        call signature:
        
            nitrogen_demand(Wpot,N_content)
        
        nitrogen_demand() calculats the nutrient demand.
        
        Wpot and N_content are float values. Wpot must be taken 
        from plant, N_content is given by the corresponding function.
        """
        return Wpot*N_content
    def stress_response(self,T_p,S_h,R_p,R_a):
        """
        call signature:
        
            stress_response(T_p,S_h,R_p,R_a)
        
        stress_response calculates a stress factor which
        can limit the plant growth. The minimal value
        for stress is zero.
        
        T_p,S_h,R_p and R_a are float values. T_p is given by
        perspire(). S_h,R_p and R_a is given by uptake().
        """
        return max((1-S_h/S_p),(1-R_a/R_p),0.)
    def uptake(self,Z_r,T_p,R_p,h_plant,depth_step,soil,K_m=0.,c_max=0.01,c_min=0.):
        """
        call siganture:
        
            uptake(self,Z_r,T_p,R_p,h_plant,depth_step,soil,K_m=0.,c_max=0.01,c_min=0.)
            
        uptake() calculates the water and nutrient uptake for defined
        depth steps from the soil interface.
    
        Z_r = Total rootingdepth, T_p = Potential transpiration,
        R_p = Potential root nutrient uptake, h_plant = critical pressurehead of
        plant for soil water extraction, depth_step = layer thickness for pressure-
        head and nutrient_c request, soil = Soil-Instance, c_max = maximal allowed 
        nutrient concentration,Mechaelis-Menten constant, c_min = minimum concetration 
        at which no net influx occurs (all float values).
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
    def water_extractionrate(self,T_p,Z_r): 
        """
        call siganture:
        
            water_extractionrate(T_p,Z_r)
            
        water_extraction() allocates the potential water uptake
        over the rooting depth.
        
        Z_r = Total rootingdepth and T_p = Potential transpiration
        are float values. Z_r equals the obkect variable
        plant.root.depth and T_p can be achieved with perspire().         
        """
        return T_p/Z_r
    def sink_therm(self,h_soil,h_plant): 
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
    def michaelis_menten(self,nutrient_c,K_m,c_min):
        """
        call signature:
        
            michaelis_menten(nutrient_c,K_m,c_min)
        
        Calculates the uptake kinetics with the michaelis menton function for
        active nutrient uptake. It returns the relationship bewteen 
        ion influx (uptake per unit root and unit time) and its concetration 
        at the root surface (nurient_c).
    
        nutrient_c = soillayer nutrient concentration ,K_m = Mechaelis-Menten constant,
        and c_min = minimum concetration at which no net influx occurs are float
        values. nutrient_c is given from the soil interface, K_m and c_min are
        crop specific coefficiants.
        """
        return (nutrient_c-c_min)/(K_m+nutrient_c-c_min)
 
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
    def __init__(self,plant):
        self.plant=plant
        self.depth=0.
        self.Wtot=0.
    def grow(self,time_step,root_growth,Wact,root_percent,BD_rootingdepth):
        """
        call signature:
        
            grow(time_step,root_growth,Wact,root_percent,BD_rootingdepth)
            
        The method calls the functions vertical_growth(), physical_constraints(),
        root_paritioning() and calculate the object variables depth and Wtot. 
        
        Root_growth,Wact,root_percent and BD_rootingdept are float-values.        
        The parameter time_step  set the duration of the growth process.
        """
        self.depth=self.depth+self.vertical_growth(self.physical_constraints(BD_rootingdepth), root_growth)*time_step
        self.Wtot=self.Wtot+self.root_partitioning(root_percent, Wact)*time_step
    def vertical_growth(self,physical_constraints,root_growth):
        """
        call signature:
            
            vertical_growth(physical_constraints,root_growth)
        
        The method calculates vertical growth.
        
        The parameter physical_constraints and root_growth are float values.
        Physical_constraints can be calculated with the corresponding function.
        Root growth is a crop specific parameter.            
        """
        return root_growth-physical_constraints*root_growth
    def physical_constraints(self,BD_rootingdepth,water_stress=0.,oxygen_deficiency=0.):
        """
        call signature: 
        
            physical_constraints(BD_rootingdepth,water_stress,oxygen_deficiency)
            
        Physical_constraints() calculates the soil resistance against root
        penetration and returns the most restricting parameter.
        
        BD_rootingdepth,water_stress and oxygen_deficiency are float values.
        BD_rootingdepth must be get from the soil interface. Water_stress and
        oxygen_deficiency are zero by default.
        """
        if BD_rootingdepth > 1.5: mechanical_impendance=0.5
        else: mechanical_impendance=0.
        water_stress=water_stress
        oxygen_deficiency=oxygen_deficiency
        return max(mechanical_impendance,water_stress,oxygen_deficiency)
    def root_partitioning(self,Wact,root_percent):
        """
        call signature:
        
            grow(Wact,root_percent)
            
        Let the root object grow.
        
        The parameter Wact is actual growthrate from the plant class and
        root_percent a crop specific coefficiant. Both are double values.        
        """
        return root_percent*plant_growthrate
    
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
    
        grow(time_step,Wact,shoot_percent)
        
    The method calls the function shoot_partitioning() and update
    the object variable Wtot.
    """
    def __init__(self,plant):
        self.plant=plant
        self.Wtot=0.
        self.leaf=Leaf(shoot)
        self.stem=Stem(shoot)
        self.storage_organs=Storage_Organs(shoot)
    def grow(self,time_step,Wact,shoot_percent):
        """
        call signature:
        
            grow(time_step,Wact,shoot_percent)
            
        Let the shoot object grow with the shoot_partitioning()
        function.
        
        The parameter Wact is actual growthrate from the plant class and
        shoot_percent a crop specific coefficiant. Both are double values.        
        The parameter time_step set the duration of the growth process.
        """
        self.Wtot=self.Wtot+self.shoot_partitioning(shoot_percent, Wact)*time_step
    def shoot_partitioning(self,shoot_percent,Wact):
        """
        call signature:
        
            grow(Wact,shoot_percent)
            
        Let the shoot object grow.
        
        The parameter Wact is actual growthrate from the plant class and
        shoot_percent a crop specific coefficiant. Both are double values.        
        """
        return shoot_percent*Wact

class Stem:
    """
    call signature:
    
        Stem(shoot)
        
    Create stem class instance. Stem is part from the Shoot class 
    and is created automatically whenever implementing shoot class.
    
    To start the growth process for a given timstep Stem must be 
    called with the grow() method, which is done by the shoot class:
    
        grow(time_step)
        
    The method calculates the Storage_Organs class variable Wtot.
    """
    def __init__(self,shoot):
        self.shoot=shoot
        self.Wtot=0.
    def grow(self):
        """
        call signature:
        
            grow(time_step)
            
        Let the stem object grow. For that, Wtot is updated
        in every step.
        
        The parameter time_step set the duration of the growth process.
        """
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
    
        grow(time_step)
        
    The method calculates the Storage_Organs class variable Wtot.
    """
    def __init__(self,shoot):
        self.shoot=shoot
        self.Wtot=0.
    def grow(self):
        """
        call signature:
        
            grow(time_step)
            
        Let the storage_organs object grow. For that, Wtot is updated
        in every step.
        
        The parameter time_step set the duration of the growth process.
        """
        pass
    
class Leaf:
    """
    call signature:
    
        Leaf(shoot)
        
    Create Leaf class instance. Leaf is part from the Shoot class and is
    created automatically whenever implementing shoot class.
    
    To start the growth process for a given timstep leaf must be 
    called with the grow() method, which is done by the shoot class:
    
        grow(time_step)
        
    The method calculates the two leaf class variables leafarea and 
    Wtot.
    """
    def __init__(self,shoot):
        self.shoot=shoot
        self.tot=0.
        self.leafarea=0.
    def grow(self,time_step):
        """
        call signature:
        
            grow(time_step)
            
        Let the leaf object grow. For that, two object variables are updated
        in every step: Wtot and leafarea. 
        
        The parameter time_step set the duration of the growth process.
        """
        pass
    
    
class Stage:
    """
    call signature:
        
        Stage(plant,thermaltime=0.,stage=0)
        
    Create stage class instance. Stage is part from the plant class and is 
    created automatically whenever implementing plant. The optional keyword 
    arguments set object variables thermal_time and stage.
    
    To start the development process for a given timestep stage must be called 
    with the develop() method, whoch is done by the plant class:
    
        develop(time_step,tmin,tmax,tbase,development)
        
    The method calculates the both stage object variables thermal_time and
    stage.
    """
     
    def __init__(self,plant,thermaltime=0.,stage=0):
        self.plant=plant
        self.thermal_time=thermaltime
        self.stage=stage
    def develop(self,time_step,tmin,tmax,tbase,development):
        """
        call signature:
        
            develop(time_step,tmin,tmax,tbase,development)
        
        Compute and set the object variables thermal_time and stage for a given timestep.
        For that the class methods thermaltime() and get_stage() are used.
        
        Tmin, tmax, tbase and tmin are float-values to compute thermaltime. Development
        must be a two dimensional list with first accumulated thermaltime values (float)
        and second the names (string) of the development stage, 
        e.g.: [[100,200,300],['Emergence','Anthesis','Maturity']]. The parameter time_step 
        set the duration of the growth process.
        """
        self.thermal_time=self.thermal_time+self.thermaltime(tmin, tmax, tbase)*time_step
        self.stage=self.get_stage(self.thermal_time,development)
    def thermaltime(self,tmin,tmax,tbase):
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
    def get_stage(self,thermaltime,development):
        """
        call signature:
        
            get_stage(thermaltime,development)
            
        Compute development stage and is called in the stage.development() method. 
        
        
        The parameter thermaltime must be a float-value.Development must be a two dimensional 
        list with first accumulated thermaltime values (float) and second the names (string) 
        of the development stage, e.g.: [[100,200,300],['Emergence','Anthesis','Maturity']]
        """
        for stage in development[0]:
            if thermaltime<=stage:
                return development[1][development[0].index(stage)]
                break
    

