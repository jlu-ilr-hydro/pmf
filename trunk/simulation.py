from pylab import *
from FlowerPower import *
import cmf
from cmf_setup import cmf1d
import struct
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
    rain=timeseries_from_file(stationname + '.rain')*0.5
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
    #legend(loc=0)
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
    imshow(transpose(pF),cmap=cm.jet,aspect='auto',interpolation='nearest',vmin=0.0,vmax=4.5)
    colorbar()
    xlabel('Time in days')
    ylabel('pF')
    grid()
    
    fig.add_subplot(428)
    imshow(transpose(flux),cmap=cm.RdYlBu,aspect='auto',interpolation='nearest',vmin=-5.0,vmax=0.0)
    xlabel('Time in days')
    ylabel('flux') 
    colorbar()
    grid()

    fig.add_subplot(427)
    plot(shoot_fraction,label='shoot')
    plot(root_layer,label='root')
    legend(loc=0)
    ylim(-0.1,1.1)
    xlabel('Time in days')
    ylabel('fraction') 
    grid()
    """
    fig.add_subplot(425)
    plot(leaf_fraction,label='leaf')
    plot(stem_fraction,label='stem')
    plot(storage_fraction,label='storage')
    legend(loc=0)
    ylim(-0.1,1.1)
    xlabel('Time in days')
    ylabel('fraction') 
    grid()
    """
    fig.add_subplot(425)
    ETact=-1*sum(flux,1)
    plot(ETpot,label='ETpot')
    plot(ETact,label='ETact')
    legend(loc=0)
    #ylim(-0.1,1.1)
    xlabel('Time in days')
    ylabel('mm/day') 
    grid()
    show()
def set_results():    
    try:
        biomass_plant.append(plant.biomass.Total);biomass_shoot.append(plant.shoot.Wtot)
        biomass_root.append(plant.root.Wtot);biomass_stem.append(plant.shoot.stem.Wtot)
        biomass_leaf.append(plant.shoot.leaf.Wtot);biomass_storage.append(plant.shoot.storage_organs.Wtot)
        thermaltime.append(plant.developmentstage.Thermaltime);rooting_depth.append(plant.root.depth*-1.)
        ETpot.append(plant.et.reference)
    except NameError:
        biomass_plant.append(0);biomass_shoot.append(0)
        biomass_root.append(0);biomass_stem.append(0)
        biomass_leaf.append(0);biomass_storage.append(0)
        thermaltime.append(0);rooting_depth.append(0)
        root_fraction.append(0)
        shoot_fraction.append(0)
        leaf_fraction.append(0)
        stem_fraction.append(0)
        storage_fraction.append(0);ETpot.append(0)  
    matrix_potential.append(c.matrix_potential);wetness.append(c.wetness);flux.append(c.flux); 
    pF.append([log10(-min(mp,-1e-2))+2 for mp in c.matrix_potential])
def plot_res(labels,res,y_label='y',x_label='x'):
    for i in range(len(res[0])):
        plot([part[i] for part in res],label=labels[i])
    grid()
    xlabel(x_label)
    ylabel(y_label)
    legend(loc=0)
    show()
