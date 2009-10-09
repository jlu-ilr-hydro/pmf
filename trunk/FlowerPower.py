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
    Calculates crop specific Evapotranspiration and correponds with the plant inferface evaporation.
    
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
    
     @see: [Allen et al, 1998]
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
        """ 
        Calculates crop specific Evapotranspiration.
        
        @type ETo: double
        @param ETo: Reference Evapotranspiration in [mm].
        @type Kcb: double
        @param Kcb: Basal crop coefficient (Kcb) in [-].
        @type Ke: double
        @type Ke: Evaporation coefficiant in [-].
        @rtype: double
        @return: Crop specific evapotranspiration in [mm].
        """
        return ETo * (Kcb+Ke)
    def adjust_Kcb(self,Kcb_tab,windspeed,RHmin,h):
        """ 
        Adjust basal crio coefficiant (Kcb) to environmental conditions.
        
        @type Kcb_tab: double
        @param Kcb_tab: Constant basal crop coefficient (Kcb) related to the development season in [-].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type RHmin: double
        @param RHmin: Mean value for daily minimum relative humidity during the mid- or late season growth stage in [percent].
        @type h: double
        @param h: mean maximum plant height during the period of calculation (initial, development, mid-season, or late-season) in [m].
        @rtype: double
        @return: Kcb adjusted with windspeed, plant height and relative humidity in [-].
        """
        return Kcb_tab + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3
    def calc_Kcb(self,time,Kcb_ini,Kcb_mid,Kcb_end,Lini,Ldev,Lmid,Llate):
        """ 
        Constructed basal crop coefficient (Kcb) curve. 
            
        @type time: double 
        @param time: Day is the actual day or thermaltime in [days] or [degreedays]. 
        @type Kcb_ini: double 
        @param Kcb_ini: Kcb for initial season  
        @type Kcb_mid: double 
        @param Kcb_mid: Kcb for mid season 
        @type Kcb_end: double 
        @param Kcb_end: Kcb for late season   
        @type Lini: double 
        @param Lini: Length of initial season  
        @type Ldev: double 
        @param Ldev: ength of crop development season  
        @type Lmid: double 
        @param Lmid: Length of mid season
        @type Llate: double 
        @param Llate: Length of late season     
        @rtype: double
        @return: Kbc depending on the actual time in [-].
        """
        if time <=Lini: return Kcb_ini
        elif time <=Lini+Ldev: return Kcb_ini+(day-Lini)/Ldev*(Kcb_mid-Kcb_ini)
        elif time <=Lini+Ldev+Lmid: return Kcb_mid
        elif time <= Lini+Ldev+Lmid+Llate: return Kcb_mid+(time-(Lini+Ldev+Lmid))/Llate*(Kcb_end-Kcb_mid)
        else: return Kcb_end
    def calc_Ke(self,Kr,Kcmax,Kcb,few):
        """
        Calculates evaporation coefficiant.
        
        @type Kr: double
        @param Kr: Evaporation reduction coefficient dependent on the cumulative depth of water depleted (evaporated) from the topsoil.
        @type Kcmax: double
        @param Kcmax: Maximum value of Kc following rain or irrigation in [-].
        @type Kcb: double
        @param Kcb: Basal crop coefficient in [mm].
        @type few: double
        @param few: Fraction of the soil that is both exposed and wetted, i.e., the fraction of soil surface from which most evaporation occurs.
        @rtype: double
        @return: Evaporation coefficiant in [mm].
        """
        return min(Kr*(Kcmax - Kcb), few*Kcmax,)
    def calc_Kcmax(self,Kcb,h,windspeed,RHmin):
        """ 
        Calcualtes maximum value of Kc following rain or irrigation.
        
        @type Kcb: double
        @param Kcb: Basal crop coefficient in [mm].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type RHmin: double
        @param RHmin: Mean value for daily minimum relative humidity during the mid- or late season growth stage in [percent].
        @type h: double
        @param h: mean maximum plant height during the period of calculation (initial, development, mid-season, or late-season) in [m].
        @rtype: double
        @return: Maximum value of Kc following rain or irrigation in [-].
        """
        return max((1.2 + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3),Kcb+0.05)
    def calc_TEW(self,qFC,qWP,Ze):
        """
        Calculates total evaporable water.
        
        TEW total evaporable water = maximum depth of water 
        that can be evaporated from the soil when the topsoil
        has been initially completely wetted.
        
        
        @type qFC: double
        @param qFC: Soil water content at field capacity in [m3 m-3].
        @type qWP: double
        @param qWP: Soil water content at wilting point in [m3 m-3].
        @type Ze: double
        @param Ze: Depth [0.10-0.15m] of the surface soil layer that is subject to drying by way of evaporation in [m].
        @rtype: double
        @return: Total evaporable water in [mm].
        """
        return 1000(qFC-0.5*qWP)*Ze
    def calc_Kr(self,De,TEW,REW):
        """
        Calcualtes vaporation reduction coefficient
        
        Kr is the dimensionless evaporation reduction coefficient dependent on the soil 
        water depletion (cumulative depth of evaporation) from the topsoil layer.
        
        @type De: double
        @param De:  Cumulative depth of evaporation (depletion) from the soil surface layer at the end of the previos day in [mm].
        @type TEW: double
        @param TEW: Total evaporable water in [mm] 
        @type param: double
        @param param: cumulative depth of evaporation (depletion) at the end of stage 1 (REW = readily evaporable water)in [mm].
        @rtype: double
        @return: Dimensionless evaporation reduction coefficient in [-].
        """
        if De > REW:
            return (TEW-De)/(TEW-REW)
        else:
            return 1.
    def calc_few(self,fc,fw=1.):#fw=1. - precipitation
        """
        Calculates fraction of the soil that is both exposed and wetted.
        
        fc and fw: [0.01 - 1], for precipitation fw = 1.0
        
        @type fc: double
        @param gc: Effective fraction of soil surface covered by vegetation in [-].
        @type fw: double
        @param fw: Average fraction of soil surface wetted by irrigation or precipitation in [-].
        @rtype: double
        @return: Fraction of the soil that is both exposed and wetted in [-].
        """
        return min(1-fc,fw)
    def calc_fc_dynamic(self,Kcb,Kcmax,h,Kcmin=0.15):#
        """ 
        Dynamic calculates effective fraction of soil surface covered by vegetation.
        
        This equation should be used with caution and validated from field observations.
        
        Kcmin=0.15 - annual crops under nearly bare soil condition
        
        @type Kcb: double
        @param Kcb: Basal crop coefficient in [mm].
        @type Kcmax: double
        @param Kcmax: Maximum value of Kc following rain or irrigation in [-].
        @type h: double
        @param h: mean maximum plant height during the period of calculation (initial, development, mid-season, or late-season) in [m].
        @type Kcmin: double
        @param Kcmin: Minimum Kc for dry bare soil with no ground cover [0.15 - 0.20] in [-].
        @rtype: double
        @return: Effective fraction of soil surface covered by vegetation in [-].
        """
        return ((Kcb-Kcmin)/(Kcmax-Kcmin))**(1+0.5*h) 
    def calc_fc_static(self,thermaltime,seasons):
        """
        Calculates effective fraction of soil surface covered by vegetation.
        
        
        The value for fc is limited to < 0.99. The user should assume appropriate values
        for the various growth stages. 
        Typical values for fc :
        Season    fc
        1        0.0-0.1
        2        0.1-0.8
        3        0.8-1.
        4        0.2-0.8
        
        @type thermaltime: double
        @param thermaltime: Thermaltime in [degreedays].
        @type seasons: list
        @param seasons: List with the length of the four development seasons in [degreedays].
        @rtype: double
        @return: Effective fraction of soil surface covered by vegetation in [-].
        """
        if thermaltime <= seasons[0]: return 0.1 
        elif thermaltime <= seasons[0]+seasons[1]: return 0.8#
        elif thermaltime <= seasons[0]+seasons[1]+seasons[2]:return 1.
        else: return 0.8
