# -*- coding: utf-8 -*-
"""
PlantModel.py holds the physical plant structure. The structure elements 
are hold from PlantModel.Plant.py. Plant.py consists of root, shoot, stem,
leaf and storage organs. These components hold the growth state variables. 
Plant.py abstractly connects the growth processes and interacts with the 
environmental models.

:author: Sebastian Multsch

:version: 0.1 (26.10.2010)

:copyright: 
 This program is free software; you can redistribute it and/or modify it under  
 the terms of the GNU General Public License as published by the Free Software  
 Foundation; either version 3 of the License, or (at your option) any later 
 version. This program is distributed in the hope that it will be useful, 
 but WITHOUT ANY  WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or  FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
 more details. You should have received a copy of the GNU General 
 Public License along  with this program;
 if not, see <http://www.gnu.org/licenses/>.
 
:summary:Physical plant structure 
"""
#import pylab as pylab
import PMF
import CropDatabase
import numpy as np
class Plant:
    """
    Plant functioning as interacting platform. It holds the plant components, 
    connects the process modules and interacts with the environmental models.
    
    Implementation
    ==============
    The implementation includes the connection to the environmental models
    and the definition of the process modules. 
    The module PMF.makePlant.py holds methods for the implementation 
    with process modules from PMF.PorcessLibrary.py. The required 
    modules are as follows:
      - Two environmental interfaces:
        - Soil (water balance data)
        - Atmosphere (meteorological data)
      - Six process modules:
        - Biomass (calculates biomass accumulation)
        - DevelopmentStage (calculates development)
        - Water (calculates water stress term)
        - ET (calculates potential transpiration)
        - Nitrogen (calculates nitrogen uptake)
        - Layer (calculates rooting zone)
        
    Attributes with default values represent crop specific properties. All 
    default values refer to cereals. 

    Call signature
    ==============
    The call includes the actual time, the timestep and the intervall. Plant 
    calculates the growth processes with the process modules for the given
    time periode.
    
    :summary: Plant connects the plant components, holds the process modules and
      interacts with the environmental models
    """ 
    Count=0   
    def __init__(self,et,water,biomass,net_radiation,interception,development,nitrogen,layer,
                 FRDR,stem_specific_factor,stem_growth_max,max_height,CO2_ring,max_depth,
                 root_growth,leaf_specific_weight,tbase,fact_sen,         
                 shoot_percent, 
                 root_percent,                
                 leaf_percent, 
                 stem_percent,
                 storage_percent,
                 plantN,
                 pressure_threshold,# corn: [15.,30.,325.,15000.]  wheat: [0.,1.,500.,16000.], pasture: [10.,25.,200.,8000.]
                 stress_adaption=1.,
                 carbonfraction=.4,
                 soil=None,atmosphere=None):                                   
        """        
        The implementation of plant requires six process modules, two 
        environmental interfaces and the specification of several crop specific 
        properties. The default values of the properties refer to cereals.
        
        :type  soil: soil
        :param soil: Interface to water balance data.
        :type  atmosphere: atmosphere
        :param atmosphere: Interface to meteorological data.
        
        :type  et: et
        :param et: Calculates potential transpiration and evaporation.
        :type  water: water
        :param water: Calculates water stress term in relation to the soil water
        status and crop specific response.
        :type  biomass: biomass
        :param biomass: Calculates potential and actual biomass accumulation.
        :type  developmentstage: developmentstage
        :param developmentstage: Calculates development status.
        :type  interception: evaporation of interception
        :param interception: Calculates evaporation of interception.       
        :type  nitrogen: nitrogen
        :param nitrogen: Calculates nitrogen uptake.
        :type layer: layer
        :param layer: Calculates rooting zone.        
        
        :type  root_percent: list
        :param root_percent: List with partitioning coefficiants for each 
        development as fraction from the plant biomass in [-].
        :type  shoot_percent: list
        :param shoot_percent: List with partitioning coefficiants for each 
        development as fraction from the plant biomass in [-].
        :type  leaf_percent: list
        :param leaf_percent: List with partitioning coefficiants for each 
        development as fraction from the plant biomass in [-].
        :type  stem_percent: list
        :param stem_percent: List with partitioning coefficiants for each 
        development as fraction from the plant biomass in [-].
        :type  storage_percent: list
        :param storage_percent: List with partitioning coefficiants for each 
        development as fraction from the plant biomass in [-].
        
        :type tbase: double
        :param tbase: Minimum temperature above growth can take place in [°C].
        :type pressure_threshold: list
        :param pressure_threshold: List with pressurehead values. These values 
        describe the limiting conditions due to soil water conditions
        in [cm water column].
        :type plantN: list
        :param plantN: List with plant nitrogen fractions in relation to
        thermaltime in [-] and [°days].        
        :type leaf_specific_weight: double
        :param leaf_specific_weight: Specific leaf weight in [g m-2].
        :type root_growth: double
        :param root_growth: Root elongation factor [cm day-1].
        :type stem_growth_shape_double
        :param stem_growth_shape: Shaping factor for logistic growth of stem [-]
        :type max_height : double
        :param max_height : Maximum crop height [m].
        :type stress_adaption: double
        :param stress_adaption: Modifies the stress influences on biomass
        accumulation (one = full stress) [-].
        :type carbonfraction: double
        :param carbonfraction: Fractional carboncontent [-].
        :type max_depth: double
        :param max_depth: Maximal rooting depth in [cm].
        :type fact_sen: double
        :param fact_sen: factor to adjust senescence rate after maturity
        :type FRDR: double
        :param FRDR: factor changing shape of senescence function [-] 
        
        :rtype:   Plant
        :return:  Plant instance
        
        :summary: Returns a plant instance
        """

        #Raise Count variable for each plant instance
        self.Count+=1
        
        #Constant variables
        self.plantN=plantN
        self.tbase=tbase
        self.pressure_threshold=pressure_threshold
        self.stress_adaption=stress_adaption
        self.carbonfraction=carbonfraction
        self.stem_specific_factor=stem_specific_factor
        self.max_height = max_height  
        self.CO2_ring = CO2_ring
        
        self.stem_growth_max = stem_growth_max
    
      
        #Handing over environmental interfaces
        self.soil=soil
        self.atmosphere=atmosphere
        
        #Handing over growth process related interfaces
        #Interfaces holds state variables for each process as properties
        self.water=water
        self.biomass=biomass
        self.developmentstage=development
        self.et=et
        self.nitrogen=nitrogen
        self.net_radiation=net_radiation
        self.interception=interception
        self.FRDR = FRDR

       
        #Implementation of root and shoot class
        self.root=Root(self,root_percent,root_growth,max_depth,layer)
        self.shoot=Shoot(self,leaf_specific_weight,fact_sen,self.FRDR,self.developmentstage[4][1],
                         shoot_percent,leaf_percent,stem_percent,storage_percent,
                         self.stem_specific_factor,self.tbase,self.stem_growth_max,self.max_height,
                         elongation_end=self.developmentstage[3][1],
                         thermaltime_maturity=self.developmentstage[-1][1])        #FRDR          
