
import cmf
from cmf.soil import layer as ka4_soil
import numpy as np
from pylab import *
from traceback import format_exc as traceback
from datetime import datetime, timedelta
#from sensitivity_analysis_I import get_starttimeT



class cmf1d(object):
    def __init__(self,sand,silt,clay,c_org,bedrock_K,layercount,layerthickness,tracertext=''):
        self.project=cmf.project(tracertext)
        self.cell=self.project.NewCell(0,0,0,1000)
        c=self.cell      
        # Add 50 layers with 10cm thickness, and 50 Neumann boundary conditions
        self.__bc=[]
        soil_depth=[]
        
        def summe(list):
            s = 0
            for element in list:
                s = s + element
            return s
            
    
        for i,val in enumerate(sand):
            Anteil_clay=clay[i]
            Anteil_silt =silt[i]
            Anteil_sand=sand[i]
            Anteil_layerthickness=layerthickness[i]
            soil_depth.append(layerthickness[i])            
            Anteil_Corg=c_org[i]
            KA4_soil=ka4_soil(Anteil_layerthickness,Anteil_clay,Anteil_silt,Anteil_sand,Corg=Anteil_Corg) # Berechnung von Ksat, Porositaet, etc. mit pedo-Transferfunktion nach kartieranleitung 4
            r_curve=cmf.BrooksCoreyRetentionCurve(KA4_soil.KSat , KA4_soil.porosity, KA4_soil.b, KA4_soil.fieldcap) # BROOKS90, berechnung der Retentionskurve mit KA4 Werten
            c.add_layer(summe(soil_depth),r_curve)
            nbc=cmf.NeumannBoundary.create(c.layers[-1])
            nbc.Name="Boundary condition #%i" % (1)
            self.__bc.append(nbc)        
        
        
#        for i in arange(0.05,2.0,layerthickness):
#            KA4_soil=ka4_soil(0.05,clay,silt,sand,Corg=c_org)
#            r_curve=cmf.BrooksCoreyRetentionCurve(KA4_soil.KSat , KA4_soil.porosity, KA4_soil.b, KA4_soil.fieldcap) 
#            c.add_layer(i,r_curve)
#            nbc=cmf.NeumannBoundary.create(c.layers[-1])
#            nbc.Name="Boundary condition #%i" % (1)
#            self.__bc.append(nbc)
        self.cell.surfacewater_as_storage()
            
    
#        #Add a bedrock layer
#       c.add_layer(7,cmf.BrooksCoreyRetentionCurve(bedrock_K,0.1,1,0.01))
#        #Add a groundwater boundary (potential=-5.0 m)
        self.groundwater=cmf.DirichletBoundary(self.project,-5)
#       self.groundwater.is_source=True
#       self.groundwater.Name="Groundwater"
#       # Connect bedrock layer with groundwater boundary, using Richards equation
        cmf.Richards(c.layers[-1],self.groundwater)
        dbc = cmf.Richards(c.layers[-1],self.groundwater)
        
        # Use Richards equation for percolation
        c.install_connection(cmf.Richards)
        c.install_connection(cmf.MatrixInfiltration)
        self.integrator=cmf.CVodeIntegrator(self.project,1e-6)
        self.integrator.LinearSolver=0
    def run(self,dt=cmf.h):
        self.integrator(self.integrator.t+dt)
    def __get_t(self):
        """The model time"""
        return self.integrator.t.AsPython()  
    def __set_t(self,time):
        self.integrator.t=cmf.AsCMFtime(time)        
    t=property(__get_t,__set_t)
    def layer(self,depth):
        pos=min(int(depth/0.1),len(self.cell.layers)-1)
    @property
    def matrix_potential(self):
        """Returns the capillary suction in m for each layer (including the bedrock layer)"""
        return [l.matrix_potential for l in self.cell.layers]
    @property
    def pF(self):
        """The pF value for each layer """
        return [l.pF for l in self.cell.layers]
    @property
    def potential(self):
        """ The actual water head of each layer """
        return [l.potential for l in self.cell.layers]
    @property
    def wetness(self):
        """ The wetness (water content per pore volume) for each layer """
        return [l.wetness for l in self.cell.layers]
    @property 
    def depth(self):
        """ Returns the center depth of each layer (including the bedrock layer) """
        return np.array([-0.5*(l.boundary[0]+l.boundary[1]) for l in self.cell.layers])
    @property
    def groundwater_flux(self):
        return -self.groundwater.waterbalance(self.t)
    @property
    def percolation(self):
        return [self.cell.layers[i].flux_to(self.cell.layers[i+1] if i+1< self.cell.layer_count() else self.groundwater,self.t) for i in range(self.cell.layer_count())]
    def __get_flux(self):
        return np.array([-bc.waterbalance(cmf.Time()) for bc in self.__bc])
    def __set_flux(self,fluxes):
       
        try:
            for i,bc in enumerate(self.__bc):
                if i<len(fluxes):
                    bc.flux=cmf.timeseries.from_scalar(fluxes[i])
                else:
                    bc.flux=cmf.timeseries.from_scalar(0.0)
        except TypeError:
            msg ="Fluxes is not a sequence of floats. Fluxes needs to be a sequence with %i float values" % self.cell.layer_count()
            msg +='\n' + traceback()
            raise TypeError(msg)            
    flux=property(__get_flux,__set_flux,"The boundary fluxes. A sequence with as many elements as layers")
    
    
   
    def load_meteo(self,start, stationname, rain_factor=1.): # am Besten mit in Sensitiv_Analysis_I aufnehmen 
