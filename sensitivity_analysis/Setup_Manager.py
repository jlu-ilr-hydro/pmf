# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:42:57 2012

@author: Tobias
"""
from numpy import *
from datetime import *
import Run_CMF_with_PMF_Tool as run
import PMF
from cmf_setup import cmf1d
import csv
import os
import Statistic_Tool as stat
#import cmf


'''
Load Setupfile
'''
def load_Setup_csv_File(Name_of_SetupFile):
    Setup = Name_of_SetupFile
    idtype=[('InputData', '|S25'), ('ClimateData', '|S25'), 
            ('Program_for_SA','|S10'),
            ('Res_Name_for_Sensitivty_Analysis', '|S40'), 
            ('Number_of_Plots', 'int16'),('Data_for_Sensitivity_Analysis', '|S50'),
            ('Repetitions_of_Sensitivity_Analysis','int32'), 
            ('Number_of_Paramaters_for_Sensitivity_Analysis', 'int16'),        
            ('Parameter1_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter1', 'f8'), ('Max_Rangevalue_of_Parameter1','f8'),
            ('Parameter2_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter2', 'f8'), ('Max_Rangevalue_of_Parameter2','f8'),
            ('Parameter3_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter3', 'f8'), ('Max_Rangevalue_of_Parameter3','f8'),
            ('Parameter4_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter4', 'f8'), ('Max_Rangevalue_of_Parameter4','f8'),
            ('Parameter5_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter5', 'f8'), ('Max_Rangevalue_of_Parameter5','f8'),
            ('Parameter6_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter6', 'f8'), ('Max_Rangevalue_of_Parameter6','f8'),
            ('Parameter7_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter7', 'f8'), ('Max_Rangevalue_of_Parameter7','f8'),
            ('Parameter8_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter8', 'f8'), ('Max_Rangevalue_of_Parameter8','f8'),
            ('Parameter9_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter9', '|S40'), ('Max_Rangevalue_of_Parameter9','|S40'),
            ('Parameter10_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter10', '|S40'), ('Max_Rangevalue_of_Parameter10','|S40')]
    SetupFile = np.genfromtxt(Setup,delimiter=';',names=True, dtype=idtype)
    return SetupFile



'''
Load Climate Data
'''
def load_ClimateDatafile(SetupFile):
    ctype=dtype([('Date', 'S20'), ('DOY', '<f8'), ('Rain_mm', '<f8'), ('Tmax_C', '<f8'), ('Tmin_C', '<f8'), ('Rhmin', '<f8'), ('Rhmax', '<f8'), ('Windspeed_ms', '<f8'), ('RS_MJm\xb2day', '<f8'), ('Sunshine_', '<f8')])
    ClimateDatafile = np.genfromtxt(SetupFile['ClimateData'][1],delimiter=';',names=True, dtype=ctype)
    return ClimateDatafile     

def getDatastart(ClimateDatafile):
    RawStart= ClimateDatafile['Date'][0]
    Split_RawStart = RawStart.split('.')
    DataStart = datetime(int(Split_RawStart[2]),int(Split_RawStart[1]),int(Split_RawStart[0]))
    return DataStart

def getDataend(ClimateDatafile):    
    RawEnd= ClimateDatafile['Date'][len(ClimateDatafile['Date'])-1]
    Split_RawEnd = RawEnd.split('.')
    DataEnd = datetime(int(Split_RawEnd[2]),int(Split_RawEnd[1]),int(Split_RawEnd[0]))
    return DataEnd



'''
Load Data for Sensitivity Analysis
'''
def load_Measured_Data(SetupFile,Plot):  
    fdtype=[('PLOT', '|S10'), ('Year', 'int16'), ('Month', 'int16'), ('Day', 'int16'), ('Data_for_Sensitivity_Analysis_0', 'f8'),('Data_for_Sensitivity_Analysis_1', 'f8'),('Data_for_Sensitivity_Analysis_2', 'f8')]
    Sensitivity = SetupFile['Data_for_Sensitivity_Analysis'][1].split('.')    
    Sensitivity_File_name = Sensitivity[0]+'_Plot'+str(Plot)+'.'+Sensitivity[1]    
    SensitivityFile = np.genfromtxt(Sensitivity_File_name,delimiter=';', dtype=fdtype)
    return SensitivityFile

def getMeasuredDays(SensitivityFile):
    Measured_Days= []
    for i in range(len(SensitivityFile['Year'])-1):
        Measured_Days.append(datetime(SensitivityFile['Year'][i+1],SensitivityFile['Month'][i+1],SensitivityFile['Day'][i+1]))
    return Measured_Days

'''
Get command for Analysed Parameter
'''
def get_Result_Parameter(Analysed_Parameter):  
    
    Space_for_Result_Table = 1
    
    if Analysed_Parameter == 'waterstorage':    
        Result_Parameter='c.cell.layers.volume'
    if Analysed_Parameter == 'watercontent_0_30cm':
        Result_Parameter='get_watercontent_0_30cm(c)'
    if Analysed_Parameter == 'watercontent_30_60cm':
        Result_Parameter='get_watercontent_30_60cm(c)'
    if Analysed_Parameter == 'watercontent_60_90cm':
        Result_Parameter='get_watercontent_60_90cm(c)'
    if Analysed_Parameter == 'watercontent_30_60_90cm':
        Result_Parameter='[get_watercontent_0_30cm(c),get_watercontent_30_60cm(c),get_watercontent_60_90cm(c)]'
        Space_for_Result_Table = 3
    if Analysed_Parameter == 'deep_perlocation':    
        Result_Parameter='c.groundwater.waterbalance(t)'
    
    Result_Parameter_plant = ''
    if Analysed_Parameter == 'PotentialGrowth':    
        Result_Parameter_plant='plant.biomass.PotentialGrowth'
    if Analysed_Parameter == 'ActualGrowth':        
        Result_Parameter_plant='plant.biomass.ActualGrowth'
    if Analysed_Parameter == 'biomass':        
        Result_Parameter_plant='plant.biomass.Total'
    if Analysed_Parameter == 'root_biomass':        
        Result_Parameter_plant='plant.root.Wtot'
    if Analysed_Parameter == 'shoot_biomass':        
        Result_Parameter_plant='plant.shoot.Wtot'
    if Analysed_Parameter == 'leaf':        
        Result_Parameter_plant='plant.shoot.leaf.Wtot'
    if Analysed_Parameter == 'stem':        
        Result_Parameter_plant='plant.shoot.stem.Wtot'
    if Analysed_Parameter == 'stem_and_leaf':        
        Result_Parameter_plant='plant.shoot.leaf.Wtot+plant.shoot.stem.Wtot'
    if Analysed_Parameter == 'storage':        
        Result_Parameter_plant='plant.shoot.storage_organs.Wtot'
    if Analysed_Parameter == 'lai':        
        Result_Parameter_plant='plant.shoot.leaf.LAI'
    if Analysed_Parameter == 'developementstage':        
        Result_Parameter_plant='plant.developmentstage.Stage[0]'
    if Analysed_Parameter == 'ETo':        
        Result_Parameter_plant='plant.et.Reference'
    if Analysed_Parameter == 'ETc':        
        Result_Parameter_plant='plant.et.Cropspecific'
    if Analysed_Parameter == 'transpiration':        
        Result_Parameter_plant='plant.et.transpiration'
    if Analysed_Parameter == '':        
        Result_Parameter_plant='plant.et.evaporation'
    if Analysed_Parameter == 'water_uptake':        
        Result_Parameter_plant='plant.Wateruptake'
    if Analysed_Parameter == 'stress':        
        Result_Parameter_plant='(plant.water_stress, plant.nutrition_stress)'
    if Analysed_Parameter == 'potential_depth':        
        Result_Parameter_plant='plant.root.potential_depth'
    if Analysed_Parameter == 'rooting_depth':        
        Result_Parameter_plant='plant.root.depth'
    if Analysed_Parameter == 'branching':        
        Result_Parameter_plant='plant.root.branching'
    if Analysed_Parameter == 'root_growth':        
        Result_Parameter_plant='plant.root.actual_distribution'
    

    if Result_Parameter_plant=='':
        return Result_Parameter,Space_for_Result_Table
    else:
        Result_Parameter=Result_Parameter_plant
        return Result_Parameter,Space_for_Result_Table


def create_Result_Parameter_List(Duration,Result_Parameter,Space_for_Result_Table):
    Result_Parameter_List = np.zeros((Duration),dtype=[(Result_Parameter, 'f8',(Space_for_Result_Table)),('Date', '|S20')])

    for i in range(Duration):
        Day=DataStart+timedelta(days=i)
        Result_Parameter_List['Date'][i]=str(Day.date())

    return Result_Parameter_List


def load_soil_Parameterset(SetupFile):
    if SetupFile['Program_for_SA'][1]=='PMF':
        alpha=0.0138
        ksat=22.1844
        n=1.5631
        porosity=0.4513
        c=cmf1d(ksat,porosity,alpha,n,layercount=50,layerthickness=[0.05]*50)
        return c
    if SetupFile['Program_for_SA'][1]=='CMF':
        for i in range(SetupFile['Number_of_Paramaters_for_Sensitivity_Analysis'][1]):
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'ksat': 
                ksat = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'porosity': 
                porosity = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'alpha': 
                alpha = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'n': 
                n = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
        
        c=cmf1d(ksat,porosity,alpha,n,layercount=50,layerthickness=[0.05]*50)
        return c,ksat,porosity,alpha,n 


def load_random_CropCoefficiants(SetupFile):
    if SetupFile['Program_for_SA'][1]=='PMF':  
        
        for i in range(SetupFile['Number_of_Paramaters_for_Sensitivity_Analysis'][1]):
            
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'tbase': 
                tbase = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(1)][1])#Default: 0
            
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'Stage':           
                min_values_raw  = SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                min_values = min_values_raw.split(',')
                max_values_raw  = SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                max_values = max_values_raw.split(',')              
                          
                stage = [['Emergence',np.random.uniform(float(min_values[0]),float(max_values[0]))],#160
                         ['Leaf development',np.random.uniform(float(min_values[1]),float(max_values[1]))],#208
                         ['Tillering',np.random.uniform(float(min_values[2]),float(max_values[2]))],#421
                         ['Stem elongation',np.random.uniform(float(min_values[3]),float(max_values[3]))],#659
                         ['Anthesis',np.random.uniform(float(min_values[4]),float(max_values[4]))],#901
                         ['Seed fill',np.random.uniform(float(min_values[5]),float(max_values[5]))],#1174
                         ['Dough stage',np.random.uniform(float(min_values[6]),float(max_values[6]))],#1556
                         ['Maturity',np.random.uniform(float(min_values[7]),float(max_values[7]))]]#1665
            
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'RUE': 
                RUE=np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 5.
        
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'k': 
                k=np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: .6
    
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'kcb':           
                min_values_raw  = SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                min_values = min_values_raw.split(',')
                max_values_raw  = SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                max_values = max_values_raw.split(',') 
                
                kcb =[np.random.uniform(float(min_values[0]),float(max_values[0])),
                      np.random.uniform(float(min_values[1]),float(max_values[1])),
                      np.random.uniform(float(min_values[2]),float(max_values[2])), 
                      np.random.uniform(float(min_values[3]),float(max_values[3]))]#Default:[0.15,1.1,0.15]
          
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'leaf_specific_weight': 
                leaf_specific_weight = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(1)][1])#Default: 40
        
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'root_growth': 
                root_growth = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(1)][1])#Default: 1.5
            
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'max_height': 
                max_height = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(1)][1])#Default: 1
         
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'carbonfraction': 
                carbonfraction = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(1)][1])#Default: .4
        
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'max_depth': 
                max_depth = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(1)][1])#Default: 150.
    
    if SetupFile['Program_for_SA'][1] == 'CMF':
        tbase = 0
        stage = [['Emergence',160.],#!!
                 ['Leaf development',208.], 
                 ['Tillering',421.],
                 ['Stem elongation',659.],
                 ['Anthesis',901.],
                 ['Seed fill',1174.],
                 ['Dough stage',1556.],
                 ['Maturity',1665.]]
        RUE=5.
        k=.4
        kcb =[0.15,1.1,0.15]
        leaf_specific_weight=40.
        root_growth=1.5
        max_height=1.
        carbonfraction=.4
        max_depth=150.

    seasons           =[160.0, 499.0, 897.0, 1006.0]    
    shoot_percent     =[.0,.5,.5,.9,.95,1.,1.,1.]
    root_percent      =[.0,.5,.5,.1,.05,.0,.0,.0]
    leaf_percent      =[.0,.5,.5,.5,.0,.0,.0,.0]
    stem_percent      =[.0,.5,.5,.5,.5,.0,.0,.0]
    storage_percent   =[.0,.0,.0,.0,.5,1.,1.,1.]
    pressure_threshold=[0.,1.,500.,16000.]
    plantN            =[[160.,0.043],[1200.,0.016]]
    stress_adaption   =1
    
    random_plant_coeff = PMF.CropCoefficiants(tbase,stage,RUE,k,seasons,kcb,shoot_percent,root_percent,
                             leaf_percent,stem_percent,storage_percent,pressure_threshold, 
                             plantN,leaf_specific_weight,root_growth,max_height,
                             stress_adaption,carbonfraction,max_depth)

    return random_plant_coeff



if __name__=='__main__':
    
    Name_of_SetupFile = 'Setup_file.csv'
    SetupFile = load_Setup_csv_File(Name_of_SetupFile) 
    
    '''
    Check settings for Program use
    '''
    
    
    if SetupFile['Program_for_SA'][1] == 'CMF':
        Program_for_Analysation='CMF'    
        print 'CMF will be analysed'
    
    if SetupFile['Program_for_SA'][1] == 'PMF':
          
        print 'PMF will be analysed'
    
    
    
    ClimateDatafile            = load_ClimateDatafile(SetupFile)
    DataStart                  = getDatastart(ClimateDatafile)
    DataEnd                    = getDataend(ClimateDatafile) 
    Duration                   = (DataEnd-DataStart).days
    Analysed_Parameter         = str(SetupFile['Res_Name_for_Sensitivty_Analysis'][1])
    Result_Parameter_Raw       = get_Result_Parameter(Analysed_Parameter)
    Result_Parameter           = Result_Parameter_Raw[0]
    Space_for_Result_Table     = Result_Parameter_Raw[1]
    Result_Parameter_List      = create_Result_Parameter_List(Duration,Result_Parameter,Space_for_Result_Table)
    baresoil                   = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    Repetitions                = SetupFile['Repetitions_of_Sensitivity_Analysis'][1]
    Plots                      = SetupFile['Number_of_Plots'][1]
    
    Errors=0
    for Repeat in range(Repetitions):
        c_Raw                  = load_soil_Parameterset(SetupFile)
        c                      = c_Raw[0]    
        random_plant_coeff = load_random_CropCoefficiants(SetupFile)
        c.load_meteo(DataStart,DataStart, SetupFile['ClimateData'][1], rain_factor=1.)
        print 'Load Data '+str(Repeat+1)+' of '+str(Repetitions)
        if SetupFile['Program_for_SA'][1] == 'CMF': 
            try:            
                Results            = run.run_CMF_with_PMF_for_one_Simulationperiod(c,random_plant_coeff,DataStart,DataEnd,Result_Parameter,Result_Parameter_List)
                
                with open('Results'+str(Repeat+1)+'.csv', 'wb') as f:    
                    writer = csv.writer(f)
                    writer.writerow(['Settings: ksat='+str(c_Raw[1]),
                                                'porosity='+str(c_Raw[2]),
                                                'alpha='+str(c_Raw[3]), 
                                                'n='+str(c_Raw[4])])
                    for Plot in range(Plots):
                        SensitivityFile            = load_Measured_Data(SetupFile,Plot+1)
                        Measured_Days              = getMeasuredDays(SensitivityFile)
                        writer.writerow([''])
                        writer.writerow(['Values for Plot '+str(Plot+1)])
                        writer.writerow(['Year','Month','Day',Analysed_Parameter])
                        Calculated_Data=[]                        
                        for i in range(len(Measured_Days)):
                            Saving_Day = Measured_Days[i]-DataStart
                            writer.writerow([Measured_Days[i].year, Measured_Days[i].month,Measured_Days[i].day,Results[Result_Parameter][Saving_Day.days]])
                            Calculated_Data.append(Results[Result_Parameter][Saving_Day.days])
                        
                        '''
                        convert Calculated Data into list
                        '''
                        EF_List=[]
                        Bias_List=[]
                        R_squared_List=[]
                        for i in range(len(Calculated_Data[0])):
                            Calc_List=[]                            
                            for j in range(len(Calculated_Data)):
                                Calc_List.append(Calculated_Data[j][i])   
                            Call_String='Data_for_Sensitivity_Analysis_'+str(i)
                            Meas_List=SensitivityFile[Call_String][1:len(SensitivityFile[Call_String])]
                            EF_List.append(stat.Nash_Sutcliff(Meas_List,Calc_List))
                            Bias_List.append(stat.Bias(Meas_List,Calc_List))
                            R_squared_List.append(stat.R_squared(Meas_List,Calc_List))                       
                        writer.writerow(['EF','Bias','R_squared'])
                        for i in range(len(EF_List)):                        
                            writer.writerow([EF_List[i],Bias_List[i],R_squared_List[i]])
                        
            except RuntimeError:
                Errors+=1
                print 'An Error has accourd ('+str(Errors)+' in '+str(Repeat+1)+' runs)'                
                #os.remove('Results'+str(Repeat+1)+'.csv')                
                #print 'Results'+str(Repeat+1)+'.csv has been delted'
    
        if SetupFile['Program_for_SA'][1] == 'PMF': 
            Results            = run.run_CMF_with_PMF_for_one_Simulationperiod(c,random_plant_coeff,DataStart,DataEnd,Result_Parameter,Result_Parameter_List)

            with open('Results'+str(Repeat+1)+'.csv', 'wb') as f:    
                writer = csv.writer(f)
                writer.writerow(['Settings: tbase='+str(random_plant_coeff.tbase),
                                         'stage='+str(random_plant_coeff.stage),
                                         'RUE='+str(random_plant_coeff.RUE),
                                         'k='+str(random_plant_coeff.k),
                                         'seasons='+str(random_plant_coeff.seasons),
                                         'kcb='+str(random_plant_coeff.kcb),
                                         'leaf_specific_weight='+str(random_plant_coeff.leaf_specific_weight),
                                         'root_growth='+str(random_plant_coeff.root_growth),
                                         'max_height='+str(random_plant_coeff.max_height),
                                         'carbonfraction='+str(random_plant_coeff.carbonfraction),
                                         'max_depth='+str(random_plant_coeff.max_depth)])
                writer.writerow([''])
                writer.writerow(['Year','Month','Day',Analysed_Parameter])
                for i in range(len(Measured_Days)):
                    Saving_Day = Measured_Days[i]-DataStart
                    writer.writerow([Measured_Days[i].year, Measured_Days[i].month,Measured_Days[i].day,Results[Result_Parameter][Saving_Day.days]])
    
    