class Water_FAO:
    """
    Simple water uptake model which computes water uptake under stressed condtionins.
    
    The model calculates plant water uptake under water stress
    conditon. Plant water demand equals the potential transpiration.
    If the soil cannot satisfy these demand, stress occurs and 
    the potential transpiration is reduced to the actual water uptake.
    The reduction facro through water stress is computed in realtion
    to "Crop evapotranspiration - Guidelines for computing crop 
    water requirements - FAO Irrigation and drainage paper 56".
    All equations and concepts implenented in this class are taken 
    from these approach.
    
    Implementation
    ==============
    WAter_FAO must be implemented wit ha crop specific stress
    coefficiant, which can be taken from the guidelines.
    
    Call signature
    ==============
    Water_FAO calculates the wateruptake under stressed pr no stressed
    conditions for a given soilprofile or rootingzone.
    
    @see: [Allen et al, 1998]
    """
    def __init__(self,average_available_soilwater=0.5):
        """
        Returns a Water_FAO instance.
        
        @type average_available_soilwater: double
        @param average_available_soilwater:  fraction of TAW that a crop can extract from the root zone without suffering water stress in [-].
        @rtype: water_fao
        @return: WAter_FAO instance
        """
        #Constant variables
        self.p = average_available_soilwater
        #State variables
        self.ks=0.
        self.uptake = 0.
    @property
    def Uptake(self):
        """
        Returns water uptake understressed conditions.
        
        @rtype: list
        @return: Water uptake under stressed conditions for each layer in the soil profile in [mm].
        """
        return self.uptake
    def __call__(self,ETo,Ke,Kcb,TAW,Dr,soillayer):
        """
        Calculates actual water uptake and contributes the uptake over the layer in the soil profile.
        
        @type ETo: double
        @param ETo: Reference Evapotranspiration in [mm].
        @type Kcb: double
        @param Kcb: Basal crop coefficient (Kcb) in [-].
        @type Ke: double
        @type Ke: Evaporation coefficiant in [-].
        @type TAW: double
        @param TAW: Total available soil water in the root zone in [mm].
        @type Dr: double
        @param Dr: Root zone depletion in [mm].
        @type soillayer: list
        @param soillayer: List with soillayer in the rootingzone over which the transpiration is contributed.
        @return: -
        
        @todo: what is soillayer?
        """
        # Calculates Readidly avaible water RAW
        RAW = TAW * self.adjust_p(self.p, ETo)
        #Calcualtes stres coefficiant
        self.ks = self.calc_Ks(TAW, Dr, RAW, self.p)
        #Calculates actual water uptake and contributes the uptake over the layer in the soil profile
        self.uptake = [Eto * (self.ks * Kcb + Ke)/len(soillayer) for l in soillayer]
    def calc_Ks(self,TAW,Dr,RAW,p):
        """ 
        Calculates transpiration reduction factor
        
        Water content in me root zone can also be expressed by root zone depletion,
        Dr, i.e., water shortage relative to field capacity. At field capacity, the root 
        zone depletion is zero (Dr = 0). When soil water is extracted by evapotranspiration, 
        the depletion increases and stress will be induced when Dr becomes equal to RAW. After 
        the root zone depletion exceeds RAW (the water content drops below the threshold q t), 
        the root zone depletion is high enough to limit evapotranspiration to less than potential 
        values and the crop evapotranspiration begins to decrease in proportion to the amount of 
        water remaining in the root zone.
        
        @type TAW: double
        @param TAW: Total available soil water in the root zone in [mm].
        @type Dr: double
        @param Dr: Root zone depletion in [mm].
        @type RAW: double
        @param RAW: Readily available soil water in the root zone in [mm].
        @type p: double
        @param p: Fraction of TAW that a crop can extract from the root zone without suffering water stress in [-].
        @rtype: double
        @return: Transpiration reduction factor dependent on available soil water in [-].
        
        When the root zone depletion is smaller than RAW, Ks = 1
        """
        return (TAW-Dr)/((1-p)*TAW) if Dr > RAW else 1.
    def adjust_p(self,p_table,ETc):
        """ 
        Adjust extractable soil water without stress.
        
        p is Fraction of TAW that a crop can extract from the root zone without 
        suffering water stress. The values for p apply for ETc 5 mm/day can be 
        adjusted with the daily ETc. 
    
        @type p_table: double
        @param p_table: Fraction of TAW that a crop can extract from the root zone without suffering water stress in [-].
        @type ETc: double
        @param ETc: Crop specific evapotranspiration in [mm].
        @rtype: double
        @return: Adjusted extractable soil water in [-].
        """
        return p_table + 0.04*(5-ETc)