#        self.net_radiation = Net_Radiation()
        
        #State variables
        self.stress = 0.
        self.water_stress = 0.
        self.nutrition_stress = 0.
        self.Rp = 0.
        self.Wateruptake = []
        
        
    @property
    def Waterstress(self):
        """
        Returns daily waterstress value.
        The value ranges between 0 and 1.
        
        :rtype: double
        :return: Water stress [-].
        """ 
        return self.water_stress   
    @property
    def ShootNitrogen(self):
        """
        Returns actual nitrogen content of the above ground biomass.
        
        :rtype: double
        :return: Above ground biomass nitrogen content in [g].
        """ 
        return self.shoot.Wtot * self.NO3cont(self.plantN, self.developmentstage.Thermaltime)
    @property
    def RootNitrogen(self):
        """
        Returns actual nitrogen content of the under ground biomass.
        
        :rtype: double
        :return: Under ground biomass nitrogen content in [g].
        """ 
        return self.root.Wtot * self.NO3cont(self.plantN, self.developmentstage.Thermaltime)
    @property
    def LeafNitrogen(self):
        """
        Returns actual nitrogen content of the leafs.
        
        :rtype: double
        :return: Leaf nitrogen content in [g].
        """ 
        return self.shoot.leaf.Wtot * self.NO3cont(self.plantN, self.developmentstage.Thermaltime)
    @property
    def StemNitrogen(self):
        """
        Returns actual nitrogen content of the stem.
        
        :rtype: double
        :return: Stem nitrogen content in [g].
        """ 
        return self.shoot.stem.Wtot * self.NO3cont(self.plantN, self.developmentstage.Thermaltime)
    @property
    def StorageNitrogen(self):
        """
        Returns actual nitrogen content of the storage organs.
        
	:rtype: double
        :return: Storage organs nitrogen content in [g].
        """ 
        return self.shoot.storage_organs.Wtot * self.NO3cont(self.plantN, self.developmentstage.Thermaltime)
    @property
    def ShootCarbon(self):
        """
        Returns actual carbon content of the above ground biomass.
        
        :rtype: double
        :return: Above ground biomass carbon content in [g].
        """ 
        return self.shoot.Wtot * self.carbonfraction
    @property
    def RootCarbon(self):
        """
        Returns actual carbon content of the under ground biomass.
        
        :rtype: double
        :return: Under ground biomass carbon content in [g].
        """ 
        return self.root.Wtot * self.carbonfraction
    @property
    def LeafCarbon(self):
        """
        Returns actual carbon content of the leafs.
        
        :rtype: double
        :return: Leaf carbon content in [g].
        """ 
        return self.shoot.leaf.Wtot * self.carbonfraction
    @property
    def StemCarbon(self):
        """
        Returns actual carbon content of the stem.
        
        :rtype: double
        :return: Stem carbon content in [g].
        """ 
        return self.shoot.stem.Wtot * self.carbonfraction
    @property
    def StorageCarbon(self):
        """
        Returns actual carbon content of the storage organs.
        
        :rtype: double
        :return: Storage organs carbon content in [g].
        """ 
        return self.shoot.storage_organs.Wtot * self.carbonfraction

    def set_soil(self,soil):
        """
        Connects the plant to the soil interface and sets the soil specific 
        values of the plant components and process modules.
        
        :type  soil: soil
        :param soil: Interface to water balance data.
        
        :return: -
        :summary: Connects plant to the soil interface.
        """
        self.soil=soil
        self.root.zone.get_rootingzone(self.soil.soilprofile())
        self.root.branching = [0. for l in self.root.zone]
        self.root.root_death = [0. for l in self.root.zone]
        self.root.actual_distribution= [0. for l in self.root.zone]
        self.water.layercount = len(self.root.zone)
        self.water.waterbalance=soil
        self.water.plant=self
        self.Wateruptake = [0. for l in self.root.zone]
        if self.nitrogen:
            self.nitrogen.layercount = len(self.root.zone)
    def set_atmosphere(self,atmosphere):
        """
        Connects the plant to the atmosphere interface.
        
        :type  atmosphere: atmosphere
        :param atmosphere: Interface to meteorological data.
        
        :return: -
        :summary: Connects the plant to the atmosphere interface.
        """
        self.atmosphere = atmosphere
    def __del__(self):
        """
        Decrease class variable Plant.Count about one.
        
        :return: -
        """
        Plant.Count-=1
    def __call__(self,day_of_simulation,time_act,step,interval):
        """
        Call plant initiate the growth process for a given time periode.
        The start of the processes is related to the development stage.
        Development and Evapotranspiration are calculated in every time step.
        Water uptake, nutrient uptake  and transpiration after germination. 
        Bioamss accumulation and partitioning takes places
        during the growing season.
        
        :type time_act: datetime(JJJJ,MM,DD)
        :param time_act: Actual time in [JJJJ,MM,DD]. 
        :type step: string
        :param step: Defines the running step. Can be 'day' or 'hour'.
        :type interval: double
        :param interval: Duration of the simulation step.
        
        :return: -
        
        :summary: Calculates the actual growth status.
        
        :todo: vegH equals at the first day of growth zero: ZeroDivisionError.
        The recent solution is very bad ( max(0.01,self.shoot.stem.height))
        """
        
        #Set time step
        time_step = 1. * interval if step == 'day' else 1./24. * interval
        #compute actual rooting zone with actual rooting depth
        #Rootingzone consists of all layers, which are penetrated from the plant root
        self.root.zone(self.root.depth)
        biomass_distribution = [biomass/sum(self.root.branching) for biomass in self.root.branching] if sum(self.root.branching)>0 else np.zeros(len(self.root.branching)) 
        if sum(biomass_distribution)==0: biomass_distribution[0]+=1
        #Development
        self.developmentstage(time_step,self.atmosphere.get_tmin(time_act), self.atmosphere.get_tmax(time_act), self.tbase, self.atmosphere.get_daylength(time_act), self.atmosphere.get_tmean(time_act)) 
        #Evapotranspiration
