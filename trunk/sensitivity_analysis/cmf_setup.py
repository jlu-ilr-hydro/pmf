import cmf
from cmf.soil import layer as ka4_soil
import numpy as np
from pylab import *
from traceback import format_exc as traceback
class cmf1d(object):
    def __init__(self,sand=.2,silt=.6,clay=.2,c_org=2.0,bedrock_K=0.01,layercount=40,layerthickness=0.05,tracertext=''):
        self.project=cmf.project(tracertext)
        self.cell=self.project.NewCell(0,0,0,1000)
        c=self.cell
        KA4_soil=ka4_soil(0.05,clay,silt,sand,Corg=c_org)        
        # Add 50 layers with 10cm thickness, and 50 Neumann boundary conditions
        self.__bc=[]
        
        for i in arange(0.05,2.0,layerthickness):
            KA4_soil=ka4_soil(0.05,clay,silt,sand,Corg=c_org)
            r_curve=cmf.BrooksCoreyRetentionCurve(KA4_soil.KSat , KA4_soil.porosity, KA4_soil.b, KA4_soil.fieldcap) 
            c.add_layer(i,r_curve)
            nbc=cmf.NeumannBoundary.create(c.layers[-1])
            nbc.Name="Boundary condition #%i" % (1)
            self.__bc.append(nbc)
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
    
    
   
    def load_meteo(self,stationname='Giessen',rain_factor=1.):
        
        # Load rain timeseries (doubled rain of giessen for more interstingresults)
        rain=cmf.timeseries.from_file(stationname + '.rain')*rain_factor
        rainstation = self.project.rainfall_stations.add('Giessen',rain,(0,0,0))
        # Create a meteo station
        meteo=self.project.meteo_stations.add_station(stationname,(0,0,0)) 
        # Meteorological timeseries
        meteo.Tmax=cmf.timeseries.from_file(stationname+'.Tmax')
        meteo.Tmin=cmf.timeseries.from_file(stationname+'.Tmin')
        meteo.rHmean=cmf.timeseries.from_file(stationname+'.rHmean')
        meteo.Windspeed=cmf.timeseries.from_file(stationname+'.Windspeed')
        meteo.Sunshine=cmf.timeseries.from_file(stationname+'.Sunshine')
        # Use the rainfall for each cell in the project
        self.project.use_nearest_rainfall()
        # Use the meteorological station for each cell of the project
        self.project.use_nearest_meteo()
#        
        
if __name__=='__main__':
    c1=cmf1d()
    print "gw_flux=",c1.groundwater_flux
    print "P(750cm)=",c1.get_pressurehead(750)

