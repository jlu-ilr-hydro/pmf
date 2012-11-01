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
            ('Parameter5_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter5', '|S40'), ('Max_Rangevalue_of_Parameter5','S40'),
            ('Parameter6_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter6', '|S40'), ('Max_Rangevalue_of_Parameter6','|S40'),
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
    if SetupFile['Program_for_SA'][1]=='PMF':
        fdtype=[('PLOT', '|S10'), ('Year', 'int16'), ('Month', 'int16'), ('Day', 'int16'), ('Data_for_Sensitivity_Analysis_0', 'f8'),('Data_for_Sensitivity_Analysis_1', 'f8'),('Data_for_Sensitivity_Analysis_2', 'f8'),('Data_for_Sensitivity_Analysis_3', 'f8'),('Data_for_Sensitivity_Analysis_4', 'f8'),('Data_for_Sensitivity_Analysis_5', 'f8')]
        Sensitivity = SetupFile['Data_for_Sensitivity_Analysis'][1].split('.')    
        Sensitivity_File_name = Sensitivity[0]+'_Plot'+str(Plot)+'.'+Sensitivity[1] 
        SensitivityFile = np.genfromtxt(Sensitivity_File_name,delimiter=';', dtype=fdtype)
        return SensitivityFile
    
    if SetupFile['Program_for_SA'][1]=='CMF':
        #fdtype=[('PLOT', '|S10'), ('Year', 'int16'), ('Month', 'int16'), ('Day', 'int16'), ('Data_for_Sensitivity_Analysis_0', 'f8'),('Data_for_Sensitivity_Analysis_1', 'f8'),('Data_for_Sensitivity_Analysis_2', 'f8'),('Data_for_Sensitivity_Analysis_3', 'f8'),('Data_for_Sensitivity_Analysis_4', 'f8'),('Data_for_Sensitivity_Analysis_5', 'f8')]
        Sensitivity = SetupFile['Data_for_Sensitivity_Analysis'][1].split('.')    
        Sensitivity_File_name = Sensitivity[0]+'_Plot'+str(Plot)+'.'+Sensitivity[1]   
        SensitivityFile = np.genfromtxt(Sensitivity_File_name,delimiter=';',names=True)
        return SensitivityFile

def load_headers(SetupFile,Plot):
    '''
    Loads Headers of Measured File
    expects 4 columns with for example 'Plot,Year,Month,Day' and reads all Headers after that    
    returns a List
    '''
    Sensitivity = SetupFile['Data_for_Sensitivity_Analysis'][1].split('.')    
    Sensitivity_File_name = Sensitivity[0]+'_Plot'+str(Plot)+'.'+Sensitivity[1]    
    HeaderFile =file(Sensitivity_File_name)     
    #Headers=HeaderFile.readline().split(';')[4:]
    Headers=HeaderFile.readline()[20:]    
    return Headers

def getMeasuredDays(SensitivityFile,SetupFile):
    Measured_Days= []
    if SetupFile['Program_for_SA'][1]=='PMF':
        for i in range(len(SensitivityFile['Year'])-1):
            Measured_Days.append(datetime(SensitivityFile['Year'][i+1],SensitivityFile['Month'][i+1],SensitivityFile['Day'][i+1]))
        return Measured_Days
    if SetupFile['Program_for_SA'][1]=='CMF':
        for i in range(len(SensitivityFile['Year'])):
            Measured_Days.append(datetime(int(SensitivityFile['Year'][int(i)]),int(SensitivityFile['Month'][int(i)]),int(SensitivityFile['Day'][int(i)])))
        return Measured_Days

'''
Get command for Analysed Parameter
'''
def get_Result_Parameter(Analysed_Parameter):  
    '''
    
    Sets the command for the runtime in Run_CMF_PMF_Tool
    This command will be called and the result saved for every day
    '''
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
    if Analysed_Parameter == 'Kersebaum_yield':
        Result_Parameter_plant='[plant.RootCarbon*10, plant.root.Wtot*10, plant.StemCarbon*10+plant.LeafCarbon*10, plant.shoot.leaf.Wtot*10+plant.shoot.stem.Wtot*10, plant.StorageCarbon*10, plant.shoot.storage_organs.Wtot*10]'
        Space_for_Result_Table = 6
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


