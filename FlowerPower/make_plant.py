'''
Created on 02.11.2009

@author: philkraf
'''
import FlowerPower
def create_crop(soil,atmosphere,filename):
    return createCrop_LUEconcept(soil, atmosphere, getCropSpecificParameter(filename))
    

def getCropSpecificParameter(path):
    """
    Reads crop specific parameters from a
    parameterisation file
    
    @type path: String
    @param path: Path from the parametrisation file.
    @rtype: list
    @return: List with crop specific parameters.
    """
    param = [line for line in file(path+'.txt',"r") if line[0]!='#']
    return [eval(each) for each in param]


def createCrop_LUEconcept(soil,atmosphere,CropParams):
    """
    Returns a plant instance with the given parameter.
    
    Creates a plant with the given soil and amtosphere interface.
    The crop specific parameters must be taken from the input file.
    All other needed interfaces are set with the default classes.
    
    Discription of the input file:
    CropParams[0] : Basal crop coefficiants for each season
    CropParams[1] : Ligth use efficiency
    CropParams[2] : Extinction coefficiant
    CropParams[3] : Development
    CropParams[4] : K_m
    CropParams[5] : NO3_min
    CropParams[6] : Partitioning shoot
    CropParams[7] : Partitioning root
    CropParams[8] : Partitioning leaf
    CropParams[9] : Partitioning stem
    CropParams[10] : Partitioning storage
    CropParams[11] : tbase
    CropParams[12] : rootability_thresholds
    CropParams[13] : pressure_threshold
    CropParams[14] : plant_N
    CropParams[15] : leaf_specific_weight
    CropParams[16] : root_growth
    CropParams[17] : max_height
    CropParams[18] : Logistic growht rate
    CropParams[19] : Capacity limit
    
    @type soil: soil
    @param soil: Soil instance
    @type atmosphere: atmosphere
    @param atmosphere: Atmosphere instance
    @type CropParams: list
    @param CropParams: List with specific crop coeffciants.
    
    @rtype: FlowerPower.PlantComponents.Plant
    @return: Plant with specific parameters and soil and atmospere interface.
    """
    #SummerWheat
    #Development
    stage = CropParams[3]#[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]]
    #Basal crop coefficiants for each season
    kcb = CropParams[0]#[0.15,1.1,0.15]
    #Lenght of seasons
    seasons = [stage[0][1], stage[3][1]-stage[0][1], stage[6][1]-stage[3][1], stage[-1][1]-stage[3][1]]
    #Ligth use efficiency
    LUE = CropParams[1]#3.0       
    #Extinction coefficiant
    k = CropParams[2]#0.4
    #K_m
    K_m = CropParams[4]#0.
    #NO3_min
    NO3_min = CropParams[5]#0.
    #Partitioning shoot
    shoot = CropParams[6]#[.0,.9,.9,.9,.95,1.,1.,1.]
    #Partitioning root
    root = CropParams[7]#[.0,.1,.1,.1,.05,.0,.0,.0]
    #Partitioning leaf
    leaf = [CropParams[8][i]*perc for i,perc in enumerate(shoot)]#[[.0,.5,.5,.3,0.,.0,.0,.0][i]*perc for i,perc in enumerate(shoot)]
    #Partitioning stem
    stem = [CropParams[9][i]*perc for i,perc in enumerate(shoot)]#[[.0,.5,.5,.7,.3,.0,.0,.0][i]*perc for i,perc in enumerate(shoot)]
    #Partitioning storage
    storage = [CropParams[10][i]*perc for i,perc in enumerate(shoot)]#[[.0,.0,.0,.0,.7,1.,1.,1.][i]*perc for i,perc in enumerate(shoot)]
    #tbase
    tbase = CropParams[11]#0.
    #rootability_thresholds
    rootability = CropParams[12]#[1.5,0.5,16000.,.0,0.0,0.0]
    #pressure_threshold
    pressure_thresholds = CropParams[13]#[0.,1.,500.,16000.]
    #plant_N
    plantN = CropParams[14]#[[160.,0.43],[1174.,0.16]]
    #leaf_specific_weight
    leaf_specific_weight = CropParams[15]#50.
    #root_growth
    root_growth = CropParams[16]#1.2
    #vetical_elongation
    max_height = CropParams[17]#1.0
    
    #Crop process models from ProcesLibrary
    et = FlowerPower.ET_FAO(kcb,seasons)
    
    biomass = FlowerPower.Biomass_LUE(LUE,k)
    development = FlowerPower.Development(stage)
    layer = FlowerPower.SoilLayer()
    layer.get_rootingzone(soil.soilprofile())
    nitrogen = FlowerPower.Nitrogen(layercount=len(layer))
    water = FlowerPower.Water_Feddes(layercount=len(layer))
    #Creates plant
    return FlowerPower.Plant(soil,atmosphere,et,water,biomass,development,layer,nitrogen,
                 shoot,root,leaf,stem,storage,root_growth=3.)
