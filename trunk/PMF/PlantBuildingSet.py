"""
Holds functions for plant implementation  

  1. Set Processes from ProcessLibrary (note *1):
    - et = PMF.ET_FAO(kcb_values = [0.15,1.1,0.15],seasons = [160.0, 499.0, 897.0, 1006.0])
    - biomass = PMF.Biomass_LUE(RUE = 3.,k=.4)
    - development = PMF.Development(stage = [['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],['Anthesis',1200.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]])
    - layer = PMF.SoilLayer(soillayer=[10,20,30,40,50,60,100])
    - nitrogen = PMF.Nitrogen(layercount = len(layer))
    - water = PMF.Water_Feddes(layercount = len(layer))


  2. Create plant (note*2,*3):
    - wheat_instance = makePlant(PMF.Plant,et=et,biomass=biomass,development=development,layer=layer,nitrogen=nitrogen,water=water)
    - wheat_classobj = PMF.Plant

  3. Connect plant with soil and amtosphere interface:
    - Loess = Soil()
    - Meteo_Giessen = Atmosphere()
    - connect(wheat_instance,Loess,Meteo_Giessen)
    - connect(wheat_classobj,Loess,Meteo_Giessen,et=et,biomass=biomass,development=development,layer=layer,nitrogen=nitrogen,water=water)

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
"""
import PMF
import CropDatabase
import copy as copy
def clone(plant):
    """
    Returns new insance of plant and the related classes
    with the actual values.
    
    Constructs a new compound object and then, recursively, 
    inserts copies into it of the objects found in the original.
    
    :rtype: PMF.Plant
    :return: New plant instance with same values.
    :see: [http://docs.python.org/library/copy.html, 11.11.2009]
    """
    return copy.deepcopy(plant)
def setProcess(p,**args):
    """
    Returns a process with the given paramter.
    
    :param p: Process class from PMF.ProcessLibrary.py
    :type p: process class
    
    :rtype: process class
    :return: Paramterised process class.
    """
    return p(**args)

def makePlant(plant,**args):
    """
    Returns a plant with the given arguments.
    
    :param plant: plant
    :type plant: Plant instance from PMF.PlantModel.Plant.py.
    
    :rtype: plant
    :return: Plant instance
    """
    return plant(**args)

def connect(plant,soil,atmosphere,**args):
    """
    Connects a plant with environmental interfaces.
    
    :param plant: plant
    :type plant: Plant instance from PMF.PlantModel.Plant.py.
    :type  soil: soil
    :param soil: Interface to water balance data.
    :type  atmosphere: atmosphere
    :param atmosphere: Interface to meteorological data.
    
    :rtype: plant
    :return: Plant instance
    """
    if isinstance(plant,PMF.Plant):
        plant.set_soil(soil)
        plant.set_atmosphere(atmosphere)
        return plant
    else:
        return 'Error: No plant instance'


wheat=CropDatabase.CropCoefficiants_wheat()
c3grass=PMF.CropCoefficiants_c3grass()
c4grass=PMF.CropCoefficiants_c4grass() 

def createPlant_wheat_SWC(**args):                                                    
    """             
    Implements a specific plant setup with summer wheat values.
    """
    print 'wheat'
    et = PMF.ET_ShuttleworthWallace(wheat.w_leafwidth,wheat.z_0w,wheat.z_0g,wheat.z_w,
                                    wheat.r_st_min,wheat.sigma_b,wheat.c_int)
    print 'Evapotranspiration: Shuttleworth-Wallace'
    biomass = PMF.Biomass_LUE_CO2_Soltani(wheat.RUE,wheat.C_0,wheat.factor_b,wheat.CO2_ring)
    print 'Biomass: Light-use-efficiency concept with CO2 response' 
    development = PMF.Development(wheat.stage,wheat.R_p, wheat.R_v, wheat.photo_on_off, wheat.verna_on_off)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    interception = PMF.Intercept_Evapo(wheat.w_leafwidth,wheat.z_0w,wheat.z_0g,wheat.z_w,
                                       wheat.r_st_min,wheat.sigma_b,wheat.c_int)
    net_radiation = PMF.Net_Radiation(wheat.albedo_m,wheat.Cr)
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,
                     interception=interception,net_radiation=net_radiation,water=water,layer=layer,
                     FRDR=wheat.FRDR,max_height=wheat.max_height,CO2_ring=wheat.CO2_ring,max_depth=wheat.max_depth, 
                     root_growth=wheat.root_growth,leaf_specific_weight=wheat.leaf_specific_weight,
                     tbase=wheat.tbase,fact_sen=wheat.fact_sen,**args)


