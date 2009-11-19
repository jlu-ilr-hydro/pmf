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
from matplotlib import pyplot
from math import sqrt
import numpy as np
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
        for i in range(layer_count):
            d=(i+1) * layer_thickness 
            self.cmf.add_layer(d,r_curve)
            nbc=cmf.NeumannBoundary.create(self.cmf.layers[-1])
            nbc.get_connection(self.cmf.layers[-1]).tracer_filter=0.0
            self.__bc.append(nbc)
        # Make DECOMP cell
        self.DECOMP=DECOMPcmf(self.cmf)
        # plant and baresoil
        self.N = cmf_project.solutes[0]
        self.plant_interface = cmf_fp_interface(self.cmf, self.N)
        #self.plant_interface.default_Nconc = .3
        self.plant=None
        self.baresoil=FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    def sow(self):
        """Creates a FlowerPower standard crop at this location
        """
        self.plant = FlowerPower.connect(FlowerPower.createPlant_CMF(),
                                         self.plant_interface,
                                         self.plant_interface)
        self.plant.nitrogen.Km = 27 * 62e-6
        self.plant.nitrogen.NO3min = 0.1e-3 # g/l
        self.plant.nitrogen.max_passive_uptake = 0.0 # g/l
    def harvest(self):
        """
        @todo: Put residual biomass to first layer
        """
        litter_C = (self.plant.StemCarbon + self.plant.LeafCarbon) * self.cmf.area
        litter_N = (self.plant.StemNitrogen + self.plant.LeafNitrogen) * self.cmf.area
        litter = DECOMP.SOM(litter_N,0.1 * litter_C, 0.5 * litter_C, 0.4 * litter_C,0.0)
        
        self.DECOMP.DECOMPlayers[0] += litter
        for i in range(self.cmf.layer_count()):
            root_M = self.plant.root.branching[i] 
            root_C = root_M * 0.4
            root_N = root_M * 0.01
            root = DECOMP.root_litter() * root_C
            root.N = root_M * 0.01
        self.plant=None
        # return biomass
    def fertilize(self,kgN_ha,is_manure=1):
        """Adds to the SOM of the first layer easily decomposable SOM components 
        with a C/N ratio of 10
        @type kgN_ha: Amount of fertilizer in kg N per ha. 
        """
        #    kgN/ha * g/kg  *      m2       * ha/m2
        gN = kgN_ha * 1000. * self.cmf.area * 1e-4
        if is_manure:
            # Create a fertilizer with a C/N ratio 10, made of easily decomposable components
            fertilizer = DECOMP.SOM(gN, 10 * gN)
            # Add fertilizer to first layer
            self.DECOMP.DECOMPlayers[0] += fertilizer
        else:
            # Put N directly into the soil solution
            self.cmf.layers[0].Solute(self.N).state += gN
    @property
    def shoot_carbon(self):
        if self.plant:
            return self.plant.ShootCarbon
        else:
            return 0.0
    @property
    def biomass(self):
        return self.plant.biomass.Total if self.plant else 0.0
    @property
    def root_mass(self):
        if self.plant:
            return self.plant.root.branching
        else:
            return [0.0] * self.cmf.layer_count()
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
                l.Solute(N).source -= self.plant.nitrogen.Total[i] * self.cmf.area
        else:
            c=self.plant_interface
            self.baresoil(c.Kr(),0.,c.get_Rn(t, 0.12, True),c.get_tmean(t),c.get_es(t),c.get_ea(t), c.get_windspeed(t),0.,RHmin=30.,h=1.)
        #Get the water flux from soil to plant
        flux     = [-uptake for uptake in self.plant.Wateruptake] if self.plant else [0.0] * self.cmf.layer_count()
        flux[0] -= self.plant.et.evaporation if self.plant else self.baresoil.evaporation
        # Set flux at the cmf boundary conditions
        for i,bc in enumerate(self.__bc):
            bc.flux=cmf.timeseries(flux[i] * self.cmf.area / 1000.0) # Convert from mm to m3
    
class Slope(object):
    def __init__(self,count=20,length=10,slope=0.05,slope_exponent=1,meteo_station_name=None,soildepth=3.0):
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
                     soildepth=soildepth, layer_thickness=0.1, 
                     sand=100, silt=0, clay=0, c_org=2)
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
        self.outlet=cmf.DricheletBoundary(p,-.25,cmf.point(-0.5 * length,0,-.5))
        self.outlet.Name='Outlet'
        self.outlet.is_source=True
        p[0].connect_soil_with_node(self.outlet,cmf.Richards_lateral,length,0.5 * length)
        # Connect surface water of cell 0 with outlet
        cmf.connect(cmf.Manning_Kinematic,p[0].surfacewater,self.outlet,cmf.Channel('R',10.0,10.0))     
        winteg=cmf.CVodeIntegrator(1e-6)
        winteg.preconditioner='R'
        sinteg=cmf.ImplicitEuler(1e-6)
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
    def __getitem__(self,index):
        return self.cells[index]
    
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
        Nconc=cmf.timeseries(2.34)
        for c in self.project:
            c.rain.concentration[self.N] = Nconc