#        Kr = self.soil.Kr()
        thermaltime = self.developmentstage.Thermaltime

        # calls the class net radiation        
        self.net_radiation(self.atmosphere.get_tmax(time_act),self.atmosphere.get_tmin(time_act),self.atmosphere.get_ea(time_act),self.atmosphere.get_Rs(time_act),self.atmosphere.get_Rs_clearsky(time_act),self.shoot.leaf.LAI)
        
        # stem growth        
        veg_H = self.shoot.stem.height_biomass
        
        T = self.atmosphere.get_tmean(time_act)
        e_s = self.atmosphere.get_es(time_act)
        e_a = self.atmosphere.get_ea(time_act)
        windspeed = self.atmosphere.get_windspeed(time_act)
        precipi = self.atmosphere.get_rainfall(time_act)
        LAI_leaf = self.shoot.leaf.LAI
        Rnet = self.net_radiation.calc_R_n(self.net_radiation.R_n_s,self.net_radiation.R_n_l)
        Rsn = self.net_radiation.calc_R_s_n(self.net_radiation.R_n,self.net_radiation.interception)   
        Cr = self.net_radiation.Cr
        self.Rs = self.atmosphere.get_Rs(time_act)
        
        self.day_of_simulation = day_of_simulation
        self.soilprofile = self.atmosphere.soilprofile()
               
#        CO2_measured = self.atmosphere.get_CO2_measured(time_act)    
        
#        Rn = self.atmosphere.get_Rn(time_act,0.12,True)
#        Tpot = self.et(Kr,thermaltime,Rn,T,e_s,e_a,windspeed,LAI)     #ET_FAO

#        Tmin = self.atmosphere.get_tmin(time_act)
#        Tmax = self.atmosphere.get_tmax(time_act)
#        Rs = self.atmosphere.get_Rs(time_act)
#        Rs_clearsky = self.atmosphere.get_Rs_clearsky(time_act)
#        Tpot = self.et(T,Tmax,Tmin,Rs,Rs_clearsky,e_s,e_a,windspeed,LAI,veg_H)           #ET_Shuttleworth and Wallace


