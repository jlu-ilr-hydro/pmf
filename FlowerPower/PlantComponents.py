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
                 leaf_specific_weight=50.,root_growth=1.2,max_height=1.):        
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
        """
        #Raise Count variable for each platn instance
        Plant.Count+=1
        
        #Handing over environmental interfaces
        self.soil=soil
        self.atmosphere=atmosphere
        
        #Handing over growth process related interfaces
        #Interfaces holds state variables for each process as properties
        self.water=water
        self.biomass=biomass
        self.developmentstage=developmentstage
        self.et=et
        self.nitrogen=nitrogen
        
        #Implemetation of root and shoot class
        self.root=Root(self,root_percent,rootability,root_growth,layer)
        self.shoot=Shoot(self,leaf_specific_weight,self.developmentstage[4][1],shoot_percent,leaf_percent,stem_percent,storage_percent,
                         max_height,elongation_end=self.developmentstage[3][1])
        
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
        @todo: vegH equals at the first day of growth zero: ZeroDivisionError. Bad solution: max(0.01,self.shoot.stem.height)
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
                                   ,self.atmosphere.get_windspeed(time_act),vegH=max(0.01,self.shoot.stem.height)
                                   ,LAI=self.shoot.leaf.LAI,stomatal_resistance=self.shoot.leaf.stomatal_resistance,)
        
        #Water uptake occurs only if germinination is finished (developmentstage > Emergence)
        if self.developmentstage.IsGerminated:
        
        #Water uptake
            #Allocation if the potential transpiration over the rootingzone
            transpiration_distribution = [self.et.Transpiration/self.root.depth * l.penetration for l in self.root.zone]
            #Calls water interface for the calculation of the water uptake
            self.water(transpiration_distribution
                         ,[self.water.soil_values(self.soil,l.center) for l in self.root.zone],self.pressure_threshold)
       
        #Nutrient uptake from soil
            #Rp = nitrogen demand, product from the potential nitrogen content in percent and athe actual biomass of plant 
            self.Rp=self.NO3dem(self.biomass.PotentialGrowth, self.NO3cont(self.plantN, self.developmentstage.Thermaltime))
            #Calls nitrogen interface for nitrogen uptake
            self.nitrogen([self.soil.get_nutrients(l.center) for l in self.root.zone],
                          self.water.Uptake, self.Rp, [l.penetration for l in self.root.zone])  
        
        
        
        #The following processes occure only in the growing season (Emergence < developmentstge <= maturity)
        if self.developmentstage.IsGrowingseason:
            #Biomass accumulation
            #Calculates stress index which limits potential growth throug water and nutrient stress
            self.stress=min(sum(self.water.Uptake) / self.et.Cropspecific, sum(self.nitrogen.Total)/ self.Rp,1.)*1.
            #Calls biomass interface for the calculation of the actual biomass
            self.biomass(self.stress,time_step,self.biomass.atmosphere_values(self.atmosphere,time_act),self.shoot.leaf.LAI)
            #Partitioning
            #Calls the root instance.Allocates biomass to root and defines the feeling good index for the root biomass
            #distribution.
            if self.developmentstage.Thermaltime <= self.developmentstage[4][1]:
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
            return [h2o/sum(H2Odis) for h2o in H2Odis]
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
    def __init__(self,plant,percent,rootability,root_growth,layer):
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
        self.growth = 0.
        #Rootingzone
        self.zone=layer
        #Biomass allocation over the rootingzone
        self.branching=[0. for l in self.zone]
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
        self.growth = biomass*step
        self.Wtot=self.Wtot+biomass*step
        #Allocate actual growth between the layers in the rooting zone
        self.branching=self.allocate(self.branching, biomass, fgi)
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
        
        @todo: Resistanc must be a list with a variable length, plant should call dynamically the soil factors for each resistance factor.
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
    def __init__(self,plant,lai_conversion,thermaltime_anthesis,shoot_percent,leaf_percent,stem_percent,storage_percent,max_height,elongation_end):
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
        self.stem=Stem(self,stem_percent,max_height,elongation_end)
        self.storage_organs=Storage_Organs(self,storage_percent)
        
        #Constant values
        self.percent=shoot_percent
        
        #State variables updated in every timestep
        #total biomass
        self.Wtot=0.
        
    def __call__(self,step,biomass,Wleaf,Wstem,Wstorage,thermaltime):
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
        @type thermaltime: double
        @param thermaltime: Actual thermaltime in [degreedays].
        """
        #Calculate actual total aboveground biomass
        self.Wtot=self.Wtot+biomass*step
        
        #Allocate biomass to above ground plant organs
        #Call leaf with actual thermaltime
        self.leaf(step,Wleaf,thermaltime)
        self.stem(step,Wstem,thermaltime)
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
    def __init__(self,shoot,percent,max_height,elongation_end):
        """
        Returns stem instance.
        
        @type shoot: shoot
        @param shoot: Shoot instance which holds stem.
        @type percent: list
        @param percent: List with partitioning coefficiants for each developmentstage as fraction from the plant biomass in [-].
        @type elongation_end: double
        @param elongation_end: Total thermal time at the end of stem elongation [degreedays].
        @type max_height: double
        @param max_height: Maximum Crop Height in [m].
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
        self.max_height = max_height
        self.elongation_end = elongation_end
    def  __call__(self,step,biomass,thermaltime):
        """
        Calculates total stem biomass and plant height.
        
        @type step: double
        @param step: Time step of the actual model period in [days or hours].
        @type biomass: double
        @param biomass: Growthrate of stem biomass in [g m-2].
        @type thermaltime: double
        @param thermaltime: Actual thermal time in [degreedays].
        @return: -
        """
        self.height = self.vertical_stem_growth(self.max_height,self.elongation_end,thermaltime)
        self.Wtot=self.Wtot+biomass*step
    def vertical_stem_growth(self,max_height,elongation_end,thermaltime):
        """
        Calculates crop height from maximal height and thernaltime.
        
        Plant height is calculatd as fraction from a crop specific maximal
        height. That fraction refers to fraction of actual thermal time
        form the total thermaltime at the end of stem elongation stage.
        
        @type max_height: double
        @param max_height: Maximum Crop Height in [m].
        @type thermaltime: double
        @param thermaltime: Actual thermal time in [degreedays].
        @type elongation_end: double
        @param elongation_end: Total thermal time at the end of stem elongation [degreedays].
        @rtype: double
        @return: Vertical growth rate depending on development in [m].
        """
        return max(thermaltime / elongation_end,1) * max_height
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
        """
        #Calculates biomass
        self.Wtot=self.Wtot+biomass*step
    def grain_yield(self,KNO,KW=0.041):
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
        @todo: Calculation of yield components must be implemented. The current approach return only dry mass of the storage components.
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
    def stomatal_resistance(self):
        """
        Reduced photosynthesis due to sink size limitation, ageing, or
        even low air humidity increases stomatal resistance and lowers the potential
        transpiration rate. The actual transpiration rate is below the potential rate
        when stomatal resistance increases in response to water shortage.
        
        @type param: double
        @param param: 
        @rtype: double
        @return: Stomatal resistance
        
        The stomatal resistance is mainly determined by photosynthesis and the
        CO 2 -internal/external fraction.
        
        @see: [O'Toole and Cruz, 1980, De Vries et al, 1989]
        
        @todo: Calculation of stomatal resistance
        """
        pass
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
        
class Water:
    def Uptake():
        pass
    
class Biomass:
    def Total():
        pass
    def Actual():
        pass
    def Potential():
        pass

class Evapotranspiration():
    def Transpiration():
        pass
    def Evaporation():
        pass
    
class DEvelopment():
    def Stage()
        pass
    def Thermaltime():
     pass

class Layer()
    def Lowerlimit()
        pass
    def Upperlimit()
        pass
    def Center()
        pass
        
class Nitrogen()
    def Passive()
        pass
    def Active():
        pass
    def Total()
        pass
'''
        
        