def createPlant_c3grass_SWC(**args):                                                    
    """             
    Implements a specific plant setup with C3 values.
    """
    print 'C3 grass'
    et = PMF.ET_ShuttleworthWallace(c3grass.w_leafwidth,c3grass.z_0w,c3grass.z_0g,c3grass.z_w,
                                    c3grass.r_st_min,c3grass.sigma_b,c3grass.c_int)
    print 'Evapotranspiration: Shuttleworth-Wallace'
    biomass = PMF.Biomass_LUE_CO2_Soltani(c3grass.RUE,c3grass.C_0,c3grass.factor_b, c3grass.CO2_ring)
    print 'Biomass: Light-use-efficiency concept with CO2 response' 
    development = PMF.Development(c3grass.stage,c3grass.R_p,c3grass.R_v, c3grass.photo_on_off, c3grass.verna_on_off)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    interception = PMF.Intercept_Evapo(c3grass.w_leafwidth,c3grass.z_0w,c3grass.z_0g,c3grass.z_w,
                                       c3grass.r_st_min,c3grass.sigma_b,c3grass.c_int)
    net_radiation = PMF.Net_Radiation(c3grass.albedo_m,c3grass.Cr)
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,
                     interception=interception,net_radiation=net_radiation,water=water,layer=layer,
                     FRDR=c3grass.FRDR,max_height=c3grass.max_height,CO2_ring=c3grass.CO2_ring,max_depth=c3grass.max_depth, 
                     root_growth=c3grass.root_growth,leaf_specific_weight=c3grass.leaf_specific_weight,
                     tbase=c3grass.tbase,fact_sen=c3grass.fact_sen,**args)

 
def createPlant_c4grass_SWC(**args):                                                    
    """             
    Implements a specific plant setup with C4 values.
    """
    print 'C4 grass'
    et = PMF.ET_ShuttleworthWallace(c4grass.w_leafwidth,c4grass.z_0w,c4grass.z_0g,c4grass.z_w,
                                    c4grass.r_st_min,c4grass.sigma_b,c4grass.c_int)
    print 'Evapotranspiration: Shuttleworth-Wallace'
    biomass = PMF.Biomass_LUE_CO2_Soltani(c4grass.RUE,c4grass.C_0,c4grass.factor_b,c4grass.CO2_ring)
    print 'Biomass: Light-use-efficiency concept with CO2 response' 
    development = PMF.Development(c4grass.stage,c4grass.R_p,c4grass.R_v, c4grass.photo_on_off, c4grass.verna_on_off)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    interception = PMF.Intercept_Evapo(c4grass.w_leafwidth,c4grass.z_0w,c4grass.z_0g,c4grass.z_w,
                                       c4grass.r_st_min,c4grass.sigma_b,c4grass.c_int)
    net_radiation = PMF.Net_Radiation(c4grass.albedo_m,c4grass.Cr)
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,
                     interception=interception,net_radiation=net_radiation,water=water,layer=layer,
                     FRDR=c4grass.FRDR,max_height=c4grass.max_height,CO2_ring=c4grass.CO2_ring,max_depth=c4grass.max_depth, 
                     root_growth=c4grass.root_growth,leaf_specific_weight=c4grass.leaf_specific_weight,
                     tbase=c4grass.tbase,fact_sen=c4grass.fact_sen,**args)   

def createPlant_wheat_CMF(**args):                                                    
    """             
    Implements a specific plant setup with summer wheat values.
    """
    print 'wheat'
    et = PMF.ET_ShuttleworthWallace(wheat.w_leafwidth,wheat.z_0w,wheat.z_0g,wheat.z_w,
                                    wheat.r_st_min,wheat.sigma_b,wheat.c_int)
    print 'Evapotranspiration: Shuttleworth-Wallace'
    biomass = PMF.Biomass_LUE_CO2_Soltani(wheat.RUE,wheat.C_0,wheat.factor_b,wheat.CO2_ring)
    print 'Biomass: Light-use-efficiency concept with CO2 response' 
    development = PMF.Development(wheat.stage,wheat.R_p, wheat.R_v, wheat.photo_on_off, wheat.verna_on_off)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    interception = PMF.Intercept_Evapo(wheat.w_leafwidth,wheat.z_0w,wheat.z_0g,wheat.z_w,
                                       wheat.r_st_min,wheat.sigma_b,wheat.c_int)
    net_radiation = PMF.Net_Radiation(wheat.albedo_m,wheat.Cr)
    water = PMF.Waterstress_Feddes()
    print 'Waterstress: Feddes'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,
                     interception=interception,net_radiation=net_radiation,water=water,layer=layer,
                     FRDR=wheat.FRDR,max_height=wheat.max_height,CO2_ring=wheat.CO2_ring,max_depth=wheat.max_depth, 
                     root_growth=wheat.root_growth,leaf_specific_weight=wheat.leaf_specific_weight,
                     tbase=wheat.tbase,fact_sen=wheat.fact_sen,**args)