class Water_Feddes:
    """
    Water uptake model based on soil matrixpotential and a crop specific uptake function.
    
    The water uptake is limited througt a sink therm variable alpha.
    This value vary with the water pressure head in the soil layer. 
    Alpha is a dimensonless factor between zero and one. The factor 
    limits water uptake due to the wilting point and oxygen dificiency.
    Alpha is determinded with four threshold values for the pressure head
    (h1-oxygen deficiency,h-4 wiliting point, h2 and h3 -optimal conditons). 
    Values for the parameters vary with the crop.  
    
    Water stress in a soil layer can bee compensated from other soil layer.
    This compensation is a empirical distribution from stressed soil layer
    in less stressed soil layers. Compensation is limited to the actual 
    uptake multiplied with the maxcomp parameter. Maxcomp is a user value.
    
    
    Implementation
    ==============
    Water_Feddes must be implementeed with the maxcom parameter,
    which is defined from the user.
    
    Call signature
    ==============
    Water_feddes calculates the water uptake under stress conditions
    and calculates the compensation therm.    
    
    @see: [Feddes et al, 1978, Feddes & Raats 2004]
    """
    def __init__(self,maxcomp=2.):
        """
        Returns a Water_Feddes instance.
        
        @type maxcomp: double
        @param maxcomp: Maximal compensation capacity factor in [-].
        @rtype: water_feddes
        @return: Water_Feddes instance
        """
        #Constant variables
        self.max_compensation_capacity=maxcomp
        #State variables
        self.Sh=[]
        self.alpha=[]
        self.compensation=[]
        self.Shcomp=[]
    @property
    def Uptake(self):
        """
        Returns actual water extraction under non optimal conditions Sh
        
        @rtype: list
        @return: List with under non optimal conditions values for each layer in the rootingzone in [mm].
        """
        return self.Sh
    @property
    def Alpha(self):
        """
        Returns water stress coefficiant alpha.
        @rtype: list
        @return: List with alpha  values for each layer in the rootingzone in [-].
        """
        return self.alpha
    def __call__(self,s_p,pressurehead,h_threshold):
        """
        Calulates water uptake under stressed conditions and compensation.
        
        @type s_p: list
        @param s_p: List with the potential water uptake for each soillayer in rootingzone in [mm].
        @type pressurehead: list
        @param pressurehead: List with the soil pressurehead for each soillayer in rootingzone in [cm].
        @type h_threshold: list
        @param h_threshold: List with soil pressurehead. These conditions limiting wate uptake in. [cm water column].
        @return: -
        """
        #Compute the actual water extraction sh under non optimal conditions 
        self.Sh =[s * self.sink_term(pressurehead[i], h_threshold)for i,s in enumerate(s_p)]
        #Compute stress therm alpha
        self.alpha = [self.sink_term(m,h_threshold)for m in pressurehead]
        #Compute compensation
        self.compensation = self.compensate(self.Sh,s_p,pressurehead, self.alpha, h_threshold[2],
                                               self.max_compensation_capacity)
        #Compute new copmensated uptake
        self.Shcomp=[s_h + self.compensation[i] for i,s_h in enumerate(self.Sh)]
    def compensate(self,Sh,Sp,pressurehead,alpha,maxopth,maxcomp):
        """
        Calculates compensation factors for each layer in the rootingzone.
        
        Compensation capacity = (Actual uptake- Potential uptake) * maxcom
        
        @type s_p: list
        @param s_p: List with the potential water uptake for each soillayer in rootingzone in [mm].
        @type s_h: list
        @param s_h: List with the actual water uptake for each soillayer in rootingzone in [mm].
        @type pressurehead: list
        @param pressurehead: List with the soil pressurehead for each soillayer in rootingzone in [cm].
        @type alpha: list
        @param alpha: Prescribed crop specific function of soil water pressure head with values between or equal zero and one in [-].
        @type maxcomp: double
        @param maxcomp: Maximal compensation capacity factor in [-].
        @type maxopth: double
        @param maxopth: Plant pressure head until water uptake can occur without stress in [cm water column].
        @rtype: list
        @return: List with the compensated uptake in [mm].
        """
        #Remaining alpha of the less stress soil layer
        remaining_alpha= [max(1-(m/maxopth),0.) for i,m in enumerate(pressurehead)] 
        #Remaining uptake capacity of the soillayer
        remaining_uptake=sum(Sp)-sum(Sh)
        #Returns list with the compensation values in mm
        return [min(r/sum(remaining_alpha)*remaining_uptake,maxcomp*Sh[i])for i,r in enumerate(remaining_alpha)]     
    def sink_term(self,h_soil,h_plant): 
        """
        Computes sink term alpha.
        
        @type h_soil: list
        @param h_soil: List with soil pressurehead for each layer in [cm water column].
        @type h_plant: list
        @param h_plant: List with soil pressurehead. These conditions limiting wate uptake in. [cm water column].
        @rtype: list
        @return: Prescribed crop specific function of soil water pressure head with values between or equal zero and one in [-].
        
        @todo: Literatur beschreiben und verweisen.
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err
    def soil_values(self,soil,depth):
        """
        Returns a method to interfere with the soil interface over the plant instance.
        
        @type soil: soil
        @param soil: Soil object from the plant interface soil.
        @type depth: double
        @param depth: Actual depth for the request in [cm].
        @rtype: method
        @return: Function for getting required soil values.
        """
        return soil.get_pressurehead(depth)
class Biomass_LOG:
    """
    Calculates plant growth based on a logistical growth function.
    
    Growth is simulated with a logistic growth function The amount of biomass 
    in per time step depends on a crop specific growth coefficiant
    multiplied with the total biomass. A capacity limit limits 
    the growth. The growthrate for a timestep is given by the following equation.
    
    Implementation
    ==============
    Biomass_LOG must be implemented with specific values
    for limiting maximal biomass and a growthfactor.
    
    Call signature
    ==============
    Biomass_LOG must be called with the actual time step and stress
    coefficiant.
    
    @see: [J.H.M. Thornley & Johnson 1990]
    """
    def __init__(self,capacitylimit,growthfactor):
        """
        Returns a Biomass_LOG instance.
        
        @type capacitylimit: double
        @param capacitylimit: Maximal plant biomass in [g]. 
        @type growthfactor: double
        @param growthfactor: Growth facor of the plant in [g biomass day-1].
        @rtype: biomass_log
        @return: Biomass_LOG instance
        """
        #Constant variables
        self.capacitylimit=capacitylimit
        self.growthfactor=growthfactor
        #State variables
        self.total=1.
        self.stress=0.
    @property
    def PotentialGrowth(self):
        """
        Return potential growth without stress.
        
        @rtype: double
        @return: Potential growth in [g biomass day-1].
        """ 
        return self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit)
    @property
    def ActualGrowth(self):
        """
        Return actual growth influenced by water and nitorgen stress.
        
        @rtype: double
        @return: Actual growth in [g biomass day-1].
        """ 
        return self.PotentialGrowth * self.stress
    @property
    def Total(self):
        """
        Return total biomass.
        
        @rtype: double
        @return: Total biomass in [g].
        """ 
        return self.total
    def __call__(self,stress,step):
        """
        Calculats total plant biomass under stressed conditions.
        
        @type stress: double
        @param stress: Parameter for water and nitrogen stress between 0 - 1. in [-].
        @type step: double
        @param step: Time of the actual intervall.
        @return: -
        """
        self.stress=stress
        self.total = self.total + self.logarithmic_growth(self.total, self.growthfactor, self.capacitylimit) * stress * step
    def logarithmic_growth(self,total_biomass,growthfactor,capacitylimit):
        """
        Return growthrate from a logarithmic growht function.
        
        Calculates the growthrare of a logarithmic growth function.
        
        @type total_biomass: double
        @param total_biomass: Total bioamss of the plant in [g].
        @type capacitylimit: double
        @param capacitylimit: Maximal plant biomass in [g]. 
        @type growthfactor: double
        @param growthfactor: Growth facor of the plant in [g biomass day-1].
        @rtype: double
        @return: Growhtrate in [g biomass day-1].
        """
        return total_biomass * growthfactor * (1- total_biomass / capacitylimit)
    def atmosphere_values(self,atmosphere,time_act):
        """
        @todo: set method for getting atmosphere values
        """
        pass
    def senescence(self):
        """
        @todo: calculate senescenes
        """
        pass
class Biomass_LUE:
    """
    Calculates biomass growth with the radiation use efficiency concept.
    
    Calculates the daily biomass gorwht form a crop specific
    radiatiion use efficiency and the daily incoming absorbed
    photosynthetic active radiation (aPAR). aPAR depnds on the
    plant leaf area index and a dimensionless distinction
    coefficiant.
    
    Implementation
    ==============
    Biomass_LUE must be implemented wit hthe crop specific paramters
    for the LUE-concept.
    
    Call signature
    ==============
    Plant must be calles with crop and environmental factors.
    
    @todo: besser beschreiben
    """
    def __init__(self,RUE,k):
        """
        Returns a Biomass_LUE instance.
        
        @type RUE: double
        @param RUE: Radiation use efficiency [g m-1 day-1]
        @type k: double
        @param k: Canopy extinction coefficient in [-].
        @rtype: biomass_lue
        @return: Biomass_LUE instance
        """
        #Constant variables
        self.rue=RUE
        self.k=k
        #State variables
        self.total=0.
        self.growthrate=0.
        self.stress=0.
    @property
    def PotentialGrowth(self):
        """
        Return potential growth without stress.
        
        @rtype: double
        @return: Potential growth in [g biomass day-1].
        """ 
        return self.growthrate
    @property
    def ActualGrowth(self):
        """
        Return actual growth influenced by water and nitorgen stress.
        
        @rtype: double
        @return: Actual growth in [g biomass day-1].
        """ 
        return self.growthrate * self.stress
    @property
    def Total(self):
        """
        Return actual growth influenced by water and nitorgen stress.
        
        @rtype: double
        @return: Actual growth in [g biomass day-1].
        """ 
        return self.total
    def __call__(self,time_act,stress,Rs,LAI):
        """
        Calcultes the stressed and unstressed growth of the plant.
        
        @type time_act: datetime
        @param time_act: Actual time in [DD,MM,JJJ].
        @type Rs: double
        @param Rs: total solar radiation [MJ m-2 day-1].
        @type stress: double
        @param stress: Parameter for water and nitrogen stress between 0 - 1. in [-].
        @type LAI: double
        @param LAI: Leaf area index of the plant in [m2 m-2].
        @param Rs: total solar radiation [MJ m-2 day-1].
        @type stress: double
        """
        self.stress=stress
        self.growthrate = self.PAR_a(Rs, self.intercept(LAI, self.k))* self.rue
        self.total = self.total + self.growthrate *stress
    def PAR_a(self,Rs,interception):
        """ 
        Returns PARa
        
        Canopy photosynthesis is closely related to the photosynthetically active (400 to 700 mm)
        absorbed radiation (PARa) by green tissue in the canopy.
        
        @type Rs: double
        @param Rs: total solar radiation [MJ m-2 day-1].
        @type interception: double
        @param interception: Fraction of total solar radiation flux, which is intercepted by the crop in [-].
        
        The values 0.5 is the fraction of total solar energy, which is photosynthetically active interception - 
        fraction of total solar radiation flux, which is intercepted by the crop
        The value 0.9 is the fraction of radiation absorbed by the crop  allowing for a 6 percent 
        albedo and for inactive radiation absorption
        @rtype: double
        @return: photosynthetically active absorbed radiation in [].????
        @todo: neu beschreiben
        """
        return Rs*0.5*0.9*(1-interception)
    def intercept(self,LAI,k):
        """
        Returns crop interception.
        
        anopy extinction coefficient in wheat crops ranges
        from 0.3 to 0.7 and is highly dependent on leaf angle
        (low K for erect leaves). From equation 3, it can be calculated that
        95 percent PAR interception requires a LAI as high as 7.5 for erect 
        leaves but a LAI of only about 4.0 for more horizontal leaves
        
        @type LAI: double
        @param LAI: Leaf area index of the plant in [m2 m-2].
        @type k: double
        @param k: Canopy extinction coefficient in [-].
        """
        return exp(-k*LAI)
    def atmosphere_values(self,atmosphere,time_act):
        """
        Returns a method to interfere with the atmosphere interface over the plant instance.
        
        @type atmosphere: atmosphere
        @param atmosphere: Atmosphere object from the plant interface soil.
        @type time_act: datetime
        @param time_act: Actual time in [DD,MM,JJJ].
        @rtype: method
        @return: Function for getting required atmosphere values.
        """
        return atmosphere.get_Rs(time_act)
class Nitrogen:
    """
    Calculates nitrogen uptake from the soil.
    
    The concepts for nitrogen uptake is taken from.The root 
    nitrogen uptake is divided into active and passive uptake. 
    Aktive uptake will occure, if passive uptake cannot satisfy 
    the demand. The passive uptake in each soil layer pa depends 
    on the soil water extraction sh and a maximum allowed solution 
    concetration cmax which can be taken up by plant roots. Low 
    values or zero inhibit passive nitrogen uptake. This can be 
    important for other nutrients which can be taken up only active.
    
    The potential active uptake from each soil layer is calculated with 
    the Michaelis-Menten function. This function descirbes the relationship 
    between influx and its concentration at the root surface. For that, the 
    crop specific Mechaelis Menten Constant Km, the minimum concentration cmin 
    at which can net influx occurr and the soil nitrogen concentration nutrientc  
    is needed
    
    Implementation
    ==============
    Nitrogen msut be impleneted withthe paramter
    for the michaelis menten equation.
    
    Call signature
    ==============
    Must be calles with water uptake, the plant nitrogen demand  
    and the nitrogen concentration in the soil.
    
    @see: [Simunek & Hopmans 2009]
    """
    def __init__(self,Km=0.,NO3_min=0.):
        """
        Returns a Biomass_LOG instance.
        
        @type Km: double
        @param Km: Maximal plant biomass in [g]. 
        @type NO3_min: double
        @param NO3_min: Growth facor of the plant in [g biomass day-1].
        @rtype: nitrogen
        @return: Nitrogen instance
        
        @todo: einheiten fuer alles!!!!!!!!!
        """
        #Constant variables
        self.Km=Km
        self.NO3min=NO3_min
        #State variables
        self.Pa=[]
        self.Aa=[]
    @property
    def Active(self):
        """
        Returns active nitrogen uptake.
        
        @rtype: double
        @return: Active nitrogen uptake.
        """
        return self.Aa
    @property
    def Passvie(self):
        """
        Returns passive nitrogen uptake.
        
        @rtype: double
        @return: Passive nitrogen uptake.
        """
        return self.Pa
    @property
    def Total(self):
        """
        Returns total nitrogen uptake.
        
        @rtype: double
        @return: Total nitrogen uptake.
        """
        return [a + self.Pa[i] for i,a in enumerate(self.Aa)]
    def __call__(self,NO3_conc,Sh,Rp,rootzone):
        """
        Calculates active and passive nitrogen uptake
        
        @type NO3_conc: list
        @param NO3_conc: NO3 concnetrations in rootzone.
        @type Sh: list
        @param Sh: Plant water uptake from the rootzone in [mm].
        @type Rp: list
        @param Rp: Potential nutrient demand of the plant in [g].
        @type rootzone: list
        @param rootzone: Layer from the plant rootingzone.
        @return: -
        """
        #Passive uptake
        self.Pa = [w*NO3_conc[i] for i,w in enumerate(Sh)]
        #Residual demand
        Ap = max(Rp-sum(self.Pa),0.)
        #distribution of residual demand over rootingzone
        ap = Ap/sum(rootzone)
        #Michelis-menten values for each layer
        michaelis_menten = [(n-self.NO3min)/(self.Km+n-self.NO3min) for n in NO3_conc]
        #Active uptake
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
        
        