class slope_fig(object):
    def __init__(self,slope,solute=None):
        self.slope=slope
        self.solute=solute
        self.hp = cmf.draw.hill_plot(cells=slope.project, t=slope.integrator.t, solute=solute)
        if solute:
            self.hp.evalfunction = lambda l: l.conc(N) / 100
            self.hp.cmap = pyplot.cm.Oranges
        else:
            self.hp.cmap = pyplot.cm.RdYlBu
            self.hp.evalfunction = lambda l: (l.wetness - l.soil.Wetness_pF(3.))/(1-l.soil.Wetness_pF(3.))  
        self.plant_bars = pyplot.bar(left  = [c.x - sqrt(c.area)*.25 for c in slope.project],
                               width = [sqrt(c.cmf.area)*.5  for c in slope.cells],
                               height = [c.biomass / 1000 for c in slope.cells] ,
                               bottom = [c.z for c in slope.project], fc='g')
        self.root_bars=[]
        for c in slope:
            self.root_bars.append(pyplot.bar(left = [c.cmf.x - b/20 for b in c.root_mass],
                                  width = [b/10 for b in c.root_mass],
                                  bottom = [c.cmf.z - l.lower_boundary for l in c.cmf.layers],
                                  height = [l.thickness for l in c.cmf.layers],
                                  fc='k',alpha=0.5))
    def __call__(self,text=''):
        for i,c in enumerate(self.slope.cells):
            self.plant_bars[i].set_height(c.biomass / 1000 )
            if c.plant:
                stress = c.plant.nutrition_stress if self.solute else c.plant.water_stress
                self.plant_bars[i].set_color(pyplot.cm.RdYlGn_r(stress))
            root_mass=c.root_mass
            for j in range(c.cmf.layer_count()):
                self.root_bars[i][j].set_width(root_mass[j]/10)
                self.root_bars[i][j].set_x(c.cmf.x - root_mass[j]/20)
        self.hp(t=self.slope.integrator.t,text=text)
            
                
            



slope = Slope(count=20,slope_exponent=2, meteo_station_name='giessen') 
slope.t = cmf.Time(1,1,1980)

for c in slope:
    for i in range(3):
        c.DECOMP.DECOMPlayers[i] = DECOMP.SOM(0.05 * 3000,0,0,50,2950) * c.cmf.area
print cmf.VERSION
N,DOC=slope.project.solutes
pyplot.subplot(211)
wet_plot=slope_fig(slope)
wet_plot.hp.scale=25
pyplot.xlim(slope[0].cmf.x - 5,slope[-1].cmf.x + 5)
pyplot.subplot(212)
N_plot=slope_fig(slope,N)
N_plot.hp.scale=25
pyplot.xlim(slope[0].cmf.x - 5,slope[-1].cmf.x + 5)
title=''    
runner=slope.run(datetime(1986,1,1),cmf.day)
cumNupt=0
cumNout=0 
cumNdem=0
Nupt=[]
Ndem=[]
Nsol=[]
for i,t in enumerate(runner):
    if t.month == 3 and t.day == 1:
        for c in slope.cells:
            c.fertilize(20,True)
            c.sow()
            title='sowing'

    if (t.month == 3 and t.day == 10) or (t.month == 5 and t.day == 10):
        for c in slope.cells:
            c.fertilize(80,False)
            title='80 kgN/ha'
    if t.month == 8 and t.day == 2:
        for c in slope.cells:
            c.harvest()
            title='harvest'
    print slope.integrator.t,"biomass =%7.5gkg/ha" % (slope[-1].biomass * 10),
    print "Nsol = %7.5gkg/ha" % (sum(l.Solute(N).state for l in list(slope[-1].cmf.layers)[:10])/slope[-1].cmf.area*10),
    plant=slope[-1].plant
    Nsol.append(sum(l.Solute(N).state for l in list(slope[-1].cmf.layers)[:10])/slope[-1].cmf.area*10)
    if plant:
        cumNdem += plant.Rp * 10
        cumNupt += sum(plant.nitrogen.Total) * 10
        cumNout += slope.outlet.water_balance(t) * slope.outlet.conc(t,N) / (slope[-1].cmf.area) * 10 
        print "cumNupt = %7.5gkg/ha, cumNout = %7.5gkg/ha" % (cumNupt, cumNout)
    else:
        cumNupt=0
        cumNout=0 
        cumNdem=0
        print
    wet_plot()
    N_plot(title)
    title=''
    pyplot.savefig('fp_images/hill%05i.png' % i,dpi=75)
        
    Nupt.append(cumNupt)
    Ndem.append(cumNdem)

pyplot.plot(Nupt,label='Uptake')
pyplot.plot(Ndem,label='Demand')
pyplot.plot(Nsol,label='Storage')
pyplot.legend()
pyplot.show()
