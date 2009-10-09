class Plant:
    """
    Main class with holds plant organs and control growth processes
    
    Plant is the main class from FlowerPower. It holds all
    plant structural classes (root, shoot, stem, leaf and
    storageorgans). Plant is linked to several interfaces.
    These interfaces represent the natural environment and
    the growth related processes.
    
    Implementation
    ==============
    Plant returns a virtual plant. Plant consists of root and
    shoot class. The shoot class consitsts of leaf, stem, and 
    storageoragans. All classs are implemented during the
    initialisation. To initiate plant several interfaces must
    be implemented.
      - Environmental interfaces:
        - Soil
        - Atmosphere
      - Growth process related interfaces:
        - Biomass
        - DevelopmentStage
        - Water
        - ET
        - Nitrogen
        - Layer
    
    The interfaces can be taken from the process library or can be
    implemented from the user. The user should notice the  
    required predifined functions of the interfaces.
    
    The default values respect crop specific parameters which refer 
    to summer wheat.

    Call signature
    ==============
    To start the growth process plant must be called with the
    actual time, time step and time intervall. Plant calls
    the root and shoot object. Plant calls the growth processes
    (water,biomass,developmentstage, et and nitrogen) and interfere
    between environmental and growth process related interfaces.
    """
    
    #Class variable which counts plant instances
    Count=0.
    
    def __init__(self,soil,atmosphere,et,water,biomass,developmentstage,layer,nitrogen,
                 shoot_percent,root_percent,leaf_percent,stem_percent,
                 storage_percent,tbase=0.,
                 rootability=[1.5,0.5,16000.,.0,0.0,0.0],
                 pressure_threshold=[0.,1.,500.,16000.],
                 plantN=[[160.,0.43],[1174.,0.16]],
                 leaf_specific_weight=50.,root_growth=1.2):        
        """
        Returns plant instance. The plant instance holds the other plant structural classes root and 
        shoot (shoot holds leaf, stem and storageaorgans). Plant interfere between the environmental 
        and growth process related interfaces.
    
        @type  soil: soil
        @param soil: Interface to the soil environment.
        @type layer: layer
        @param layer: Interface for the calculation of the rooting zone.
        @type  atmosphere: atmosphere
        @param atmosphere: Interface to the atmnospheric environment.
        @type  water: water
        @param water: Calculates water uptake from the soil.
        @type  biomass: biomass
        @param biomass: Calculates potential and actual growth, total biomass.
        @type  developmentstage: DevelopmentStage
        @param developmentstage: Calculatese thermal time and actual developmentstage.
        @type  et: ET
        @param et: Calculatese potential and actual transpiration and evaporation.
        @type  nitrogen: Nitrogen
        @param nitrogen: Calculatese nitrogen uptake from soil
        @type  shoot_percent: list
        @param shoot_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  root_percent: list
        @param root_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  leaf_percent: list
        @param leaf_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  stem_percent: list
        @param stem_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  storage_percent: list
        @param storage_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type tbase: double
        @param tbase: Minimum temperature above growth can take place in Celsius.
        @type rootability: List
        @param rootability: List with critical thresholds for the root penetration resistance of the soil and the 
                            related growth limiting coefficiants as 
                            fraction from the root elongation in [-]. 
                            Example: [critical bulkdensity, limiting coefficiant, critical pressurehead, limiting coefficant, ...]
        @type pressure_threshold: list
        @param pressure_threshold: List with soil pressurehead. These conditions limiting wate uptake and regulate root 
                                   biomass distribution in [cm water column].
                                   Example: [0.,1.,500.,16000.]
        @type plantN: list
        @param plantN: List with thermal time thresholds in [degreedays] and related nitrogen fraction in plant biomass in [-].
                       Example: [[degreeday, fraction],[degreeday, fraction]]
        @type leaf_specific_weight: double
        @param leaf_specific_weight: Defines leaf specific weight in [g m-2]
        @type root_growth: double
        @param root_growth: Root elongation factor in [cm day-1]
        @rtype:   plant
        @return:  Plant instance
        @todo: 
        """
        #Raise Count variable for each platn instance
        Plant.Count+=1
        
        #Handing over environmental interfaces
        self.soil=soil
        self.atmosphere=atmosphere
        
        #Handing over growth process related interfaces
        #Interfaces holds state variables for each process as properties
        self.water=water
        self.biomass=Bbiomass
        self.developmentstage=developmentstage
        self.et=et
        self.nitrogen=nitrogen
        
        #Implemetation of root and shoot class
        self.root=Root(self,root_percent,rootability,root_growth,self.soil.get_profile(),layer)
        self.shoot=Shoot(self,leaf_specific_weight,self.developmentstage[4][1],shoot_percent,leaf_percent,stem_percent,storage_percent)
        
        #Constant variables
        self.plantN=plantN
        self.tbase=tbase
        self.pressure_threshold=pressure_threshold
    def __del__(self):
        """
        Decrease class variable Plant.Count about one.
        
        @param -: 
        @return: -
        """
        Plant.Count-=1
    def __call__(self,time_act,step,interval):
        """
        Call plant initiate the growth process for a given intervall with a given step. The appearance of
        a process is related to the development stage of the plant. Development and Evapotranspiration
        is calcluted for every step. Water uptake and transpiration only occurs if germiantion is finished.
        Nutrient uptake, bioamss accumulation and partitioning takes only in the growing season place. This
        is between the development stages emergence and maturity.
        
        @type time_act: datetime(JJJJ,MM,DD)
        @param time_act: Gives the actual time. 
        @type step: string
        @param step: Time step for the call intervall. Can be day or hour.
        @type interval: double
        @param interval: repeating of the step for the call periode.
        @return: -
        """
        #Set time step
        time_step = 1. * interval if step == 'day' else 1./24. * interval
        
        #compute actual rooting zone with actual rooting depth
        #Rootingzone consists of all layers, which are penetrated from the plant root
        self.root.zone(self.root.depth)
        
        #Development
        self.developmentstage(time_step,self.atmosphere.get_tmin(time_act), self.atmosphere.get_tmax(time_act), self.tbase)
        
        #Evapotranspiration
        self.et(self.soil.Kr_cmf(),self.developmentstage.Thermaltime,self.atmosphere.get_Rn(time_act,0.12,True),self.atmosphere.get_tmean(time_act)
                                   ,self.atmosphere.get_es(time_act),self.atmosphere.get_ea(time_act)
                                   ,self.atmosphere.get_windspeed(time_act),vegH=1.
                                   ,LAI=self.shoot.leaf.LAI,stomatal_resistance=self.shoot.leaf.stomatal_resistance,)
        
        #Water uptake occurs only if germinination is finished (developmentstage > Emergence)
        if self.developmentstage.IsGerminated:
        
        #Water uptake
            #Allocation if the potential transpiration over the rootingzone
            transpiration_distribution = [self.et.Reference/self.root.depth * l.penetration for l in self.root.zone]
            #Calls water interface for the calculation of the water uptake
            self.water(transpiration_distribution
                         ,[self.water.soil_values(self.soil,l.center) for l in self.root.zone],self.pressure_threshold)
        
        #The following processes occure only in the growing season (Emergence < developmentstge <= maturity)
        if self.developmentstage.IsGrowingseason:
            
            #Nutrient uptake from soil
            #Rp = nitrogen demand, product from the potential nitrogen content in percent and athe actual biomass of plant 
            self.Rp=self.NO3dem(self.biomass.PotentialGrowth, self.NO3cont(self.plantN, self.developmentstage.Thermaltime))
            #Calls nitrogen interface for nitrogen uptake
            self.nitrogen([self.soil.get_nutrients(l.center) for l in self.root.zone],
                          self.water.Uptake, self.Rp, [l.penetration for l in self.root.zone])  
            
            #Biomass accumulation
            #Calculates stress index which limits potential growth throug water and nutrient stress
            self.stress=min(sum(self.water.Uptake) / self.et.Cropspecific, sum(self.nitrogen.Total)/ self.Rp,1.)*1.
            #Calls biomass interface for the calculation of the actual biomass
            self.biomass(self.stress,time_step,self.biomass.atmosphere_values(self.atmosphere,time_act),self.shoot.leaf.LAI)
            
            #Partitioning
            #Calls the root instance.Allocates biomass to root and defines the feeling good index for the root biomass
            #distribution.        
            self.root(time_step,self.get_fgi(sum(self.water.Uptake), self.et.Reference, sum(self.nitrogen.Total), self.Rp, 
                                            [self.nitrogen.Total[i] if l.penetration>0. else 0. for i,l in enumerate(self.root.zone)],
                                            [self.water.Alpha[i] if l.penetration>0. else 0. for i,l in enumerate(self.root.zone)]),
                                            (self.root.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                                            self.soil.get_pressurehead(self.root.depth),self.stress)
            #Calls the shoot instance. Alocates biomass to shoot and the other above ground plant organs.
            self.shoot(time_step,(self.shoot.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.leaf.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.stem.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.storage_organs.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       self.developmentstage.Thermaltime)
    def get_fgi(self,Sh,Tp,Ra,Rp,NO3dis,H2Odis):
        """
        Returns the FellingGoodIndex (fgi) for given ditribtuion of water
        and nitrogen in the rootingzone. The fgi is a list with allocation
        coefficants for the root bioamss for each layer in the rootingzone. 
        The coefficants ranges between zero and one. the sum of all 
        coefficants for one timestept must be one (100%). 
        
        The water conditions can be represented through watercontent in [m3 m-3],
        wateruptake [mm] or a stress index depending on the pressure head [-]. The 
        nitrogen conditions are represented with the nitrogen concentration.
        
        First the most limiting resource is determined (water or nitrogen). In the
        second step the percentage of the resource for each layer from the whole
        rootingzone is calculated.
        
        @type Sh: list
        @param Sh: Actual water uptake from soil in [mm].
        @type Tp: double
        @param Tp: Potential transpiration in [mm].
        @type Ra: list
        @param Ra: List with actual nitrogenuptake from soil in [mg].
        @type Rp: double
        @param Rp: Potential nitrogen demand of the plant in [g].
        @type NO3dis: list
        @param NO3dis: Nitrogen conditions in each layer of the rootingzone.
        @type H2Odis: list
        @param H2Odis: Water conditions in each layer of the rootingzone.
        @rtype: list
        @return: List with distribution coefficiants for the root biomass.
        """
        #Compute stress index for nitrogen and water
        w=1-Sh/Tp
        n=1-(Ra/Rp) if Rp>0. else 0.
        #Return list for the factor wit hthe higher stress index
        if  w >= n:
            return [w/sum(H2Odis) for w in H2Odis]
        else:
            return [n/sum(NO3dis) for n in NO3dis]
    def respire(self,g,Wact,m,Wtot):
        """
        Returns empirical respiration for a given total biomass
        and growthrate. Both parameter are multiplied with
        adjustment coefficiants. The product from growthrate and g is
        the growth respiration, the product of total bioamss
        and m the maintenance respiration.
        
        @type Wact: double
        @param Wact: Actual growthrate in [g day-1]
        @type Wtot: double
        @param Wtot: Total biomass in [g]
        @type g: double
        @param g: Adjustment coefficiant for growth respiration.
        @type m: double
        @param m: Adjustment coefficiant for maintenance respiration.
        @rtype: double
        @return: Respiration
        """
        return g*Wact+m*Wtot
    def NO3cont(self,plantN,tt):
        """
        Returns percential nitrogen content of te plant
        biomass depending on the actual thermaltime. The nitrogen content
        before emergence and after maturity doesn't change. For thermal
        time values between this stage the nitrogen content decreases
        linear from emergence to maturity.
        
        @type plantN: list
        @param plantN: List with thermal time thresholds in [degreedays] and related nitrogen fraction in plant biomass in [-].
                       Example: [[degreeday, fraction],[degreeday, fraction]].
        @type tt: double
        @param tt: Actual thermaltime in [degreedays].
        @rtype: double
        @return: Nitrogen fraction of the plant biomass in [-].
        """
        #Computes nitrogen fraction
        if tt<=plantN[0][0]: return plantN[0][1]
        elif tt>=plantN[1][0]: return plantN[1][1]
        else: return plantN[0][1]+(plantN[1][1]-plantN[0][1])/(plantN[1][0]-plantN[0][0])*(tt-plantN[0][0])
    def NO3dem(self,Wpot,NO3conc):
        """
        Returns the nitrogen demand of the plant from the
        potential growthrate and the actual nitrogen content
        of the biomass.
        
        @type Wpot: double
        @param Wpot: Potential growthrate in [g day-1]
        @type NO3conc: double
        @param NO3conc: Actual nitrogen fraction of the biomass in [-].
        @rtype: double
        @return: Nitrogen demand in [g]
        """
        return Wpot*NO3conc
    def vernalisation(self,tmean,plant_vern):
        """
        Returns the relative vernalisation based on the daily mean
        temperature. This ocefficiant is reqired for many cereals,
        which rewuire a periode of time with temperatures
        over a crop specific threshold.
        
        @type tmean: double
        @param tmean: Daily average temperature in [Celsius]
        @type plant_vern: list
        @type plant_vern: List with vernlisation coefficiants.
        @rtype: double
        @return: Relative vernalisation coefficiant.
        
        """
        if tmean<plant_vern[0] or tmean>plant_vern[2]: return 0.
        elif tmean>=plant_vern[0] and tmean<=plant_vern[1]: return 1.0
        else: return (plant_vern[-1]-tmean)/(plant_vern[-1]-plant_vern[-2])    
    def photoperiod(self,dl,type,plant_photoperiod):
        """
        Returns the relative photoperiod coefficiant. The value can
        accelerate development depending on the daylenght and the plant
        type.
        
        @type dl: double
        @param dl: Daylenght in [hour].
        @type type: string
        @param type: Plant photopreiod type, can be longday or shortday plant.
        @type plant_photoperiod: list
        @param plant_photoperiod: List with the photoperiod coefficiants.
        @rtype: double
        @return: Relative photoperiod coefficiant in [-].
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
    Allocates underground biomass to rootoingzone and controls underground growth processes.
    
    Root is a part from plant and represents the under
    ground biomass fraction of the plant. Root growths
    vertical (elongation) and allocates root biomass
    over the rootingzone (distribution). The rootingzone
    is includes the root penetrated soillayer in the
    soilprofile.
    
    Implementation
    ==============
    Root is implemented from the plant class. Root must
    be implemented with a layer object. From this layer
    object the actual rootingzone is calculated from
    the plant class.

    Call signature
    ==============
    Root growth includese two process, elongation and 
    distribution.The elongation process is the vertical 
    growth witha constant growth coefficaiant. This constant 
    growth is limited through physical soil factors, which 
    limit root penetration. The whole plant stress can
    alos restrict root elongation.
    The distribution process is the allocation of root
    biomass over the rootingzone. The allocation is based
    on the feeling good index. The biomass is allocated to
    the layers, which have the highest amount of the
    most limiting resource (nitrogen or water).
    The actual rootzone is calculated form the plant class.
    """
    def __init__(self,plant,percent,rootability,root_growth,soilprofile,layer):
        """
        Returns a root instance and creates a rootingzone from the soilprofile.
        
        @type plant: plant
        @param plant: Plant class, which owns root.
        @type  root_percent: list
        @param root_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type rootability: List
        @param rootability: List with critical thresholds for the root penetration resistance of the soil and the 
                            related growth limiting coefficiants as 
                            fraction from the root elongation in [-]. 
                            Example: [critical bulkdensity, limiting coefficiant, critical pressurehead, limiting coefficant, ...]
        @type root_growth: double
        @param root_growth: Root elongation factor in [cm day-1]
        @type layer: layer
        @param layer: Interface for the calculation of the rooting zone.
        @type soilprofile: list
        @param soilprofile: List with the lower limits of the layers in the soilprofile from the soil interface.
        @rtype: root
        @return: Root instance
        """
        #Root is part from plant
        self.plant=plant
        
        #Constant variables
        self.rootability=rootability
        self.elong=root_growth
        self.percent=percent
        
        #State variables updated in every timestep
        #Rootingdepth
        self.depth=1.
        #Root biomass
        self.Wtot=0.
        #Biomass allocation over the rootingzone
        self.distr=[0. for l in self.zone]
        #Rootingzone
        self.zone=layer
        self.zone.get_rootingzone(soilprofile)
        #FeelingGoodIndex
        self.fgi=[]
    def __call__(self,step,fgi,biomass,h,stress):
        """
        Root call calculates the actual rootingdepth and the allocates
        the biomass between the layers in the rootingzone and
        calculats the actual total bioamss of root.
        
        @type step: double
        @param step: Time step of the run period.
        @type fgi: list
        @param fgi: FeelingGoodIndex for root biomass distritbution for each layer in rootingzone in [-].
        @type h: double
        @param h: Pressurehead at rootingdepth in [cm]
        @type stress: double
        @param stress: Stress index from plant water/nitrogen stress in [-].
        """
        #FeelingGoodIndex
        self.fgi=fgi
        #Calculate actual rooting depth, restricted by plant stress and soil resistance 
        self.depth=self.depth+self.elongation(self.penetrate(1.,h,self.rootability),self.elong)*stress*step
        #Calculate toal biomass
        self.Wtot=self.Wtot+biomass*step
        #Allocate actual growth between the layers in the rooting zone
        self.distr=self.allocate(self.distr, biomass, fgi)
    def allocate(self,distr,biomass,fgi):
        """
        Returns the biomass distribution over the rootingzone, depending
        on the FeelingGoodIndex.
        
        The product of fgi and biomass is calculated for every layer in the
        rootingzone. This product is added to the biomass in each layer.
        
        @type distr: list
        @param distr: List with the total biomass allocation over the rootingzone in [g].
        @type biomass: double
        @param biomass: Actual root growthrate in [g day-1]
        @type fgi: list
        @param fgi: FeelingGoodIndex for root biomass distritbution for each layer in rootingzone in [-].
        @rtype: list
        @return: List with the total biomass in each layer in the rootingzone in [g].
        """
        return [b+(biomass*fgi[i]) for i,b in enumerate(distr)]
    def elongation(self,physical_constraints,root_growth):
        """
        Return vertical growthrate depending on the potential rate
        and the soil resistance represented through physical impendance.
        
        @type physical_imdendance: double
        @param physical_imdendance: Soil resistance against root penetration in [-].
        @type root_growth: double
        @param root_growth: Potential vertical root growth in [cm day-1]
        @rtype: double
        @return: Actual root elongation in [cm day-1]
        """
        return root_growth-physical_constraints*root_growth
    def penetrate(self,bd,h,rootability):
        """
        Returns the most limiting soil resitance factor against
        root penetration.
        
        @type bd: double
        @param bd: Bulkdensity of the soil at rootingdepth in [g cm-3]
        @type h: double
        @param h: Pressurehead at rootingdepth in [cm]
        @type rootability: List
        @param rootability: List with critical thresholds for the root penetration resistance of the soil and the 
                            related growth limiting coefficiants as 
                            fraction from the root elongation in [-]. 
                            Example: [critical bulkdensity, limiting coefficiant, critical pressurehead, limiting coefficant, ...]
        @rtype: double
        @return: Most limiting resitance factor against root penetration in [-].
        
        @todo: resistanc must be a list with a variable length, plant should call dynamically the soil factors for each resistance factor.
        """
        
        #Calculates resistance though mechanical stress
        if bd>=rootability[0]: mechanical_impendance=rootability[1]
        else: mechanical_impendance=0.
        
        #Calculates resistance through water stress
        if h>=rootability[2]:water_stress=rootability[3]
        else: water_stress=0.
        
        #Calculates restiance through oxygen stress
        if h<=rootability[4]:oxygen_deficiency=rootability[5]
        else: oxygen_deficiency=0.
        
        #Returns the most limiting facor against root penetration
        return max(mechanical_impendance,water_stress,oxygen_deficiency)
class Shoot:
    """
    Allocates aboveground biomass to leaf, stem and sotrageorgans.
    
    Shoot is a part from plant and represents the above
    ground biomass. This biomass is diveded into leaf,
    stem and storage organs. The allocation between these
    parts is determined by the development. The partitioning
    rules are input from the user.
    
    Implementation
    ==============
    Shoot is implemented from the plant class. Shoot for
    it self implements leaf, stem and storageorgans.

    Call signature
    ==============
    Shoot growth includes the biomass accumulation of the 
    above ground biomass and the allocation to the other
    above ground parts.
    """
    def __init__(self,plant,lai_conversion,thermaltime_anthesis,shoot_percent,leaf_percent,stem_percent,storage_percent):
        """
        Returns shoot instance. Shoot implements leaf, stem
        and storageorgans.
        
        @type plant: plant
        @param plant: Plant instance which owns shoot.
        @type lai_conversion: double
        @param lai_conversion: Constant conversion coefficiant from leaf weight to leaf area index [g m-2].
        @type thermaltime_anthesis: double
        @param thermaltime_anthesis: Total thermaltime at developmentstage anthesis in [degreedays].
        @type  shoot_percent: list
        @param shoot_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  leaf_percent: list
        @param leaf_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  stem_percent: list
        @param stem_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type  storage_percent: list
        @param storage_percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @rtype: shoot
        @return: shoot instance
        """
        #Shoot is part from plant
        self.plant=plant
        
        #Shoot owns leaf, tem and storage_organs
        self.leaf=Leaf(self,leaf_percent,lai_conversion,thermaltime_anthesis)
        self.stem=Stem(self,stem_percent)
        self.storage_organs=Storage_Organs(self,storage_percent)
        
        #Constant values
        self.percent=shoot_percent
        
        #State variables updated in every timestep
        #total biomass
        self.Wtot=0.
        
    def __call__(self,step,biomass,Wleaf,Wstem,Wstorage,tt):
        """
        Call shoot calculates the actual above ground biomass and allocates
        these biomass between the above ground plant organs. The allocated
        fractions for each organ are calculated from plant. Shoot distributes
        these fractions.
        
        @type step: double
        @param step: Time step of the actual model period in [days or hours].
        @type biomass: double
        @param biomass: Growthrate of the above ground biomass in [g m-2].
        @type Wleaf: double
        @param Wleaf: Gorwhtrate of the leaf biomass in [g m-2].
        @type Wstem: double
        @param Wstem: Gorwhtrate of the stem biomass in [g m-2].
        @type Wstorage: double
        @param Wstorage: Gorwhtrate of the leaf biomass in [g m-2].
        @type tt: double
        @param tt: Actual thermaltime in [degreedays].
        """
        #Calculate actual total aboveground biomass
        self.Wtot=self.Wtot+biomass*step
        
        #Allocate biomass to above ground plant organs
        #Call leaf with actual thermaltime
        self.leaf(step,Wleaf,tt)
        self.stem(step,Wstem)
        self.storage_organs(step,Wstorage)    
class Stem:
    """
    Calcultes stem biomass and plant height.
    
    Implementation
    ==============
    Stem is implemented from the shoot class.
    
    Call signature
    ==============
    Stem must be called with timestep and the stem growthrate
    and calcultes the actual stem biomass and plant height.
    """
    def __init__(self,shoot,percent):
        """
        Returns stem instance.
        
        @type shoot: shoot
        @param shoot: Shoot instance which holds stem.
        @type percent: list
        @param percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @rtype: stem
        @return: stem instance 
        """
        #Stem is part from shoot
        self.shoot=shoot
        
        #Constant values
        self.percent=percent
        
        #State variables updated in every timestep
        #total biomass
        self.Wtot=0.
        #Plant hight/ stem length
        self.height=0.
        
    def  __call__(self,step,biomass):
        """
        Calculates total stem biomass and plant height.
        
        @type step: double
        @param step: Time step of the actual model period in [days or hours].
        @type biomass: double
        @param biomass: Growthrate of stem biomass in [g m-2].
        
        @todo: Calculation of plant height/ stem lenght
        """
        self.height = self.calc_height()
        self.Wtot=self.Wtot+biomass*step
    def calc_height(self):
        pass
class Storage_Organs:
    """
    Calcultes storageorgans biomass and yield components.
    
    Implementation
    ==============
    Storageorgans is implemented from the shoot class.
    
    Call signature
    ==============
    Storageorgans must be called with timestep and the stem growthrate
    and calcultes the actual stem biomass and the yield components.
    """
    def __init__(self,shoot,percent):
        """
        Returns storageorgans instance.
        
        @type shoot: shoot
        @param shoot: Shoot instance which holds sotragaorgans.
        @type percent: list
        @param percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @rtype: storage_organs
        @return: storaga_organs instance
        """
        #Part from plant
        self.shoot=shoot
        
        #Constant variables
        self.percent=percent
        
        #State variables updated in every timestep
        #Total biomass
        self.Wtot=0.
        #Yield components
        self.yield_components=0.
        
    def  __call__(self,step,biomass):
        """
        Calculates storageorgans total biomass.
        
        @type step: double
        @param step: Time step of the actual model period in [days or hours].
        @type biomass: double
        @param biomass: Growthrate of storageorgans biomass in [g m-2].
        @return: -
        
        @todo: Calculation of yield components
        """
        #Calculates biomass
        self.Wtot=self.Wtot+biomass*step
    def grain_yield(self,KNO,KW=0.041):#KW for wheat
        """ 
        Returns the grain yield of a cereal. Yield is the 
        product of kernel number and kernel weight.
        
        KNO is established in the period between 20 and 30 days 
        before flowering and ten days after anthesis.
        
        @type KNO: double
        @param KNO: Kernel number in [Kernel m-2]
        @type KW: double
        @param KW: The kernel weight in [g]
        @rtype: double
        @return: Grain yield (g/m2)
        
        @see: [Acevedo et al, 2002]
        """
        return KNO*KW
class Leaf:
    """
    Calcultes leaf biomass and leaf area index.
    
    Implementation
    ==============
    Leaf is implemented from the shoot class.
    
    Call signature
    ==============
    Leaf calcultes actual tota biomass and the LAI with
    the specific leaf weight and biomass.
    """
    def __init__(self,shoot,percent,lai_conversion,thermaltime_anthesis):
        """
        Returns a leaf instance.
        
        @type shoot: shoot
        @param shoot: Shoot instance which holds sotragaorgans.
        @type percent: list
        @param percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type lai_conversion: double
        @param lai_conversion: Constant conversion coefficiant from leaf weight to leaf area index [g m-2].
        @type thermaltime_anthesis: double
        @param thermaltime_anthesis: Total thermaltime at developmentstage anthesis in [degreedays].
        @rtype: leaf
        @return: leaf instance
        """
        #Part from shoot
        self.shoot=shoot
        
        #Constant variables
        self.specific_weight=lai_conversion
        self.ttanthesis = thermaltime_anthesis
        self.percent=percent
        
        #State variables updated in every timestep
        self.stomatal_resistance=0.
        self.Wtot=0.
        self.leafarea=0.1
        
    @property
    def LAI(self):
        """
        @rtype: double
        @return: LeafAreaIndex in [m2 m-2]
        """
        return self.leafarea
    def  __call__(self,step,biomass,tt):
        """
        Call leaf calculates total leaf biomass and LAI. Additional LAI is
        calculated from the specific leaf weight and leaf biomass.
        
        @type step: double
        @param step: Time step of the actual model period in [days or hours].
        @type biomass: double
        @param biomass: Growthrate of the above ground biomass in [g m-2].
        @type Wleaf: double
        @type tt: double
        @param tt: Actual thermaltime in [degreedays].
        
        @todo: Calculation of stomatal resistance.
        """
        #Calculate total biomass
        self.Wtot = self.Wtot + biomass * step
        #Calcualte LAI
        self.leafarea += self.convert(biomass, self.adj_weigth(tt, self.ttanthesis)*self.specific_weight)
        self.stomatal_resistance= 100 if self.shoot.plant.developmentstage.IsGerminated else 300
    def convert(self,biomass,specific_weight):
        """ Calculates LeafAreaIndex from leaf biomass and leaf specific weight.
        
        Leaf specific weight is a constant factor. It can be adjusted to the
        actual development stage with the function leaf.adj_weight().
        
        @type biomass: double
        @param biomass: Biomass of leafs in [g m-2].
        @type specific_weight: double
        @param specific_weight: Specific biomass of the leafs in [g m-2].
        @rtype: double
        @return: LeafAreaIndex in [m2 m-2]
        
        @see: [De Vries et al, 1989]
        """
        return biomass/specific_weight
    def adj_weigth(self,tt,tt_anthesis):
        """
        Returns the ajdusted specific weight depending on the plant development.
        
        To adjuste the specific weight to thermaltime the specificd weight
        is multiplied with a weighting factor depending on the development
        stage of the crop.
        
        @type tt: double
        @param tt: Actual thermaltime in [degreedays].
        @type thermaltime_anthesis: double
        @param thermaltime_anthesis: Total thermaltime at developmentstage anthesis in [degreedays].
        he specific leaf weight of new leaves is calculated by
        multiplying the specific leaf weight constant with a factor that depends on the
        development stage of the crop.
        
        @see: [De Vries et al, 1989]
        """
        return min((tt/tt_anthesis+0.25),1.)
class Development:
    """
    Calculates the developmentstage of plant with the thermaltime concept.
    
    Development is an implementation of the plant interface
    development with the required functions.

    Implementation
    ==============
    A development instance must be hand over to plant for the 
    implementation of plant. Development for itsel must be
    implemented with the crop specific developmentstages and the
    related total thermaltime for each dtage.
    
    Call signature
    ==============
    Call development calculates thermaltime.
    """
    def __init__(self,stage):
        """
        Returns a development instance.
        
        Development is defined throug the stage parameter. 
        this parameter holds a list with the name of each
        stage and the related total thermaltime. The total
        values are the thresholds for changing the stage.
        The total thermaltime values of the stages are 
        constant values. Variation of the amount of time,
        which is required to reach the next stage, is only
        possibl through the variation of the daily calculated
        degree days.
        
        @type stage: list
        @param stage: List with names and total thermaltime requirement for each stage in [degreedays].
                      Example: [['Emergence',160.],['Leaf development',208.],...]
        @rtype: development
        @return: Development instance        
        """
        #List with all names and thermaltime thresholds of each stage
        self.stages=[]
        #State vairbles updated in every timestep
        self.tt=0.
        for s in stage:
            self.__setitem__(s)
    @property
    def StageIndex(self):
        """
        Returns the index of the actual development stage in the stage attribute of the development class
        
        @rtype: interger
        @return: Index of the actual development stage
        """
        return self.stages.index(self.Stage)
    @property
    def IsGrowingseason(self):
        """
        Returns True during growingseason.
        
        @rtype: boolean
        @return: True during growingseason.
        """
        return True if self.tt>=self.stages[0][1] and self.tt< self.stages[-1][1] else False
    @property
    def IsGerminated(self):
        """
        Return True, if germination is complete.
        
        @rtype: boolean
        @return: True, if germmination is complete.
        """
        return True if self.tt > self.stages[0][1] else False
    @property
    def Thermaltime(self):
        """
        Return actual thermaltime
        
        @rtype: double
        @return: Thermaltime in [degreedays].
        """
        return self.tt
    @property
    def Stage(self):
        """
        Returns the name of the actual development stage
        
        If development is finished, the function returns 'Development finished'
        
        @rtype: String
        @return: Actual developmentstage.
        """
        return filter(lambda i:i[1]>=self.tt, self.stages)[0] if self.tt<=self.stages[-1][1] else 'Development finished'
    def __setitem__(self,stage):
        self.stages.append(stage)
    def __getitem__(self,index):
        return self.stages[index]
    def __iter__(self):
        for s in self.stages:
            yield s
    def __call__(self,step,tmin,tmax,tbase):
        """
        Calcultes thermaltime.
        
        @type step: double
        @param step: Time step of the actual model period in [days or hours].
        @type tmin: double
        @param tmin: Daily minimum temperature in [Celsius].
        @type tmax: double
        @param tmax: Daily maximum temperature in [Celsius].
        @type tbase: double 
        @param tbase: Crop specific base temperature over which development can occur in [Celsius].
        """
        self.tt = self.tt + self.develop(tmin, tmax, tbase) * step
    def develop(self,tmin,tmax,tbase):
        """
        Returns thermaltime rate for given temperature and crop specific base temperature.
        
        If tmax or min smaller than tbase, the rate is defined to be zero.
        Else the rate is computed as (tmax+tmin/2 - tbase).
        
        @type tmin: double
        @param tmin: Daily minimum temperature in [Celsius].
        @type tmax: double
        @param tmax: Daily maximum temperature in [Celsius].
        @type tbase: double 
        @param tbase: Crop specific base temperature over which development can occur in [Celsius].
        @rtype: double
        @return: Thermaltime rate in [degreedays].
         
        @see: [Bonhomme, 2000, McMaster & Wilhelm, 1997] 
        """
        if tmax < tbase or tmin < tbase:
            return 0
        else:
            return ((tmax+tmin)/2.0-tbase)
class SoilLayer:
    """
    SoilLayer is the framework for the rootingzone and holds the geometrica attributes.
    
    Soillayer holds values for the geometrical descritpion
    of the rootingzone. It is devided into layers which can
    be penetrated from the plant root. 
    
    
    Soillayer holds values which describe the constantant
    
    Development is an implementation of the plant interface
    development with the required functions.

    Implementation
    ==============
    Soillayer is implemented without values. With the
    function get_rootingzone() a rootingzone can be created.
    
    Call signature
    ==============
    Call Soillayer calculates the actual rootingzone, depending
    on the pentration depth of the plant root.For that
    the root penetration for each layer is calculated.
    """
    def __init__(self,lower=0.,upper=0.,center=0.,thickness=0.,penetration=0.):
        """
        Returns a soillayer instance with zero values for all attributes.
        
        To create a rootingzone get_rootingzone() must be called.
        
        @type lower: double
        @param lower: Lower limit of the soil layer relative to ground surface level in [cm].
        @type upper: double
        @param upper: Upper limit of the soil layer relative to ground surface level in [cm].
        @type center: double
        @param center: Center of the soil layer relative to ground surface level in [cm].
        @type thickness: double
        @param thickness: Thickness of the layer in [cm].
        @type penetration: double 
        @param penetration: Root penetrated fraction of the layer in [cm].
        @rtype: soillayer
        @return: soillayer instance
        """
        #Constant variables
        #Geometrical detail of the layer
        self.lower=lower
        self.upper=upper
        self.center=center
        self.thickness=thickness
        #List with all layers in the soilprofile, which is created with get_rootingzone()
        self.rootingzone=[]
        
        #State variables updated in every timestep
        self.penetration=penetration
    def __getitem__(self,index):
        return self.rootingzone[index]
    def __iter__(self):
        for horizon in self.rootingzone:
            yield horizon
    def get_rootingzone(self,soilprofile):
        """ Returns a rootingzone with the geomertical details of each layer.
        
        @type soilprofile: list
        @param soilprofile: List with the lower limits of the layers in the soilprofile in [cm].
        @rtype: soilprofile
        @return: Soilprofile which defines the actual rootingzone.
        """
        #Create soillayer for each layer in soilprofile
        for i,layer in enumerate(soilprofile):
            #Each layer is a soillayer instance
            self.rootingzone.append(SoilLayer())
            #set lower limit
            self.rootingzone[i].lowerlimit=layer
            #first layer upper limit = 0.
            if i == 0: 
                self.rootingzone[i].upperlimit = 0.
            #all other layers upper limit = lower limit of the above layer
            else: 
                self.rootingzone[i].upperlimit = (soilprofile[i-1])
            #Center and thickness of each layer
            self.rootingzone[i].center = (self.rootingzone[i].lowerlimit + self.rootingzone[i].upperlimit) / 2.
            self.rootingzone[i].thickness = self.rootingzone[i].lowerlimit - self.rootingzone[i].upperlimit 
    def __call__(self,Zr):
        """
        Calculates the pentration depth for each soillayer in the rootingzone.
        
        @type Zr: double
        @param: Rootingdepth in [cm].
        """
        #For each layer in rootingzone
        for layer in self.rootingzone:
            #If lower limit <= rootingdepth, the soillayer is full penetrated
            if layer.lowerlimit <= Zr:
                layer.penetration = layer.depth
            #If upperlimit above rootingdepth, layer is not penetrated
            elif layer.upperlimit>Zr:
                layer_penetration = 0.
            #If only a part from the layer is penetrated, the value is rootingdepth minus upperlimit
            else: 
                layer.penetration = Zr - layer.upperlimit
class ET_FAO:
    """
    The class calcultes crop specific Evapotranspiration and correponds with the plant inferface evaporation.
    
    
    ET_FAO calculates the crop specific Evapotranspiration.
    This concept based on the Penmnan-Monteith equation. 
    Reference Evapotranspiration (ETo) is ajdusted with crop 
    specific values. The resulting crop specific Evapotranspiration (ETc)
    is divided into a transpiration and a evaporation component.
    All equations and concepts implenented in this class are taken from
    "Crop evapotranspiration - Guidelines for computing crop water requirements - FAO Irrigation and drainage paper 56"
    except for the calculation of the fieldcover. In this case the calculation
    based on the leaf area index and not on the FAO-concept.
    All coefficiants used in this approach can be recieved from
    these guidelines.
       
    @see: [Allen et al, 1998]
    
    Implementation
    ==============
    ET_FAO must be implemented with the crop specif parameter.
    These parameter are related to the development of the plant.
    For the discritpion of influences of the development the development
    of the plant is divided into four seasons. This arrangement
    can be taken form the plant development class. For the calculation
    of the transpiration crop specific transpiration coefficiants for 
    each season are required, which can be received from th FAO-guidelines.
    
    Call signature
    ==============
    ET_FAO msut be called with crop specific values discribing vegetation
    strucute and development and the actual wheather conditions. For the calculation
    of the evaporation the calculation of a daily oil water balance is needed. For
    that the FAO water balance model can be used. These model is 
    implemented in the class SWC - SoilWaterContainer. It is possible
    to use other water balance models, if they match the interface requirements.    
    """
    def __init__(self,kcb_values,seasons):
        """
        Returns a ET_FAO instance.
        
        @type seasons: list
        @param seasons: List with the length of the four development seasons in [degreedays].
        @type kcb_values: list
        @param kcb_values: List with basal crop coefficiants for each season in seasons parameter in [-].
        
        @rtype: ET_FAO
        @return: ET_FAO instance
        """
        #Constant variables
        self.kcb_values=kcb_values
        self.seasons=seasons
        #State vairables
        self.eto=0.
        self.kcb=0.
        self.ke=0.
        self.fw=1.
        self.fc=0.
    @property
    def FieldCover(self):
        """
        Returns the fieldcover after the FAO-concept
        
        @rtype: double
        @return: Fieldcover in [-].
        """
        return self.fc
    @property
    def Transpiration(self):
        """
        Returns transpiration
        
        @rtype: double
        @return: Transpiration in [mm].
        """
        return self.eto * self.kcb
    @property
    def Evaporation(self):
        """
        Returns Evaporation
        
        @rtype: double
        @return: Evaporation in [mm].
        """
        return self.eto * self.ke
    @property
    def Reference(self):
        """
        Returns reference Evapotranspiration.
        
        @rtype: double
        @return: Reference Evapotranspiration in [mm].
        """
        return self.eto
    @property
    def Cropspecific(self):
        """
        Returns Cropspecific Evapotranspiration.
        
        @rtype: double
        @return: Cropspecific Evapotranspiration in [mm].
        """
        return self.eto * (self.kcb+self.ke)
    @property
    def Adjusted(self):
        """
        Returns Adjusted cropspecific Evapotranspiration to water stress.
        
        @rtype: double
        @return: Adjusted cropspecific Evapotranspiration to water stress in [mm].
        """
        return self.eto * (self.kcb*self.ks+self.ke)
    def __call__(self,Kr,thermaltime,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,RHmin=30.,h=1.):
        """
        Calculates reference Evapotranspiration and the crop specific adjustment factors Kcb and Ke.
        
        The user cann call the transpiration coefficiants wit hthe corresonding properties of the class.
        
        @type Kr: double 
        @param Kr: evaporation reduction coefficient dependent on the soil water depletion from the topsoil layer in [-].
        @type thermaltime: double
        @param thermaltime: Thermaltime in [degreedays].
        @type Rn: double
        @param Rn: Net radiation at the crop surface in [MJ m-2].
        @type T: double
        @param T: Mean daily air temperature at 2 m height in  [Celsius].
        @type e_s: double
        @param e_s: Saturation vapour pressure in [kPa].
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type vegH: double
        @param vegH: Vegetation height in [m].
        @type LAI: double
        @param LAI: Leaf are index in [m2 m-2].
        @type stomatal_resistance: double
        @param stomatal_resistance: Stomatal ristance in [cm].
        @type RHmin: double
        @param RHmin: Mean value for daily minimum relative humidity during the mid- or late season growth stage in [percent].
        @type h: double
        @param h: mean maximum plant height during the period of calculation (initial, development, mid-season, or late-season) in [m].
        
        @todo: Unit for stomatal resistance
        """
        #Calculates reference Evapotranspiration
        self.eto = self.calc_ETo(Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0)
        
        #Calculates basal crop coefficaint for thhe transpiration calculation
        self.kcb = self.calc_Kcb(thermaltime, self.kcb_values[0], self.kcb_values[1],
                                 self.kcb_values[2], self.seasons[0], self.seasons[1], 
                                 self.seasons[2], self.seasons[3])
        
        #Calculates upper limit on the evaporation and transpiration from any cropped surface
        kcmax = self.calc_Kcmax(self.kcb, h, windspeed, RHmin)
        
        #Calcultes fieldcover afte FAO and exposed and wetted soil fraction
        self.fc = self.calc_fc_dynamic(self.kcb, kcmax, vegH)
        few = self.calc_few(self.fc, self.fw)
        
        #Calculates evaporation coefficiant
        self.ke = self.calc_Ke(Kr, kcmax, self.kcb, few)
        
    def calc_ETo(self,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0,daily=True):
        """
        Calculates the reference Evapotranspiration.
        
        @type Rn: double
        @param Rn: Net radiation at the crop surface in [MJ m-2].
        @type T: double
        @param T: Mean daily air temperature at 2 m height in  [Celsius].
        @type e_s: double
        @param e_s: Saturation vapour pressure in [kPa].
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type vegH: double
        @param vegH: Vegetation height in [m].
        @type LAI: double
        @param LAI: Leaf are index in [m2 m-2].
        @type stomatal_resistance: double
        @param stomatal_resistance: Stomatal ristance in [cm].
        @rtype: double
        @return: Reference evapotranspiration in [mm].
        
        @todo: defintion of altitude
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
class Water_FAO:
    def __init__(self,average_available_soilwater=0.5):
        self.ks=0.
        self.p = average_available_soilwater
        self.uptake = 0.
    @property
    def Uptake(self):
        return self.uptake
    def __call__(self,ETo,Ke,Kcb,TAW,Dr,soillayer):
        RAW = TAW * self.adjust_p(self.p, ETo)
        self.ks = self.calc_Ks(TAW, Dr, RAW, self.p)
        self.uptake = [Eto * (self.ks * Kcb + Ke)/len(soillayer) for l in soillayer]
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
class Water_Feddes:
    def __init__(self,maxcomp=2.):
        self.max_compensation_capacity=maxcomp
        self.Sh=[]
        self.alpha=[]
        self.compensation=[]
        self.Shcomp=[]
    @property
    def Uptake(self):
        return self.Sh
    @property
    def Alpha(self):
        return self.alpha
    def __call__(self,s_p,pressurehead,h_threshold):
        self.Sh =[s * self.sink_term(pressurehead[i], h_threshold)for i,s in enumerate(s_p)]
        self.alpha = [self.sink_term(m,h_threshold)for m in pressurehead]
        self.compensation = self.compensate(self.Sh,s_p,pressurehead, self.alpha, h_threshold[2],
                                               self.max_compensation_capacity)
        self.Shcomp=[s_h + self.compensation[i] for i,s_h in enumerate(self.Sh)]
    def compensate(self,Sh,Sp,pressurehead,alpha,maxopth,maxcomp):
        remaining_alpha= [max(1-(m/maxopth),0.) for i,m in enumerate(pressurehead)] 
        remaining_uptake=sum(Sp)-sum(Sh)
        return [min(r/sum(remaining_alpha)*remaining_uptake,maxcomp*Sh[i])for i,r in enumerate(remaining_alpha)]     
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
    def __init__(self,capacitylimit,growthfactor):
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
    def __call__(self,stress,step):
        self.stress=stress
        self.total = self.total + self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit) * stress * step
    def logarithmic_growth(self,total_biomass,growthfactor,capacitylimit):
        return total_biomass * growthfactor * (1- total_biomass / capacitylimit)
    def atmosphere_values(self,atmosphere,time_act):
        pass
    def senescence(self):
        pass
class Biomass_LUE:
    def __init__(self,RUE,k):
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
    def atmosphere_values(self,atmosphere,time_act):
        return atmosphere.get_Rs(time_act)
class Nitrogen:
    def __init__(self,Km=0.,NO3_min=0.):
        self.Pa=[]
        self.Aa=[]
        self.Km=Km
        self.NO3min=NO3_min
    @property
    def Active(self):
        return self.Aa
    @property
    def Passvie(self):
        return self.Pa
    @property
    def Total(self):
        return [a + self.Pa[i] for i,a in enumerate(self.Aa)]
    def __call__(self,NO3_conc,Sh,Rp,rootzone):
        self.Pa = [w*NO3_conc[i] for i,w in enumerate(Sh)]
        Ap = max(Rp-sum(self.Pa),0.)
        ap = Ap/sum(rootzone)
        michaelis_menten = [(n-self.NO3min)/(self.Km+n-self.NO3min) for n in NO3_conc]
        self.Aa = [ap*michaelis_menten[i]*l for i,l in enumerate(rootzone)]

''' Plant Interfaces:
class Soil:
    def pressurehead(self,depth):
        """ Depth in cm; Returns the capillary suction for a given depth in [cm]."""
    def nitrogen_conc(self,depth):
       """ Depth in cm; Returns the nitrogen concentration in the soil solution in [mol l-1]"""
    def soilprofile(self):
        """ Returns a list with the lower limits of the layers in the whole soilprofile in [cm]. """
     
    Der Kr-Wert(dimensionless evaporation reduction coefficient dependent on the soil 
    water depletion (cumulative depth of evaporation) from the topsoil layer) ist spezifisch fuer die 
    Art der Berechnung der Evaporation. Waere sinnvoll, wenn das Evapotranspirationsmodul die
    einzelnen  Werte zur Berecnung abfragt. Dann wuerde die Kr Abfrage wegfallen.
    
    def Kr(self):
        """ dimensionless evaporation reduction coefficient from the topsoil layer) """
    
    def fc(self,depth):
        """ soil water content at field capacity [m3 m-3] """
    def wp(self,depth):
        """ soil water content at wilting point [m3 m-3] """
    def wetness(self,depth,depth)
        """ wetness in the top soil layer in [m3 m-3] """
        
          
class Atmosphere:
    def tmin(self,time):
       """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in Celsius """
    def tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in Celsius """
    def Rs(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
    def ea(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
    def es(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
    def windspeed(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
    def sunshine(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns sunshine hours in [hour]"""
'''
        
        