from pylab import *
import FlowerPower
import cmf
from cmf_setup import *
import struct

def getCropSpecificParameter(path):
    param = filter(lambda line: line[0]!='#',open(path,"r"))
    return [eval(each) for each in param]
def timeseries_from_file(f):

    """ Loads a timeseries saved with to_file from a file

    Description of the file layout:

    byte:

    0   Number of (int64)

    8   Begin of timeseries (in ms since 31.12.1899) (int64)

    16  Step size of timeseries (in ms) (int64)

    24  Interpolation power (int64)

    32  First value of timeseries (float64)

    """
    # Open the file
    if isinstance(f,str):
        f=file(f,'rb')
    elif not hasattr(f,'read'):
        raise TypeError("The file f must either implement a 'read' method,like a file, or must be a valid file name")
    # Get the meta data header
    header_length=struct.calcsize('qqqq')
    header=struct.unpack('qqqq',f.read(header_length))
    # Create a timeseries
    res=cmf.timeseries(header[1]*cmf.ms,header[2]*cmf.ms,header[3])
    # Put the data into the timeseries
    res.extend(struct.unpack('%id' % header[0],f.read(-1)))
    return res 
def load_meteo(project,stationname='Giessen'):
    # Load rain timeseries (doubled rain of giessen for more interstingresults)
    rain=timeseries_from_file(stationname + '.rain')
    # Create a meteo station
    meteo=project.meteo_stations.add_station(stationname)
    # Meteorological timeseries
    meteo.Tmax=timeseries_from_file(stationname+'.Tmax')
    meteo.Tmin=timeseries_from_file(stationname+'.Tmin')
    meteo.rHmean=timeseries_from_file(stationname+'.rHmean')
    meteo.Windspeed=timeseries_from_file(stationname+'.Windspeed')
    meteo.Sunshine=timeseries_from_file(stationname+'.Sunshine')
    # Use the rainfall for each cell in the project
    cmf.set_precipitation(project.cells,rain)
    # Use the meteorological station for each cell of the project
    cmf.set_meteo_station(project.cells,meteo)

def createCrop(soil,atmosphere,CropParams,et,water,biomass,development,layer,nitrogen,plant):
    return plant(soil,atmosphere,et,water,biomass(Cropparams[-1],CropParams[-2]),development(CropParams[0]),layer,nitrogen)

if __name__=='__main__':
    from datetime import *
    
    #Create cmf cell
    c=cmf1d(sand=90,silt=0,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    
    #Load meteological data
    load_meteo(c.project,stationname='Giessen')
    c.cell.saturated_depth=5
    
    #Crop parameter
    SummerWheat = getCropSpecificParameter('SummerWheat.txt')
    
    #Crop process models from ProcesLibrary
    et = FlowerPower.ET_FAO
    water = FlowerPower.Water_Feddes
    biomass = FlowerPower.Biomass_LUE
    development = FlowerPower.Development
    layer = FlowerPower.SoilLayer
    nitrogen = FlowerPower.Nitrogen
    
    #set actual time amd timestep
    time_act=datetime
    time_step=timedelta(1)
    c.t=time_act
    
    #set management
    sowing_date=[datetime(1980,3,1),datetime(1981,3,1),datetime(1982,3,1),datetime(1983,3,1),datetime(1984,3,1)]
    harvest_date=[datetime(1980,8,1),datetime(1981,8,30),datetime(1982,8,30),datetime(1983,8,30),datetime(1984,8,30)]
    
    #run simulation
    while time_act<=end:
        #sowing
        if filter(lambda s: s==time_act, sowing_date): plant=createCrop(c,c,SummerWheat,et,water,biomass,development,layer,nitrogen) 
        #harvest
        if filter(lambda s: s==time_act, harvest_date): Plant.Count-=1
        #plant growth
        if Plant.Count >= 1.: plant(time_act,'day',1.)
        #water flux from soil to plant
        c.flux = [uptake*-1. for uptake in plant.water.Uptake] if Plant.Count >= 1. else [0]*50