#def load_soil_Parameterset(Setupfile):
#    #old
##    alpha=0.0138
##    ksat=22.1844
##    n=1.5631
##    porosity=0.4513
#    alpha=0.0153
#    ksat=22.431
#    n=1.3743
#    porosity=0.3326
#
#    c=cmf1d(ksat,porosity,alpha,n,layercount=50,layerthickness=[0.05]*50)
#    #c=cmf1d(sand=[90.00,90.00,90.00,90.00,90.00,90.00,90.00,90.00,90.00,90.00,90.00,90.00,90.00,88.33,86.67,85.00,83.33,81.67,80.00,82.00,84.00,86.00,88.00,90.00,92.00,92.33,92.67,93.00,93.33,93.67,94.00,94.13,94.27,94.40,94.53,94.67,94.80,94.93,95.07,95.20,95.33,95.47,95.60,95.73,95.87,96.00],silt=[2.00,2.17,2.33,2.50,2.67,2.83,3.00,3.33,3.67,4.00,4.33,4.67,5.00,5.50,6.00,6.50,7.00,7.50,8.00,7.33,6.67,6.00,5.33,4.67,4.00,3.83,3.67,3.50,3.33,3.17,3.00,2.93,2.87,2.80,2.73,2.67,2.60,2.53,2.47,2.40,2.33,2.27,2.20,2.13,2.07,2.00],clay=[8.00,7.83,7.67,7.50,7.33,7.17,7.00,6.67,6.33,6.00,5.67,5.33,5.00,6.17,7.33,8.50,9.67,10.83,12.00,10.67,9.33,8.00,6.67,5.33,4.00,3.83,3.67,3.50,3.33,3.17,3.00,2.93,2.87,2.80,2.73,2.67,2.60,2.53,2.47,2.40,2.33,2.27,2.20,2.13,2.07,2.00],c_org=[76.00,74.33,72.67,71.00,69.33,67.67,66.00,57.67,49.33,41.00,32.67,24.33,16.00,14.67,13.33,12.00,10.67,9.33,8.00,6.67,5.33,4.00,2.67,1.33,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],bedrock_K=0.01,layercount=6,layerthickness=[.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05],tracertext='')
#    return c,ksat,porosity,alpha,n 
    
def load_soil_Parameterset(SetupFile):
    if SetupFile['Program_for_SA'][1]=='PMF':
        alpha=0.0153
        ksat=22.431
        n=1.3743
        porosity=0.3326
        c=cmf1d(ksat,porosity,alpha,n,layercount=50,layerthickness=[0.05]*50)
        return c,ksat,porosity,alpha,n
    if SetupFile['Program_for_SA'][1]=='CMF':
#        for i in range(SetupFile['Number_of_Paramaters_for_Sensitivity_Analysis'][1]):
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'ksat': 
#                ksat = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'porosity': 
#                porosity = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'alpha': 
#                alpha = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'n': 
#                n = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])
        #alpha=0.0138
        #ksat=22.1844
        #n=1.5631
        #porosity=0.4513     
        alpha=0.0153
        ksat=22.431
        n=1.3743
        porosity=0.3326
        c=cmf1d(ksat,porosity,alpha,n,layercount=50,layerthickness=[0.05]*50)
        return c,ksat,porosity,alpha,n 


def load_random_CropCoefficiants(SetupFile):
    if SetupFile['Program_for_SA'][1]=='PMF':  
        
        for i in range(SetupFile['Number_of_Paramaters_for_Sensitivity_Analysis'][1]):
            
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'tbase': 
                tbase = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 0
            #else:
            #    tbase=0
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'Stage':           
                min_values_raw  = SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                min_values = min_values_raw.split(',')
                max_values_raw  = SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                max_values = max_values_raw.split(',')              
                 
                stage = [['Emergence',np.random.uniform(float(min_values[0]),float(max_values[0]))],
                         ['Leaf development',np.random.uniform(float(min_values[1]),float(max_values[1]))],
                         ['Anthesis',np.random.uniform(float(min_values[2]),float(max_values[2]))],
                         ['Maturity',np.random.uniform(float(min_values[3]),float(max_values[3]))]]
                 
