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

def createPlant(soil,atmosphere):
    et = FlowerPower.ET_FAO(kcb_values = [0.15,1.1,0.15],seasons = [160.0, 499.0, 897.0, 1006.0])
    print 'Evapotranspiration: FAO - Penman-Monteith'
    biomass = FlowerPower.Biomass_LUE(RUE = 3.,k=.4)
    print 'Biomass: Light-use-efficiency concept' 
    development = FlowerPower.Development(stage = [['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],['Anthesis',1200.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]])
    layer = FlowerPower.SoilLayer(soilprofile = soil.soilprofile())
    nitrogen = FlowerPower.Nitrogen(layercount = len(soil.soilprofile()))
    water = FlowerPower.Water_Feddes(layercount = len(soil.soilprofile()))
    print 'Waterstress: Feddes'
    wheat_instance = makePlant(FlowerPower.Plant,et=et,biomass=biomass,development=development,layer=layer,nitrogen=nitrogen,water=water)
    return connect(wheat_instance,soil,atmosphere)

class CropCoefficiants:
    def __init__(self,shoot=[.0,.5,.5,.9,.95,1.,1.,1.],
                 root = [.0,.5,.5,.1,.05,.0,.0,.0],
                 leaf = [.0,.5,.5,.5,0.,.0,.0,.0],
                 stem = [.0,.5,.5,.5,.3,.0,.0,.0],
                 storage = [.0,.0,.0,.0,.7,1.,1.,1.],
                 tbase = 0.,
                 pressure_threshold = [0.,1.,500.,16000.],
                 plantN= [[160.,0.43],[1200.,0.16]],
                 leaf_specific_weight = 50.,
                 root_growth=1.5,
                 max_height = 1.,
                 stage = [['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],['Anthesis',1200.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]],
                 RUE=3.,
                 k=4.,
                 seasons =[160.0, 499.0, 897.0, 1006.0],
                 kcb =[0.15,1.1,0.15] ):
        self.shoot = shoot
        self.root = root
        self.leaf = leaf
        self.stem = stem
        self.storage = storage
        self.tbase = tbase
        self.pressure_threshold = pressure_threshold
        self.plantN = plantN
        self.leaf_specific_weight = leaf_specific_weight
        self.root_growth= root_growth
        self.max_height =max_height
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb

def setProcess(p,**args):
    return p(**args)

def makePlant(plant,**args):
    return plant(**args)

def connect(plant,soil,atmosphere,**args):
    if isinstance(plant,FlowerPower.Plant):
        plant.atmosphere=atmosphere
        plant.soil=soil
        return plant
    else:
        return makePlant(plant,soil=soil,atmosphere=atmosphere,**args)






















