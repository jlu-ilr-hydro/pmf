'''
Created on 16.11.2009

@author: philkraf
'''
from __future__ import division
import cmf
from cmf.soil import layer as KA4soil 
import FlowerPower
from DECOMP.cmf_DECOMP import DECOMPcmf,DECOMP
from cmf_fp_interface import cmf_fp_interface
from datetime import datetime
import pylab
from math import sqrt
class Cell(object):
    """ A (creating) wrapper class for a cmf cell, a DECOMP/cmf cell, and a plant instance
    Creates a cell in a given cmf.project with a DECOMP layer for each layer
    """
    def __init__(self,cmf_project,x,y,z,area=100,soildepth=2.0,layer_thickness=0.1,sand=20,silt=60,clay=20,c_org=2):
        # Make cmf cell
        self.cmf=cmf_project.NewCell(x,y,z,area)
        layer_count=int(soildepth/layer_thickness)
        self.__bc=[]
        KA4_soil=KA4soil(0.05,clay=clay,silt=silt,sand=sand,Corg=c_org)
        r_curve=cmf.BrooksCoreyRetentionCurve(KA4_soil.KSat , KA4_soil.porosity, KA4_soil.b, KA4_soil.fieldcap) 
        print self.cmf, r_curve
        for i in range(layer_count):
            d=(i+1) * layer_thickness 
            self.cmf.add_layer(d,r_curve)
            nbc=cmf.NeumannBoundary.create(self.cmf.layers[-1])
            self.__bc.append(nbc)
        # Make DECOMP cell
        self.DECOMP=DECOMPcmf(self.cmf)
        # plant and baresoil
        self.N = cmf_project.solutes[0]
        self.plant_interface = cmf_fp_interface(self.cmf, self.N)
        self.plant=None
        self.baresoil=FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    def sow(self):
        """Creates a FlowerPower standard crop at this location
        """
        N = self.cmf.project().solutes[0]    
        self.plant = FlowerPower.connect(FlowerPower.createPlant_CMF(),
                                         self.plant_interface,
                                         self.plant_interface)
    def harvest(self):
        """
        @todo: Put residual biomass to first layer
        """
        litter_C = (self.plant.StemCarbon + self.plant.LeafCarbon) * self.cmf.area
        litter_N = (self.plant.StemNitrogen + self.plant.LeafNitrogen) * self.cmf.area
        litter = DECOMP.SOM(litter_N,0.1 * litter_C, 0.5 * litter_C, 0.4 * litter_C,0.0)
        self.DECOMP.DECOMPlayers[0] += litter
        self.plant=None
        # return biomass
    def fertilize(self,kgN_ha):
        """Adds to the SOM of the first layer easily decomposable SOM components 
        with a C/N ratio of 10
        @type kgN_ha: Amount of fertilizer in kg N per ha. 
        """
        gN = kgN_ha * 1e3 * self.cmf.area * 1e-4
        self.DECOMP.DECOMPlayers[0] += DECOMP.SOM(gN,10 * gN)
    @property
    def biomass(self):
        if self.plant:
            return self.plant.shoot.Wtot
        else:
            return 0.0
    def run(self,t,dt=1.0):
        """Runs the DECOMPcell and the FlowerPower instance. Does not check for sowing or harvest activities
        and does not run cmf
        @type t: datetime 
        @param t: Actual model time 
        @type dt: float
        @param dt: Actual time step (float in days)
        """
        N=self.cmf.project().solutes[0]
        # Run the DECOMP cell
        T=self.cmf.get_weather(t).T
        self.DECOMP.run(T,dt)
        # run flower power and distribute N uptake in profile 
        if self.plant:
            self.plant(t,'day',dt)
            for i,l in enumerate(self.cmf.layers):
                # Uptake in FlowerPower as g/m2 and in cmf as g
                l.Solute(N).source -= self.plant.nitrogen.Active[i] * self.cmf.area
        #Get the water flux from soil to plant
        flux     = [-uptake for uptake in self.plant.water.Uptake] if self.plant else [0.0] * self.cmf.layer_count()
        flux[0] -= self.plant.et.evaporation if self.plant else self.baresoil.evaporation
        # Set flux at the cmf boundary conditions
        for i,bc in enumerate(self.__bc):
            bc.flux=cmf.timeseries(flux[i] * self.cmf.area / 1000.0) # Convert from mm to m3
    