#                stage = [['Emergence',np.random.uniform(float(min_values[0]),float(max_values[0]))],#160
#                         ['Leaf development',np.random.uniform(float(min_values[1]),float(max_values[1]))],#208
#                         ['Tillering',np.random.uniform(float(min_values[2]),float(max_values[2]))],#421
#                         ['Stem elongation',np.random.uniform(float(min_values[3]),float(max_values[3]))],#659
#                         ['Anthesis',np.random.uniform(float(min_values[4]),float(max_values[4]))],#901
#                         ['Seed fill',np.random.uniform(float(min_values[5]),float(max_values[5]))],#1174
#                         ['Dough stage',np.random.uniform(float(min_values[6]),float(max_values[6]))],#1556
#                         ['Maturity',np.random.uniform(float(min_values[7]),float(max_values[7]))]]#1665
            
#            else:
#                stage=[['Emergence',160.],#!!
#                 ['Leaf development',208.], 
#                 ['Tillering',421.],
#                 ['Stem elongation',659.],
#                 ['Anthesis',901.],
#                 ['Seed fill',1174.],
#                 ['Dough stage',1556.],
#                 ['Maturity',1665.]]
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'RUE': 
                RUE=np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 5.
#            else:
#                RUE=5
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'k': 
                k=np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: .6
#            else:
#                k=.4
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'kcb':           
                min_values_raw  = SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                min_values = min_values_raw.split(',')
                max_values_raw  = SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1].strip('[]')
                max_values = max_values_raw.split(',') 
                
                kcb =[np.random.uniform(float(min_values[0]),float(max_values[0])),
                      np.random.uniform(float(min_values[1]),float(max_values[1])),
                      np.random.uniform(float(min_values[2]),float(max_values[2]))]#Default:[0.15,1.1,0.15]
#            else:
#                kcb=[0.15,1.1,0.15]
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'leaf_specific_weight': 
#                leaf_specific_weight = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 40
#            else:
#                leaf_specific_weight=40
            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'root_growth': 
                root_growth = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 1.5
#            else:
#                root_growth=1.5
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'max_height': 
#                max_height = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 1
#            else:
#                max_height=1.
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'carbonfraction': 
#                carbonfraction = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: .4
#            else:
#                carbonfraction = .4
#            if SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1] == 'max_depth': 
#                max_depth = np.random.uniform(SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1],SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1])#Default: 150.
#            else:
#                max_depth = 150.

    random_plant_coeff = PMF.CropCoefficiants()
    if SetupFile['Program_for_SA'][1]=='PMF':
        random_plant_coeff.tbase                 = tbase
        random_plant_coeff.stage                 = [['Emergence', 135], ['Leaf development', 558],['S',600],['T',700], ['Anthesis', 1267],['R',1300],['U',1400], ['Maturity', 1592]]  #stage
        random_plant_coeff.RUE                   = RUE                 
        random_plant_coeff.k                     = k
        random_plant_coeff.kcb                   = kcb
        #random_plant_coeff.leaf_specific_weight  = leaf_specific_weight
        random_plant_coeff.root_growth           = root_growth
        #random_plant_coeff.max_height            = max_height
        #random_plant_coeff.carbonfraction        = carbonfraction
        #random_plant_coeff.max_depth             = max_depth
        #random_plant_coeff = PMF.CropCoefficiants() # entfernen für zufällige Verteilung!!!
        
