# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 17:34:39 2012

@author: Tobias
"""
from numpy import *
import numpy as np
from datetime import *
import PMF
import cmf
from cmf_setup import cmf1d
from cmf_fp_interface import cmf_fp_interface


#
#def getRandomCoeffcient(default_Cropcoefficient):
#    
#    new_cropCoefficant = PMF.CropCoefficiants() 
#    new_cropCoefficant.k = np.random(default_Cropcoefficient*0.5,default_Cropcoefficient*1.5)
#    #...rue ...
#    #...
#    
#    
#    
#    return new_cropCoeffcient

def Sensitivity_Analysis(SetupFile, ClimateDatafile, DataStart, DataEnd, SensitivityFile, Parameterset, Set_Van_Genuchten_values, Result_Parameter, Result_Parameter_plant, Measured_Days,Plant, Space_for_Result_Table):
    
    Repetitions=SetupFile['Repetitions_of_Sensitivity_Analysis'][1]
    Raw_Duration=DataEnd-DataStart
    Duration=Raw_Duration.days
    Result_Parameter_List = np.zeros((Duration),dtype=[(Result_Parameter, 'f8',(Repetitions, Space_for_Result_Table)),('Year', 'int16'),('Month','int16'),('Day','int16')])

    if Set_Van_Genuchten_values==True:
        #Best Settings for Plot 1 with 22000 runs        

        for Repeat in range(Repetitions):
            alpha=0.0138
            ksat=22.1844
            n=1.5631
            porosity=0.4513
            c=get_soil_data(ksat,porosity,alpha,n)
            
               
            #actuell_cropcoeff = getRandomCoefficient(PMF.CropDatabase.CropCoefficiants)
            
            
            Result = run_CMF_with_PMF_for_one_Simulationperiod(c,DataStart,DataEnd,SetupFile,Result_Parameter,Measured_Days,Repeat,Repetitions,Result_Parameter_List,Duration,Plant)  
                      
            #for i in range(SetupFile['Repetitions_of_Sensitivity_Analysis'][1]):
            '''
            Place here Parameteres for change, otherwise nothing happens
            '''
        return Result
        
    
    if Set_Van_Genuchten_values==False: 
        '''
        Van-Genuchten-Values will be estimated with a random search algorithm with 
        the boundaries set in the setup file 
        '''
        for i in range(Repetitions):
            #try:
            Random_Van_Genuchten_Parameter1 = np.random.uniform(Parameterset['Min_value'][0], Parameterset['Max_value'][0])
            Random_Van_Genuchten_Parameter2 = np.random.uniform(Parameterset['Min_value'][1], Parameterset['Max_value'][1])
            Random_Van_Genuchten_Parameter3 = np.random.uniform(Parameterset['Min_value'][2], Parameterset['Max_value'][2])
            Random_Van_Genuchten_Parameter4 = np.random.uniform(Parameterset['Min_value'][3], Parameterset['Max_value'][3])
            c=get_soil_data(Random_Van_Genuchten_Parameter1,Random_Van_Genuchten_Parameter4,Random_Van_Genuchten_Parameter2,Random_Van_Genuchten_Parameter3,layercount=50,layerthickness=[0.05]*50)
            return c            
                #run_CMF_with_PMF_for_one_Simulationperiod(c,DataStart,DataEnd,SetupFile, Result_Numpy_Array)
            #except RuntimeError:
                #pass
        #print 'Hallo'
#
            
            
            
#def run_CMF_with_PMF_for_one_Simulationperiod(c,DataStart,DataEnd,SetupFile, Result_Parameter,Measured_Days, Repeat,Repetitions,Result_Parameter_List,Duration,Plant):
def run_CMF_with_PMF_for_one_Simulationperiod(c,DataStart,DataEnd,Result_Parameter,Result_Parameter_List,random_plant_coeff):
    
    #c.load_meteo(DataStart,DataStart, SetupFile['ClimateData'][1], rain_factor=1.)
    #cmf_fp = cmf_fp_interface(c.cell)
    #cmf_fp.default_Nconc = .3
    #c.cell.saturated_depth=5.
    #Create evapotranspiration instance or bare soil conditions
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    #set management
    #sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    #harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    cmf_fp = cmf_fp_interface(c.cell)
    cmf_fp.default_Nconc = .3
    c.cell.saturated_depth=5.

    #Simulation
    #res = Res()
    plant = None
    #print "Run ... "    
    c.t = DataStart
    #Analysed_Parameter=str(SetupFile['Res_Name_for_Sensitivty_Analysis'][1])
    #start_content = np.sum(c.cell.layers.volume)
    Expired_Days = 0
#    while c.t<DataStart+timedelta(days=1):
#        print c.t
#        plant=run(c.t,plant,baresoil,cmf_fp,c,Vergangene_Tage,Duration,DataStart,Analysed_Parameter)
    #baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    while c.t<DataEnd:
        #print Cropvalues.RUE
        plant=run(c,plant,cmf_fp,Result_Parameter,Result_Parameter_List,Expired_Days,random_plant_coeff)
        #calculate evaporation from bare soil        
        baresoil(cmf_fp.Kr(),0.,cmf_fp.get_Rn(c.t, 0.12, True),cmf_fp.get_tmean(c.t),cmf_fp.get_es(c.t),cmf_fp.get_ea(c.t), cmf_fp.get_windspeed(c.t),0.,RHmin=30.,h=1.)    
        #get plant water uptake   
        flux = [uptake*-1. for uptake in plant.Wateruptake] if plant  else zeros(c.cell.layer_count())    
        #get evaporation from bare soil or plant model    
        flux[0] -= plant.et.evaporation if plant else baresoil.evaporation
        # set water flux of each soil layer from cmf   
        c.flux=flux
        # run cmf        
        if plant:
            Result_Parameter_List[Result_Parameter][Expired_Days]=eval(Result_Parameter)
            #print plant.root.Wtot
        else:
            try:
                Result_Parameter_List[Result_Parameter][Expired_Days]=eval(Result_Parameter)
            except:
                Result_Parameter_List[Result_Parameter][Expired_Days]=0                
        Expired_Days+=1
        #Raw_Result_Parameter=eval(Result_Parameter)
        #Result_Parameter_List[Result_Parameter]=for i in range(len(Raw_Result_Parameter)):Raw_Result_Parameter[i]
#        if Plant == True:
#            if plant:
#                Result_Parameter_List[Result_Parameter][Vergangene_Tage][Repeat]=eval(Result_Parameter)
#                Result_Parameter_List['Year'][Vergangene_Tage]=c.t.year
#                Result_Parameter_List['Month'][Vergangene_Tage]=c.t.month
#                Result_Parameter_List['Day'][Vergangene_Tage]=c.t.day    
#            else:
#                Result_Parameter_List[Result_Parameter][Vergangene_Tage][Repeat]=0
#                Result_Parameter_List['Year'][Vergangene_Tage]=c.t.year
#                Result_Parameter_List['Month'][Vergangene_Tage]=c.t.month
#                Result_Parameter_List['Day'][Vergangene_Tage]=c.t.day   
#        if Plant == False:
#            Result_Parameter_List[Result_Parameter][Vergangene_Tage][Repeat]=eval(Result_Parameter)
#            Result_Parameter_List['Year'][Vergangene_Tage]=c.t.year
#            Result_Parameter_List['Month'][Vergangene_Tage]=c.t.month
#            Result_Parameter_List['Day'][Vergangene_Tage]=c.t.day
#        Vergangene_Tage+=1
        #print get_status_variable[Analysed_Parameter]

    
    return Result_Parameter_List
    
    
    
    







'''
Other Stuff to making it work
'''


def run(c,plant,cmf_fp,Result_Parameter,Result_Parameter_List,Expired_Days,random_plant_coeff):#actual_coeff):    
#    if c.t.day==1 and c.t.month==3: #check sowing
#        #plant = PMF.createPlant_CMF() #create a plant instance without interfaces
#        #Parameter=actual_coeff[0]
#        plant = PMF.createPlant_fromCoefficiant(random_plant_coeff)#actual_coeff)        
#        plant = PMF.connect(plant,cmf_fp,cmf_fp) #connect the plant with soil and atmosphere interface 
#        
#    if c.t.day==1 and c.t.month==8: #check harvest
#        plant =  None #delete plant instance
#    if plant: #check, if plant exists
#        #print plant
#        plant(c.t,'day',1.) #run plant, daily time step, timeperiod: 1.
#    #calculate evaporation from bare soil
#    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)    
#    baresoil(cmf_fp.Kr(),0.,cmf_fp.get_Rn(c.t, 0.12, True),cmf_fp.get_tmean(c.t),cmf_fp.get_es(c.t),cmf_fp.get_ea(c.t), cmf_fp.get_windspeed(c.t),0.,RHmin=30.,h=1.)    
#    #get plant water uptake   
#    flux = [uptake*-1. for uptake in plant.Wateruptake] if plant  else zeros(c.cell.layer_count())    
#    #get evaporation from bare soil or plant model    
#    flux[0] -= plant.et.evaporation if plant else baresoil.evaporation
#    # set water flux of each soil layer from cmf   
#    c.flux=flux
#    # run cmf
#    c.run(cmf.day)
    if c.t.day==15 and c.t.month==10: #check sowing
        #plant = PMF.createPlant_CMF() #create a plant instance without interfaces
        plant = PMF.createPlant_fromCoefficiant(random_plant_coeff)        
        plant = PMF.connect(plant,cmf_fp,cmf_fp) #connect the plant with soil and atmosphere interface
    if c.t.day==29 and c.t.month==7: #check harvest
        plant =  None #delete plant instance
    if plant: #check, if plant exists
        plant(c.t,'day',1.) #run plant, daily time step, timeperiod: 1.
    
    
    
    
    
    
    c.run(cmf.day)
    #print get_status_variable(c,Analysed_Parameter)
    return plant
    
    

    
  


    
    
def get_watercontent_0_30cm(c,watercontent=0,Layer_per_horizon=6,porosity=[]): #returns calculated watercontent for 0-30cm,30-60cm and 60-90cm
    
    
    
    
    #for i,index in enumerate():
   watercontent=0    
   Layer_per_horizon=6 #6 because soil layers are split in 5cm steps. For 30cm you need six-5cm-layers                
    
   for i in range(Layer_per_horizon):
        watercontent+=c.wetness[i]*c.porosity[i]*100
   return watercontent/Layer_per_horizon
#   for i in range(Layer_pro_Schicht):
#        print Res['porosity']
#        watercontent+=(Res['porosity'][Vergangene_Tage][i+0])*(Res['wetness'][Vergangene_Tage][i+0])*100
#   return watercontent/Layer_pro_Schicht

def get_watercontent_30_60cm(c): #returns calculated watercontent for 0-30cm,30-60cm and 60-90cm
    watercontent=0
    Layer_per_horizon=6
    for i in range(Layer_per_horizon):
        watercontent+=c.wetness[i+6]*c.porosity[i+6]*100
    return watercontent/Layer_per_horizon
#    watercontent=0    
#    Layer_pro_Schicht=6 #6 because soil layers are split in 5cm steps. For 30cm you need six-5cm-layers               
#    for i in range(Layer_pro_Schicht):
#        watercontent+=(Res['porosity'][Vergangene_Tage-1][i+6]*Res['wetness'][Vergangene_Tage-1][i+6]*100)
#    return watercontent/Layer_pro_Schicht

def get_watercontent_60_90cm(c): #returns calculated watercontent for 0-30cm,30-60cm and 60-90cm
    watercontent=0
    Layer_per_horizon=6
    for i in range(Layer_per_horizon):
        watercontent+=c.wetness[i+12]*c.porosity[i+12]*100
    return watercontent/Layer_per_horizon
#    watercontent=0        
#    Layer_pro_Schicht=6 #6 because soil layers are split in 5cm steps. For 30cm you need six-5cm-layers               
#    for i in range(Layer_pro_Schicht):
#        watercontent+=(Res['porosity'][Vergangene_Tage-1][i+12]*Res['wetness'][Vergangene_Tage-1][i+12]*100)
#    return watercontent/Layer_pro_Schicht       

#    
#def get_soil_data(Ksat,porosity,alpha,n):
#    c=cmf1d(Ksat=Ksat,porosity=porosity,alpha=alpha,n=n,layercount=50,layerthickness=[0.05]*50)            
#    return c
#
#def load_random_Parameter(Parameter):
#    Random_Parameter = np.random.uniform(load_Parameter_settings(Parameter)[0], load_Parameter_settings(Parameter)[1])
#    return Random_Parameter



'''
res class as numpy structured array
'''
#depths=[np.float(i) for i in "0:30_30:60".split('_')]
#
#
#
#depths_dtype=[]
#for d,depth in enumerate(depths):
#    dtype.append((depth,'f8')
#
#Res = np.zeros([],dtpe=[tuple(depths_dtype),tuple(biomass_types), ...]
#
#
#
#for d,depth in enumerate(depths):
#    res[''] = get_watercontent_0_30cm(c,depth)
#
#
#    Res = np.zeros([1],dtype=[('water_uptake','f8',(c.cell.layer_count())),('branching','f8',(len(zeros(c.cell.layer_count())))),
#    ('transpiration','f8'),('evaporation','f8'),('biomass','f8'),('root_biomass','f8'),
#    ('shoot_biomass','f8'),('lai','f8'),('root_growth','f8',(len(zeros(c.cell.layer_count())))),('ETo','f8'),
#    ('ETc','f8'),
#    ('temperature','f8'),('stress','f8',(2)),('leaf','f8'),
#    ('stem','f8'),('steam_and_leaf','f8'),('storage','f8'),('potential_depth','f8'),
#    ('rooting_depth','f8'),('developementstage','|S20'),('PotentialGrowth','f8'),
#    ('ActualGrowth','f8'),('developementindex','|S20'),('deep_perlocation','f8'),
#    ('waterstorage','f8',(len(c.cell.layers.volume))),('watercontent_0_30cm','f8'),('watercontent_30_60cm','f8'),('watercontent_60_90cm','f8'),
#    ('watercontent_30_60_90cm','f8',(3))])
#    
#if Analysed_Parameter == 'waterstorage':    
#    Res['waterstorage']                  =c.cell.layers.volume
#if Analysed_Parameter == 'watercontent_0_30cm':
#    Res['watercontent_0_30cm']           =get_watercontent_0_30cm(c)
#if Analysed_Parameter == 'watercontent_30_60cm':
#    Res['watercontent_30_60cm']          =get_watercontent_30_60cm(c)
#if Analysed_Parameter == 'watercontent_60_90cm':
#    Res['watercontent_60_90cm']          =get_watercontent_60_90cm(c)
#if Analysed_Parameter == 'watercontent_30_60_90cm':
#    Res['watercontent_30_60_90cm']       =[get_watercontent_0_30cm(c)+get_watercontent_30_60cm(c)+get_watercontent_60_90cm(c)]
#if Analysed_Parameter == 'deep_perlocation':    
#    Res['deep_perlocation']              =c.groundwater.waterbalance(t)
#
#if plant:
#    if Analysed_Parameter == 'PotentialGrowth':    
#        Res['PotentialGrowth']      =plant.biomass.PotentialGrowth
#    if Analysed_Parameter == 'ActualGrowth':        
#        Res['ActualGrowth']         =plant.biomass.ActualGrowth
#    if Analysed_Parameter == 'biomass':        
#        Res['biomass']              =plant.biomass.Total
#    if Analysed_Parameter == 'root_biomass':        
#        Res['root_biomass']         =plant.root.Wtot
#    if Analysed_Parameter == 'shoot_biomass':        
#        Res['shoot_biomass']        =plant.shoot.Wtot
#    if Analysed_Parameter == 'leaf':        
#        Res['leaf']                 =plant.shoot.leaf.Wtot
#    if Analysed_Parameter == 'stem':        
#        Res['stem']                 =plant.shoot.stem.Wtot
#    if Analysed_Parameter == 'stem_and_leaf':        
#        Res['stem_and_leaf']       =plant.shoot.leaf.Wtot+plant.shoot.stem.Wtot
#    if Analysed_Parameter == 'storage':        
#        Res['storage']              =plant.shoot.storage_organs.Wtot
#    if Analysed_Parameter == 'lai':        
#        Res['lai']                  =plant.shoot.leaf.LAI
#    if Analysed_Parameter == 'developementstage':        
#        Res['developementstage']    =plant.developmentstage.Stage[0]
#    if Analysed_Parameter == 'ETo':        
#        Res['ETo']                  =plant.et.Reference
#    if Analysed_Parameter == 'ETc':        
#        Res['ETc']                  =plant.et.Cropspecific
#    if Analysed_Parameter == 'transpiration':        
#        Res['transpiration']        =plant.et.transpiration
#    if Analysed_Parameter == '':        
#        Res['evaporation']          =plant.et.evaporation
#    if Analysed_Parameter == 'water_uptake':        
#        Res['water_uptake']         =plant.Wateruptake
#    if Analysed_Parameter == 'stress':        
#        Res['stress']               =(plant.water_stress, plant.nutrition_stress)
#    if Analysed_Parameter == 'potential_depth':        
#        Res['potential_depth']      =plant.root.potential_depth
#    if Analysed_Parameter == 'rooting_depth':        
#        Res['rooting_depth']        =plant.root.depth
#    if Analysed_Parameter == 'branching':        
#        Res['branching']            =plant.root.branching
#    if Analysed_Parameter == 'root_growth':        
#        Res['root_growth']          =plant.root.actual_distribution
#    if Analysed_Parameter == 'developementindex':
#        if plant.developmentstage.Stage[0] != "D":
#            Res['developementindex']=plant.developmentstage.StageIndex
#        else:
#            Res['developementindex']=""
#        
#else:
#    if Analysed_Parameter == 'PotentialGrowth':        
#        Res['PotentialGrowth']      =0
#    if Analysed_Parameter == 'ActualGrowth':
#        Res['ActualGrowth']         =0
#    if Analysed_Parameter == 'biomass':
#        Res['biomass']              =0
#    if Analysed_Parameter == 'root_biomass':
#        Res['root_biomass']         =0
#    if Analysed_Parameter == 'shoot_biomass':
#        Res['shoot_biomass']        =0
#    if Analysed_Parameter == 'leaf':
#        Res['leaf']                 =0
#    if Analysed_Parameter == 'stem':
#        Res['stem']                 =0
#    if Analysed_Parameter == 'steam_and_leaf':
#        Res['steam_and_leaf']       =0
#    if Analysed_Parameter == 'storage':
#        Res['storage']              =0
#    if Analysed_Parameter == 'lai':
#        Res['lai']                  =0
#    if Analysed_Parameter == 'developementstage':
#        Res['developementstage']    =""
#    if Analysed_Parameter == 'developementindex':
#        Res['developementindex']    =""
#    if Analysed_Parameter == 'ETo':            
#        Res['ETo']                  =0
#    if Analysed_Parameter == 'ETc':
#        Res['ETc']                  =0
#    if Analysed_Parameter == 'transpiration':
#        Res['transpiration']        =0
#    if Analysed_Parameter == 'evaportation':
#        Res['evaporation']          =0
#    if Analysed_Parameter == 'water_uptake':
#        Res['water_uptake']         =0
#    if Analysed_Parameter == 'stress':
#        Res['stress']               =(0,0)
#    if Analysed_Parameter == '':
#        Res['potential_depth']      =0
#    if Analysed_Parameter == 'rooting_depth':
#        Res['rooting_depth']        =0
#    if Analysed_Parameter == 'branching':
#        Res['branching']            =zeros(c.cell.layer_count())
#    if Analysed_Parameter == 'root_growth':
#        Res['root_growth']          =zeros(c.cell.layer_count())
#return plant

     
'''
old res class
'''    
#       
#class Res(object):
#    def __init__(self):
#        self.flux=[]
#        self.water_uptake = []
#        self.branching = []
#        self.transpiration = []
#        self.evaporation = []
#        self.biomass = []
#        self.root_biomass = []
#        self.shoot_biomass = []
#        self.lai = []
#        self.root_growth = []
#        self.ETo = []
#        self.ETc = []
#        self.wetness = []
#        #self.pF=[]
#        #self.potential=[]#!!
#        self.porosity=[]#!!
#        self.rain = []
#        self.temperature = []
#        self.DAS = []
#        self.stress = []
#        self.leaf=[]
#        self.stem=[]
#        self.stem_and_leaf=[]
#        self.storage=[]
#        self.potential_depth=[]
#        self.rooting_depth=[]
#        self.time = []
#        self.developmentstage = []
#        self.PotentialGrowth = []
#        self.ActualGrowth = []
#        self.developmentindex=[]
#        self.deep_percolation=[]
#        self.baresoil_evaporation=[]
#        self.waterstorage=[]
#        self.watercontent_0_30cm=[]
#        self.watercontent_30_60cm=[]
#        self.watercontent_60_90cm=[]
#        self.watercontent_30_60_90cm=[]
#    def __repr__(self):
#        return "Shoot=%gg, Root=%gg, ETc = %gmm, Wateruptake=%gmm, Stress=%s" % (self.shoot_biomass[-1],self.root_biomass[-1],self.ETc[-1],sum(self.water_uptake[-1]),self.stress[-1])
#
#
  
#    #get status variables of cmf
#    res.waterstorage.append(c.cell.layers.volume) #water content of each layer in [mm/day] (list with 40 soil layers)
#    res.flux.append(c.flux) #water flux of each layer in [mm/day] (list with 40 soil layers)
#    res.wetness.append(c.wetness) #wetness/water content of each layer in [%/day] (list with 40 soil layers)
#    #res.pF.append(c.pF)
#    #res.potential.append(c.potential)#!!
#    res.porosity.append(c.porosity)#!!
#    res.watercontent_0_30cm.append(get_watercontent_0_30cm(c))
#    res.watercontent_30_60cm.append(get_watercontent_30_60cm(c))
#    res.watercontent_60_90cm.append(get_watercontent_60_90cm(c))
#    res.watercontent_30_60_90cm.append([get_watercontent_0_30cm(c),get_watercontent_30_60cm(c),get_watercontent_60_90cm(c)])    
#    res.deep_percolation.append(c.groundwater.waterbalance(t)) #water flux to groundwater [mm/day]
#    res.rain.append(c.cell.get_rainfall(t)) #rainfall in [mm/day]
#    #get baresoil evaporation [mm/day]
#    res.baresoil_evaporation.append(0.0) if plant else  res.baresoil_evaporation.append(baresoil.evaporation)       
#    #get status variables of pmf
#    #biomass status
#    res.PotentialGrowth.append(plant.biomass.PotentialGrowth) if plant else res.PotentialGrowth.append(0) #[g/m2/day]
#    res.ActualGrowth.append(plant.biomass.ActualGrowth) if plant else res.ActualGrowth.append(0) #[g/m2/day]
#    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0) #[g/m2]
#    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0) #[g/m2]
#    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0) #[g/m2]
#    res.leaf.append(plant.shoot.leaf.Wtot) if plant else res.leaf.append(0) #[g/m2]
#    res.stem.append(plant.shoot.stem.Wtot) if plant else res.stem.append(0) #[g/m2]
#    res.stem_and_leaf.append(plant.shoot.leaf.Wtot+plant.shoot.stem.Wtot) if plant else res.stem_and_leaf.append(0)
#    res.storage.append(plant.shoot.storage_organs.Wtot) if plant else res.storage.append(0) #[g/m2]   
#    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0) #[m2/m2]
#    #development    
#    res.developmentstage.append(plant.developmentstage.Stage[0]) if plant else res.developmentstage.append("")
#    res.DAS.append(t-datetime(1980,3,1)) if plant else res.DAS.append(0)
#    if plant:       
#        if plant.developmentstage.Stage[0] != "D": 
#            res.developmentindex.append(plant.developmentstage.StageIndex) if plant else res.developmentindex.append("")
#        else:
#            res.developmentindex.append("")
#    #else:
#        res.developmentindex.append("")    
#    #plant water balance [mm/day]
#    res.ETo.append(plant.et.Reference) if plant else res.ETo.append(0)
#    res.ETc.append(plant.et.Cropspecific) if plant else res.ETc.append(0)
#    #transpiration is not equal to water uptake! transpiration is calculated without stress and wateruptake with stress!!!
#    res.transpiration.append(plant.et.transpiration) if plant else res.transpiration.append(0) 
#    res.evaporation.append(plant.et.evaporation) if plant else  res.evaporation.append(0)
#    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append(zeros(c.cell.layer_count())) #(list with 40 layers)    
#    res.stress.append((plant.water_stress, plant.nutrition_stress) if plant else (0,0)) # dimensionsless stress index (0-->no stress; 1-->full stress)    
#    #root growth
#    res.potential_depth.append(plant.root.potential_depth) if plant else res.potential_depth.append(0) #[cm]
#    res.rooting_depth.append(plant.root.depth) if plant else res.rooting_depth.append(0) #[cm]
#    res.branching.append(plant.root.branching) if plant else res.branching.append(zeros(c.cell.layer_count())) # growth RATE in each layer per day [g/day](list with 40 layers)
#    res.root_growth.append(plant.root.actual_distribution) if plant else  res.root_growth.append(zeros(c.cell.layer_count())) # total root biomass in each layer [g/layer]
#    res.time.append(t)
#    return plant

    