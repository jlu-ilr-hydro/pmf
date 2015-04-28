# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 16:51:30 2015

@author: kellner-j
"""

import cmf
import numpy as np
from traceback import format_exc as traceback
from pylab import *
from datetime import datetime, date, time, timedelta



class cmf1d(object):
    def __init__(self,DataStart_gw,DataEnd_gw,load_gw_data,Datenstart,Ksat_1,Ksat_2,Ksat_3,porosity_1,porosity_2,porosity_3,alpha_1,alpha_2,alpha_3,
                             n_1,n_2,n_3,layers,tracertext=''): #,ldepth
#    def __init__(self,Ksat,porosity,alpha,n,layercount,layerthickness,tracertext,Datenstart,start, stationname):
        """Creates a Richards Equation 1D model of water fluxes with a lower constant head boundary condition
        to the groundwater and flux (Neumann) boundary condition for each layer for ET
        Ksat: sat. conductivity in m/day eg. 1.3
        porosity: porevolume per soil volume in m³/m³ eg. 0.45
        alpha: VanGenuchten alpha in 1/cm eg. 0.01
        n: VanGenuchten n, eg. 1.9
        bedrock_K: Conductivity of the bedrock in m/day eg. 1.3
        layercount = layers : Number of layers, eg. 50
        layerthickness = ldepth: sequence of layer thickness in m
        tracertext: cmf conform string, describing the available tracers
        """        
     
#        # Add 50 layers with 10cm thickness, and 50 Neumann boundary conditions
        self.__bc=[]  # boundary condition

    
        self.DataStart_gw=DataStart_gw
        self.DataEnd_gw=DataEnd_gw
        
        self.Datenstart = Datenstart
        self.project=cmf.project()
        self.cell = self.project.NewCell(x=0,y=0,z=0,area=1000, with_surfacewater=True)
        c=self.cell
#        print 'n= '+str(n)
#        print 'alpha='+str(alpha)
#        print 'Ksat= '+str(Ksat)
#        print 'porosity= '+str(porosity)
#        print '##############################'
        print 'n_1= '+str(n_1),'n_2= '+str(n_2),'n_3= '+str(n_3)
        print 'alpha_1= '+str(alpha_1),'alpha_2= '+str(alpha_2),'alpha_3= '+str(alpha_3)
        print 'porosity_1= '+str(porosity_1),'porosity_2= '+str(porosity_2),'porosity_3= '+str(porosity_3)
        print 'Ksat_1= '+str(Ksat_1), 'Ksat_2= '+str(Ksat_2), 'Ksat_3= '+str(Ksat_3)
        r_curve_1 = cmf.VanGenuchtenMualem(Ksat=Ksat_1,phi=porosity_1,alpha=alpha_1,n=n_1)
        r_curve_2 = cmf.VanGenuchtenMualem(Ksat=Ksat_2,phi=porosity_2,alpha=alpha_2,n=n_2)
        r_curve_3 = cmf.VanGenuchtenMualem(Ksat=Ksat_3,phi=porosity_3,alpha=alpha_3,n=n_3)
#        ldepth =0.05
#        for i in range(layers):
#            depth = (i+1) * ldepth         #depth: 0.05, 0.1, 0.15, 0.2,...0.95
#            c.add_layer(depth,r_curve)     #equidistant

#        for i in range(1,layers+1):
#            depth = 0.005*(i+1)**2 - 0.005*(i+1)    #depth: 0.01, 0.03, 0.06, 0.1, 0.15, 0.21,...,1.9
#            print depth                             #polygonal 
#            c.add_layer(depth,r_curve)       
#            # create neumann boundary condition for ET from PMF
#            nbc=cmf.NeumannBoundary.create(c.layers[-1])
#            nbc.Name="Boundary condition #%i" % (i)
#            self.__bc.append(nbc)         
        for i in range(1,5):
            depth = 0.005*(i+1)**2 - 0.005*(i+1)    #depth: 0.01, 0.03, 0.06, 0.1
            print depth                             #polygonal 
            c.add_layer(depth,r_curve_1)       
            # create neumann boundary condition for ET from PMF
            nbc=cmf.NeumannBoundary.create(c.layers[-1])
            nbc.Name="Boundary condition #%i" % (i)
            self.__bc.append(nbc)  

        for i in range(5,9):
            depth = 0.005*(i+1)**2 - 0.005*(i+1)    #depth: 0.15, 0.21, 0.28, 0.36
            print depth                             #polygonal 
            c.add_layer(depth,r_curve_2)       
            # create neumann boundary condition for ET from PMF
            nbc=cmf.NeumannBoundary.create(c.layers[-1])
            nbc.Name="Boundary condition #%i" % (i)
            self.__bc.append(nbc)     
            
        for i in range(9,layers+1):
            depth = 0.005*(i+1)**2 - 0.005*(i+1)    #depth: 0.45, 0.55, ..., 1.71
            print depth                             #polygonal 
            c.add_layer(depth,r_curve_3)       
            # create neumann boundary condition for ET from PMF
            nbc=cmf.NeumannBoundary.create(c.layers[-1])
            nbc.Name="Boundary condition #%i" % (i)
            self.__bc.append(nbc)     

            
        # Use Richards equation for percolation
        c.install_connection(cmf.Richards)
#        c.install_connection(cmf.ShuttleworthWallace)
        c.saturated_depth =.5   #für die Anfangsbedingung
        self.integrator = cmf.CVodeIntegrator(self.project,1e-6)      # solver for Richards equation            

         
        
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
    def porosity(self):
        """The porosity value for each layer """
        return [l.porosity for l in self.cell.layers]
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
        return -self.load_data.groundwater.waterbalance(self.t)
    @property
    def percolation(self):
        return [self.cell.layers[i].flux_to(self.cell.layers[i+1] if i+1< self.cell.layer_count() else self.load_data.groundwater,self.t) for i in range(self.cell.layer_count())]
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
    
    
   
    def load_meteo(self,Datenstart,start, stationname, rain_factor=1.): # am Besten mit in Sensitiv_Analysis_I aufnehmen 

        """
        Loads the meteorology from a csv file.
        """
        
        # Create a timeseries for rain - timeseries objects in cmf is a kind of extensible array of 
        # numbers, with a begin date, a timestep.
        #begin = datetime(1992,1,1)
        #begin = get_starttimeT()
        begin=start
        Differenz = start-Datenstart
        Sprung = Differenz.days +1
        
        rain = cmf.timeseries(begin = begin, step = timedelta(days=1))
        
        Split_stationname =stationname.split('.')
        
    
        # Create a meteo station
        meteo=self.project.meteo_stations.add_station(Split_stationname[0],position = (0,0,0))
    
        # Meteorological timeseries, if you prefer the beginning of the timeseries
        # read in from file, just go ahead, it is only a bit of Python programming
        meteo.Tmax      = cmf.timeseries(begin = begin, step = timedelta(days=1))
        meteo.Tmin      = cmf.timeseries(begin = begin, step = timedelta(days=1))
        meteo.rHmean    = cmf.timeseries(begin = begin, step = timedelta(days=1))# als RHmin das Minimum aus Rh14uhr und Rhmean nehmen, Rhmean braucht python nicht. Rhmax auf 100 setzen. Sind das wirklich Rh Daten bei Muencheberg oder ist das das Saettigungsdefizit? Ueberpruefen!
#        meteo.rHmax     = cmf.timeseries(begin = begin, step = timedelta(days=1))        
        meteo.Windspeed = cmf.timeseries(begin = begin, step = timedelta(days=1))
#        meteo.Sunshine  = cmf.timeseries(begin = begin, step = timedelta(days=1)) # sind cloud daten 1-(cloud/100)
        meteo.e_a       = cmf.timeseries(begin = begin, step = timedelta(days=1))
        meteo.e_s       = cmf.timeseries(begin = begin, step = timedelta(days=1))        
        meteo.Rs        = cmf.timeseries(begin = begin, step = timedelta(days=1))
        #meteo.Cloud     = cmf.timeseries(begin = begin, step = timedelta(days=1)) # so nicht cloud = sunshine
        meteo.T         = (meteo.Tmax + meteo.Tmin) * 0.5
        
              
        # Load climate data from csv file
        # could be simplified with numpy's 
        csvfile =file(stationname) 
        for i in range(Sprung):
            csvfile.readline()        
        #csvfile.readline() # Read the headers, and ignore them
        for line in csvfile:
            columns = line.split(';')
            # Get the values, but ignore the date, we have begin and steo
            # of the data file hardcoded
            # If you don't get this line - it is standard Python, I would recommend the official Python.org tutorial
#            for timeseries,value in zip([rain,meteo.Tmax,meteo.Tmin,meteo.rHmean,meteo.Windspeed,meteo.e_a,meteo.e_s,meteo.Rs], #zip fuegt zwei Listen zu einer Zusammen
#                                       [float(col) for col in columns[2:10]]):    
            for timeseries,value in zip([rain,meteo.Tmax,meteo.Tmin,meteo.rHmean,meteo.Windspeed,meteo.Rs], #zip fuegt zwei Listen zu einer Zusammen
                                       [float(col) for col in columns[1:7]]): 
#                print columns[1:8]
                # Add the value from the file to the timeseries
                timeseries.add(value)
                
            #print line
        # Create a rain gauge station
        self.project.rainfall_stations.add(stationname,rain,(0,0,0))
        
        
        
        
        # Use the rainfall for each cell in the project
        self.project.use_nearest_rainfall()
        # Use the meteorological station for each cell of the project
        self.project.use_nearest_meteo()
    
    Plot=[]        
    Datum=[]
    Jahr=[]
    Monat=[]
    Tag=[]
    Julian_Day=[]
    water0_30=[]
    water30_60=[]
    water60_90=[] 
    
    
    def load_water_content(self,Dateiname):
#    def load_water_content(self,Dateiname, Date):               
        water_content_file =file(Dateiname) 
        water_content_file.readline()        
        #csvfile.readline() # Read the headers, and ignore them
        for line in water_content_file:
            columns = line.split(';')
            # Get the values, but ignore the date, we have begin and steo
            # of the data file hardcoded          
            # If you don't get this line - it is standard Python, I would recommend the official Python.org tutorial
            cmf1d.Plot.append(columns[0])            
            cmf1d.Datum.append(columns[1])
            cmf1d.Jahr.append(columns[2])
            cmf1d.Monat.append(columns[3])
            cmf1d.Tag.append(columns[4])
            cmf1d.Julian_Day.append(columns[5])
            cmf1d.water0_30.append(columns[6])
            cmf1d.water30_60.append(columns[7])
            cmf1d.water60_90.append(columns[8])
        #print '# Water_content_Kersebaum #'    
        #print '\nWassergehalt [%] gemessen fuer: ' + Datum[Date]
        #print 'Wassergehalt 0 bis 30 cm:'
        #print str(water0_30[Date])
        #print 'Wassergehalt 30 bis 60 cm:'
        #print str(water30_60[Date])
        #print 'Wassergehalt 60 bis 90 cm:'
        #print str(water60_90[Date])
        
                    
#if __name__=='__main__':
#    c1=cmf1d()
#    print "gw_flux=",c1.groundwater_flux
    #print "P(750cm)=",c1.get_pressurehead(750)
    