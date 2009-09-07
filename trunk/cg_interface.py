from pylab import *
from CG_plant import *
import cmf
from cmf_setup import cmf1d
import struct
def load_dwd(c):
    #Load meteo data
    import cmf.cmfDWD as dwd
    # Load meteoroligical stations
    MeteoStations=dwd.GetMeteorology(c.project,'dwddaten/kl_bestand_abgabe440_1','dwddaten/kl_satz_abgabe440_1','dwddaten/kl_dat_abgabe440_1',cmf.Time(1,1,1980),cmf.Time(1,1,2006))
    # Load rainfall stations
    rainfall=dwd.get_rainfall('dwddaten/rr_dat_abgabe440')
    # Set Giessen as actual meteo station
    c.cell.meteorology=cmf.MeteoStationReference( MeteoStations['02609'],c.cell)
    # Set Giessen as rainfall station
    c.cell.rain.flux=rainfall['76148']
def load_meteo(project):
    # Load rain timeseries (doubled rain of giessen for more intersting results)
    rain=cmf.timeseries.from_file('giessen.rain')*2
    # Create a meteo station
    meteo=project.meteo_stations.add_station('Giessen')
    # Meteorological timeseries
    meteo.Tmax=cmf.timeseries.from_file('giessen.Tmax')
    meteo.Tmin=cmf.timeseries.from_file('giessen.Tmin')
    meteo.rHmean=cmf.timeseries.from_file('giessen.rHmean')
    meteo.Windspeed=cmf.timeseries.from_file('giessen.Windspeed')
    meteo.Sunshine=cmf.timeseries.from_file('giessen.Sunshine')
    # Use the rainfall for each cell in the project
    cmf.set_precipitation(project.cells,rain)
    # Use the meteorological station for each cell of the project
    cmf.set_meteo_station(project.cells,meteo)
