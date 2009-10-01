from pylab import *
from FlowerPower import *
import cmf
from cmf_setup import cmf1d
import struct
from swc import *
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
        ETpot.append(plant.ET.reference)
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
def wheat(soil,atmosphere):
    #Parameter development:
    stage=[['Emergence',160.],['Leaf development',208.],['Tillering',421.],['Stem elongation',659.],
                   ['Anthesis',901.],['Seed fill',1174.],['Dough stage',1556.],['Maturity',1665.]]
    
    shoot_percent =[.0,.9,.9,.9,.95,1.,1.,1.]
    root_percent = [.0,.1,.1,.1,.05,.0,.0,.0]
    leaf_percent = [[.0,.5,.5,.3,0.,.0,.0,.0][i]*perc for i,perc in enumerate(shoot_percent)]
    stem_percent = [[.0,.5,.5,.7,.3,.0,.0,.0][i]*perc for i,perc in enumerate(shoot_percent)]
    storage_percent = [[.0,.0,.0,.0,.7,1.,1.,1.][i]*perc for i,perc in enumerate(shoot_percent)]
    #Partitioning coefficiants:
    root=[['Emergence',0.],['Stem elongation',0.1],['Anthesis',0.05],['Maturity',0.]]
    shoot=[['Emergence',0.],['Stem elongation',0.9],['Anthesis',0.95],['Maturity',1.]]
    leaf=[['Emergence',0.],['Tillering',0.5],['Stem elongation',0.3],['Maturity',0.]]
    stem=[['Emergence',0.],['Tillering',0.5],['Stem elongation',0.7],['Anthesis',0.3],['Maturity',0.]]
    storage=[['Seed fill',0.],['Anthesis',0.7],['Maturity',1.]]
    def fractioning(plant_organ,stage):
        return [[max([s[1] if s[0] == item[0] else 0. for i,s in enumerate(stage)]),item[1]] for item in plant_organ]
    wheat=Plant(soil,atmosphere,stage,shoot_percent,root_percent,
                leaf_percent,stem_percent,storage_percent)
    return wheat

class Field:
    def __init__(self):
        self.sowing=sowing
        self.harvest=harvest
if __name__=='__main__':
    import datetime as t
    import time
    c=cmf1d(sand=60,silt=30,clay=10,c_org=2.0,layercount=20,layerthickness=.1)
    load_meteo(c.project,stationname='Giessen')
    c.cell.saturated_depth=5
    time_act=t.datetime(1980,1,1)
    time_step=t.timedelta(1)
    c.t=time_act
    i=0
    start = time.time()
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
    res=[]
    swc = SWC()
    swc.calc_InitialDepletion(FC, q, Zr)
    while time_act<t.datetime(1980,10,1):
        i+=1        
        if filter(lambda s: s==time_act, sowing_date):
            plant=wheat(c,c)
        if filter(lambda s: s==time_act, harvest_date):
            Plant.Count - 1#del plant
        if Plant.Count>=1:
            plant(time_act,'day',1.)
            c.flux=[s_h*-1. for s_h in plant.water.Uptake]
        else:
            c.flux=[0]*50
        if i%1==0:
            if Plant.Count>=1:
                
                #Daily waterbalance:
                
                
                
                
                
                
                
                print time_act,plant.developmentstage.Stage,i-90#, plant.developmentstage.Thermaltime
                res.append([plant.ET.Cropspecific,plant.ET.Reference])
            else:
                pass#print 'No plant'
        c.run(cmf.day)
        time_act+=time_step
    elapsed = (time.time() - start)
