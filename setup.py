"""
This setup build a cmf1d cell with defualt values. For a
given management with harvest and sowingdates a crop is 
created from the FlowerPower crop model. The plant growth
processes are taken from the FlowerPower process library.
The crop parameters are created from liture data which refer
to summer wheat. Meterological timeseries refer to a weather 
station from Giessen.
"""
from pylab import *
from datetime import *
import FlowerPower
import cmf
from cmf_setup import *
import struct

def getCropSpecificParameter(path):
    """
    Reads crop specific parameters from a
    parameterisation file
    
    @type path: String
    @param path: Path from the parametrisation file.
    @rtype: list
    @return: List with crop specific parameters.
    """
    
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
def createCrop(soil,atmosphere,CropParams):
    """
    Returns a plant instance with the given parameter.
    
    
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
    
    #Crop process models from ProcesLibrary
    et = FlowerPower.ET_FAO(kcb,seasons)
    water = FlowerPower.Water_Feddes()
    biomass = FlowerPower.Biomass_LUE(LUE,k)
    development = FlowerPower.Development(stage)
    layer = FlowerPower.SoilLayer()
    layer.get_rootingzone(c.get_profile())
    nitrogen = FlowerPower.Nitrogen()
    
    #Creates plant
    return FlowerPower.Plant(soil,atmosphere,et,water,biomass,development,layer,nitrogen,
                 shoot,root,leaf,stem,storage)
def run(timeact,timeend,timestep):
     c.t = timeact
     results = [];label=[]
     
     while timeact<timeend:
        #sowing
        if filter(lambda s: s==timeact, sowing_date): 
            plant=createCrop(c,c,SummerWheat)
        #harvest
        if filter(lambda s: s==timeact, harvest_date): 
            FlowerPower.Plant.Count-=1
        #plant growth
        if FlowerPower.Plant.Count > 0: plant(timeact,'day',1.)
        #water flux from soil to plant
        c.flux = [uptake*-1. for uptake in plant.water.Uptake] if FlowerPower.Plant.Count >0 else [0]*50
        #water balance
        c.run(cmf.day)
        timeact+=timestep
        biomass_out([plant.developmentstage.Thermaltime,plant.biomass.Total,plant.shoot.leaf.LAI] if FlowerPower.Plant.Count > 0 else [0.,0.,0.])
        process_out([plant.et.Potential,plant.water.Uptake] if FlowerPower.Plant.Count > 0 else [0.,0.])
        print timeact,process_out.Step
class Output:
    def __init__(self,labels,start=0.,end=1826.):
        """
        @todo: dynamic plot: function init and call
        """
        self.labels=labels
        self.results=[]
        
        '''
        #Dynamic plot
        ion()
        self.biomass = zeros(end - start)
        self.thermaltime = zeros(end - start)
        
        
        self.fig = Figure()
        
        self.dynamicplots = self.create_dynamicplot(labels,start,end)
        self.x = range(1826) 
        
        
        #plot biomass
        self.fig.add_subplot(111)
        self.biomass_plot, = plot(self.x,self.biomass,'g',label = self.labels[1])
        ylabel('Biomass [g * m-1]')
        grid()
        
        #plot thermaltime
        ax2=twinx()
        self.thermaltime_plot, = plot(self.x,self.thermaltime,color='blue',label = self.labels[0])
        ylabel('DeegreeDays [Celsius]')
        grid()
        xlabel('Day of simulation period [day]')
        legend(loc=0)
        '''
        
    def __setitem__(self,stage):
        self.results.append(stage)
    def __getitem__(self,index):
        return self.results[index]
    def __iter__(self):
        for res in self.results:
            yield res
    @property
    def Whole(self):
        return [[self.labels[i] +': ' +  '%4.2f' % r for i,r in enumerate(res)] for res in self.results]
    @property
    def Step(self):
        return [self.labels[i]+': '+  '%4.2f' % res for i,res in enumerate(self.results[-1])]
    @property
    def Plot(self):
        return self.plot(self.results,self.labels)
    @property
    def Dynamic(self):
        #Reefresh plot data
        self.biomass_plot.set_ydata(self.biomass)
        self.thermaltime_plot.set_ydata(self.thermaltime)
        draw()
    def __call__(self,results):
        #set resutls
        self.results.append(results)
        '''
        #set data for dynamic plot
        self.biomass[self.results.index(self.results[-1])]+=self.results[-1][0]
        self.thermaltime[self.results.index(self.results[-1])]+=self.results[-1][1]
        '''
    def plot(self,results,labels):
        for i in range(len(results[0])):
            plot([res[i] for res in results],label=labels[i])
        show()
    def create_dynamicplot(self,labels,start,end):
        lenght = start - end
        return [zeros(end - start) for l in labels]
        
     
if __name__=='__main__':
    #Create cmf cell
    c=cmf1d(sand=90,silt=0,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    
    #Load meteological data
    load_meteo(c.project,stationname='Giessen')
    c.cell.saturated_depth=5
    
    #Crop parameter
    SummerWheat = getCropSpecificParameter('SummerWheat.txt')
    
    #set management
    sowing_date=[datetime(1980,3,1),datetime(1981,3,1),datetime(1982,3,1),datetime(1983,3,1),datetime(1984,3,1)]
    harvest_date=[datetime(1980,8,1),datetime(1981,8,30),datetime(1982,8,30),datetime(1983,8,30),datetime(1984,8,30)]
    
    #Model output
    biomass_out = Output(['Thermaltime','Biomass','LAI'])
    process_out = Output(['Waterdemand','Wateruptake'])
    
    #run simulation
    run(datetime(1980,1,1),datetime(1984,12,31),timedelta(1))
    