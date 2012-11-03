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

@author: Sebastian Multsch

@version: 0.1 (26.10.2010)

@copyright: 
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
    
    @rtype: PMF.Plant
    @return: New plant instance with same values.
    @see: [http://docs.python.org/library/copy.html, 11.11.2009]
    """
    return copy.deepcopy(plant)
def setProcess(p,**args):
    """
    Returns a process with the given paramter.
    
    @param p: Process class from PMF.ProcessLibrary.py
    @type p: process class
    
    @rtype: process class
    @return: Paramterised process class.
    """
    return p(**args)

def makePlant(plant,**args):
    """
    Returns a plant wit hthe given arguments.
    
    @param plant: plant
    @type plant: Plant instance from PMF.PlantModel.Plant.py.
    
    @rtype: plant
    @return: Plant instance
    """
    return plant(**args)

def connect(plant,soil,atmosphere,**args):
    """
    Connects a plant with environmental interfaces.
    
    @param plant: plant
    @type plant: Plant instance from PMF.PlantModel.Plant.py.
    @type  soil: soil
    @param soil: Interface to water balance data.
    @type  atmosphere: atmosphere
    @param atmosphere: Interface to meteorological data.
    
    @rtype: plant
    @return: Plant instance
    """
    if isinstance(plant,PMF.Plant):
        plant.set_soil(soil)
        plant.set_atmosphere(atmosphere)
        return plant
    else:
        return 'Error: No plant instance'


wheat=CropDatabase.CropCoefficiants()

def createPlant_CMF(**args):
    """
    Implements a specific plant setup with summer wheat values.
    """
    et = PMF.ET_FAO(kcb_values = wheat.kcb,seasons = wheat.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = PMF.Biomass_LUE(wheat.RUE,wheat.k)
    print 'Biomass: Light-use-efficiency concept' 
    development = PMF.Development(stage = wheat.stage)
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
    development = PMF.Development(stage = wheat.stage)
    nitrogen = PMF.Nitrogen()
    print 'No nitrogen uptake'
    water = PMF.Waterstress_FAO()
    print 'Waterstress: FAO'
    layer = PMF.SoilLayer()
    return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)




def createPlant_fromCoefficiant(cropCoefficiant,**args):
    """
    Implements a specific plant setup with the values from the crop coefficant class.
    """
    et = PMF.ET_FAO(kcb_values = cropCoefficiant.kcb, seasons = cropCoefficiant.seasons)
    #print cropCoefficiant.kcb
    #print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = PMF.Biomass_LUE(cropCoefficiant.RUE, cropCoefficiant.k)
    #print 'Biomass: Light-use-efficiency concept' 
    development = PMF.Development(stage = cropCoefficiant.stage)
    nitrogen = PMF.Nitrogen()
    water = PMF.Waterstress_Feddes()
    #print 'Waterstress: Feddes'
    layer = PMF.SoilLayer()
    #return makePlant(PMF.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)
    
    return makePlant(PMF.Plant,et=et,water=water,biomass=biomass,development=development,nitrogen=nitrogen,layer=layer,
                 shoot_percent        = cropCoefficiant.shoot_percent,
                 root_percent         = cropCoefficiant.root_percent,
                 leaf_percent         = cropCoefficiant.leaf_percent,
                 stem_percent         = cropCoefficiant.stem_percent,
                 storage_percent      = cropCoefficiant.storage_percent,
                 tbase                = cropCoefficiant.tbase,
                 pressure_threshold   = cropCoefficiant.pressure_threshold,
                 plantN               = cropCoefficiant.plantN,
                 leaf_specific_weight = cropCoefficiant.leaf_specific_weight,
                 root_growth          = cropCoefficiant.root_growth,
                 max_height           = cropCoefficiant.max_height,
                 stress_adaption      = cropCoefficiant.stress_adaption,
                 carbonfraction       = cropCoefficiant.carbonfraction,
                 max_depth            = cropCoefficiant.max_depth,
                 soil=None,atmosphere=None,**args)












