print elapsed
plot_res(['ETc','ETo'],res)
"""
#print time_act, 'ET %4.2f, sh %4.2f,comp %4.2f, sh_comp %4.2f, rootingdepth %4.2f' % (plant.ET.reference,sum(plant.water.Uptake),sum(plant.water.compensation),sum(plant.water.s_h_compensated),plant.root.depth)
                #print time_act ,'fgi',['%4.2f' %  a for a in plant.root.fgi][:10],sum(plant.root.fgi)
                #print time_act,'pF',['%4.2f' % a for a in c.pF][:10]
                #print time_act, 's_h', ['%4.2f' % u for u in plant.water.Uptake][:10]
                #print time_act, 'alpha', ['%4.2f' % u for u in plant.water.alpha][:10]
                #print time_act, 's_h_comp', ['%4.2f' % u for u in plant.water.Compensated_Uptake][:10]
                #print time_act, 'flux',['%4.2f' % f for f in c.flux][:10]
                print time_act
                print time_act, plant.biomass.PotentialGrowth,plant.biomass.ActualGrowth,plant.biomass.Total, plant.shoot.leaf.LAI,plant.shoot.leaf.Wtot
                
                
                
                
                new_CGR = plant.atmosphere.get_Rs(time_act) * 0.5 * 0.9 * (1-exp(-0.4 * adjusted_lai)) * 3.0 if plant.thermaltime >=plant.stage[0][1] and plant.thermaltime <= plant.stage[-1][1] else 0.
                new_biomass += new_CGR
                new_leaf_biomass += new_CGR * plant.shoot.fraction(plant.thermaltime) * plant.shoot.leaf.fraction(plant.thermaltime)
                new_lai += new_CGR * plant.shoot.fraction(plant.thermaltime) * plant.shoot.leaf.fraction(plant.thermaltime) / plant.shoot.leaf.specific_weight
                
                ajdusted_specific_weight = min(plant.thermaltime/plant.stage[-1][1]+0.25,1) * plant.shoot.leaf.specific_weight
                adjusted_lai += new_CGR * plant.shoot.fraction(plant.thermaltime) * plant.shoot.leaf.fraction(plant.thermaltime) / ajdusted_specific_weight 
                
                #print time_act,plant.stage(plant.thermaltime),i-90,'adj_weight %4.2f, adj_LAI %4.2f, old_LAI %4.2f' % (ajdusted_specific_weight,adjusted_lai,new_lai)
                                
                new_root += new_CGR * plant.root.fraction(plant.thermaltime)
                new_stem += new_CGR * plant.shoot.stem.fraction(plant.thermaltime)
                new_storage += new_CGR * plant.shoot.storage_organs.fraction(plant.thermaltime)
                
                #senescence
                senescence = (0.001 if plant.thermaltime > plant.stage[-1][1] else 0.)
                new_biomass -= new_biomass  * senescence
                new_root -= new_root * senescence
                new_stem -= new_stem * senescence
                new_storage -= new_storage * senescence
                new_leaf_biomass -= new_leaf_biomass * senescence
              
                #print time_act,plant.stage(plant.thermaltime),i-90,'LAI %4.2f, Biomass %4.2f, CGR %4.2f, Leaf %4.2f, Stem %4.2f, Storage %4.2f, Root %4.2f, Rs %4.2f' % (adjusted_lai,new_biomass,new_CGR,new_leaf_biomass,new_stem,new_storage,new_root,plant.atmosphere.get_Rs(time_act))
                res.append([new_root,new_leaf_biomass,new_stem,new_storage,new_biomass])
                #plot_res(['new_root','new_leaf_biomass','new_stem','new_storage','new_biomass'],res)







    ion()
    root=zeros(1826)
    alpha=zeros(1826)
    biomass = zeros(1826)
    ETp=zeros(1826)
    ETa=zeros(1826)
    x = range(1826) 
    f=figure()
    f.add_subplot(311)
    ETp_plot, = plot(x,ETp,color='blue',label='ETp')
    ETa_plot, = plot(x,ETa,color='green',label='ETa')
    legend(loc=0)
    ylim(0,6)
    title('Crop: SummerWheat, Weather: Giessen, Period: 1980 - 1985 ')
    ylabel('Evapotranspiration [mm]')
    xlabel('Day of simulation period [day]')
    grid()
    f.add_subplot(312)
    root_plot, = plot(x,root,color='blue',label='Rootingdepth')
    ylim(-200,0)
    ylabel('Depth [cm]')
    grid()
    xlabel('Day of simulation period [day]')
    legend(loc=0)
    f.add_subplot(313)
    alpha_plot, = plot(x,alpha,color='r',label='stress index')
    ylabel('fraction [-]')
    legend(loc=0)
    ylim(-0.1,1.1)
    ax2=twinx()
    biomass_plot, = plot(x,biomass,'g',label='Biomass')
    ylim(0,300)
    ylabel('Biomass [g * m-1]')
    grid()



        try:
            biomass[i]+=plant.Wtot
            ETp[i]+=plant.ET.reference
            ETa[i]+=sum(plant.water.Uptake)
            root[i]+=-plant.root.depth
            alpha[i]+=1-plant.stress
        except NameError:
           pass
        if i%7==0:
            ETp_plot.set_ydata(ETp)
            #fill_between(x,0,ETp,facecolor='blue')
            ETa_plot.set_ydata(ETa)
            #fill_between(x,0,ETa,facecolor='green')
            biomass_plot.set_ydata(biomass)
            root_plot.set_ydata(root)
            alpha_plot.set_ydata(alpha)
            draw()
     



"""













 


