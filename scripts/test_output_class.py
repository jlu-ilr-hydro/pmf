"""
This setup build a cmf1d cell with defualt values. For a
given management with harvest and sowingdates a crop is 
created from the PMF crop model. The plant growth
processes are taken from the PMF process library.
The crop parameters are created from liture data which refer
to summer wheat. Meterological timeseries refer to a weather 
station from Giessen.
"""
from pylab import *
from datetime import *
import PMF
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
    param = filter(lambda line: line[0]!='#',open(path+'.txt',"r"))
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
def createCrop_LogisticGrowth(soil,atmosphere,CropParams):
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
    
    @rtype: PMF.PlantModel.Plant
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
    #root_growth
    logistic_growhtrate = CropParams[18]#0.05
    #vetical_elongation
    capacity_limit = CropParams[19]#1500
    
    #Crop process models from ProcesLibrary
    et = PMF.ET_FAO(kcb,seasons)
    
    biomass = PMF.Biomass_LOG(capacity_limit,logistic_growthrate)
    development = PMF.Development(stage)
    layer = PMF.SoilLayer()
    layer.get_rootingzone(c.get_profile())
    nitrogen = PMF.Nitrogen(layercount=len(layer))
    water = PMF.Water_Feddes(layercount=len(layer))
    #Creates plant
    return PMF.Plant(soil,atmosphere,et,water,biomass,development,layer,nitrogen,
                 shoot,root,leaf,stem,storage)
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
    
    @rtype: PMF.PlantModel.Plant
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
    et = PMF.ET_FAO(kcb,seasons)
    
    biomass = PMF.Biomass_LUE(LUE,k)
    development = PMF.Development(stage)
    layer = PMF.SoilLayer()
    layer.get_rootingzone(c.get_profile())
    nitrogen = PMF.Nitrogen(layercount=len(layer))
    water = PMF.Water_Feddes(layercount=len(layer))
    #Creates plant
    return PMF.Plant(soil,atmosphere,et,water,biomass,development,layer,nitrogen,
                 shoot,root,leaf,stem,storage)
def run(start,end,step):
     #Set cmf time
     c.t = start
     #Modelrun for the given time period
     for index,t in enumerate(drange(start,end,step)):
        time = num2date(t)
            
        #sowing
        if t in sowingdate: crop = PMF.connect(PMF.createPlant_CMF(),c,c)
        #harvest
        if t in harvestdate: PMF.Plant.Count-=1

        #Let grow
        if PMF.Plant.Count > 0: crop(time,'day',1.)
        
        #Water flux from soil to plant
        c.flux = [uptake*-1. for uptake in crop.Wateruptake] if PMF.Plant.Count >0 else [0]*50
        
        
        #Calculation of water balance with cmf
        c.run(cmf.day)
        
        
        #Save results for each element from output
        for i,out in enumerate(output):
            #Call plant only if plant exists
            if PMF.Plant.Count > 0:
                #call out objects with PMF values
                out([eval(param) for param in PMF_params[i]])
            else:
                #call out objects with zero values
                out([0. for l in range(len(out.labels))])
        
        #Output in console    
        if index % 1 == 0:
            print index,num2date(t), [out.Step for out in output] 
            for i,out in enumerate(output):
                #Draw a dynamic plot, if True
                if out.dynamic == True:
                    out.DynamicPlot
        
        
        
