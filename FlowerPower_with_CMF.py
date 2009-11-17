def run(t,res,plant):
    if t.day==1 and t.month==3:
        plant = FlowerPower.connect(FlowerPower.createPlant_CMF(),cmf_fp,cmf_fp)
        #plant.nitrogen.Km = 0.0
    if t.day==1 and t.month==8:
        plant =  None
    #Let grow
    if plant: 
        plant(t,'day',1.)
    #Calculates evaporation for bare soil conditions
    baresoil(c.Kr(),0.,c.get_Rn(t, 0.12, True),c.get_tmean(t),c.get_es(t),c.get_ea(t), c.get_windspeed(t),0.,RHmin=30.,h=1.)    
    flux = [uptake*-1. for uptake in plant.Wateruptake] if plant  else zeros(c.cell.layer_count())
    flux[0] -= plant.et.evaporation if plant else baresoil.evaporation
    c.flux=flux
    c.run(cmf.day)    
    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append(zeros(c.cell.layer_count()))
    #res.water_uptake.append(flux)
    res.branching.append(plant.root.branching) if plant else res.branching.append(zeros(c.cell.layer_count()))
    res.transpiration.append(plant.et.transpiration) if plant else res.transpiration.append(0)
    res.evaporation.append(plant.et.evaporation) if plant else  res.evaporation.append(0)
    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0)
    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0)
    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0)
    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0)
    res.root_growth.append(plant.root.actual_distribution) if plant else  res.root_growth.append(zeros(c.cell.layer_count()))
    res.ETo.append(plant.et.Reference) if plant else res.ETo.append(0)
    res.ETc.append(plant.et.Cropspecific) if plant else res.ETc.append(0)
    res.wetness.append(c.wetness) 
    res.rain.append(c.cell.rain(t))
    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
    res.temperature.append(cmf_fp.get_tmean(t))
    res.radiation.append(cmf_fp.get_Rs(t))
    res.stress.append((plant.water_stress, plant.nutrition_stress) if plant else (0,0))
    res.alpha.append(plant.water.Alpha) if plant else res.alpha.append(zeros(c.cell.layer_count()))
    res.matrix_potential.append(c.matrix_potential)
    res.activeNO3.append(plant.nitrogen.Active)if plant else res.activeNO3.append(zeros(c.cell.layer_count()))
    res.passiveNO3.append(plant.nitrogen.Passive)if plant else res.passiveNO3.append(zeros(c.cell.layer_count()))
    return plant

class Res(object):
    def __init__(self):
        self.water_uptake = []
        self.branching = []
        self.transpiration = []
        self.evaporation = []
        self.biomass = []
        self.root_biomass = []
        self.shoot_biomass = []
        self.lai = []
        self.root_growth = []
        self.ETo = []
        self.ETc = []
        self.matrix_potential = []
        self.wetness = []
        self.rain = []
        self.temperature = []
        self.radiation = []
        self.DAS = []
        self.stress = []
        self.alpha = []
        self.activeNO3=[]
        self.passiveNO3=[]
    def __repr__(self):
        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])
    
if __name__=='__main__':
    
    from pylab import *
    from datetime import *
    import FlowerPower
    import cmf
    from cmf_setup import cmf1d
    from cmf_fp_interface import cmf_fp_interface
    import psyco
    psyco.full()
    
    #Create cmf cell    
    c=cmf1d(sand=20,silt=60,clay=20,c_org=2.0,bedrock_K=0.01,layercount=20,layerthickness=0.1)
    print "cmf is setup"
    c.load_meteo(rain_factor=1)
    print "meteo loaded"
    cmf_fp = cmf_fp_interface(c.cell)
    #cmf_fp.default_Nconc = .001
    print "Interface to FlowerPower"
    c.cell.saturated_depth=5.
    #Create evapotranspiration instance or bare soil conditions
    baresoil = FlowerPower.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    
    #set management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #Simulation period
    start = datetime(1980,1,1)
    end = datetime(1980,12,31)
    #Simulation
    res = Res()
    plant = None
    print "Run ... "    
    start_time = datetime.now()
    c.t = start
    while c.t<end:
        plant=run(c.t,res,plant)
        print c.t,res
    print 'Duration:',datetime.now()-start_time
    def showit(a,pos,posmax,**kwargs):
        subplot(posmax,1,pos)
        imshow(transpose(a),aspect='auto',interpolation='nearest',**kwargs)
        colorbar()
    #Calculates DAS for each development stage
    stages = FlowerPower.make_plant.CropCoefficiants().stage
    #Days after sowing (DAS) unit maturity
    DAS = filter(lambda res: res!=0,res.DAS)[-1]
    #Fraction of each development stage from maturity 
    relStages = [s[1] / stages[-1][1] for s in stages]
    #DAS for each stage
    DAS = [DAS.days * s for s in relStages]
    figtext(.01, .97, ('Rain %4.2f, Radiation %4.2f, Temperature: %4.2f') % (sum(res.rain),sum(res.radiation),sum(res.temperature)))
    figtext(.01, .95, ('ETo %4.2f, ETc %4.2f, transpiration %4.2f, evaporation %4.2f') % (sum(res.ETo),sum(res.ETc),sum(res.transpiration),sum(res.evaporation)))
    figtext(.01, .93, ('Plant biomass %4.2f, Root biomass %4.2f, Shoot biomass %4.2f, LAI %4.2f, Water uptake: %4.2f') % (filter(lambda res: res>0,res.biomass)[-1], filter(lambda res: res>0,res.root_biomass)[-1], filter(lambda res: res>0,res.shoot_biomass)[-1], filter(lambda res: res>0,res.lai)[-1],sum(res.water_uptake)))
    figtext(.01, .91, ('Emergence %4.2f,Leaf development %4.2f,  Tillering %4.2f, Stem elongation %4.2f, Anthesis %4.2f, Seed fill %4.2f, Dough stage %4.2f, Maturity %4.2f') % (DAS[0],DAS[1],DAS[2],DAS[3],DAS[4],DAS[5],DAS[6],DAS[7]))
   
    showit(res.branching,1,6,cmap = cm.Greens)
    showit(res.root_growth,2,6,cmap = cm.Greens)
    showit(res.water_uptake,3,6,cmap = cm.Blues)
    showit(res.passiveNO3,4,6,cmap=cm.Reds)
    showit(res.activeNO3,5,6,cmap=cm.Reds)
    showit(res.wetness,6,6,cmap=cm.RdYlBu)
    show()