class Field:
    def __init__(self):
        self.sowing_date=self.set_management()[0]
        self.harvest_date=self.set_management()[1]
        self.total_harvest=[]
    def isharvest(self,time_act):
        for date in self.harvest_date:
            if time_act==date:
                return True
                break
    def issowing(self,time_act):
        for date in self.sowing_date:
            if time_act==date:
                return True
                break
    def set_management(self):
        sowing_date=[t.datetime(1991,3,1),t.datetime(1992,3,1),t.datetime(1993,3,1),t.datetime(1994,3,1),t.datetime(1995,3,1)
                      ,t.datetime(1996,3,1),t.datetime(1997,3,1),t.datetime(1998,3,1),t.datetime(1999,3,1),t.datetime(2000,3,1)
                      ,t.datetime(1980,3,1),t.datetime(1981,3,1),t.datetime(1982,3,1),t.datetime(1983,3,1),t.datetime(1984,3,1)
                      ,t.datetime(1985,3,1),t.datetime(1986,3,1),t.datetime(1987,3,1),t.datetime(1988,3,1),t.datetime(1989,3,1)
                      ,t.datetime(1990,3,1)]
        harvest_date=[t.datetime(1991,8,30),t.datetime(1992,8,30),t.datetime(1993,8,30),t.datetime(1994,8,30),t.datetime(1995,8,30)
                      ,t.datetime(1996,8,30),t.datetime(1997,8,30),t.datetime(1998,8,30),t.datetime(1999,8,30),t.datetime(2000,8,30)
                      ,t.datetime(1980,8,30),t.datetime(1981,8,30),t.datetime(1982,8,30),t.datetime(1983,8,30),t.datetime(1984,8,30)
                      ,t.datetime(1985,8,30),t.datetime(1986,8,30),t.datetime(1987,8,30),t.datetime(1988,8,30),t.datetime(1989,8,30)
                      ,t.datetime(1990,8,30)]
        return [sowing_date,harvest_date]

def wheat(soil,atmosphere):
    #Parameter development:
    stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
                   ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]]
    
    #Partitioning coefficiants:
    root=[['Emergence',0.],['Stem elongation',0.1],['Anthesis',0.05],['Maturity',0.]]
    shoot=[['Emergence',0.],['Stem elongation',0.9],['Anthesis',0.95],['Maturity',1.]]
    leaf=[['Emergence',0.],['Tillering',0.5],['Stem elongation',0.3],['Maturity',0.]]
    stem=[['Emergence',0.],['Tillering',0.5],['Stem elongation',0.7],['Anthesis',0.3],['Maturity',0.]]
    storage=[['Seed fill',0.],['Anthesis',0.7],['Maturity',1.]]
    def fractioning(plant_organ,stage):
        return [[max([s[1] if s[0] == item[0] else 0. for i,s in enumerate(stage)]),item[1]] for item in plant_organ]
    wheat=Plant(soil,atmosphere,stage,fractioning(root,stage),fractioning(shoot,stage),
                fractioning(leaf,stage),fractioning(stem,stage),fractioning(storage,stage))
    return wheat
if __name__=='__main__':
    import datetime as t
    import time
    #Create cmf1d instance: sand=60,silt=30,clay=10,c_org=2.0,layercount=20,layerthickness=.1, saturated_depth=2.5
    c=cmf1d(sand=60,silt=30,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    load_meteo(c.project,stationname='Giessen')
    c.cell.saturated_depth=5
    #Create management with sowing and harvest dates
    field=Field()
    #Startng time of simulation
    time_act=t.datetime(1980,1,1)
    #Timestep: must be daily
    time_step=t.timedelta(1)
    c.t=time_act
    i=0
    
    while time_act<t.datetime(1980,10,1):
        if field.issowing(time_act) == True:
            plant=wheat(c,c)
        if field.isharvest(time_act) == True:
            field.total_harvest.append(plant.biomass.Total)
        if Plant.Count>=1:
            plant(time_act,'day',1.)
            c.flux=[s_h*-1. for s_h in plant.water.Uptake]
        else:
            c.flux=[0]*50
        if i%1==0:
            if Plant.Count>=1:
                print time_act,plant.developmentstage.Stage,i-90,plant.biomass.Total,plant.shoot.leaf.LAI
                print time_act, 'ET %4.2f, sh %4.2f,comp %4.2f, sh_comp %4.2f, rootingdepth %4.2f' % (plant.et.reference,sum(plant.water.Uptake),sum(plant.water.compensation),sum(plant.water.s_h_compensated),plant.root.depth)
            else:
                print 'No plant'
        c.run(cmf.day)
        time_act+=time_step
    elapsed = (time.time() - start)
print elapsed













 


