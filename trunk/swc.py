class SoilWaterContainer:
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
    def __init__(self,sand=.9,clay=.1,initial_Zr=0.1,Ze=0.1):
        self.sand=sand
        self.clay=clay
        self.silt = max(1-(clay+sand),0.)
        self.soiltype = self.soiltype(self.sand, self.clay, self.silt)
        self.fc=self.calc_soilproperties(self.sand, self.clay)[0]
        self.wp=self.calc_soilproperties(self.sand, self.clay)[1]
        
        #self.calc_InitialDepletion(self.fc, average_available_soilwater, initial_Zr)
        self.dr = 0.
        
        #Where unknown, a value for Ze, the effective depth of the soil evaporation layer, of 0.10-0.15 m is recommended
        self.ze=Ze
        
        self.rew = self.calc_REW(soiltype=self.soiltype)
        self.tew = self.calc_TEW(self.fc, self.wp, self.ze)
        self.kr=0.
        
        #topsoil is near field capacity following a heavy rain or irrigation or 
        #TEW (long period of time has elapsed since the last wetting) 
        self.de = self.tew
        
        self.taw = 0.
        self.fw = 1. #precipition
    @property
    def Dr(self):
        return self.dr
    @property
    def Kr(self):
        return self.kr
    @property
    def taw(self):
        return self.taw
    def __call__(self,ET,ETc,evaporation,rainfall,Zr,fc,runoff=0.,irrigation=0.,capillarrise=0.):
        #Calcultes dr and taw for water stress factor Ks
        self.dr = self.calc_WaterBalance(self.dr, rainfall, runoff, irrigation, capillarrise, ETc)
        self.taw = self.calc_TAW(self.fc, self.wp, Zr)
        
        #Calculate Kr for the evapotranspiration
        self.de = max(self.de-rainfall,0)
        self.de =  self.calc_EvaporationLayer(self.de, rainfall, runoff, irrigation, self.fw, evaporation, fc)
        self.kr = self.calc_Kr(self.de, self.tew, self.rew)
    def calc_EvaporationLayer(self,de,P,RO,I,fw,E,fc,Tew=0.):
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
        DPe - deep percolation loss from the topsoil layer on day i if 
             soil water content exceeds field capacity [mm],
        fw - fraction of 
             soil surface wetted by irrigation [0.01 - 1],
        few- exposed and wetted soil fraction [0.01 - 1]
        
        Deep percolation:
        
            Following heavy rain or irrigation, the soil water content in the topsoil 
            (Ze layer) might exceed field capacity. However, in this simple procedure it is 
            assumed that the soil water content is at q FC nearly immediately following a 
            complete wetting event.
            
            As long as the soil water content in the evaporation layer is below 
            field capacity (i.e., De, i > 0), the soil will not drain and DPe, i = 0. 
        """
        
        DPe = max(P + I/fw - de,0)
        
        #return de-(P-RO)-(I/fw)+(E*(min(1-fc,fw)))+Tew+DPe
        return de-(P-RO)-(I/fw)+E+Tew+DPe
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
    def calc_WaterBalance(self,Dr,P,RO,I,CR,ETc):
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
        
            Depp percolation:
            
            Following heavy rain or irrigation, the soil water content in the root zone might 
            exceed field capacity. In this simple procedure it is assumed that the soil water content 
            is at q FC within the same day of the wetting event, so that the depletion Dr 
            becomes zero. Therefore, following heavy rain or irrigation.
            
            
            The DP calculated for calc_WaterBalance() is independent of the DP calculted in
            calc_De().As long as the soil water content in the root zone is below field 
            capacity (i.e., Dr, i > 0), the soil will not drain and DPi = 0.
        """
        
        DPr = max(P - RO + I - ETc - Dr,0)
        
        return Dr - (P-RO) - I - CR + ETc + DPr
    def calc_InitialDepletion(self,FC,q,Zr):
        """ To initiate the water balance for the root zone, the initial depletion Dr, i-1 should 
        be estimated. 
        
        where q i-1 is the average soil water content for the effective root zone. Following heavy 
        rain or irrigation, the user can assume that the root zone is near field capacity, 
        i.e., Dr, i-1  0
        
        The initial depletion can be derived from measured soil water content by:
        """
        return 1000*(FC-q)*Zr
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
            return 1000*(qFC-0.5*qWP)*Ze   
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
    
