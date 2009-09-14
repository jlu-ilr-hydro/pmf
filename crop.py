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
    plot(penetrated_layer,label='root')
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
        biomass_plant.append(plant.Wtot);biomass_shoot.append(plant.shoot.Wtot)
        biomass_root.append(plant.root.Wtot);biomass_stem.append(plant.shoot.stem.Wtot)
        biomass_leaf.append(plant.shoot.leaf.Wtot);biomass_storage.append(plant.shoot.storage_organs.Wtot)
        thermaltime.append(plant.thermaltime);rooting_depth.append(plant.root.depth*-1.)
        penetrated_layer.append(plant.root.fraction(plant.thermaltime))
        shoot_fraction.append(plant.shoot.fraction(plant.thermaltime))
        leaf_fraction.append(plant.shoot.leaf.fraction(plant.thermaltime))
        stem_fraction.append(plant.shoot.stem.fraction(plant.thermaltime))
        storage_fraction.append(plant.shoot.storage_organs.fraction(plant.thermaltime))
        ETpot.append(plant.ETp)
    except NameError:
        biomass_plant.append(0);biomass_shoot.append(0)
        biomass_root.append(0);biomass_stem.append(0)
        biomass_leaf.append(0);biomass_storage.append(0)
        thermaltime.append(0);rooting_depth.append(0)
        penetrated_layer.append(0)
        shoot_fraction.append(0)
        leaf_fraction.append(0)
        stem_fraction.append(0)
        storage_fraction.append(0);ETpot.append(0)  
    matrix_potential.append(c.matrix_potential);wetness.append(c.wetness);flux.append(c.flux); 
    pF.append([log10(-min(mp,-1e-2))+2 for mp in c.matrix_potential])
def set_flux(water_uptake):
    try:
        c.flux=[s_h*-1. for s_h in plant.s_h]
    except NameError:
        c.flux=[0]*50
class Field:
    def __init__(self):
        self.sowing_date=self.set_management()[0]
        self.harvest_date=self.set_management()[1]
        self.total_harvest=[]
        self.dict_of_plants={}
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
        harvest_date=[t.datetime(1991,9,30),t.datetime(1992,9,30),t.datetime(1993,9,30),t.datetime(1994,9,30),t.datetime(1995,9,30)
                      ,t.datetime(1996,9,30),t.datetime(1997,9,30),t.datetime(1998,9,30),t.datetime(1999,9,30),t.datetime(2000,9,30)
                      ,t.datetime(1980,9,30),t.datetime(1981,9,30),t.datetime(1982,9,30),t.datetime(1983,9,30),t.datetime(1984,9,30)
                      ,t.datetime(1985,9,30),t.datetime(1986,9,30),t.datetime(1987,9,30),t.datetime(1988,9,30),t.datetime(1989,9,30)
                      ,t.datetime(1990,9,30)]
        return [sowing_date,harvest_date]
    def __call__(self,time_act):
        if self.issowing(time_act) == True:
            return True
        elif self.isharvest(time_act) == True:
            return True

def wheat(soil,atmosphere):
    #Parameter development:
    stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
                   ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]]
    #Parameter partitioning:
    root_fraction=[[160.,1.],[901.,0.5],[1665.,0.]]
    shoot_fraction=[[160.,0.],[901.,0.5,],[1665.,1.,]]
    leaf_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
    stem_fraction=[[160.,0.],[901.,0.5],[1174.,0.375],[1665.,0.]]
    storage_fraction=[[160.,0.],[901.,0.0],[1174.,0.25],[1665.,1.]]
    plant=Plant(soil,atmosphere,stage,root_fraction,shoot_fraction,leaf_fraction,stem_fraction,
                 storage_fraction)
    return plant
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
    
    #Results
    biomass_plant=[];biomass_shoot=[];biomass_root=[];biomass_stem=[]
    biomass_leaf=[];biomass_storage=[];thermaltime=[];rooting_depth=[]
    water_uptkake=[];nutrient_uptake=[]
    shoot_fraction=[];penetrated_layer=[]
    matrix_potential=[];wetness=[];flux=[]
    penetrated_layer=[];shoot_fraction=[];
    leaf_fraction=[];stem_fraction=[];
    storage_fraction =[];ETpot=[];pF=[]
    
    start = time.time()
    ion()
    biomass = zeros(1826)
    ETp=zeros(1826)
    ETa=zeros(1826)
    x = range(1826) 
    ETp_plot, = plot(x,ETp,color='blue',label='ETp')
    ETa_plot, = plot(x,ETa,color='green',label='ETa')
    legend(loc=0)
    ylim(0,6)
    title('Crop: SummerWheat, Weather: Giessen, Period: 1980 - 1985 ')
    ylabel('Evapotranspiration [mm]')
    xlabel('Day of simulation period [day]')
    ax2=twinx()
    biomass_plot, = plot(x,biomass,'r',label='Biomass')
    ylim(0,300)
    ylabel('Biomass [g * m-1]')
    grid()
    
    #Simulation period
    while time_act<t.datetime(1984,12,31):
        i+=1
        
        try:
            biomass[i]+=plant.Wtot
            ETp[i]+=plant.ETp
            ETa[i]+=sum(plant.s_h)
        except NameError:
            biomass[i]+=0.
            ETp[i]+=0.
            ETa[i]+=0.
        if i%7==0:
            ETp_plot.set_ydata(ETp)
            #fill_between(x,0,ETp,facecolor='blue')
            ETa_plot.set_ydata(ETa)
            #fill_between(x,0,ETa,facecolor='green')
            biomass_plot.set_ydata(biomass)
            draw()
        
        if field.issowing(time_act) == True:
            plant=wheat(c,c)
        if field.isharvest(time_act) == True:
            field.total_harvest.append(plant.Wtot)
            del plant
        try:
            plant(time_act,'day',1.)
            c.flux=[s_h*-1. for s_h in plant.s_h]
        except NameError:
            c.flux=[0]*50
        set_results()        
        if i%28==0:
            try:
                print time_act,plant.stage(plant.thermaltime)
                #print time_act,plant.stage(plant.thermaltime),'stress',plant.stress,'water',sum(plant.s_h),'etp',plant.ETp,'depth',plant.root.depth
                #print time_act,"ET= %0.2f" % plant.ETp,"Water uptake=%4.2f" % sum(plant.s_h),plant.ETp/plant.root.depth
                #print time_act,'penetration' ,['%4.2f' % a for a in plant.penetration][:10]
                #print time_act,'pF',['%4.2f' % a for a in c.pF][:10]
                #print time_act,'alpha' ,['%4.2f' % a for a in plant.alpha][:10]
                #print time_act,'pressure',['%4.2f' % a for a in plant.pressure_head][:10]
                #print time_act,'matrix',['%4.2f' % -a for a in c.matrix_potential][:10]
                #print time_act, 's_h', ['%4.2f' % s_h for s_h in plant.s_h][:10]
                #print time_act, 'flux',['%4.2f' % f for f in c.flux][:10]
            except NameError: 
                print 'No crop'
        c.run(cmf.day)
        time_act+=time_step
    elapsed = (time.time() - start)

print elapsed

 
 