class Output:
    def __init__(self,labels,start,end,step,dynamic=False):
        """
        @todo: ylim, axis labels for deynamic plot and Image property doesen't run, because
               of the resutls list. 
        """
        #Variables with labes and all resutls of the output
        self.labels=labels
        self.results=[]
        self.delta_time = drange(start,end,step)
        
        #Dynamic plotting during the model run
        self.dynamic=dynamic
        
        if self.dynamic == True:
            #Dynamic plot
            ion()
            
            #Zero list for each paramter
            self.dynamicdata = [zeros(len(self.delta_time)) for l in self.labels]
            
            #Create figure with x-axes for the simulation period
            self.fig = Figure()
            self.x = self.delta_time
           
            #Create list for dynamic plots
            self.dynamicplots = []
            
            #Create subplot with line2d object for each parameter
            for i,dat in enumerate(self.dynamicdata):
                #Create subplot
                res  = subplot(len(self.dynamicdata),1,i+1)
                #set date plot instance for each subplot
                res,  = plot_date(self.delta_time,dat,label = self.labels[i])
                ylim(0,1)
                legend(loc=0)
                self.dynamicplots.append(res)

    def __setitem__(self,stage):
        self.results.append(stage)
    def __getitem__(self,index):
        return self.results[index]
    def __iter__(self):
        for res in self.results:
            yield res
    @property
    def Results(self):
        return [[self.labels[i] +': ' +  str(r) for i,r in enumerate(res)] for res in self.results]
    @property
    def Step(self):
        """
        Return the last record from the results parameter.
        The rocord parameter constis of n parameters,
        which aredefined during the model initialisation.
        
        If the paratermer is not a list, the output is
        formated as 4.2f. Otherwise the function resturns
        the parameter list.
        
        @rtype: list
        @return: Last record from the output
        
        @todo: typeerror bei liste mit nur einem wert
        """
        if type(self.results[-1]) == float or  type(self.results[-1]) == double:
            return  [self.labels[i]+': '+  '%4.2f' % res for i,res in enumerate(self.results[-1])]
        elif  type(self.results[-1]) == list:
            try:
                return [self.labels[i]+': '+  str(['%4.2f' % r for r in res]) for i,res in enumerate(self.results[-1])]
            except TypeError:
                pass
    @property
    def Image(self):
        list =[]
        for i in range(len(self.results[0])):
            res  = subplot(len(self.results[0]),1,i+1)
            res, = imshow(transpose([res[i] for res in self.results]),cmap=cm.RdYlBu,aspect='auto')
            colobar()
            grid()
            ylabel(self.labels[i])
        list.append(res)
        return list
        
        for i in range(len(self.results[0])):
            res  = subplot(len(self.results[0]),1,i+1)
            res, = imshow(transpose([res[i] for res in self.results]),cmap=cm.RdYlBu,aspect='auto')
            colorbar()
            grid()
            ylabel(self.labels[i])
        
    @property
    def Plot(self):
        list = []
        for i in range(len(self.results[0])):
            res  = subplot(len(self.results[0]),1,i+1)
            res,  = plot_date(self.delta_time,[res[i] for res in self.results],label = self.labels[i])
            legend(loc=0)
            list.append(res)
        return list
    @property
    def DynamicPlot(self):
        #Refresh plot data
        for i,plot in enumerate(self.dynamicplots):
           plot.set_ydata(self.dynamicdata[i])
        draw()
    def __call__(self,results):
        #set resutls
        self.results.append(results)
        
        #set data for dynamic plot
        if self.dynamic == True:
            for i,data in enumerate(self.dynamicdata):
                data[len(self.results)-1]+=self.results[-1][i]       
     
if __name__=='__main__':
    #Create cmf cell
    c = cmf1d(sand=90,silt=0,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    c.cell.saturated_depth=5
    res=[]
    
    
    #Load meteological data
    load_meteo(c.project,stationname='Giessen')
    

    #set management
    sowingdate = [date2num(d) for d in [datetime(1980,3,1),datetime(1981,3,1),datetime(1982,3,1),
                 datetime(1983,3,1),datetime(1984,3,1)]]
    harvestdate = [date2num(d) for d in [datetime(1980,8,1),datetime(1981,8,30),datetime(1982,8,30),
                  datetime(1983,8,30),datetime(1984,8,30)]]
    
    #Simulation period
    start = datetime(1980,1,1)
    end = datetime(1980,12,31)
    
    #timestep = daily
    step = timedelta(1)
    
    #Initialise output classes whith labels for each parameter
    output = [Output(['Wateruptake'],start,end,step,dynamic=True)]
    
    #Set PMF call function for each parameter in output
    PMF_params =[['sum(crop.Wateruptake)']]
    

    run(start,end,step)

    