class Slope(object):
    def __init__(self,count=20,length=10,slope=0.05,slope_exponent=1,meteo_station_name=None):
        """ Creates <count=20> cells in <project> in a row with a slope of <slope=5%>, <length=10m> length per cell and <length**2> area"""
        self.project=cmf.project('N DOC')
        self.N,self.DOC = self.project.solutes
        p=self.project
        x_max=count*float(length)
        c_last=None
        self.cells=[]
        for i in range(count):
            # Create a cell
            x = i * length
            z = (x/x_max)**slope_exponent * x_max * slope 
            c = Cell(cmf_project=p, x=x, y=0, z=z, area=length**2, 
                     soildepth=3.0, layer_thickness=0.1, 
                     sand=80, silt=5, clay=15, c_org=2)
            c.cmf.install_connection(cmf.Richards)
            c.cmf.surfacewater_as_storage()
            c.cmf.install_connection(cmf.SimpleTindexSnowMelt)
            c.cmf.saturated_depth = c.cmf.z * .5 + .5
            # Setup a topological connection between c and the last created cell
            if i:
                c.cmf.topology.AddNeighbor(c_last,length)
                c_last.topology.AddNeighbor(c.cmf,length)
            c_last=c.cmf
            self.cells.append(c)
    
        cmf.connect_cells_with_flux(p, cmf.Richards_lateral)
        cmf.connect_cells_with_flux(p, cmf.Manning_Kinematic)
        #Create an outlet at the bottom of the slope
        self.outlet=cmf.DricheletBoundary(p,-.5,cmf.point(-5,0,-.5))
        self.outlet.Name='Outlet'
        p[0].connect_soil_with_node(self.outlet,cmf.Richards_lateral,length,0.5 * length)
        # Connect surface water of cell 0 with outlet
        cmf.connect(cmf.Manning_Kinematic,p[0].surfacewater,self.outlet,cmf.Channel('R',10.0,10.0))     
        winteg=cmf.CVodeIntegrator(1e-6)
        winteg.preconditioner='R'
        sinteg=cmf.BDF2(1e-6)
        self.integrator=cmf.SoluteWaterIntegrator(winteg,sinteg,p)
        if meteo_station_name:
            self.load_meteo(meteo_station_name, 1.0)
    def run(self, until, dt):
        while self.t < until:
            for c in self.cells:
                c.run(self.t,dt.AsDays())
            self.integrator(dt)
            yield self.t
        
    def __get_t(self):
        """The model time"""
        return self.integrator.t.AsPython()  
    def __set_t(self,time):
        self.integrator.t=time        
    t=property(__get_t,__set_t)
    def load_meteo(self,stationname='Giessen',rain_factor=1.):
        # Load rain timeseries (doubled rain of giessen for more interstingresults)
        rain=cmf.timeseries.from_file(stationname + '.rain')*rain_factor
        # Create a meteo station
        meteo=self.project.meteo_stations.add_station(stationname)
        # Meteorological timeseries
        meteo.Tmax=cmf.timeseries.from_file(stationname+'.Tmax')
        meteo.Tmin=cmf.timeseries.from_file(stationname+'.Tmin')
        meteo.rHmean=cmf.timeseries.from_file(stationname+'.rHmean')
        meteo.Windspeed=cmf.timeseries.from_file(stationname+'.Windspeed')
        meteo.Sunshine=cmf.timeseries.from_file(stationname+'.Sunshine')
        # Use the rainfall for each cell in the project
        cmf.set_precipitation(self.project.cells,rain)
        # Use the meteorological station for each cell of the project
        cmf.set_meteo_station(self.project.cells,meteo)

    def draw(self,solute=None,plot=None):
        if not plot:
            hp = cmf.draw.hill_plot(cells=self.project, t=self.integrator.t, solute=solute)
            plant_bars = pylab.bar(left  = [c.x - sqrt(c.area)*.125 for c in self.project],
                                   width = [sqrt(c.cmf.area)*.25  for c in self.cells],
                                   height = [c.biomass / 1500 for c in self.cells] ,
                                   bottom = [c.z for c in self.project], fc='g')
            return hp,plant_bars
        else:
            hp,plant_bars=plot
            for i,c in enumerate( self.cells):
                plant_bars[i].set_height(c.biomass / 1500 )
            hp(t=self.integrator.t,solute=solute)
            
                
            



slope = Slope(count=20,slope_exponent=2, meteo_station_name='giessen') 
slope.t = cmf.Time(1,3,1980)
N,DOC=slope.project.solutes
for c in slope.cells[5:]:
    c.fertilize(50)
    c.sow()
runner=slope.run(datetime(1981,1,1),cmf.day)
pylab.subplot(211)
wet_plot=slope.draw()
wet_plot[0].scale=25
pylab.xlim(-5,195)
pylab.subplot(212)
N_plot=slope.draw(N)
N_plot[0].scale=25
pylab.xlim(-5,195)

def run():
    runner.next()
    slope.draw(plot=wet_plot)
    slope.draw(plot=N_plot,solute=N)