def create_cmf():
    # Create a soil column
    c=cmf1d(sand=60,silt=30,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    load_dwd(c)
    c.cell.saturated_depth=2.5
    return c
def run(time_act,time_end,time_step):
    pass
def show_graph():
    hold=0
    fig=figure()
    fig.add_subplot(421)
    plot(thermaltime,label='thermaltime')
    legend(loc=0)
    ylabel('GDD')
    grid()
    
    fig.add_subplot(423)
    plot(biomass_plant,label='Plant')
    plot(biomass_root,label='Root')
    plot(biomass_shoot,label='Shoot')
    plot(biomass_stem,label='Stem')
    plot(biomass_leaf,label='Leaf')
    plot(biomass_storage,label='Storage')
    legend(loc=0)
    ylabel('biomass in g')
    grid()
    
    fig.add_subplot(422)
    plot(rooting_depth,label='rooting_depth')
    legend(loc=0)
    ylabel('cm')
    ylim(-200,0.)
    grid()
    
    fig.add_subplot(424)
    imshow(transpose(wetness),cmap=cm.RdYlBu,aspect='auto')
    colorbar()
    grid()
    ylabel('wetness')
    
    fig.add_subplot(426)
    #contourf(matrix_potential,[0,-0.01,-0.1,-1,-5,-10,-100,-160])
    imshow(log10(-transpose(matrix_potential)*100),cmap=cm.jet,aspect='auto',interpolation='nearest')
    colorbar()
    xlabel('Time in days')
    ylabel('pF')
    grid()
    
    fig.add_subplot(428)
    imshow(transpose(flux),cmap=cm.RdYlBu,aspect='auto',interpolation='nearest')
    xlabel('Time in days')
    ylabel('flux') 
    colorbar()
    grid()

    fig.add_subplot(427)
    plot(shoot_fraction,label='shoot')
    plot(root_fraction,label='root')
    legend(loc=0)
    ylim(-0.1,1.1)
    xlabel('Time in days')
    ylabel('fraction') 
    grid()
    
    fig.add_subplot(425)
    plot(leaf_fraction,label='leaf')
    plot(stem_fraction,label='stem')
    plot(storage_fraction,label='storage')
    legend(loc=0)
    ylim(-0.1,1.1)
    xlabel('Time in days')
    ylabel('fraction') 
    grid()
    show()
def set_results():    
    if plant.stage.is_growingseason(plant.thermaltime)==True:
        c.flux=[s_h*-1. for s_h in plant.s_h]
        biomass_plant.append(plant.Wtot);biomass_shoot.append(plant.shoot.Wtot)
        biomass_root.append(plant.root.Wtot);biomass_stem.append(plant.shoot.stem.Wtot)
        biomass_leaf.append(plant.shoot.leaf.Wtot);biomass_storage.append(plant.shoot.storage_organs.Wtot)
        thermaltime.append(plant.thermaltime);rooting_depth.append(plant.root.depth*-1.)
        root_fraction.append(plant.root.fraction(plant.thermaltime))
        shoot_fraction.append(plant.shoot.fraction(plant.thermaltime))
        leaf_fraction.append(plant.shoot.leaf.fraction(plant.thermaltime))
        stem_fraction.append(plant.shoot.stem.fraction(plant.thermaltime))
        storage_fraction.append(plant.shoot.storage_organs.fraction(plant.thermaltime))
    else:
        c.flux=[0]*50
        biomass_plant.append(0);biomass_shoot.append(0)
        biomass_root.append(0);biomass_stem.append(0)
        biomass_leaf.append(0);biomass_storage.append(0)
        thermaltime.append(0);rooting_depth.append(0)
        root_fraction.append(0)
        shoot_fraction.append(0)
        leaf_fraction.append(0)
        stem_fraction.append(0)
        storage_fraction.append(0)  
    matrix_potential.append(c.matrix_potential);wetness.append(c.wetness);flux.append(c.flux)
def show_results():
    if i%7==0:
        print c.t,'water uptake', '%4.2f' % sum(plant.s_h), 'Wpot','%4.2f' % plant.Wpot,'Wact','%4.2f' % plant.Wact,'Wtot','%4.2f' % plant.Wtot,'stress response',plant.stress    
def isharvest(time_act,harvest_date):
    for date in harvest_date:
        if time_act==date:
            return True
            break
def issowing(time_act,sowing_date):
    for date in sowing_date:
        if time_act==date:
            return True
            break
def create_plant():
    stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
            ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',3000.]]#'Maturity',1665.
    #Parameter for partitioning:
    root_fraction=[[160.,1.],[901.,0.5],[1665.,0.]]
    shoot_fraction=[[160.,0.],[901.,0.5,],[1665.,1.,]]
    leaf_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
    stem_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
    storage_fraction=[[160.,0.],[901.,0.0],[1174.,0.25],[1665.,1.]]
    #Create plant with default values
    p=Plant(stage,root_fraction,shoot_fraction,leaf_fraction,stem_fraction,storage_fraction)
    return p
def set_management():
    sowing_dates=[t.datetime(1991,3,1),t.datetime(1992,3,1),t.datetime(1993,3,1),t.datetime(1994,3,1),t.datetime(1995,3,1)
                  ,t.datetime(1996,3,1),t.datetime(1997,3,1),t.datetime(1998,3,1),t.datetime(1999,3,1),t.datetime(2000,3,1)
                  ,t.datetime(1980,3,1),t.datetime(1981,3,1),t.datetime(1982,3,1),t.datetime(1983,3,1),t.datetime(1984,3,1)
                  ,t.datetime(1985,3,1),t.datetime(1986,3,1),t.datetime(1987,3,1),t.datetime(1988,3,1),t.datetime(1989,3,1)
                  ,t.datetime(1990,3,1)]
    harvest_dates=[t.datetime(1991,9,30),t.datetime(1992,9,30),t.datetime(1993,9,30),t.datetime(1994,9,30),t.datetime(1995,9,30)
                  ,t.datetime(1996,9,30),t.datetime(1997,9,30),t.datetime(1998,9,30),t.datetime(1999,9,30),t.datetime(2000,9,30)
                  ,t.datetime(1980,9,30),t.datetime(1981,9,30),t.datetime(1982,9,30),t.datetime(1983,9,30),t.datetime(1984,9,30)
                  ,t.datetime(1985,9,30),t.datetime(1986,9,30),t.datetime(1987,9,30),t.datetime(1988,9,30),t.datetime(1989,9,30)
                  ,t.datetime(1990,9,30)]
    return [sowing_dates,harvest_dates]         
class Soil:
    """call siganture:
    
        Soil(cmf1d)
        
    Soil implements the interface for the interactions between
    cmf1d and the crop growth model.
    
    Cmf1d must be implementated from the corresponding class.
    """
    def __init__(self,cmf1d):
        self.cmf1d=cmf1d
    def get_pressurehead(self,depth):
        """ Depth in cm; Returns the capillary suction in cm for a given depth."""
        d=depth-1.
        layer=self.layer(d/100.)
        if self.cmf1d.matrix_potential[layer]>0:
            return 0
        else: return -self.cmf1d.matrix_potential[layer]*100 
    def get_porosity(self,depth):
        """ Depth in cm; Returns the porosity in m3/m3 of the soil in the given depth."""
        layer=self.cmf1d.layer(depth/100)
        return self.cmf1d.get_porosity(layer)
    def get_nutrients(self,depth):
        """ Depth in cm; Returns 0.5"""
        return 0.5
    def get_bulkdensity(self,depth):
        """ Depth in cm; Returns 1.5"""
        return 1.5
    def get_profile(self):
        """ Returns a list with the lower limits of the
            layers in the soilprofile in cm.
        """
        return [l.boundary[1]*100. for l in self.cmf1d.cell.layers]
    def layer(self,depth):
        return min(int(depth/0.1),len(self.cmf1d.cell.layers)-1)



class Atmosphere:
    """call siganture:
    
        Atmosphere(cmf1d)
        
    Atmosphere implements the interface for the interactions between
    cmf1d and the crop growth model.
    
    Cmf1d must be implementated from the corresponding class.
    """
    def __init__(self,cmf1d):
        self.cmf1d=cmf1d
    def get_tmin(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal Temperature at time """
        return self.cmf1d.cell.get_weather(time).Tmin
    def get_tmax(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal Temperature at time """
        return self.cmf1d.cell.get_weather(time).Tmax
    def get_etp(self,time):
        """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns 5.0 """
        return 5.

if __name__=='__main__':
    import datetime as t
    sowing_date=set_management()[0];harvest_date=set_management()[1]
    c=create_cmf()
    soil=Soil(c)
    atmosphere=Atmosphere(c)
    time_act=t.datetime(1980,1,1)
    time_step=t.timedelta(1)
    c.t=time_act
    i=0
    biomass_plant=[];biomass_shoot=[];biomass_root=[];biomass_stem=[]
    biomass_leaf=[];biomass_storage=[];thermaltime=[];rooting_depth=[]
    water_uptkake=[];nutrient_uptake=[]
    shoot_fraction=[];root_fraction=[]
    matrix_potential=[];wetness=[];flux=[]
    root_fraction=[];shoot_fraction=[];
    leaf_fraction=[];stem_fraction=[];
    storage_fraction =[]
    harvest=[]
    
    while time_act<t.datetime(2000,12,31):
        i+=1
        
        if issowing(time_act,sowing_date)==True:
            plant=create_plant()
            
            print 'Sowing'
        if isharvest(time_act,harvest_date)==True:
            harvest.append(plant.Wtot)
            del plant
            print 'Harvest'
        try:
            plant(c.t,'day',1.,soil,atmosphere)
            if plant.stage.is_growingseason(plant.thermaltime)==True:
                c.flux=[s_h*-1. for s_h in plant.s_h]
                biomass_plant.append(plant.Wtot);biomass_shoot.append(plant.shoot.Wtot)
                biomass_root.append(plant.root.Wtot);biomass_stem.append(plant.shoot.stem.Wtot)
                biomass_leaf.append(plant.shoot.leaf.Wtot);biomass_storage.append(plant.shoot.storage_organs.Wtot)
                thermaltime.append(plant.thermaltime);rooting_depth.append(plant.root.depth*-1.)
                root_fraction.append(plant.root.fraction(plant.thermaltime))
                shoot_fraction.append(plant.shoot.fraction(plant.thermaltime))
                leaf_fraction.append(plant.shoot.leaf.fraction(plant.thermaltime))
                stem_fraction.append(plant.shoot.stem.fraction(plant.thermaltime))
                storage_fraction.append(plant.shoot.storage_organs.fraction(plant.thermaltime))
        except NameError:
            c.flux=[0]*50
            biomass_plant.append(0);biomass_shoot.append(0)
            biomass_root.append(0);biomass_stem.append(0)
            biomass_leaf.append(0);biomass_storage.append(0)
            thermaltime.append(0);rooting_depth.append(0)
            root_fraction.append(0)
            shoot_fraction.append(0)
            leaf_fraction.append(0)
            stem_fraction.append(0)
            storage_fraction.append(0)  
        matrix_potential.append(c.matrix_potential);wetness.append(c.wetness);flux.append(c.flux)     
        c.run(cmf.day)
        time_act+=time_step
        #print c.t
        if i%7==0:
            print c.t, 'pF',['%4.2f' % pF for pF in c.pF][:10]
        #    print '%4.2f' % atmosphere.get_tmin(time_act),'%4.2f' % atmosphere.get_tmax(time_act)
      
        
        
annual_wetness=[sum(w) for w in wetness]
annual_flux=[sum(f) for f in flux]

show_graph()
f=figure()
f.add_subplot(311)
plot(annual_wetness,label='wetness')
legend(loc=0)
f.add_subplot(312)
plot(annual_flux,label='flux')
legend(loc=0)
f.add_subplot(313)
plot(biomass_plant,label='biomass')
legend(loc=0)
show()

    
 
 