#        ['Emergence', 54], ['Leaf development', 403], ['Anthesis'], ['Maturity', 1826]
      
        print random_plant_coeff.stage
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
    Repetitions                = SetupFile['Repetitions_of_Sensitivity_Analysis'][1]
    Plots                      = SetupFile['Number_of_Plots'][1]
    Errors=0
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    
    for Repeat in range(Repetitions):
        c_Settings                  = load_soil_Parameterset(SetupFile)
        c                           = c_Settings[0]    
        random_plant_coeff               = load_random_CropCoefficiants(SetupFile)
        c.load_meteo(DataStart,DataStart, SetupFile['ClimateData'][1], rain_factor=1.)
        print 'Load Data '+str(Repeat+1)+' of '+str(Repetitions)
         
        try:            
            Results            = run.run_CMF_with_PMF_for_one_Simulationperiod(c,DataStart,DataEnd,Result_Parameter,Result_Parameter_List,random_plant_coeff)
            
            
            with open('Results'+str(Repeat+1)+Analysed_Parameter+'_test.csv', 'wb') as f:    
                writer = csv.writer(f)
                #######
                #Write Header with Settings
                if SetupFile['Program_for_SA'][1] == 'CMF':
                    writer.writerow(['Settings:'])
                    writer.writerow(['ksat='+str(c_Settings[1])+';'+
                                     'porosity='+str(c_Settings[2])+';'+
                                     'alpha='+str(c_Settings[3])+';'+ 
                                     'n='+str(c_Settings[4])])
                                                
                if SetupFile['Program_for_SA'][1] == 'PMF':    
                    writer.writerow(['Settings:'])
                    writer.writerow(['CropCoeff:'+';'+'tbase'+';'+'stage1_Emergence'+';'+'stage2_LeafDevelopment'+';'+'stage3_Tillering'+';'+'stage4_TemElongation'+';'+'stage5_Anthesis'+';'+'stage6_SeedFill'+';'+'stage7_DoughStage'+';'+'stage8_Maturity'
                                    +';'+'RUE'+';'+'k'
                                    +';'+'kcb1'+';'+'kcb2'+';'+'kcb3'+';'+'leaf_specific_weight'+';'+'root_growth'
                                    +';'+'max_height'+';'+'carbonfraction'+';'+'max_depth'])
                    writer.writerow(['RandomValue'+ ' ; '+str(random_plant_coeff.tbase)  +';'+str(random_plant_coeff.stage[0][1])+';'+str(random_plant_coeff.stage[1][1])+';'+str(random_plant_coeff.stage[2][1])+';'+str(random_plant_coeff.stage[3][1])+';'+str(random_plant_coeff.stage[4][1])+';'+str(random_plant_coeff.stage[5][1])+';'+str(random_plant_coeff.stage[6][1])+';'+str(random_plant_coeff.stage[7][1])
                                +';'+str(random_plant_coeff.RUE)           +';'+str(random_plant_coeff.k)
                                +';'+str(random_plant_coeff.kcb[0])        +';'+str(random_plant_coeff.kcb[1])+';'+str(random_plant_coeff.kcb[2])           +';'+str(random_plant_coeff.leaf_specific_weight) 
                                +';'+str(random_plant_coeff.root_growth)   +';'+str(random_plant_coeff.max_height)
                                +';'+str(random_plant_coeff.carbonfraction)+';'+str(random_plant_coeff.max_depth)])      
                    writer.writerow(['Default:;0;160;208;421;659;901;1174;1556;1665;3;0.4;0.15;1.1;0.15;40;1.5;1;0.4;150'])                 