#        Tpot = self.et(T,Rnet,Rsn,e_s,e_a,windspeed,LAI_leaf,veg_H,CO2_measured)   #returns the potential transpiration according to Shuttleworth-Wallace
        Tpot = self.et(T,Rnet,Rsn,e_s,e_a,windspeed,LAI_leaf,veg_H,self.biomass.measured_CO2(self.atmosphere,time_act))
        ET_Intercept = self.interception(T,Rnet,Rsn,e_s,e_a,windspeed,LAI_leaf,veg_H,precipi)
            #ET_Shuttleworth-Wallace mit Rn und Rsn aus PlantModel (unten)     
        if self.developmentstage.IsGerminated:
            #Water uptake
            s_p = [Tpot*biomass for biomass in biomass_distribution]  # mm * %   ... s_p =  potential water uptake from each layer, biomass_distribution Wert zwischen 0 und 1 über das soil profile aufsummiert = 1
            rootzone = [l.center for l in self.root.zone]
            alpha = self.water(rootzone)  #wasserstressfaktor
            s_h = [s * alpha[i] for i,s in enumerate(s_p)]
            self.Wateruptake = s_h
            
            #pressurehead = [self.waterbalance.get_pressurehead(z) for z in rootzone]
            #s_h_comp = self.water.compensate(s_h,s_p,pressurehead,alpha,maxopth,2.) 
            
            
            #Nutrient uptake
            NO3content=self.NO3cont(self.plantN, self.developmentstage.Thermaltime)
            self.Rp=self.NO3dem(self.biomass.PotentialGrowth, NO3content)
            self.nitrogen([self.soil.get_nitrogen(l.center) for l in self.root.zone],
                              s_h, self.Rp,biomass_distribution)  
        if self.developmentstage.IsGrowingseason:
            self.water_stress = max(0, 1 - sum(s_h) / Tpot*self.stress_adaption)
            self.nutrition_stress = max(0, 1 - sum(self.nitrogen.Total)/ self.Rp * self.stress_adaption if self.Rp>0 else 0.0)
            self.stress = min(max(self.water_stress, self.nutrition_stress),1)
            #Calls biomass interface for the calculation of the actual biomass                                                  ## CO2 neu eingefügt  ####
            self.biomass(time_step,self.stress,self.Rs,self.net_radiation.calc_interception(LAI_leaf,Cr),self.shoot.leaf.LAI,self.biomass.measured_CO2(self.atmosphere,time_act),self.shoot.leaf.senesced_leafmass)            
            #Root partitining
            if self.developmentstage.Thermaltime <= self.developmentstage[4][1]:
                                
                physical_constraints = self.water([self.root.depth])[0]
                
                Sh = sum(s_h)
                Ra = sum(self.nitrogen.Total)
                Rp=self.Rp
                NO3dis = [self.soil.get_nitrogen(l.center) if l.penetration>0 else 0. for l in self.root.zone]
                H2Odis = [alpha[i]  if l.penetration>0 else 0. for i,l in enumerate(self.root.zone)]
                fgi = self.get_fgi(Sh, Tpot, Ra, Rp, NO3dis, H2Odis)
                
                root_biomass = self.root.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth
                vertical_root_growth_stress = self.stress
                physical_constraints = self.water([self.root.depth])[0]
                self.root(self.soilprofile,self.day_of_simulation,time_step,fgi,root_biomass,vertical_root_growth_stress,physical_constraints)
            #Shoot partitioning
            self.shoot(time_step,(self.shoot.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.leaf.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.stem.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       (self.shoot.storage_organs.percent[self.developmentstage.StageIndex] * self.biomass.ActualGrowth),
                       self.developmentstage.Thermaltime,self.developmentstage.rate,self.stress)
            #biomass turnover / leave senescence
            # senescence rate actual time step
            shootWtot_before =self.shoot.Wtot            
            self.shoot.Wtot -=  self.shoot.leaf.senesced_leafmass           
            shootWtot_after =self.shoot.Wtot
               
            if shootWtot_after<0.:
                print 'shootWtot_before', shootWtot_before
                print 'shootWtot_after', shootWtot_after   


        else: self.biomass.growthrate = 0.0
  
         
    def get_fgi(self,Sh,Tpot,Ra,Rp,NO3dis,H2Odis):
        """
        Returns the FeelingGoodIndex (fgi) for given distribtuion of water
        and nitrogen in the rootingzone. The fgi is a list with allocation
        coefficient for the root bioamss for each layer in the rootingzone. 
        The coefficients range between zero and one. The sum of all 
        coefficients for one is one (100%). 
        
        :type Sh: list
        :param Sh: Total actual water uptake in [mm].
        :type Tpot: double
        :param Tpot: Potential transpiration in [mm].
        :type Ra: list
        :param Ra: Total actual nitrogen uptake in [g].
        :type Rp: double
        :param Rp: Nitrogen demand of the plant in [g].
        :type NO3dis: list
        :param NO3dis: Nitrogen conditions in each layer of the rootingzone.
        :type H2Odis: list
        :param H2Odis: Water conditions in each layer of the rootingzone.
        
        :rtype: list
        :return: Distribution coefficiants for the root biomass.
        
        :summary: Calculates root biomass distribution coeffciants.
        """
        #Compute stress index for nitrogen and water
        w=1-Sh/Tpot
        n=1-(Ra/Rp) if Rp>0. else 0.
        #Return list for the factor with the higher stress index
        H2Odis_sum=sum(H2Odis)
        if H2Odis_sum<=0: 
            H2Odis_sum=1 
        NO3dis_sum=sum(NO3dis)
        if NO3dis_sum<=0: 
            NO3dis_sum=1 
        if  w >= n:
            return [h2o/H2Odis_sum for h2o in H2Odis]
        else:
            return [n/NO3dis_sum for n in NO3dis]
    def respire(self,g_resp,Wact,m_resp,Wtot):
        """
        Returns the respiration for a given total biomass
        and growthrate. Both parameter are multiplied with
        adjustment coefficiants. The product from growthrate and g_resp is
        the growth respiration, the product of total bioamss
        and m_resp the maintenance respiration.
        
        :type Wact: double
        :param Wact: Actual growthrate in [g day-1].
        :type Wtot: double
        :param Wtot: Total biomass in [g].
        :type g_resp: double
        :param g_resp: Adjustment coefficiant for growth respiration in [-].
        :type m_resp: double
        :param m_resp: Adjustment coefficiant for maintenance respiration
        in [-].
        
        :rtype: double
        :return: Respiration
        
        :summary: Calculates respiration.
        """
        return g_resp*Wact+m_resp*Wtot
    def NO3cont(self,plantN,thermaltime):
        """
        The calculation depends on the development. The nitrogen content
        before emergence and after maturity doesn't change. For thermal
        time values between this stages the nitrogen content decreases
        linear from emergence to maturity.
        
        :param plantN: List with plant nitrogen fractions in relation to
        thermaltime in [-] and [°days].
        :type thermaltime: double
        :param thermaltime: Thermaltime in [°days].
        
        :rtype: double
        :return: Nitrogen fraction of the plant biomass in [-].
        
        :summary: Calculates fractional nitrogen content.
        """
        if thermaltime<=plantN[0][0]: return plantN[0][1]
        elif thermaltime>=plantN[1][0]: return plantN[1][1]
        else: return plantN[0][1]+(plantN[1][1]-plantN[0][1])/(plantN[1][0]-plantN[0][0])*(thermaltime-plantN[0][0])
    def NO3dem(self,Wpot,NO3conc):
        """
        Returns the nitrogen demand of the plant from the
        potential growthrate and the actual nitrogen content
        of the biomass.
        
        :type Wpot: double
        :param Wpot: Potential growthrate in [g day-1]
        :type NO3conc: double
        :param NO3conc: Actual nitrogen fraction of the biomass in [-].
        
        :rtype: double
        :return: Nitrogen demand in [g]
        
        :summary: Calculates nitrogen demand.
        """
        return Wpot*NO3conc
    def sink_term(self,h_soil,h_plant): 
        """
        Calculates the crop response due to the soil water conditions.
        
        :type h_soil: list
        :param h_soil: Pressurehead from each soil layer in [cm water column].
        :type h_plant: list
        :param h_plant: List with pressurehead values. These values 
        describe the limiting conditions due to soil water conditions
        in [cm water column].
        
        :rtype: list
        :return: Response value due to soil water conditions between zero 
        and one in [-].
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err
class Root:
    """  
    Root represents the underground biomass. Root growth is divided into
    vertical (elongation) growth and biomass distribution (branching). The 
    resulting root system is specific for each crop type. 
    
    Implementation
    ==============
    Root is implemented from PlantModel.Plant.py. The specification 
    values refer to a vertical growth rate, a maximum root depth and the
    biomass fraction, which is allocated to the root. In addition to the crop
    specific paramters a layer object is required, which represents the rooting
    zone. 
    
    Call signature
    ==============
    Root calculates the actual rootingzone with a biomass distribution index and
    the elongation rate. A stress values limits root growth through drought or
    nutrient stress. Physical contraints retrict vertical growth. These refer to 
    water stress, oxygen defenciency and penetration resistance. The actual
    setup includes water stress influences.
    
    @summary: Represent the underground plant components.
    """
    def __init__(self,plant,percent,root_growth,max_depth,layer):
        """
        Returns a root instance and creates a rootingzone from the soilprofile.
        
        :type plant: plant
        :param plant: Plant class, which owns root.
        :type  root_percent: list
        :param root_percent: List with partitioning coefficiants for each 
        developmentstage as fraction from the plant biomass in [-].
        :type root_growth: double
        :param root_growth: Root elongation factor in [cm day-1]
        :type layer: layer
        :param layer: Calculates rooting zone.

        :rtype: root
        :return: Root instance
        """
        #Root is part from plant
        self.plant=plant
        
        #Constant variables
        self.elong=root_growth
        self.percent=percent
        self.max_depth=max_depth
        #State variables updated in every timestep
        #Rootingdepth
        self.depth=1.
        #Root biomass
        self.Wtot=0.
        self.growth = 0.
        #Rootingzone
        self.zone=layer
        #Biomass allocation over the rootingzone
        self.potential_depth=0.
        self.branching=[0. for l in self.zone]
        self.root_death=[0. for l in self.zone]
        
        self.actual_distribution = [0. for l in self.zone]
        self.fgi = [0. for l in self.zone]
        

        
        
    def __call__(self,soilprofile,day_of_simulation,step,fgi,biomass,stress,physical_constraints):
        """
        Root calculates the actual rootingdepth and allocates
        the biomass between the layers in the rootingzone. The vertical growth
        is restricted due to the water conditions at actual depth and drought
        stress influences on the whole plant. 
        
        
        :type layerdepth_percent: list
        :param layerdepth_percent: Percentage of  mass of each layer related to entire soil profile. Value between 0 and 1. 
        :type physical_constraints: double
        :param physical_constraints: Resistance of the soil against root 
        penetration in [-].
        :type step: double
        :param step: Time step of the run period.
        :type fgi: list
        :param fgi: Biomass distribution values for each layer in [-].
        :type stress: double
        :param stress: Stress index from plant drought/nitrogen stress 
        (0 optimal, 1 worst conditions) in [-].
        """
        
        
        #Calculate actual rooting depth, restricted by plant stress and soil resistance 
        self.potential_depth = self.potential_depth + self.elong
        self.depth=self.depth+self.elong*physical_constraints*(1-stress)*step
        if self.depth>self.max_depth:
            self.depth=self.max_depth
            
        # exponential equ. for root allocation over depth
        # Taking into account changing layer thickness with depth
        self.soilprofile = soilprofile
        cum_sum =  [1./np.exp((b/100.)*5.5) for i,b in enumerate(self.soilprofile)]
        # amount of root allocation per layer 
        self.biomass_percent_per_layer = []
        for i,b in enumerate(cum_sum):
            if i == 0:
                self.biomass_percent_per_layer.append(1.- cum_sum[i])
            else:
                self.biomass_percent_per_layer.append(cum_sum[i-1]-cum_sum[i])
        self.biomass_income_per_layer = [biomass*layer_percent for i,layer_percent in enumerate(self.biomass_percent_per_layer)]
        #Allocate actual growth between the layers in the rooting zone 
        self.root_allocation=self.allocate(self.branching, self.biomass_income_per_layer, fgi,self.soilprofile)
        self.root_death = self.root_decay(self.branching)
#        print 'root decay', self.root_death

        #Calculate total biomass  
        every_7th_day = day_of_simulation % 7
        if every_7th_day == 0:
            self.branching=[self.root_allocation[i] - self.root_death[i] for i in range(len(self.root_allocation))]
            self.Wtot = self.Wtot + biomass - 0.1 * self.Wtot 
        else:
            self.branching=self.root_allocation
            self.Wtot = self.Wtot + biomass
#    
        
    def allocate(self,distr,biomass,fgi,layerlepth,k_shape=0.05):
        """        
        Allocates biomass over the rooting zone in realtion to a distribution
        index fgi (FeelingGoodIndex).
        
        :type distr: list
        :param distr: Total biomass allocation over the rootingzone in [g]. 
        :type biomass: double
        :param biomass: Actual root growthrate in [g day-1]
        :type fgi: list
        :param fgi: Biomass distribution values for each layer in [-].

        :rtype: list
        :return: List with the total biomass in each layer in the rootingzone 
        in [g].
        
        :summary: Returns the biomass distribution over the rootingzone.
        """
#        return [b+(np.exp(layerlepth[i]*k_shape*-1)*biomass[i]) for i,b in enumerate(distr)]
#        return [b+(biomass[i]*fgi[i]) for i,b in enumerate(distr)]
        return [b+biomass[i] for i,b in enumerate(distr)]

    def root_decay(self,distr):
        """
        Calculates root decay for each layer [g]
        
        :type distr: list
        :param distr: Total biomass allocation over the rootingzone in [g]. 
        :rtype: list
        :return: List with the dead biomass in each layer in the rootingzone 
        in [g].

        """        
        return [b*0.1 for i,b in enumerate(distr)]

    
class Shoot:
    """    
    Shoot is a part from plant and represents the above
    ground biomass. This biomass is diveded into leaf,
    stem and storage organs. The allocation between these
    parts is determined by the development. The partitioning
    rules are input values from the user.
    
    Implementation
    ==============
    Shoot is implemented from the plant class. Shoot for
    it self implements leaf, stem and storageorgans.

    Call signature
    ==============
    Shoot growth includes the biomass accumulation of the 
    above ground biomass and the allocation to the other
    above ground parts.
    
    :summary: Allocates aboveground biomass to leaf, stem and storage organs.
    """
    def __init__(self,plant,leaf_specific_weight,fact_sen,FRDR,thermaltime_anthesis,
                 shoot_percent,leaf_percent,stem_percent,storage_percent,
                 stem_specific_factor,t_base,stem_growth_rate_max,max_height,
                 elongation_end,thermaltime_maturity):    #FRDR new
        """
        Returns shoot instance. Shoot implements leaf, stem and storageorgans.
        
        :type plant: plant
        :param plant: Plant instance which owns shoot.
        :type leaf_specific_weight: double
        :param leaf_specific_weight: Specific leaf weight in [g m-2].
        :type thermaltime_anthesis: double
        :param thermaltime_anthesis: Accumulative thermaltime at anthesis 
        in [°days].
        :type  shoot_percent: list
        :param shoot_percent: List with partitioning coefficiants for each
        developmentstage as fraction from the plant biomass in [-].
        :type  leaf_percent: list
        :param leaf_percent: List with partitioning coefficiants for each
        developmentstage as fraction from the plant biomass in [-].
        :type  stem_percent: list
        :param stem_percent: List with partitioning coefficiants for each
        developmentstage as fraction from the plant biomass in [-].
        :type  storage_percent: list
        :param storage_percent: List with partitioning coefficiants for
        each developmentstage as fraction from the plant biomass in [-].
        
        :rtype: shoot
        :return: shoot instance
        """
        #Shoot is part from plant
        self.plant=plant
        #Constant values
        self.percent=shoot_percent
        leaf = [leaf_percent[i]*percent for i,percent in enumerate(self.percent)]
        stem = [stem_percent[i]*percent for i,percent in enumerate(self.percent)]
        storage = [storage_percent[i]*percent for i,percent in enumerate(self.percent)]
        #Shoot owns leaf, stem and storage_organs
        self.leaf=Leaf(self,leaf,leaf_specific_weight,thermaltime_anthesis,thermaltime_maturity,fact_sen,FRDR)    # FRDR new, weil hier leaf aufgerufen wird
        self.stem=Stem(self,stem,stem_specific_factor,t_base,stem_growth_rate_max,max_height,elongation_end)
        self.storage_organs=Storage_Organs(self,storage)
        #State variables updated in every time step
        #total biomass
        self.Wtot=0.
        
    @property
    def Wleaf_1(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.Wleaf_1
        
    @property
    def Wstem_1(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.Wstem_1
        
    @property
    def Wstorage_1(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.Wstorage_1
                
    @property
    def biomass_1(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.biomass_1
                        
        
    def __call__(self,step,biomass,Wleaf,Wstem,Wstorage,thermaltime,tt_rate,water_stress):
        """
        Shoot calculates the actual above ground biomass and allocates
        these biomass between the above ground plant organs.
        
        :type step: double
        :param step: Time step of the actual model period in [days or hours].
        :type biomass: double
        :param biomass: Growthrate of the above ground biomass in [g m-2].
        :type Wleaf: double
        :param Wleaf: Growthrate of the leaf biomass in [g m-2].
        :type Wstem: double
        :param Wstem: Growthrate of the stem biomass in [g m-2].
        :type Wstorage: double
        :param Wstorage: Growthrate of the storage biomass in [g m-2].
        :type thermaltime: double
        :param thermaltime: Thermaltime in [°days].
        """
        #Calculate actual total aboveground biomass
        self.Wtot=self.Wtot+biomass*step
        
        
        self.Wleaf_1 = Wleaf
        self.Wstem_1 = Wstem
        self.biomass_1 = biomass
        self.Wstorage_1 = Wstorage
        
        
        #Allocate biomass to above ground plant organs
        #Call leaf with actual thermaltime
        self.leaf(step,Wleaf,thermaltime,tt_rate)
        self.stem(step,Wstem,thermaltime,tt_rate,water_stress)
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
    and calculates the actual stem biomass and plant height.
    """
    def __init__(self,shoot,percent,stem_specific_factor,t_base,stem_growth_rate_max,max_height,elongation_end): 
        """
        Returns stem instance.
        
        :type shoot: shoot
        :param shoot: Shoot instance which holds stem.
        :type percent: list
        :param percent: List with partitioning coefficiants for each 
        developmentstage as fraction from the plant biomass in [-].
        :type elongation_end: double
        :param elongation_end: Total thermaltime at the end of stem elongation
        in  [°days].
        :type max_height: double
        :param max_height: Maximum crop height in [m].
        
        :rtype: stem
        :return: stem instance 
        """
        #Stem is part from shoot
        self.shoot=shoot
        #Constant values
        self.percent=percent
        #State variables updated in every timestep
        #total biomass
        self.Wtot=0.01
        #Plant hight/ stem length
        self.height=0.02
        
#        self.height_ttrate = 0.001
        self.height_biomass = 0.001
#        self.height_tt = 0.001
        
        
#        self.t_base = t_base
#        self.stem_growth_rate_max = stem_growth_rate_max
#      
        self.stem_specific_factor = stem_specific_factor
        self.max_height = max_height
#        self.stem_growth_shape = stem_growth_shape
        self.elongation_end = elongation_end

    @property
    def stemdailygrowth(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.stemdailygrowth
        
    def  __call__(self,step,biomass,thermaltime,tt_rate,water_stress):
        """
        Calculates total stem biomass and plant height.
        
        :type step: double
        :param step: Time step of the actual model period in [days or hours].
        :type biomass: double
        :param biomass: Growthrate of stem biomass in [g m-2].
        :type thermaltime: double
        :param thermaltime: Thermal time in [°days].
        :return: -
        """
        self.stemdailygrowth = biomass        
        self.Wtot=self.Wtot+biomass*step
        
        #height based on rate
#        self.stem_growth =  self.stemgrowth(self.t_base,self.stem_growth_rate_max,self.elongation_end,tt_rate,thermaltime,water_stress)
#        self.height_ttrate = self.height_ttrate + self.stem_growth

        #height absolut
        self.height_biomass = self.stem_height_biomass(self.stem_specific_factor,self.max_height,self.Wtot)
#        self.height = self.stem_height_linear(self.max_height,self.elongation_end,thermaltime)
#        self.height = self.stem_height_log(self.stem_growth_shape,self.max_height,self.elongation_end,thermaltime)
        
    def stemgrowth(self,t_base,stem_growth_rate_max,elongation_end,tt_rate,thermaltime,water_stress):
        """
        Calculates stem growth rate depending on thermaltime and waterstress [m/d].
        
        Stem growth is calculatd as fraction from a crop specific maximal
        stem growth factor per day. That fraction refers to fraction of actual thermal time rate
        from a maximal the total thermaltime at the end of stem elongation stage.
        Stem growth is linear.
        
        :type factor: double
        :param factor:  factor to calculate stem height out of stem biomass []
        :type max_height: double
        :param max_height: Maximum Crop Height in [m].
        :type thermaltime: double
        :param thermaltime: Actual thermal time in [degreedays].
        :type elongation_end: double
        :param elongation_end: Total thermal time at the end of stem elongation [degreedays].
        :type start_height: double
        :param start_height: inital and minimum height of the vegetation [m].
        :rtype: double
        :return: Vertical growth rate depending on development in [m].
        """        
        if thermaltime <= elongation_end:
            tt_rate_max = 26.9 - t_base #[°C], 26.9 is the max reached tt_rate during these 10 years            
            stem_growth =  tt_rate/tt_rate_max * stem_growth_rate_max * water_stress            
        else: stem_growth = 0. #after elongation_end the stem is not growing anymore
        
        return stem_growth        
        
        
    def stem_height_biomass(self,factor,max_height,biomass):
        """
        Calculates crop height from stem biomass considering maximal height and thermaltime.
        
        Plant height is calculatd as fraction from a crop specific maximal
        height. That fraction refers to fraction of actual thermal time
        form the total thermaltime at the end of stem elongation stage.
        Stem growth is linear.
        
        :type factor: double
        :param factor:  factor to calculate stem height out of stem biomass []
        :type max_height: double
        :param max_height: Maximum Crop Height in [m].
        :type biomass: double
        :param biomass: Maximum Crop Height in [m].
        :rtype: double
        :return: Vertical crop height in [m].
        """        
#        if thermaltime <= elongation_end:
#            height = min(biomass/factor, max_height)
#        
#        return height
        return min(biomass/factor, max_height)
        
        
    def stem_height_linear(self,max_height,elongation_end,thermaltime,start_height=0.0001):
        """
        Calculates crop height from maximal height and thermaltime.
        
        Plant height is calculatd as fraction from a crop specific maximal
        height. That fraction refers to fraction of actual thermal time
        form the total thermaltime at the end of stem elongation stage.
        Stem growth is linear.
        
        :type max_height: double
        :param max_height: Maximum Crop Height in [m].
        :type thermaltime: double
        :param thermaltime: Actual thermal time in [degreedays].
        :type elongation_end: double
        :param elongation_end: Total thermal time at the end of stem elongation [degreedays].
        :type start_height: double
        :param start_height: inital and minimum height of the vegetation [m].
        :rtype: double
        :return: Vertical growth rate depending on development in [m].
        """
        return max(start_height, min((thermaltime / elongation_end) * max_height,max_height))


    def stem_height_log(self,stem_growth_shape,max_height,elongation_end,thermaltime,start_height=0.0001):
        """
        Calculates crop height from maximal height and thermaltime.
        
        Plant height is calculatd as fraction from a crop specific maximal
        height. That fraction refers to fraction of actual thermal time
        form the total thermaltime at the end of stem elongation stage.
        Calculation of stem growth accoording to logistic growth.
        
        :type max_height: double
        :param max_height: Maximum Crop Height in [m].
        :type thermaltime: double
        :param thermaltime: Actual thermal time in [degreedays].
        :type elongation_end: double
        :param elongation_end: Total thermal time at the end of stem elongation [degreedays].
        :type start_height: double
        :param start_height: inital and minimum height of the vegetation [m].
        :rtype: double
        :return: Vertical growth rate depending on development in [m].
        """
                
        return max(start_height, max_height*start_height/(start_height + (max_height-start_height)*np.exp(-stem_growth_shape*thermaltime)))
        
        
        
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
        
        :type shoot: shoot
        :param shoot: Shoot instance which holds sotragaorgans.
        :type percent: list
        :param percent: List with partitioning coefficiants for each 
        developmentstage as fraction from the plant biomass in [-].
        :rtype: storage_organs
        :return: storaga_organs instance
        """
        self.shoot=shoot
        #Constant variables
        self.percent=percent
        #State variables updated in every timestep
        #Total biomass
        self.Wtot=0.
        #Yield components
        self.yield_components=0.
        
    @property
    def storagedailygrowth(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.storagedailygrowth

        
        
    def  __call__(self,step,biomass):
        """
        Calculates storageorgans total biomass.
        
        :type step: double
        :param step: Time step of the actual model period in [days or hours].
        :type biomass: double
        :param biomass: Growthrate of storageorgans biomass in [g m-2].
        
        :return: -
        """
        self.storagedailygrowth = biomass
        self.Wtot=self.Wtot+biomass*step

class Leaf:
    """
    Calculates leaf biomass and leaf area index.
    
    Leaf is implemented from the shoot class.
    
    Leaf calculates actual total biomass and the leaf area index with
    the specific leaf weight and a partitioing coefficiant.
    """
    def __init__(self,shoot,percent,leaf_specific_weight,thermaltime_anthesis,ttmaturity,fact_sen,FRDR,min_LAI=0.1):                #FRDR new
        """
        Returns a leaf instance.
        
        :type shoot: shoot
        :param shoot: Shoot instance which holds storageorgans.
        :type percent: list
        :param percent: List with partitioning coefficiants for each 
        developmentstage as fraction from the plant biomass in [-].
        :type leaf_specific_weight: double
        :param leaf_specific_weight: Specific leaf weight in [g m-2].
        weight to leaf area index [g m-2].
        :type thermaltime_anthesis: double
        :param thermaltime_anthesis: Total thermaltime at 
        developmentstage anthesis in [degreedays].
        :type fact_sen: double
        :param fact_sen: factor to adjust senescence rate after maturity 
        :type min_LAI: double
        :param min_LAI: Minimum leaf area index [m2 m-2].
        :rtype: leaf
        :return: leaf instance
        """
        #Part from shoot
        self.shoot=shoot
    
        
        #Constant variables
        self.specific_weight = leaf_specific_weight
        self.ttanthesis = thermaltime_anthesis
        self.ttmaturity = ttmaturity    
        self.percent = percent
        self.fact_sen = fact_sen
        self.FRDR = FRDR     
        self.min_LAI = min_LAI                      # inital value of leaf area index                                                             

        
        #State variables updated in every timestep
#        self.stomatal_resistance=0. #is now calculated in ET-Shuttleworth script
        self.Wtot=0.
        self.leafarea = 0.1       
        self.senesced_leafmass = 0. 
        self.senescence_factor = 0.                            
        
    @property
    def LAI(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.leafarea
    @property
    def senescence_leaf(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.senescence_factor
    @property
    def leafdailygrowth(self):
        """
        Returns leaf area index.
        
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        """
        return self.leafdailygrowth
        
    def  __call__(self,step,biomass,thermaltime,tt_rate):
        """
        Call leaf calculates total leaf biomass and LAI. Additional LAI is
        calculated from the specific leaf weight and leaf biomass.
        
        :type step: double
        :param step: Time step of the actual model period in [days or hours].
        :type biomass: double
        :param biomass: Growthrate of the above ground biomass in [g m-2 d-1].
        :type Wleaf: double
        :type thermaltime: double
        :param thermaltime: Thermaltime in [°days].
        """
        
        self.leafdailygrowth = biomass
        
        #Calculate total biomass
        self.Wtot = self.Wtot + biomass * step
        
       #senescence starting with end of anthesis
        if thermaltime >= self.ttanthesis:
            self.senescence_factor = self.senescence(tt_rate,thermaltime,self.ttmaturity,self.fact_sen,self.FRDR)
        else:
            self.senescence_factor = 0.
#        print thermaltime,sen
        self.senesced_leafmass = self.Wtot * self.senescence_factor
        self.Wtot = self.Wtot - self.senesced_leafmass       
        
        #Calculate LAI with scenscence
#        self.leafarea = 0.1 + self.convert(self.Wtot, self.adj_weigth(thermaltime, self.ttanthesis)*self.specific_weight)
#        self.leafarea = max(self.min_LAI, self.convert(self.Wtot, self.specific_weight))
        self.leafarea = max(self.min_LAI, self.convert(self.Wtot, self.adj_weigth(thermaltime, self.ttanthesis)*self.specific_weight))
   
    def senescence(self,tt_rate,tt_sum,tt_maturity,fact_sen, FRDR):
        """ Calculates the relative senescence rate for leaves [1/d]. Before anthesis no senscence occurs.
        The calculation is based on the concept applied in SUCROS97.
        The aging and linked leave biomass reduction starts at anthesis level (see above).
        Between anthesis and maturity the senescence factor is value between 0 and 1. Reaching the maturity level 
        the senescence rate varies with an adjusted mean temperature (tt_rate/fact_sen).
        Here self.senescence_factor (PMF) equate to RDR (SUCROS97).
        
        :type tt_rate: double
        :param tt_rate: degree day (Tmean - Tbase) [°C days]
        :type tt_maturity: doulbe
        :param tt_maturity: sum of degree days when maturity is reached [°C days]
        :type tt_sum: double
        :param tt_sum: sum of all degree days [°C days]
        :type fact_sen: double
        :param fact_sen: factor to adjust senescence rate 
        :type FRDR: double
        :param FRDR: factor varying senescence rate [-]
        :return: senenscenece 
        :rtype: double
        """
        if tt_maturity - tt_sum > 0.1:
            senesc = tt_rate / ((tt_maturity - tt_sum) * fact_sen) * FRDR
        else:
            senesc = tt_rate / fact_sen * FRDR
           
           #fact_sen 50
           #FRDR 0.5 --> tt_rate * 0.01
        return senesc
#        return 0.

    def convert(self,biomass,specific_weight):
        """ Calculates LeafAreaIndex from leaf biomass and leaf specific weight.
        
        Leaf specific weight is a constant factor. It can be adjusted to the
        actual development stage with the function leaf.adj_weight().
        
        :type biomass: double
        :param biomass: Biomass of leafs in [g m-2].
        :type specific_weight: double
        :param specific_weight: Specific biomass of the leafs in [g m-2].
        :rtype: double
        :return: LeafAreaIndex in [m2 m-2]
        
        :see: [De Vries et al, 1989]
        """
        return biomass/specific_weight             
            
    def adj_weigth(self,thermaltime,tt_anthesis):
        """
        Returns the ajdusted specific weight depending on the plant development.
        
        To adjuste the specific weight to thermaltime the specificd weight
        is multiplied with a weighting factor depending on the development
        stage of the crop. The specific leaf weight of new leaves is 
        calculated by multiplying the specific leaf weight constant with a 
        factor that depends on the development stage of the crop.
        
        
        :type thermaltime: double
        :param thermaltime: Actual thermaltime in [degreedays].
        :type thermaltime_anthesis: double
        :param thermaltime_anthesis: Thermaltime at anthesis in [°days].
        
        """
#        return min((thermaltime/tt_anthesis+0.25),1.)
        return 1.


