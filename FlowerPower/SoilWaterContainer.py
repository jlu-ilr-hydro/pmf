class SWC:
    """ 
    Soil water calculates a daily water balance.
    
    The root zone can be presented by means of a container in
    which the water content may fluctuate. To express the water
    content as root zone depletion is useful. It makes the adding
    and subtracting of losses and gains straightforward as the various
    parameters of the soil water budget are usually expressed in terms
    of water depth. Rainfall, irrigation and capillary rise of groundwater
    towards the root zone add water to the root zone and decrease the root
    zone depletion. Soil evaporation, crop transpiration and percolation
    losses remove water from the root zone and increase the depletion.
    This concept is taken from the "Crop evapotranspiration - Guidelines 
    for computing crop water requirements - FAO Irrigation and drainage 
    paper 56 ". 

    Implementation
    ==============
    SWC is implemented with the sand and clay fractions from the
    soil. SWC calculates the usda soiltype, the water cocntent at
    field capacity and the water content at wilting point. 
    
    
    related total thermaltime for each dtage.
    
    Call signature
    ==============
    Call development calculates thermaltime.
    
    @see: [Allen et al, 1998]
    """
    def __init__(self,fc=.3,wp=.17,rew=8.,initial_Zr=0.1,Ze=0.1):
        """
        Returns a SWC instance from a soil  particle size distribution.
        
        @param rew: Cumulative depth of evaporation (depletion) at the end of stage 1 (REW = readily evaporable water) [mm]
        @type  rew: double
        @type initital_Zr: double
        @param initial_Zr: Initial rooting depth in [m].
        @type Ze: double
        @param param: Effective depth of the soil evaporation layer in [m].
        @type fc: double 
        @param fc: Water content at field capacity in [m3 m-3].
        @type wp: double 
        @param wp: Water content at wilting point in [m3 m-3].
        
        
        @rtype: swc
        @return: SWC instance.
        """        
        #Water content at fieldcapacity and wiltingpoint
        self.fc=fc
        self.wp=wp
        
        #effective depth of the soil evaporation layer, of 0.10-0.15 m is recommended
        self.ze=Ze
        
        #Cumulative depth of evaporation (depletion) at the end of stage 1 (REW = readily evaporable water) in [mm].
        self.rew = rew
        #total evaporable water
        self.tew = self.calc_TEW(self.fc, self.wp, self.ze)
        
        #State variables
        #Initial depletion = total evaporable water
        self.de = self.tew
        
        #Initial root zone depletion 
        self.dr = 0.        
        
        #Dimensionless evaporation reduction coefficient
        self.kr=0.
       
        #total available water in the root zone
        self.TAW = 0.
        
        #fraction of soil surface wetted by irrigation or precipitation; fw = 1. for pcp
        self.fw = 1. 
    @property
    def Dr(self):
        """
        Returns Root zone depletion at the end of day.
        
        @rtype: double
        @return: Root zone depletion at the end of day in [mm]. 
        """
        return self.dr
    
    def Kr(self):
        """
        Returns evaporation reduction coefficient.
        
        @rtype: double
        @return: Revaporation reduction coefficient in [-].
        """
        return self.kr
    @property
    def TAW(self):
        """
        Returns total available soil water in the root zone.
        
        @rtype: double
        @return: Total available soil water in the root zone in [mm].
        """
        return self.TAW
    def get_nutrients(self,depth):
        return 100000
    def __call__(self,ETc,evaporation,rainfall,Zr,runoff=0.,irrigation=0.,capillarrise=0.):
        """
        Calculates Root zone depletion Dr, total available soil water TAW, 
        cumulative depth of evaporation De and the evaporation reduction coefficient Kr. 
        
        The values for runoff and capillarrise are zero.
        
        @type ETc: double
        @param ETc: i crop evapotranspiration on day in [mm],
        @type evaporation: double
        @param evaporation: Evaporation in [mm],
        @type rainfall: double
        @param rainfall:  Rainfall in [-].
        @type Zr: double
        @param Zr:  Rooting depth in [m].
        @type fc:double 
        @param fc: File cover in [-].
        @type runoff: double
        @param runoff: Runoff from the soil surface on day in [mm],
        @type irrigation: double
        @param irrigation: net irrigation depth on day i that infiltrates the soil in [mm] 
        @type capillarrise: double
        @param capillarrise: capillary rise from the groundwater table on day in [mm],
        
        @return: -
        """
        #Root zone depletion
        self.dr = self.calc_WaterBalance(self.dr, rainfall, runoff, irrigation, capillarrise, ETc)
        #Total available soil watet
        self.TAW = self.calc_TAW(self.fc, self.wp, Zr)
        
        #Cumulative depth of evaporation
        self.de = max(self.de-rainfall,0)
        self.de =  self.calc_EvaporationLayer(self.de, rainfall, runoff, irrigation, self.fw, evaporation)
        #Evaporation reduction coefficient
        self.kr = self.calc_Kr(self.de, self.tew, self.rew)
    def soilprofile(self):
        return [200]
    def calc_EvaporationLayer(self,de,P,RO,I,fw,E,Tew=0.):
        """
        Returns the cumulative depth of evaporation.
        
        The estimation of Ke in the calculation procedure requires a 
        daily water balance computation for the surface soil layer for
        the calculation of the cumulative evaporation or depletion from 
        the wet condition.
        
        Following heavy rain or irrigation, the soil water content in the topsoil 
        (Ze layer) might exceed field capacity. However, in this simple procedure it is 
        assumed that the soil water content is at q FC nearly immediately following a 
        complete wetting event. As long as the soil water content in the 
        evaporation layer is below field capacity (i.e., De, i > 0), 
        the soil will not drain and DPe, i = 0. 
        
        @type De: double
        @param De: Cumulative depth of evaporation in [mm]
        @type P: double
        @param P: Precipitation on day in [mm]
        @type RO: double
        @param RO: Precipitation run off from the soil surface on day in [mm],
        @type I: double 
        @param I: Irrigation depth on day i that infiltrates the soil in [mm]
        @type fw: double 
        @param fw: Fraction of soil surface wetted by irrigation in [-],
        @type E: double
        @param E: Evaporation in [mm],
        @type Tew: double
        @param Tew: Depth of transpiration from the exposed and wetted fraction of the soil surface layer on day in [mm].
        
        @rtype: double
        @return: Cumulative depth of evaporation (depletion) following complete wetting at the end of the day in [mm]
        """
        #DPe:
        DPe = max(P + I/fw - de,0)
        #De:
        return de-(P-RO)-(I/fw)+E+Tew+DPe
    def calc_TAW(self,FC,WP,Zr):
        """ 
        Returns total available water in the root zone.
        
        The total available water in the root zone is the difference 
        between the water content at field capacity and wilting point.
        TAW is the amount of water that a crop can extract from its root zone,
        and its magnitude depends on the type of soil and the rooting depth
        
        @type FC: double 
        @param FC: Water content at field capacity in [m3 m-3].
        @type WP: double 
        @param WP: Water content at wilting point in [m3 m-3].
        @type Zr: double 
        @param Zr: Rooting depth in [m] 
        
        @rtype: double
        @return: Total available soil water in the root zone in [mm].
        """
        return 1000*(FC-WP)*Zr
    def calc_RAW(self,p,TAW):
        """ 
        Returns he readily available soil water in the root zone.
        
        The fraction of TAW that a crop can extract from the root zone 
        without suffering water stress is the readily available soil water.
        
        The factor p differs from one crop to another. The factor p normally varies 
        from 0.30 for shallow rooted plants at high rates of ETc (> 8 mm d-1) to 0.70
        for deep rooted plants at low rates of ETc (< 3 mm d-1). A value of 0.50 for 
        p is commonly used for many crops.  
          
        @type p: double
        @param p: Average fraction of Total Available Soil Water (TAW) that can be depleted from the root zone before moisture stress (reduction in ET) occurs in [-].
        @type TAW: double
        @param TAW: Total available soil water in the root zone in [mm].
        
        @rtype: double
        @return: Readily available soil water in [mm].
        """
        return p*TAW
    def calc_WaterBalance(self,Dr,P,RO,I,CR,ETc):
        """ 
        Returns root zone depletion at the end of day.
        
        The root zone can be presented by means of a container in which the water 
        content may fluctuate. To express the water content as root zone depletion 
        is useful. It makes the adding and subtracting of losses and gains straightforward 
        as the various parameters of the soil water budget are usually expressed in terms of 
        water depth. Rainfall, irrigation and capillary rise of groundwater towards the root 
        zone add water to the root zone and decrease the root zone depletion. Soil evaporation, 
        crop transpiration and percolation losses remove water from the root zone and increase 
        the depletion.
        
        By assuming that the root zone is at field capacity following heavy rain or 
        irrigation, the minimum value for the depletion Dr is zero. At that moment no water is 
        left for evapotranspiration in the root zone, Ks becomes zero, and the root zone 
        depletion has reached its maximum value TAW.
        
        Following heavy rain or irrigation, the soil water content in the root zone might 
        exceed field capacity. In this simple procedure it is assumed that the soil water content 
        is at q FC within the same day of the wetting event, so that the depletion Dr 
        becomes zero. Therefore, following heavy rain or irrigation.
            
        @type Dr: double
        @param Dr: Water content in the root zone at the end of the previous day in [mm].
        @type P: double
        @param P: precipitation on day i [mm],
        @type RO: double
        @param RO: runoff from the soil surface on day i [mm],
        @type I: double
        @param I: net irrigation depth on day i that infiltrates the soil [mm],
        @type CR: double
        @param CR: capillary rise from the groundwater table on day i [mm],
        @type ETc: double
        @param ETc: crop evapotranspiration on day i [mm],
        
        @rtype: double
        @return: Root zone depletion at the end of day in [mm].
        """
        return Dr - (P-RO) - I - CR + ETc + max(P - RO + I - ETc - Dr,0)
    def calc_InitialDepletion(self,FC,q,Zr):
        """ 
        Returns initial depletion.
        
        To initiate the water balance for the root zone, the initial depletion Dr, i-1 should 
        be estimated.Where q i-1 is the average soil water content for the effective root zone. 
        Following heavy rain or irrigation, the user can assume that the root zone is near field capacity, 
        i.e., Dr, i-1  0
        
         @type FC: double 
        @param FC: Water content at field capacity in [m3 m-3].
        @type q: double
        @param q: Average soil water content for the effective root zone in [-].
        @type Zr: double
        @param Zr: Initial rooting depth in [-].
        
        @rtype: double
        @return: Initial depletion in [mm].
        """
        return 1000*(FC-q)*Zr
    def calc_soilproperties(self,sand,clay):
        """ 
        Returns volumetric water content theta for fieldcapacity and wiltingpoint.
        
        @type sand: double
        @param sand: Sand fraction in the soilprofile in [-].
        @type clay: double
        @param clay: Clay fraction in the soilprofile in [-].
        
        @rtype: list
        @return: List with volumetric water content for FC and WP in [m3 m-3].
            
        Soil type                    Theta [m3/m3]
                            FC            WP            FC - WP
            sand            0.07 - 0.17 0.02 - 0.07 0.05 - 0.11 
        @todo: water content ausrechen, momentan noch feste werte  
        """
        return [0.17,0.07]
    def calc_Kr(self,De,TEW,REW):
        """
        Returns evaporation reduction coefficient.
        
        Kr is the dimensionless evaporation reduction coefficient dependent on the soil 
        water depletion (cumulative depth of evaporation) from the topsoil layer.
        
        @type De: double
        @param De: Cumulative depth of evaporation in [mm]
        @type TEW: double
        @param TEW: Depth of transpiration from the exposed and wetted fraction of the soil surface layer on day in [mm].
        @type REW: double
        @param REW: Cumulative depth of evaporation (depletion) at the end of stage 1 (REW = readily evaporable water) in [mm].
        
        @rtype: double
        @return: Evaporation reduction coefficient in [-].
        """
        if De > REW:
            return (TEW-De)/(TEW-REW)
        else:
            return 1.
    def calc_TEW(self,FC,WP,Ze):
        """
        Returns total evaporable water.
        
        TEW total evaporable water = maximum depth of water 
        that can be evaporated from the soil when the topsoil
        has been initially completely wetted [mm],
        
        @type FC: double
        @param FC:soil water content at field capacity [m3 m-3] 
        @type WP: double
        @param WP: oil water content at wilting point [m3 m-3]
        @type Ze: double
        @param Ze: Depth of the surface soil layer that is subject to drying by way of evaporation in [m].
       
        @rtype: double
        @return: Total evaporable water in [mm].
        """
        return 1000*(FC-0.5*WP)*Ze   
    def calc_REW(self,soiltype='Sand'):
        """ 
        Return REW cumulative depth of evaporation.
        
        The cumulative depth of evaporation, De, at the end of stage 1 
        drying is REW (Readily evaporable water, which is the maximum 
        depth of water that can be evaporated from the topsoil layer 
        without restriction during stage 1). The depth normally ranges
        from 5 to 12 mm and is generally highest for medium and fine 
        textured soils.
            
        @type soiltype: string
        @param soiltype: USDA soil type.
        
        @rtype: double
        @return: Return REW cumulative depth of evaporation in [mm].
        """
        return 7. #sand 2-7 mm
    def soiltype(self,sand,clay):
        """
        Returns usda soiltype.
        
        @type sand: double
        @param sand: Sand fraction in the soilprofile in [-].
        @type clay: double
        @param clay: Clay fraction in the soilprofile in [-].
        
        @rtype: string
        @return: USDA soil type.
        
        @todo: Calculation of soil type from sand and clay fraction.
        """
        return 'Sand'
    
