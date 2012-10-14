# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:42:57 2012

@author: Tobias
"""
from numpy import *
from datetime import *
import Run_CMF_with_PMF_Tool as run
import csv
#import cmf



'''
Load Setupfile
'''
Setup = 'Setup_file.csv'
idtype=[('InputData', '|S25'), ('ClimateData', '|S25'), 
        ('Program_for_SA','|S10'),
        ('Res_Name_for_Sensitivty_Analysis', '|S40'), ('Data_for_Sensitivity_Analysis', '|S50'),
        ('Repetitions_of_Sensitivity_Analysis','int32'), 
        ('Number_of_Paramaters_for_Sensitivity_Analysis', 'int16'),        
        ('Parameter1_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter1', 'f8'), ('Max_Rangevalue_of_Parameter1','f8'),
        ('Parameter2_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter2', 'f8'), ('Max_Rangevalue_of_Parameter2','f8'),
        ('Parameter3_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter3', 'f8'), ('Max_Rangevalue_of_Parameter3','f8'),
        ('Parameter4_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter4', 'f8'), ('Max_Rangevalue_of_Parameter4','f8'),
        ('Parameter5_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter5', 'f8'), ('Max_Rangevalue_of_Parameter5','f8'),
        ('Parameter6_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter6', 'f8'), ('Max_Rangevalue_of_Parameter6','f8'),
        ('Parameter7_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter7', 'f8'), ('Max_Rangevalue_of_Parameter7','f8'),
        ('Parameter8_for_Sensitivity_Analysis', '|S40'), ('Min_Rangevalue_of_Parameter8', 'f8'), ('Max_Rangevalue_of_Parameter8','f8')]
SetupFile = np.genfromtxt(Setup,delimiter=';',names=True, dtype=idtype)




'''
Load Climate Data
'''
dtype=dtype([('Date', 'S20'), ('DOY', '<f8'), ('Rain_mm', '<f8'), ('Tmax_C', '<f8'), ('Tmin_C', '<f8'), ('Rhmin', '<f8'), ('Rhmax', '<f8'), ('Windspeed_ms', '<f8'), ('RS_MJm\xb2day', '<f8'), ('Sunshine_', '<f8')])
ClimateDatafile = np.genfromtxt(SetupFile['ClimateData'][1],delimiter=';',names=True, dtype=dtype)

RawStart= ClimateDatafile['Date'][0]
RawEnd= ClimateDatafile['Date'][len(ClimateDatafile['Date'])-1]

Split_RawStart = RawStart.split('.')
Split_RawEnd = RawEnd.split('.')

DataStart = datetime(int(Split_RawStart[2]),int(Split_RawStart[1]),int(Split_RawStart[0]))
#DataEnd=datetime(1992,12,31)
DataEnd = datetime(int(Split_RawEnd[2]),int(Split_RawEnd[1]),int(Split_RawEnd[0]))




'''
Load Data for Sensitivity Analysis
'''
Sensitivity = SetupFile['Data_for_Sensitivity_Analysis'][1]
fdtype=[('PLOT', '|S10'), ('YEAR_', 'int16'), ('MONTH_', 'int16'), ('DAY_', 'int16'), ('WATER_0_30_CM_VOL_PROZ', 'f8')]
SensitivityFile = np.genfromtxt(Sensitivity,delimiter=';',names=True, dtype=fdtype)
Measured_Days= []
for i in range(len(SensitivityFile['Year'])):
    Measured_Days.append(datetime(SensitivityFile['Year'][i],SensitivityFile['Month'][i],SensitivityFile['Day'][i]))




'''
Load Parameter with range into numpy Array
'''
Parameterset = np.zeros((SetupFile['Number_of_Paramaters_for_Sensitivity_Analysis'][1],),dtype=[('Parameter', 'a20'),('Min_value', 'f8'),('Max_value', 'f8')])

for i in range(SetupFile['Number_of_Paramaters_for_Sensitivity_Analysis'][1]):
    Parameterset[i][0] = SetupFile['Parameter'+str(i+1)+'_for_Sensitivity_Analysis'][1]
    Parameterset[i][1] = SetupFile['Min_Rangevalue_of_Parameter'+str(i+1)][1]
    Parameterset[i][2] = SetupFile['Max_Rangevalue_of_Parameter'+str(i+1)][1]
    



'''
Check settings for Program use
'''
if SetupFile['Program_for_SA'][1] == 'CMF':
    Set_Van_Genuchten_values=False    
    print 'CMF will be analysed'

if SetupFile['Program_for_SA'][1] == 'PMF':
    Set_Van_Genuchten_values=True    
    print 'PMF will be analysed'




'''
Get command for Analysed Parameter
'''
Analysed_Parameter = str(SetupFile['Res_Name_for_Sensitivty_Analysis'][1])

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

#if plant:
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
    Plant = False
else:
    Plant = True
    Result_Parameter=Result_Parameter_plant





'''
Run PMF with CMF
''' 
print 'Load Data from '+str(SetupFile['Program_for_SA'][1])  
Result_all = run.Sensitivity_Analysis(SetupFile, ClimateDatafile, DataStart, DataEnd, SensitivityFile, Parameterset, Set_Van_Genuchten_values, Result_Parameter, Result_Parameter_plant, Measured_Days, Plant, Space_for_Result_Table)
    




'''
Pick only data on days with measuerments
'''
Calculated_Days = []
for i in range(len(Result_all['Year'])):
    Calculated_Days.append(datetime(int(Result_all['Year'][i]),int(Result_all['Month'][i]),int(Result_all['Day'][i])))

Results_for_Comparision=[]
Days=[]
for i in range(len(Measured_Days)):
    for j in range(len(Calculated_Days)):
        if Measured_Days[i]==Calculated_Days[j]:
            Results_for_Comparision.append(Result_all[Result_Parameter][j])
            Days.append(Calculated_Days[j])
 


    
'''
Write Result in .csv File
'''
print 'Saving results in "Results.csv"'
with open('Results.csv', 'wb') as f:    
    writer = csv.writer(f) 
    writer.writerow(['Year','Month','Day',Analysed_Parameter])
    for i in range(len(Results_for_Comparision)):
        writer.writerow([Days[i].year,Days[i].month,Days[i].day,Results_for_Comparision[i]])