#        #meteo2= ClimateStation() #!!!
#        #meteo2.load_weather('climate_giessen.csv') #!!!
#        #meteo3= meteo2.rain
#        # Load rain timeseries (doubled rain of giessen for more interstingresults)
#        rain=cmf.timeseries.from_file(stationname+'.Rain')*rain_factor
#        rainstation = self.project.rainfall_stations.add('Giessen',rain,(0,0,0))
#        # Create a meteo station
#        meteo=self.project.meteo_stations.add_station(stationname,(0,0,0))
#        # Meteorological timeseries
#        meteo.Tmax=cmf.timeseries.from_file(stationname+'.Tmax')
#        meteo.Tmin=cmf.timeseries.from_file(stationname+'.Tmin')
#        meteo.rHmean=cmf.timeseries.from_file(stationname+'.rHmean')
#        meteo.Windspeed=cmf.timeseries.from_file(stationname+'.Windspeed')
#        meteo.Sunshine=cmf.timeseries.from_file(stationname+'.Sunshine')
#        # Use the rainfall for each cell in the project
#        self.project.use_nearest_rainfall()
#        # Use the meteorological station for each cell of the project
#        self.project.use_nearest_meteo()
        
        """
        Loads the meteorology from a csv file.
        """
            
        # Create a timeseries for rain - timeseries objects in cmf is a kind of extensible array of 
        # numbers, with a begin date, a timestep.
        #begin = datetime(1992,1,1)
        #begin = get_starttimeT()
        begin=start
        rain = cmf.timeseries(begin = begin, step = timedelta(days=1))
    
        # Create a meteo station
        meteo=self.project.meteo_stations.add_station(stationname,position = (0,0,0))
    
        # Meteorological timeseries, if you prefer the beginning of the timeseries
        # read in from file, just go ahead, it is only a bit of Python programming
        meteo.Tmax      = cmf.timeseries(begin = begin, step = timedelta(days=1))
        meteo.Tmin      = cmf.timeseries(begin = begin, step = timedelta(days=1))
        meteo.rHmin     = cmf.timeseries(begin = begin, step = timedelta(days=1))# als RHmin das Minimum aus Rh14uhr und Rhmean nehmen, Rhmean braucht python nicht. Rhmax auf 100 setzen. Sind das wirklich Rh Daten bei Muencheberg oder ist das das Saettigungsdefizit? Ueberpruefen!
        meteo.rHmax     = cmf.timeseries(begin = begin, step = timedelta(days=1))        
        meteo.Windspeed = cmf.timeseries(begin = begin, step = timedelta(days=1))
        meteo.Sunshine  = cmf.timeseries(begin = begin, step = timedelta(days=1)) # sind cloud daten 1-(cloud/100)
        meteo.Rs        = cmf.timeseries(begin = begin, step = timedelta(days=1))
        #meteo.Cloud     = cmf.timeseries(begin = begin, step = timedelta(days=1)) # so nicht cloud = sunshine
        meteo.T         = (meteo.Tmax + meteo.Tmin) * 0.5
        
       
        
        # Load climate data from csv file
        # could be simplified with numpy's 
        csvfile =file('ClimateMuencheberg.csv') 
        csvfile.readline() # Read the headers, and ignore them
        for line in csvfile:
            columns = line.split(';')
            # Get the values, but ignore the date, we have begin and steo
            # of the data file hardcoded
            # If you don't get this line - it is standard Python, I would recommend the official Python.org tutorial
            for timeseries,value in zip([rain,meteo.Tmax,meteo.Tmin,meteo.rHmin, meteo.rHmax,meteo.Windspeed,meteo.Rs,meteo.Sunshine], #zip fuegt zwei Listen zu einer Zusammen
                                       [float(col) for col in columns[2:]]):    
                # Add the value from the file to the timeseries
                timeseries.add(value)
            #print line
        # Create a rain gauge station
        self.project.rainfall_stations.add(stationname,rain,(0,0,0))
            
        # Use the rainfall for each cell in the project
        self.project.use_nearest_rainfall()
        # Use the meteorological station for each cell of the project
        self.project.use_nearest_meteo()
    
if __name__=='__main__':
    c1=cmf1d()
    print "gw_flux=",c1.groundwater_flux
    #print "P(750cm)=",c1.get_pressurehead(750)

