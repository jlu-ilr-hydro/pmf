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
    def __init__(self,soil,atmosphere,stage,root_fraction,shoot_fraction,leaf_fraction,stem_fraction,
                 storage_fraction,tbase=0.,Wmax=1000.,growth=0.05,
                 rootability_thresholds=[1.5,0.5,16000.,.0,0.0,0.0],pressure_threshold=[0.,1.,500.,16000.],
                 plant_N=[[160.,0.43],[1174.,0.16]],lai_conversion=1.,root_growth=1.2,K_m=0.,c_min=0.):
        self.Wtot=1.
        self.Rtot=0.
        self.thermaltime=0.
        self.soil=soil
        self.atmosphere=atmosphere
        self.pressure_threshold=pressure_threshold
        self.plant_N=plant_N
        self.K_m=K_m
        self.c_min=c_min
        self.tbase=tbase
        self.Wmax=Wmax
        self.growth=growth
        self.stage=Stage(self,stage)
        self.root=Root(self,root_fraction,rootability_thresholds,root_growth)
        self.shoot=Shoot(self,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction,lai_conversion)
        self.rootingzone=RootingZone()
        self.rootingzone.get_rootingzone(self.soil.get_profile())
        self.pressure_head=[]
        self.s_h=[]
        self.alpha=[]
        self.Wact=0.
        self.Wpot=0.
        self.stress=1.
        self.ETp=0.
        self.penetration=[]
        self.R_a=0.
        self.R_p=0.
    def __del__(self):
        pass
    @property 
    def is_germinated(self):
        return self.stage.is_growingseason(self.thermaltime)
    @property 
    def water(self):
        return self.wateruptake(self.ETp, self.root.depth, self.alpha, [l.penetration for l in self.rootingzone])
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
        #Compute time_step     
        time_step=self.step(step,interval)
        
        self.thermaltime += self.develop(self.atmosphere.get_tmin(time_act), self.atmosphere.get_tmax(time_act), self.tbase)
        
        #Compute ETp
        ''' Transpiration '''
        # TODO: Value from literature
        
        # TODO: Change vegH and LAI calculation to something less mental
        if self.Wtot>=1.0:
            ETp=self.perspire(True,self.atmosphere.get_Rn(time_act,0.12,True),self.atmosphere.get_tmean(time_act),
                              self.atmosphere.get_es(time_act),self.atmosphere.get_ea(time_act),
                              self.atmosphere.get_windspeed(time_act),alt=0,vegH=self.Wtot/900.+0.01,
                              LAI=1+3*self.shoot.plant.Wtot/900.,stomatal_resistance=self.shoot.leaf.stomatal_resistance,printSteps=0)
        self.ETp=ETp
                
        ''' Water uptake '''
        self.rootingzone(self.root.depth)
        #if self.root.depth>0.:
        if self.stage(self.thermaltime) == self.stage[0][0]:
            pass
        else:
            pressure_head = [self.soil.get_pressurehead(layer.center) for layer in self.rootingzone]
            self.pressure_head=pressure_head
            alpha = [self.sink_term(p,self.pressure_threshold) for p in pressure_head]
            self.alpha=alpha
            layer_penetration=[p.penetration  for p in self.rootingzone]
            self.penetration=layer_penetration        
            self.s_h = self.wateruptake(self.ETp, self.root.depth, alpha, layer_penetration)
        if self.stage.is_growingseason(self.thermaltime):
            ''' Potential growth  '''
            Wpot = self.assimilate(self.Wtot, self.Wmax, self.growth)
            
            ''' Nutrient uptake '''
            self.R_p=self.nitrogen_demand(Wpot, self.nitrogen_content(self.plant_N, self.thermaltime))
            self.R_a=self.nutrientuptake(self.root.depth, 
                                         [self.soil.get_nutrients(l.center) for l in self.rootingzone], 
                                         self.s_h, self.R_p, [l.penetration for l in self.rootingzone], 
                                         self.c_min, self.K_m)
            self.stress=self.stress_response(sum(self.s_h), self.ETp, self.R_a, self.R_p)*1.
            Wact=Wpot*self.stress
            self.Wtot = self.Wtot + Wact*time_step
            self.Rtot = self.respire(0.5,Wact,0.5,self.Wtot)               
            ''' root and shoot growth '''
            self.root(time_step,Wact)
            self.shoot(time_step,Wact)
    def grow(self,Wpot,stress):
        return Wpot * stress
    def wateruptake(self,ETp,rooting_depth,alpha,layer_penetration):
        try:
            s_p = float(ETp)/float(rooting_depth)
        except ZeroDivisionError:
            s_p = 0.
        return [s_p * alpha[i] * p for i,p in enumerate(layer_penetration)]
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
    def perspire(self,daily,Rn,T,e_s,e_a,windspeed=2.,alt=0,vegH=0.12,LAI=24*0.12,stomatal_resistance=100,printSteps=0):
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
    def __init__(self,plant,root_fraction,rootability_thresholds,root_growth):
        self.plant=plant
        self.rootability_thresholds=rootability_thresholds
        self.root_growth=root_growth
        self.fraction=Fraction(root_fraction)
        self.depth=1.
        self.Wtot=0.
    def __call__(self,time_step,Wact):
        """
        call signature:
        
            __call__(time_step,root_growth,Wact,root_percent,bulkdensity,h,rootability_thresholds)
            
        The method calls the functions elongation(), physical_constraints(),
        root_paritioning() and calculate the object variables depth and Wtot. 
        
        Root_growth,Wact,root_percent, bulkdensity and h are float-values.        
        The parameter time_step  set the duration of the growth process.
        """
        self.depth=self.depth+self.elongation(self.physical_constraints(self.plant.soil.get_bulkdensity(self.depth),self.plant.soil.get_pressurehead(self.depth),self.rootability_thresholds),self.root_growth)*self.plant.stress*time_step
        self.Wtot=self.Wtot+self.root_partitioning(self.fraction(self.plant.thermaltime), Wact)*time_step
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
    def __init__(self,shoot,leaf_fraction,lai_conversion):
        self.shoot=shoot
        self.fraction=Fraction(leaf_fraction)
        self.lai_conversion=lai_conversion
        self.stomatal_resistance= 100 if self.shoot.plant.is_germinated else 300
        self.Wtot=0.
        self.lai=0.
    def  __call__(self,time_step,Wact_shoot):
        """
        call signature:
        
            grow(time_step,leaf_fraction,Wact_shoot)
            
        Let the leaf object grow. For that, two object variables are updated
        in every step: Wtot and leafarea. 
        
        The parameter time_step set the duration of the growth process.
        """
        self.Wtot=self.Wtot+self.leaf_partitioning(self.fraction(self.shoot.plant.thermaltime), Wact_shoot)*time_step
        self.lai+=self.lai_calc(self.Wtot, self.lai_conversion)
    def leaf_partitioning(self,leaf_fraction,Wact_shoot):
        """
        call signature:
        
            leaf_partitioning(self,leaf_fraction,Wact_shoot):
            
        Allocates biomass to leaf biomass.
        
        The parameter Wact is actual growthrate from the plant class and
        leaf_fraction a crop specific coefficiant. Both are double values.        
        """
        return leaf_fraction*Wact_shoot
    def lai_calc(self,Wtot,lai_conversion):
        """
        call signature:
        
            leaf_area(Wtot,lai_conversion):
            
        Calcualtes leaf area from the leaf weight.
        
        Wtot from leaf class and lai_conversion as crop specific paramater. Both float values.       
        """
        return Wtot*lai_conversion
    
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

class RootingZone:
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
            self.rootingzone.append(RootingZone())
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
            def get_ea(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure"""
            def get_es(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure """
            def get_windspeed(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed """
            def get_tmean(self,time):
                """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns tmean """
'''
        
        