#                    writer.writerow(['tbase='+str(random_plant_coeff.tbase)+' ; '+
#                                     'stage='+str(random_plant_coeff.stage)+' ; '+
#                                     'RUE='+str(random_plant_coeff.RUE)+' ; '+
#                                     'k='+str(random_plant_coeff.k)+' ; '+
#                                     'seasons='+str(random_plant_coeff.seasons)+' ; '+
#                                     'kcb='+str(random_plant_coeff.kcb)+' ; '+
#                                     'leaf_specific_weight='+str(random_plant_coeff.leaf_specific_weight)+' ; '+
#                                     'root_growth='+str(random_plant_coeff.root_growth)+' ; '+
#                                     'max_height='+str(random_plant_coeff.max_height)+' ; '+
#                                     'carbonfraction='+str(random_plant_coeff.carbonfraction)+' ; '+
#                                     'max_depth='+str(random_plant_coeff.max_depth)])                        
                
                ######
                #Write Results
                for Plot in range(Plots):
                    #Headers                    = load_headers(SetupFile,Plot+1)
                    #Headers_String=''
                    #for i in range(len(Headers)):
                    #    if i ==len(Headers)-1:
                    #        Headers_String+=str(Headers[i])
                    #    else:
                    #        Headers_String+=str(Headers[i])+' ; '
                    SensitivityFile            = load_Measured_Data(SetupFile,Plot+1)
                    Measured_Days              = getMeasuredDays(SensitivityFile,SetupFile)
                    writer.writerow([''])
                    writer.writerow(['Values for Plot '+str(Plot+1)])
                    #writer.writerow([Headers_String])#+'; '+'Year'+' ; '+'Month'+' ; '+'Day'])
                    #writer.writerow([Headers])
                    if SetupFile['Program_for_SA'][1] == 'PMF':
                        writer.writerow([';Calc_Root_kgC;Meas_Root_kgC;;Calc_Root_kgha;Meas_Root_kgha;;Calc_StemLeaves_kgC;Meas_StemLeaves_kgC;;Calc_StemLeaves_kgha;Meas_StemLeaves_kgha;;Calc_StorageOrgans_kgC;Meas_StorageOrgans_kgC;;Calc_StorageOrgans_kgha;Meas_StorageOrgans_kgha;;Year;Month;Day'])
                    if SetupFile['Program_for_SA'][1] == 'CMF':
                        writer.writerow([';Calc_Water030cm;Meas__Water030cm;;Calc_Water3060cm;Meas__Water3060cm;;Calc_Water60_90cm;Meas_Water60_90cm'])
                    Calculated_Data=[]
                    for i in range(len(Measured_Days)):
                        Saving_Day = Measured_Days[i]-DataStart
                        if SetupFile['Program_for_SA'][1] == 'PMF':                         
                            writer.writerow([';'+str(Results[Result_Parameter][Saving_Day.days][0])+';'+str(SensitivityFile[i+1][4])+';;'+str(Results[Result_Parameter][Saving_Day.days][1])+';'+str(SensitivityFile[i+1][5])+';;'+str(Results[Result_Parameter][Saving_Day.days][2])+';'+str(SensitivityFile[i+1][6])+';;'+str(Results[Result_Parameter][Saving_Day.days][3])+';'+str(SensitivityFile[i+1][7])+';;'+str(Results[Result_Parameter][Saving_Day.days][4])+';'+str(SensitivityFile[i+1][8])+';;'+str(Results[Result_Parameter][Saving_Day.days][5])+';'+str(SensitivityFile[i+1][9])+';;'+str(Measured_Days[i].year)+';'+str(Measured_Days[i].month)+';'+str(Measured_Days[i].day)])                        
                        if SetupFile['Program_for_SA'][1] == 'CMF':
                            writer.writerow([';'+str(Results[Result_Parameter][Saving_Day.days][0])+';'+str(SensitivityFile[i][4])+';;'+str(Results[Result_Parameter][Saving_Day.days][1])+';'+str(SensitivityFile[i][5])+';;'+str(Results[Result_Parameter][Saving_Day.days][2])+';'+str(SensitivityFile[i][6])+';;'+str(Measured_Days[i].year)+';'+str(Measured_Days[i].month)+';'+str(Measured_Days[i].day)])
                        #Row = str(Results[Result_Parameter][Saving_Day.days])+';'+str(Measured_Days[i].year)+';'+str(Measured_Days[i].month)+';'+str(Measured_Days[i].day)
                        #Result = Row.split(' ; ')[0].strip(']').strip('[').split('   ')
                        
                        #Result_String=''
                        #for i in range(len(Result)):
                        #    if i ==len(Result)-1:
                        #        Result_String+=str(Result[i])
                        #    else:
                        #        Result_String+=str(Result[i])+';'
                        #writer.writerow([Row[0],Row[1],Row[2],Result_String])
                        Calculated_Data.append(Results[Result_Parameter][Saving_Day.days])

                    
                    #########
                    #Make Statistik
                    EF_List=[]
                    Bias_List=[]
                    R_squared_List=[]  
                    if SetupFile['Program_for_SA'][1] == 'PMF': 
                        for i in range(len(Calculated_Data[0])):
                            Calc_List=[]                            
                            for j in range(len(Calculated_Data)):
                                Calc_List.append(Calculated_Data[j][i])   
                            Call_String='Data_for_Sensitivity_Analysis_'+str(i)
                            Meas_List=SensitivityFile[Call_String][1:len(SensitivityFile[Call_String])]
                                                    
                            for i in range(len(Meas_List)):
                                if Meas_List[i] == -99999:
                                    Calc_List[i]=-99999
                            
                            
                            Meas_List_for_stat=[]
                            Calc_List_for_stat=[]
                            
                            for i in range(len(Meas_List)):
                                Meas_List_for_stat.append(Meas_List[i])
                                Calc_List_for_stat.append(Calc_List[i])
                                                    
                            k=0                                
                            for i in range(len(Meas_List)):
                                if Meas_List[i] ==-99999:
                                    '''
                                    Cleans out all no data values for Statistik
                                    '''
                                    Calc_List_for_stat.pop(i-k)
                                    Meas_List_for_stat.pop(i-k)
                                    k+=1
                            EF_List.append(stat.Nash_Sutcliff(Meas_List_for_stat,Calc_List_for_stat))
                            Bias_List.append(stat.Bias(Meas_List_for_stat,Calc_List_for_stat))
                            R_squared_List.append(stat.R_squared(Meas_List_for_stat,Calc_List_for_stat))
                        
                        writer.writerow([''])
                        writer.writerow(['EF'+';'+str(EF_List[0])+';;;'+str(EF_List[1])+';;;'+str(EF_List[2])+';;;'+str(EF_List[3])+';;;'+str(EF_List[4])+';;;'+str(EF_List[5])])
                        writer.writerow(['Bias'+';'+str(Bias_List[0])+';;;'+str(Bias_List[1])+';;;'+str(Bias_List[2])+';;;'+str(Bias_List[3])+';;;'+str(Bias_List[4])+';;;'+str(Bias_List[5])])
                        writer.writerow(['R_squared'+';'+str(R_squared_List[0])+';;;'+str(R_squared_List[1])+';;;'+str(R_squared_List[2])+';;;'+str(R_squared_List[3])+';;;'+str(R_squared_List[4])+';;;'+str(R_squared_List[5])])

                    if SetupFile['Program_for_SA'][1] == 'CMF':
                        Meas_List=[]
                        for i in range(len(SensitivityFile)):
                                Meas_List.append([SensitivityFile['WATER_0_30_CM_VOL_PROZ'][i], SensitivityFile['WATER_30_60_CM_VOL_PROZ'][i], SensitivityFile['WATER_60_90_CM_VOL_PROZ'][i]])
                        for i in range(len(Calculated_Data[0])):
                            Calc_List_for_stat=[]
                            Meas_List_for_stat=[]                            
                            for j in range(len(Calculated_Data)):
                                Calc_List_for_stat.append(Calculated_Data[j][i])  
                                Meas_List_for_stat.append(Meas_List[j][i])
                            EF_List.append(stat.Nash_Sutcliff(Meas_List_for_stat,Calc_List_for_stat))
                            Bias_List.append(stat.Bias(Meas_List_for_stat,Calc_List_for_stat))
                            R_squared_List.append(stat.R_squared(Meas_List_for_stat,Calc_List_for_stat)) 
                        writer.writerow([''])
                        writer.writerow(['EF'+';'+str(EF_List[0])+';;;'+str(EF_List[1])+';;;'+str(EF_List[2])])
                        writer.writerow(['Bias'+';'+str(Bias_List[0])+';;;'+str(Bias_List[1])+';;;'+str(Bias_List[2])])
                        writer.writerow(['R_squared'+';'+str(R_squared_List[0])+';;;'+str(R_squared_List[1])+';;;'+str(R_squared_List[2])])
            f.close()                           
        except RuntimeError:
            Errors+=1
            print 'An Error has accourd ('+str(Errors)+' in '+str(Repeat+1)+' runs)'  



























              
            #os.remove('Results'+str(Repeat+1)+'.csv')                
            #print 'Results'+str(Repeat+1)+'.csv has been delted'