def createPlant_c3grass_CMF(**args):                                                    
    """             
    Implements a specific plant setup with C3 values.
    """
    print 'C3 grass'
    et = PMF.ET_ShuttleworthWallace(c3grass.w_leafwidth,c3grass.z_0w,c3grass.z_0g,c3grass.z_w,
                                    c3grass.r_st_min,c3grass.sigma_b,c3grass.c_int)
    print 'Evapotranspiration: Shuttleworth-Wallace'
    biomass = PMF.Biomass_LUE_CO2_Soltani(c3grass.RUE,c3grass.C_0,c3grass.factor_b, c3grass.CO2_ring)
    print 'Biomass: Light-use-efficiency concept with CO2 response' 
    development = PMF.Development(c3grass.stage,c3grass.R_p,c3grass.R_v, c3grass.photo_on_off, c3grass.verna_on_off)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    interception = PMF.Intercept_Evapo(c3grass.w_leafwidth,c3grass.z_0w,c3grass.z_0g,c3grass.z_w,
                                       c3grass.r_st_min,c3grass.sigma_b,c3grass.c_int)
    net_radiation = PMF.Net_Radiation(c3grass.albedo_m,c3grass.Cr)
    water = PMF.Waterstress_Feddes()
    print 'Waterstress: Feddes'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,
                     interception=interception,net_radiation=net_radiation,water=water,layer=layer,
                     FRDR=c3grass.FRDR,max_height=c3grass.max_height,CO2_ring=c3grass.CO2_ring,max_depth=c3grass.max_depth, 
                     root_growth=c3grass.root_growth,leaf_specific_weight=c3grass.leaf_specific_weight,
                     tbase=c3grass.tbase,fact_sen=c3grass.fact_sen,**args)

 
def createPlant_c4grass_CMF(**args):                                                    
    """             
    Implements a specific plant setup with C4 values.
    """
    print 'C4 grass'
    et = PMF.ET_ShuttleworthWallace(c4grass.w_leafwidth,c4grass.z_0w,c4grass.z_0g,c4grass.z_w,
                                    c4grass.r_st_min,c4grass.sigma_b,c4grass.c_int)
    print 'Evapotranspiration: Shuttleworth-Wallace'
    biomass = PMF.Biomass_LUE_CO2_Soltani(c4grass.RUE,c4grass.C_0,c4grass.factor_b,c4grass.CO2_ring)
    print 'Biomass: Light-use-efficiency concept with CO2 response' 
    development = PMF.Development(c4grass.stage,c4grass.R_p,c4grass.R_v, c4grass.photo_on_off, c4grass.verna_on_off)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    interception = PMF.Intercept_Evapo(c4grass.w_leafwidth,c4grass.z_0w,c4grass.z_0g,c4grass.z_w,
                                       c4grass.r_st_min,c4grass.sigma_b,c4grass.c_int)
    net_radiation = PMF.Net_Radiation(c4grass.albedo_m,c4grass.Cr)
    water = PMF.ProcessLibrary.Waterstress_Feddes()
    print 'Waterstress: Feddes'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,
                     interception=interception,net_radiation=net_radiation,water=water,layer=layer,
                     FRDR=c4grass.FRDR,max_height=c4grass.max_height,CO2_ring=c4grass.CO2_ring,max_depth=c4grass.max_depth, 
                     root_growth=c4grass.root_growth,leaf_specific_weight=c4grass.leaf_specific_weight,
                     tbase=c4grass.tbase,fact_sen=c4grass.fact_sen,**args)   
                     
def createPlant_CMF(**args):                                                    
    """
    Implements a specific plant setup with summer wheat values.
    """
    et = PMF.ET_FAO(kcb_values = wheat.kcb,seasons = wheat.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = PMF.Biomass_LUE(wheat.RUE,wheat.k)
    print 'Biomass: Light-use-efficiency concept' 
    development = PMF.Development(wheat.stage,wheat.R_p, wheat.R_v)                         
    nitrogen = PMF.Nitrogen()
    water = PMF.Waterstress_Feddes()
    print 'Waterstress: Feddes'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)

def createPlant_SWC(**args):                                                    
    """             
    Implements a specific plant setup with summer wheat values.
    """
    et = PMF.ET_FAO(kcb_values = wheat.kcb,seasons = wheat.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = PMF.Biomass_LUE(wheat.RUE,wheat.k)
    print 'Biomass: Light-use-efficiency concept' 
    development = PMF.Development(wheat.stage,wheat.R_p, wheat.R_v)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)


def createPlant_SWC_Soltani(**args):                                                   
    """             
    Implements a specific plant setup with summer wheat values.
    """
    et = PMF.ET_FAO(kcb_values = wheat.kcb,seasons = wheat.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = PMF.Biomass_LUE_CO2_Soltani(wheat.RUE,wheat.k)
    print 'Biomass: Light-use-efficiency concept with CO2 response according to Soltani and Sinclair 2012' 
    development = PMF.Development(wheat.stage,wheat.R_p, wheat.R_v)                          
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)

def createPlant_fromCoefficiant(CropCoefficiant,**args):
    """
    Implements a specific plant setup with the values from the crop coefficant class.
    """
    et = PMF.ET_FAO(kcb_values =CropCoefficiant.kcb,seasons = CropCoefficiant.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = PMF.Biomass_LUE(CropCoefficiant.RUE,CropCoefficiant.k)
    print 'Biomass: Light-use-efficiency concept' 
    development = PMF.Development(wheat.stage,wheat.R_p, wheat.R_v)
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)
