"""
Make a plant and connect it to the soil and atmosphere interface in three steps:

1. Set Processes from ProcessLibrary (note *1):
    et = FlowerPower.ET_FAO(kcb_values = [0.15,1.1,0.15],seasons = [160.0, 499.0, 897.0, 1006.0])
    biomass = FlowerPower.Biomass_LUE(RUE = 3.,k=.4)
    development = FlowerPower.Development(stage = [['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],['Anthesis',1200.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]])
    layer = FlowerPower.SoilLayer(soillayer=[10,20,30,40,50,60,100])
    nitrogen = FlowerPower.Nitrogen(layercount = len(layer))
    water = FlowerPower.Water_Feddes(layercount = len(layer))


2.Create plant (note*2,*3):
    a) wheat_instance = makePlant(FlowerPower.Plant,et=et,biomass=biomass,development=development,layer=layer,nitrogen=nitrogen,water=water)
    b) wheat_classobj = FlowerPower.Plant

3. Couple plant with soil and amtosphere interface (note*2,*3):
    Loess = Soil()
    Meteo_Giessen = Atmosphere()
    a) connect(wheat_instance,Loess,Meteo_Giessen)
    b) connect(wheat_classobj,Loess,Meteo_Giessen,et=et,biomass=biomass,development=development,layer=layer,nitrogen=nitrogen,water=water)


 *1 A plant instance must be implemented with six process instances from the FlowerPower.ProcessLibrary
 
 *2 a) Plant is instance and created with soil,atmosphere = None
    b) Plant is an classobject of FlowerPower plant; all atributes must be setted during the connection
    
 *3  make_plant() and connect() accept additional crop specific parameters,
     to create crop which differ from the default setting. The default paramters
     refer to summerwheat.
     
         shoot=[.0,.5,.5,.9,.95,1.,1.,1.],
         root = [.0,.5,.5,.1,.05,.0,.0,.0],
         leaf = [.0,.5,.5,.5,0.,.0,.0,.0],
         stem = [.0,.5,.5,.5,.3,.0,.0,.0],
         storage = [.0,.0,.0,.0,.7,1.,1.,1.],
         tbase = 0.,
         pressure_threshold = [[160.,0.43],[1200.,0.16]],
         plantN= [[160.,0.43],[1200.,0.16]],
         leaf_specific_weight = 50.,
         root_growth=1.5,
         max_height = 1.
     
    Example: make_plant(FlowerPower.Plant,et=et, ..., root_growth=3.,tbase=5.)
"""
import FlowerPower
import copy as copy
def clone(plant):
    """
    Returns new insance of plant and the related classes
    with the actual values.
    
    Constructs a new compound object and then, recursively, 
    inserts copies into it of the objects found in the original.
    
    @rtype: FlowerPower.Plant
    @return: New plant instance with same values.
    @see: [http://docs.python.org/library/copy.html, 11.11.2009]
    """
    return copy.deepcopy(plant)
def setProcess(p,**args):
    return p(**args)

def makePlant(plant,**args):
    return plant(**args)

def connect(plant,soil,atmosphere,**args):
    if isinstance(plant,FlowerPower.Plant):
        plant.set_soil(soil)
        plant.set_atmosphere(atmosphere)
        return plant
    else:
        return 'Error: No plant instance'

class CropCoefficiants:
    def __init__(self,
                 tbase = 0.,
                 stage = [['Emergence',160.],
                          ['Leaf development',208.],
                          ['Tillering',421.],
                          ['Stem elongation',659.],
                          ['Anthesis',901.],
                          ['Seed fill',1174.],
                          ['Dough stage',1556.],
                          ['Maturity',1665.]],
                 RUE=3.,
                 k=.4,
                 seasons =[160.0, 499.0, 897.0, 1006.0],
                 kcb =[0.15,1.1,0.15] ):
        self.tbase = tbase
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb
        self.RUE=RUE

wheat=CropCoefficiants()

def createPlant_CMF(**args):
    et = FlowerPower.ET_FAO(kcb_values = wheat.kcb,seasons = wheat.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = FlowerPower.Biomass_LUE(wheat.RUE,wheat.k)
    print 'Biomass: Light-use-efficiency concept' 
    development = FlowerPower.Development(stage = wheat.stage)
    nitrogen = FlowerPower.Nitrogen()
    water = FlowerPower.Water_Feddes()
    print 'Waterstress: Feddes'
    layer = FlowerPower.SoilLayer()
    return makePlant(FlowerPower.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)

def createPlant_SWC(**args):
    et = FlowerPower.ET_FAO(kcb_values = wheat.kcb,seasons = wheat.seasons)
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = FlowerPower.Biomass_LUE(wheat.RUE,wheat.k)
    print 'Biomass: Light-use-efficiency concept' 
    development = FlowerPower.Development(stage = wheat.stage)
    nitrogen = FlowerPower.Nitrogen()
    print 'No nitrogen uptake'
    water = FlowerPower.Water_FAO()
    print 'Waterstress: FAO'
    layer = FlowerPower.SoilLayer()
    return makePlant(FlowerPower.Plant,et=et,biomass=biomass,development=development,nitrogen=nitrogen,water=water,layer=layer,**args)















