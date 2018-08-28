from ProcessLibrary import *
# Besser: import ProcessLibrary 
# Folge: swc = PMF.SWC() geht nicht mehr 
# nur noch swc = PMF.ProcessLibrary.SWC()
from PlantModel import *
from CropDatabase import *
from PlantBuildingSet import createPlant_CMF,makePlant,createPlant_SWC,connect,clone,createPlant_fromCoefficiant