#    
#        if SetupFile['Program_for_SA'][1] == 'PMF': 
#            Results            = run.run_CMF_with_PMF_for_one_Simulationperiod(c,random_plant_coeff,DataStart,DataEnd,Result_Parameter,Result_Parameter_List)
#
#            with open('Results'+str(Repeat+1)+'.csv', 'wb') as f:    
#                writer = csv.writer(f)
#                writer.writerow(['Settings: tbase='+str(random_plant_coeff.tbase),
#                                         'stage='+str(random_plant_coeff.stage),
#                                         'RUE='+str(random_plant_coeff.RUE),
#                                         'k='+str(random_plant_coeff.k),
#                                         'seasons='+str(random_plant_coeff.seasons),
#                                         'kcb='+str(random_plant_coeff.kcb),
#                                         'leaf_specific_weight='+str(random_plant_coeff.leaf_specific_weight),
#                                         'root_growth='+str(random_plant_coeff.root_growth),
#                                         'max_height='+str(random_plant_coeff.max_height),
#                                         'carbonfraction='+str(random_plant_coeff.carbonfraction),
#                                         'max_depth='+str(random_plant_coeff.max_depth)])
#                for Plot in range(Plots):
#                        Headers                    = load_headers(SetupFile,Plot+1)
#                        SensitivityFile            = load_Measured_Data(SetupFile,Plot+1)
#                        Measured_Days              = getMeasuredDays(SensitivityFile)
#                        writer.writerow([''])
#                        writer.writerow(['Values for Plot '+str(Plot+1)])
#                        writer.writerow(['Year','Month','Day',Analysed_Parameter,Headers])
#                        Calculated_Data=[]                        
#                        for i in range(len(Measured_Days)):
#                            Saving_Day = Measured_Days[i]-DataStart
#                            writer.writerow([Measured_Days[i].year, Measured_Days[i].month,Measured_Days[i].day,Results[Result_Parameter][Saving_Day.days]])
#                            Calculated_Data.append(Results[Result_Parameter][Saving_Day.days])
#                        
#                        '''
#                        convert Calculated Data into list
#                        '''
#                        EF_List=[]
#                        Bias_List=[]
#                        R_squared_List=[]
#                        for i in range(len(Calculated_Data[0])):
#                            Calc_List=[]                            
#                            for j in range(len(Calculated_Data)):
#                                Calc_List.append(Calculated_Data[j][i])   
#                            Call_String='Data_for_Sensitivity_Analysis_'+str(i)
#                            Meas_List=SensitivityFile[Call_String][1:len(SensitivityFile[Call_String])]
#                            EF_List.append(stat.Nash_Sutcliff(Meas_List,Calc_List))
#                            Bias_List.append(stat.Bias(Meas_List,Calc_List))
#                            R_squared_List.append(stat.R_squared(Meas_List,Calc_List))                       
#                        writer.writerow(['EF','Bias','R_squared'])
#                        for i in range(len(EF_List)):                        
#                            writer.writerow([EF_List[i],Bias_List[i],R_squared_List[i]])
#                    

#                writer.writerow([''])
#                writer.writerow(['Year','Month','Day',Analysed_Parameter])
#                for i in range(len(Measured_Days)):
#                    Saving_Day = Measured_Days[i]-DataStart
#                    writer.writerow([Measured_Days[i].year, Measured_Days[i].month,Measured_Days[i].day,Results[Result_Parameter][Saving_Day.days]])
#    
#    




