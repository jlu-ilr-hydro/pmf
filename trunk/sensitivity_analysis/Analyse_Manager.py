# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 17:20:55 2012

@author: Pooder
"""
import numpy as np
from datetime import *
import matplotlib.pyplot as plt
import math
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.dates import date2num

def load_Settings_for_all_files(Runs, Setting_Parameter):
    if Setting_Parameter == 'tbase':
        Step=1
    if Setting_Parameter == 'Emergence':
        Step=2
    if Setting_Parameter == 'LeafDevelopment':
        Step=3
    if Setting_Parameter == 'Tillering':
        Step=4
    if Setting_Parameter == 'StemElongation':
        Step=5
    if Setting_Parameter == 'Anthesis':
        Step=6
    if Setting_Parameter == 'SeedFill':
        Step=7
    if Setting_Parameter == 'DoughStage':
        Step=8
    if Setting_Parameter == 'Maturity':
        Step=9
    if Setting_Parameter == 'RUE':
        Step=10
    if Setting_Parameter == 'k':
        Step=11
    if Setting_Parameter == 'kcb1':
        Step=12
    if Setting_Parameter == 'kcb2':
        Step=13
    if Setting_Parameter == 'kcb3':
        Step=14
    if Setting_Parameter == 'root_growth':
        Step=15
    
    Settings_List=[]
    for csv_Files in range(1000):
        j=csv_Files+1                
        Resultfile_Jump=j*100
        Resultfile = 'Results%05i.csv'%(Resultfile_Jump)
        File=file(Resultfile)
        Number_of_runs_in_file=file_lenght(Resultfile)/58
        File_for_one_run=[]
        for Jump in range(Position_of_Resultfile):        
            for rows in range(58):
                File.readline()
        for rows in range(58):
            File_for_one_run.append(File.readline())   
    
        for Number_of_run in range(Number_of_runs_in_file):
            
            Setting=File_for_one_run[2]
            Settings_List.append(Setting.split(';')[Step])
        #print Settings_List
#            for i in range(len(Setting_Names)):
#                if i==0:
#                    Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '
#                if i==1:
#                    Setting_String+=str(int(round(float(Setting_List[0][1+1]),0)))+', '+str(int(round(float(Setting_List[0][2+1]),0)))+', '+str(int(round(float(Setting_List[0][3+1]),0)))+', '+str(int(round(float(Setting_List[0][4+1]),0)))+', '+str(int(round(float(Setting_List[0][5+1]),0)))+', '+str(int(round(float(Setting_List[0][6+1]),0)))+', '+str(int(round(float(Setting_List[0][7+1]),0)))+','
#                if i==9:
#                    Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '             
#                if i==10:
#                    Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '            
#                if i==11:
#                    Setting_String+=str(round(float(Setting_List[0][11+1]),2))+', '+str(round(float(Setting_List[0][12+1]),2))+', '+str(round(float(Setting_List[0][13+1]),2))+', '        
#                if i==14:
#                    Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))
#        
#            Settings_List.append(load_Settings_for_one_file(Resultfile, Number_of_run).split(',')[Step])
            #print load_Settings_for_one_file(Resultfile, Number_of_run).split(',')[Step]    
            #print Result_for_one_run[14].split(';')   
        #    Statistik = load_Result_Table(Result_for_one_run) 
#    for Number in range(Runs):
#        try:
#            Resultfile = file('Results'+str(Number)+'Kersebaum_yield_test.csv')
#            Resultfile.readline()#Setting:
#            Resultfile.readline()#tbase,stage, etc.
#            Settings = Resultfile.readline()
#            Settings_List.append(Settings.split(';')[Step])
#        except: IOError
    return Settings_List




def load_Settings_for_one_file(Name_of_Resultfile,Position_of_Resultfile):
    #Resultfile=file(Resultfile)
    File=file(Name_of_Resultfile)
    File_for_one_run=[]
    for Jump in range(Position_of_Resultfile):        
        for rows in range(58):
            File.readline()
    for rows in range(58):
        File_for_one_run.append(File.readline())    
    Setting_List=[]   
    #Resultfile.readline()#Setting:
    #Resultfile.readline()#tbase,stage, etc.
    #Setting = Resultfile.readline()
    Setting=File_for_one_run[2]
    Setting_List.append(Setting.split(';'))
    
    Setting_Names=['tbase','Emergence','LeafDevelopment','Tillering','StemElongation','Anthesis','SeedFill','DoughStage',
    'Maturity','RUE','k','kcb1','kcb2','kcb3',
    'root_growth']
    Setting_String=''
    

    for i in range(len(Setting_Names)):
        if i==0:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),4))+', '
        if i==1:
            Setting_String+='Stage=['+str(int(round(float(Setting_List[0][1+1]),0)))+', '+str(int(round(float(Setting_List[0][2+1]),0)))+', '+str(int(round(float(Setting_List[0][3+1]),0)))+', '+str(int(round(float(Setting_List[0][4+1]),0)))+', '+str(int(round(float(Setting_List[0][5+1]),0)))+', '+str(int(round(float(Setting_List[0][6+1]),0)))+', '+str(int(round(float(Setting_List[0][7+1]),0)))+', '+str(int(round(float(Setting_List[0][8+1]),0)))+'],\n'
        if i==9:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),4))+', '             
        if i==10:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),4))+', '            
        if i==11:
            Setting_String+='kcb=['+str(round(float(Setting_List[0][11+1]),2))+', '+str(round(float(Setting_List[0][12+1]),2))+', '+str(round(float(Setting_List[0][13+1]),2))+'], '        
        if i==14:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),4))
        
    return Setting_String


def file_lenght(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

    
def Overview(Runs,Min_EF,Min_Bias,Max_Bias,Min_R_Squared):       
    Good_runs_Plot1=0
    Good_runs_Plot2=0
    Good_runs_Plot3=0
    Good_Setting_Files_Plot1=[]
    Good_Setting_Files_Plot2=[]
    Good_Setting_Files_Plot3=[]
    
    Succeeded_Runs=0
    
    Failed_for_EF=0
    Failed_for_Bias=0
    Failed_for_R_Squared=0
    #Good_Setting_Files_Plot[='String'

    #for Number in range(Runs):
        #try:
    for csv_Files in range(Runs/100):
        j=csv_Files+1                
        Resultfile_Jump=j*100
        Resultfile = 'Results%05i.csv'%(Resultfile_Jump)
        File=file(Resultfile)
        Number_of_runs_in_file=file_lenght(Resultfile)/58
        
        for Number_of_run in range(Number_of_runs_in_file):
            Result_for_one_run=[]
            for rows in range(58):
                Result_for_one_run.append(File.readline()) 
            
            #print Result_for_one_run[14].split(';')   
            Statistik = load_Result_Table(Result_for_one_run)   
            EF        = Statistik[0]
            Bias      = Statistik[1]
            R_Squared = Statistik[2]
            Succeeded_Runs+=1
        
        
            for Plot in range(3):
                Good_run = True
                for element in range(len(EF[0])):
                    if EF[Plot][element] <= Min_EF:
                        Good_run = False
                        Failed_for_EF+=1
                    
                    if Bias[Plot][element] <= Min_Bias:
                        Good_run = False
                        Failed_for_Bias+=1
                    
                    if Bias[Plot][element] >= Max_Bias:
                        Good_run = False
                        Failed_for_Bias+=1
                        
                    if R_Squared[Plot][element] <= Min_R_Squared:
                        Good_run = False
                        Failed_for_R_Squared+=1
            
                if Good_run == True:
                    if Plot == 0:
                        Good_runs_Plot1+=1
                        Good_Setting_Files_Plot1.append([File.name,Number_of_run])
                    if Plot == 1:
                        Good_runs_Plot2+=1
                        Good_Setting_Files_Plot2.append([File.name,Number_of_run])
                    if Plot == 2:
                        Good_runs_Plot3+=1
                        Good_Setting_Files_Plot3.append([File.name,Number_of_run])
        File.close()
#     except: IOError
#        
    print 'Plot 1 has '+str(Good_runs_Plot1)+' good runs'
    print 'Plot 2 has '+str(Good_runs_Plot2)+' good runs'
    print 'Plot 3 has '+str(Good_runs_Plot3)+' good runs'    
    
    Procentual_Fail_EF = round(float(float(Failed_for_EF)/3/6/float(Succeeded_Runs)*100),2)    
    Procentual_Fail_Bias = round(float(float(Failed_for_Bias)/3/6/float(Succeeded_Runs)*100),2)
    Procentual_Fail_R_Squared = round(float(float(Failed_for_R_Squared)/3/6/float(Succeeded_Runs)*100),2)

    print str(Succeeded_Runs)+' of '+str(Runs)+' worked'    
    print str(Procentual_Fail_EF)+'% failed because of EF limit'    
    print str(Procentual_Fail_Bias)+'% failed because of Bias limit'
    print str(Procentual_Fail_R_Squared)+'% failed because of R_Squared limit'
    
    return Good_Setting_Files_Plot1, Good_Setting_Files_Plot2, Good_Setting_Files_Plot3
    
        
def load_Result_Table(Resultfile):
    #Resultfile = file('Results'+str(Number)+'Kersebaum_yield.csv')
    #Resultfile=file(Resultfile)
    #Resultfile.readline()
    #columns=[]    
    #for line in Resultfile:
        #columns.append(line.split(';'))
        #zeilen = line.split(';')
        #print zeilen

    EF       =np.zeros((3),dtype=[('Root_drymatter', 'f8'), ('StemLeaves_drymatter', 'f8'),('Storage_drymatter', 'f8')])              
    Bias     =np.zeros((3),dtype=[('Root_drymatter', 'f8'), ('StemLeaves_drymatter', 'f8'),('Storage_drymatter', 'f8')])              
    R_Squared=np.zeros((3),dtype=[('Root_drymatter', 'f8'), ('StemLeaves_drymatter', 'f8'),('Storage_drymatter', 'f8')])              
    
    for Plot in range(3):
        if Plot ==0:
            EF_Jump=14
        if Plot==1:
            EF_Jump=32
        if Plot==2:
            EF_Jump=50
        
#        EF['Root_drymatter'][Plot]               = Resultfile[EF_Jump].split(';')[1]
#        EF['StemLeaves_drymatter'][Plot]       = Resultfile[0][1]
#        EF['Storage_drymatter'][Plot]         = Resultfile[0][2]
#        
#        Bias_Jump=EF_Jump+1
#        Bias['Root_drymatter'][Plot]               = Resultfile[1][0]
#        Bias['StemLeaves_drymatter'][Plot]      = Resultfile[1][1]
#        Bias['Storage_drymatter'][Plot]         = Resultfile[1][2]
#    
#        R_Squared_Jump=EF_Jump+2
#        R_Squared['Root_drymatter'][Plot]               = Resultfile[2][0]
#        R_Squared['StemLeaves_drymatter'][Plot]      = Resultfile[2][1]
#        R_Squared['Storage_drymatter'][Plot]         = Resultfile[2][2]
#        
        EF['Root_drymatter'][Plot]               = Resultfile[EF_Jump].split(';')[1]
        EF['StemLeaves_drymatter'][Plot]       = Resultfile[EF_Jump].split(';')[4]
        EF['Storage_drymatter'][Plot]         = Resultfile[EF_Jump].split(';')[7]
        
        Bias_Jump=EF_Jump+1
        Bias['Root_drymatter'][Plot]               = Resultfile[Bias_Jump].split(';')[1]
        Bias['StemLeaves_drymatter'][Plot]      = Resultfile[Bias_Jump].split(';')[4]
        Bias['Storage_drymatter'][Plot]         = Resultfile[Bias_Jump].split(';')[7]
    
        R_Squared_Jump=EF_Jump+2
        R_Squared['Root_drymatter'][Plot]               = Resultfile[R_Squared_Jump].split(';')[1]
        R_Squared['StemLeaves_drymatter'][Plot]      = Resultfile[R_Squared_Jump].split(';')[4]
        R_Squared['Storage_drymatter'][Plot]         = Resultfile[R_Squared_Jump].split(';')[7]
    
   
    return EF,Bias,R_Squared


def load_Statistik_for_all_files(Runs,Statistik_Parameter,Analysed_Parameter, Plot):
    Plot=Plot-1
    Statistik_Parameter_Value=-99999    
    if Statistik_Parameter == 'EF':
        Statistik_Parameter_Value=0
    if Statistik_Parameter == 'Bias':
        Statistik_Parameter_Value=1
    if Statistik_Parameter == 'R_Squared':
        Statistik_Parameter_Value=2
    if Statistik_Parameter_Value==-99999:
        print 'Error: Please enter a correct Statisitk Parameter (EF,Bias,R_Squared)'
        pass
        
    Statistik_Parameter_List=[]
    for csv_Files in range(1000):
        j=csv_Files+1                
        Resultfile_Jump=j*100
        Resultfile = 'Results%05i.csv'%(Resultfile_Jump)
        File=file(Resultfile)
        Number_of_runs_in_file=file_lenght(Resultfile)/58
        
        EF=[]
        Bias=[]
        R_Squared=[]
        for Number_of_run in range(Number_of_runs_in_file):
            Result_for_one_run=[]
            for rows in range(58):
                Result_for_one_run.append(File.readline()) 
            Statistik = load_Result_Table(Result_for_one_run)
            Statistik_Parameter_List.append(Statistik[Statistik_Parameter_Value][Analysed_Parameter][Plot])
            #print Result_for_one_run[14].split(';')   
            
            #Statistik = load_Result_Table(Result_for_one_run)   
            #EF.append(Statistik[0])
            #Bias.append(Statistik[1])
            #R_Squared.append(Statistik[2])
        #print EF
#    for Number in range(Runs):
#        try:
#            Statistik = load_Result_Table('Results'+str(Number)+'Kersebaum_yield_test.csv')
#            Statistik_Parameter_List.append(Statistik[Statistik_Parameter_Value][Analysed_Parameter][Plot])
#        except: IOError        
    return Statistik_Parameter_List

def load_Good_run_new(Good_run_file,Position):
    File=file(Good_run_file)
    File_for_one_run=[]
    for Jump in range(Position):        
        for rows in range(58):
            File.readline()
    for rows in range(58):
        File_for_one_run.append(File.readline())
    
    columns=[]    
    for line in File_for_one_run:
        columns.append(line.split(';'))
    Results = np.zeros((3),dtype=[('Root_drymatter', 'f8',(2,4)), ('StemLeaves_drymatter', 'f8',(2,6)),('Storage_drymatter', 'f8',(2,3)),('Date', 'int16',(6,3))])
    for Plot in range(3):
        for Calc_Meas in range(2):
            for Steps in range(6):
                if Plot==0:
                    Jump =7+Steps+0
                if Plot==1:
                    Jump =7+Steps+18
                if Plot==2:
                    Jump =7+Steps+36
                Results['StemLeaves_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+4]                
                if Steps <4:
                    #Results['Root_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]
                    Results['Root_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]                               
                #if Steps <5: 
                #    Results['StemLeaves_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+7]                
                if Steps >=3:
                    Short_Step=Steps-3
                    Results['Storage_drymatter'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+7] 
                    #if Steps <5:
                        #Results['Storage_C'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+13]
                for Date in range(3):
                    Results['Date'][Plot][Steps][Date] = columns[7+Steps][10+Date]         
    file.close(File)
    return Results
    
def load_Good_run_new2(Good_run_file,Position):
    File=file(Good_run_file)
    File_for_one_run=[]
    for Jump in range(Position):        
        for rows in range(58):
            File.readline()
    for rows in range(58):
        File_for_one_run.append(File.readline())
    
    columns=[]    
    for line in File_for_one_run:
        columns.append(line.split(';'))
    Results = np.zeros((3),dtype=[('Root_drymatter', 'f8',(2,4)), ('StemLeaves_drymatter', 'f8',(2,5)),('Storage_drymatter', 'f8',(2,2)),('Date', 'int16',(6,3))])
    for Plot in range(3):
        for Calc_Meas in range(2):
            for Steps in range(6):
                if Plot==0:
                    Jump =7+Steps+0
                if Plot==1:
                    Jump =7+Steps+18
                if Plot==2:
                    Jump =7+Steps+36
                if Steps<5:
                    Results['StemLeaves_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+4]                
                if Steps <4:
                    #Results['Root_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]
                    Results['Root_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]                               
                #if Steps <5: 
                #    Results['StemLeaves_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+7]                
                if Steps >=3:
                    if Steps<5:
                        Short_Step=Steps-3
                        Results['Storage_drymatter'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+7] 
                    #if Steps <5:
                        #Results['Storage_C'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+13]
                for Date in range(3):
                    Results['Date'][Plot][Steps][Date] = columns[7+Steps][10+Date]         
    file.close(File)
    return Results
    
def load_Good_run(Good_run_file):
    Good_run_file=file(Good_run_file)        
    Good_run_file.readline()
    columns=[]    
    for line in Good_run_file:
        columns.append(line.split(';'))
        
    Results = np.zeros((3),dtype=[('Root_drymatter', 'f8',(2,4)), ('StemLeaves_drymatter', 'f8',(2,6)),('Storage_drymatter', 'f8',(2,3)),('Date', 'int16',(6,3))])
    for Plot in range(3):
        for Calc_Meas in range(2):
            for Steps in range(6): 
                Jump =6+Steps+Plot*13
                Results['StemLeaves_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+4]                
                if Steps <4:
                    #Results['Root_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]
                    Results['Root_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]                               
                #if Steps <5: 
                #    Results['StemLeaves_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+7]                
                if Steps >=3:
                    Short_Step=Steps-3
                    Results['Storage_drymatter'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+7] 
                    #if Steps <5:
                        #Results['Storage_C'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+13]
                for Date in range(3):
                    Results['Date'][Plot][Steps][Date] = columns[Jump][10+Date]         
    file.close(Good_run_file)
    return Results


def load_Datetimes(Results, Result_Parameter):
    if Result_Parameter == 'Root_C':
        lenght = 4 
        Step   = 0
    if Result_Parameter == 'Root_drymatter':
        lenght = 4 
        Step   = 0
    if Result_Parameter == 'StemLeaves_C':
        lenght = 5 
        Step   = 0
    if Result_Parameter == 'StemLeaves_drymatter':
        lenght = 6 
        Step   = 0
    if Result_Parameter == 'Storage_drymatter':
        lenght = 3 
        Step   = 3
    if Result_Parameter == 'Storage_C':    
        lenght = 2 
        Step   = 3
        
    Result_Dates = Results['Date'][0]   
    Datum=[]
    for i in range(lenght):
        Datum.append(datetime(Result_Dates[i+Step][0],Result_Dates[i+Step][1],Result_Dates[i+Step][2]))   
    return Datum

def load_Datetimes_new(Results, Result_Parameter):

    if Result_Parameter == 'Root_drymatter':
        lenght = 4 
        Step   = 0
    if Result_Parameter == 'StemLeaves_drymatter':
        lenght = 5 
        Step   = 0
    if Result_Parameter == 'Storage_drymatter':
        lenght = 2 
        Step   = 3

        
    Result_Dates = Results['Date'][0]   
    Datum=[]
    for i in range(lenght):
        Datum.append(datetime(Result_Dates[i+Step][0],Result_Dates[i+Step][1],Result_Dates[i+Step][2]))   
    return Datum
    

def Plot_Good_Run(Results, Datum, Result_Parameter, Resultfile, Plot):    
#    if Statistik_Parameter == 'EF':
#        Statistik_Parameter_value=0
#    if Statistik_Parameter == 'Bias':
#        Statistik_Parameter_value=1
#    if Statistik_Parameter == 'R_Squared':
#        Statistik_Parameter_value=2
    
    
    'Root_C','Root_drymatter','StemLeaves_C','StemLeaves_drymatter',
    'Storage_C','Storage_drymatter'
    Values =[]
    for Plot in range(3):       
        Values.append(Results[Result_Parameter][Plot])
    Biggest_value = np.max(np.max(np.max(Values)))    
    
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)

    plt.title('Test_'+str(Result_Parameter))   
    
    for Plot in range(3):  
        Plot+=1
        if Plot ==1:
            #ax1.set_ylim(0,35,1)
            #Biggest_value = math.ceil(np.max(Values))
            #print Biggest_value*1.1
            ax1.set_xlim(datetime(1992,1,1),datetime(1999,1,1))
            ax1.set_ylim(0,Biggest_value*1.1)
            #ax1.plot(Datum,Calc.Water0_30cm,'b--')
            ax1.plot(Datum,Results[Result_Parameter][Plot-1][0],'bo', ms=4,label='PMF')
            #ax1.plot(Datum,Meas.Water0_30cm,'g--')
            ax1.plot(Datum,Results[Result_Parameter][Plot-1][1],'gs', ms=4,label='Kersebaum') 
            #leg = ax1.legend(bbox_to_anchor=(1.05, -0.15), loc='best', fancybox=True)
            #leg.get_frame().set_alpha(0.5)
            #print Datum
            #textstr = 'r**2 = %.4f\nBias = %.1f\nEF = %.4f'%(R_Squared, Bias, EF)
            #props = dict(boxstyle='round',facecolor='white', alpha=0.5)
            #ax1.text(0.02, 0.85, textstr, transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)                       
            #ax1.set_title('Plot '+str(Plot)+' with 'r'$r$'+'='+str(round(cc,4))+', ' r'$Bias$'+'='+str(round(Bias,2))+' and 'r'$EF$'+'='+str(round(Nash_Sutcliff,2)))
            ax1.set_title(Result_Parameter+'Plot '+r'$1$')           
            ax1.grid()    
            ax1.set_xlabel('Date '+r'$[Years]$')
            ax1.set_ylabel(Result_Parameter, fontsize=9)
            ax1.fill_between(Datum,Results[Result_Parameter][Plot-1][0],Results[Result_Parameter][Plot-1][1],facecolor='red', alpha=0.5)    
    
        if Plot ==2:
            #ax2.set_ylim(0,35,1)
            #print math.ceil(np.max(Values))
            ax2.set_xlim(datetime(1992,1,1),datetime(1999,1,1))
            ax2.set_ylim(0,Biggest_value*1.1)
            #ax2.plot(Datum,Calc.W'Root_C','Root_drymatter','StemLeaves_C','StemLeaves_drymatter' 'Storage_C','Storage_drymatter'ater0_30cm,'b--')
            ax2.plot(Datum,Results[Result_Parameter][Plot-1][0],'bo', ms=4,label='PMF')
            #ax2.plot(Datum,Meas.Water0_30cm,'g--')
            ax2.plot(Datum,Results[Result_Parameter][Plot-1][1],'gs', ms=4,label='Kersebaum')
            #textstr = 'r = %.4f\nBias = %.1f\nEF = %.4f'%(r, Bias, EF)
            #props = dict(boxstyle='round',facecolor='white', alpha=0.5)
            #ax2.text(0.02, 0.85, textstr, transform=ax2.transAxes, fontsize=14, verticalalignment='top', bbox=props)  
            #ax2.legend(loc=2, bbox_to_anchor = (0.77, 0.4),scatterpoints=0)
            #ax2.set_title('Plot '+str(Plot)+' with 'r'$r$'+'='+str(round(cc,4))+', ' r'$Bias$'+'='+str(round(Bias,2))+' and 'r'$EF$'+'='+str(round(Nash_Sutcliff,2)))
            ax2.set_title(Result_Parameter+'Plot '+r'$2$')             
            ax2.grid()    
            ax2.set_xlabel('Date '+r'$[Years]$')
            ax2.set_ylabel(Result_Parameter, fontsize=9)
            ax2.fill_between(Datum,Results[Result_Parameter][Plot-1][0],Results[Result_Parameter][Plot-1][1],facecolor='red', alpha=0.5)   
        if Plot ==3:
            #ax3.set_ylim(0,35,1)
            ax3.set_xlim(datetime(1992,1,1),datetime(1999,1,1))
            ax3.set_ylim(0,Biggest_value*1.1)
            #ax3.plot(Datum,Calc.Water0_30cm,'b--')
            ax3.plot(Datum,Results[Result_Parameter][Plot-1][0],'bo', ms=4,label='PMF')
            #ax3.plot(Datum,Meas.Water0_30cm,'g--')
            ax3.plot(Datum,Results[Result_Parameter][Plot-1][1],'gs', ms=4,label='Kersebaum')
            #textstr = 'r = %.4f\nBias = %.1f\nEF = %.4f'%(r, Bias, EF)
            #props = dict(boxstyle='round',facecolor='white', alpha=0.5)
            #ax3.text(0.02, 0.85, textstr, transform=ax3.transAxes, fontsize=14, verticalalignment='top', bbox=props)  
            #ax3.legend(loc=2, bbox_to_anchor = (0.77, 0.4),scatterpoints=0)
            ax3.set_title(Result_Parameter+'Plot '+r'$3$')             
            #ax3.set_title('Plot '+str(Plot)+' with 'r'$r$'+'='+str(round(cc,4))+', ' r'$Bias$'+'='+str(round(Bias,2))+' and 'r'$EF$'+'='+str(round(Nash_Sutcliff,2)))
            ax3.grid()    
            ax3.set_xlabel('Date '+r'$[Years]$')
            ax3.set_ylabel(Result_Parameter, fontsize=9)
            ax3.fill_between(Datum,Results[Result_Parameter][Plot-1][0],Results[Result_Parameter][Plot-1][1],facecolor='red', alpha=0.5)   
                    
            #legend(bbox_to_anchor=(0., 3.40, 1., 2.102), loc=0,
            #       ncol=2, mode="expand", borderaxespad=0.)
    plt.tight_layout()
    plt.draw()
    plt.show()
            #plt.savefig('Default_values_Van_Genuchten'+Parameter+' for all plots and RUE = '+str(RUE), dpi=400)    
            #plt.close()  

def Plot_all_results_for_Good_run(Resultfile,Plot,Name_of_Resultfile,Position_of_Resultfile):
    Default_PMF_Results=load_Good_run('Default_Results_Kersebaum_yield.csv')
    Results = load_Good_run_new(Name_of_Resultfile,Position_of_Resultfile)    
    #Results = Resultfile
#    EF_List           = Results[0][Plot-1]
#    Bias_List         = Results[1][Plot-1]
#    R_Squared_List    = Results[2][Plot-1]
#    print Resultfile
    File=file(Name_of_Resultfile)
    File_for_one_run=[]
    for Jump in range(Position_of_Resultfile):        
        for rows in range(58):
            File.readline()
    for rows in range(58):
        File_for_one_run.append(File.readline())
    EF_List        =load_Result_Table(File_for_one_run)[0][Plot-1]
    Bias_List      =load_Result_Table(File_for_one_run)[1][Plot-1]      
    R_Squared_List =load_Result_Table(File_for_one_run)[2][Plot-1]
    Setting_String = load_Settings_for_one_file(Name_of_Resultfile,Position_of_Resultfile)    
    Result_Parameter_List=['Root_drymatter','StemLeaves_drymatter','Storage_drymatter']
    ax_Number=0
    
    for row in range(3):
        for columen in range(1):
            ax_Number+=1
            ax1 = plt.subplot(3,1,ax_Number)#Root_C
            #ax2 = plt.subplot(612)#Root_drymatter
            #ax3 = plt.subplot(613)#Stem_Leaves_C
            #ax4 = plt.subplot(621)#Stem_Leaves_drymatter
            #ax5 = plt.subplot(622)#Storage_C
            #ax6 = plt.subplot(623)#Storage_drymatter

            Biggest_value1 = np.max(Results[Result_Parameter_List[ax_Number-1]][Plot-1])
            Biggest_value2 =np.max(Default_PMF_Results[Result_Parameter_List[ax_Number-1]][Plot-1])         
            Biggest_value= np.max([Biggest_value1, Biggest_value2])
            Datum   = load_Datetimes(Results, Result_Parameter_List[ax_Number-1])
            ax1.set_xlim(datetime(1994,3,1),datetime(1999,10,1))
            ax1.set_ylim(0,Biggest_value*1.1)
            ax1.plot(Datum,Results[Result_Parameter_List[ax_Number-1]][Plot-1][0],'bo', ms=4,label='PMF')
            ax1.plot(Datum,Results[Result_Parameter_List[ax_Number-1]][Plot-1][1],'gs', ms=4,label='Kersebaum')
            ax1.plot(Datum,Default_PMF_Results[Result_Parameter_List[ax_Number-1]][Plot-1][0],'k.', ms=8,label='Default_PMF')
            if ax_Number==1:            
                leg = ax1.legend(bbox_to_anchor=(1.05, -2.1), loc='best', fancybox=True)
                leg.get_frame().set_alpha(0.5)
                props = dict(boxstyle='round',facecolor='white', alpha=0.5)
                ax1.text(0.2,-0.45,Setting_String, transform=ax1.transAxes, fontsize=10, verticalalignment='top', bbox=props)
            textstr = 'EF = %.4f\nBias = %.1f\nR = %.4f'%(EF_List[ax_Number-1], Bias_List[ax_Number-1], R_Squared_List[ax_Number-1])
            props = dict(boxstyle='round',facecolor='white', alpha=0.5)
            ax1.text(0.83, 0.925, textstr, transform=ax1.transAxes, fontsize=10, verticalalignment='top', bbox=props)
                                  
            ax1.set_title('Plot '+str(Plot)+' with 'r'$r$'+'='+str(round(R_Squared_List[ax_Number-1],4))+', ' r'$Bias$'+'='+str(round(Bias_List[ax_Number-1],2))+' and 'r'$EF$'+'='+str(round(EF_List[ax_Number-1],2)))
            ax1.set_title(str(Result_Parameter_List[ax_Number-1])+'_Plot '+str(Plot))           
            ax1.grid()    
            ax1.set_xlabel('Date '+r'$[Years]$')
            ax1.set_ylabel(str(Result_Parameter_List[ax_Number-1]), fontsize=9)
            ax1.fill_between(Datum,Default_PMF_Results[Result_Parameter_List[ax_Number-1]][Plot-1][0],Results[Result_Parameter_List[ax_Number-1]][Plot-1][1],facecolor='green',alpha=0.4)            
            ax1.fill_between(Datum,Results[Result_Parameter_List[ax_Number-1]][Plot-1][0],Results[Result_Parameter_List[ax_Number-1]][Plot-1][1],facecolor='red')#, alpha=0.5)    
            
        
    plt.tight_layout(pad=0.4, w_pad=0.55, h_pad=2.0)
    plt.draw()
    plt.show()
    plt.savefig('Picture_'+Name_of_Resultfile+'_on_Plot'+str(Plot)+'.png', dpi=500)



def Plot_Statistik(Runs,Statistik_Parameter, Analysed_Setting):

    Analysed_Parameter_List=['Root_drymatter','StemLeaves_drymatter','Storage_drymatter']
    
    
    ax_Number=0#Start of Plot
    Setting_List  = load_Settings_for_all_files(Runs, Analysed_Setting)
    for Analysed_Parameter in range(len(Analysed_Parameter_List)):#3
        for plots in range(3):
            Statistik = load_Statistik_for_all_files(Runs,Statistik_Parameter,Analysed_Parameter_List[Analysed_Parameter], plots+1)      
            ax_Number+=1
            ax1 = plt.subplot(3,3,ax_Number)
            if Statistik_Parameter == 'Bias':
                ax1.set_ylim(-100,100)
            else:
                ax1.set_ylim(0,1)
            if Analysed_Setting=='tbase':
                ax1.set_xlim(-1,5)
            if Analysed_Setting=='Emergence':
                ax1.set_xlim(30,190)
            if Analysed_Setting=='LeafDevelopment':
                ax1.set_xlim(190,250)
            if Analysed_Setting=='Tillering':
                ax1.set_xlim(350,470)
            if Analysed_Setting=='StemElongation':
                ax1.set_xlim(550,725)
            if Analysed_Setting=='Anthesis':
                ax1.set_xlim(800,1000)
            if Analysed_Setting=='SeedFill':
                ax1.set_xlim(1050,1300)
            if Analysed_Setting=='DoughStage':
                ax1.set_xlim(1400,1670)
            if Analysed_Setting=='Maturity':
                ax1.set_xlim(1500,1832)
            if Analysed_Setting=='RUE':
                ax1.set_xlim(1,8)
            if Analysed_Setting=='k':
                ax1.set_xlim(0.2,0.8)
            if Analysed_Setting=='kcb1':
                ax1.set_xlim(0.05,0.4)
            if Analysed_Setting=='kcb2':
                ax1.set_xlim(0.5,1.5)
            if Analysed_Setting=='kcb3':
                ax1.set_xlim(0.075,0.225)
            if Analysed_Setting=='root_growth':
                ax1.set_xlim(0.5,4)
           
            for label in ax1.xaxis.get_ticklabels():
                label.set_fontsize(7)
            for label in ax1.yaxis.get_ticklabels():
                label.set_fontsize(7)
                
            #print Setting_List
            ax1.plot(Setting_List,Statistik,'bo',ms=1)
            ax1.set_title(Statistik_Parameter+' for '+Analysed_Parameter_List[Analysed_Parameter]+'\n on Plot'+str(plots+1), fontsize=9)
            ax1.set_xlabel(Analysed_Setting, fontsize=7)
            ax1.set_ylabel(str(Statistik_Parameter), fontsize=7)
    
    plt.tight_layout(pad=0.4, w_pad=0.55, h_pad=2.0)
    plt.draw()
    plt.show()    
    #plt.savefig(Statistik_Parameter+'_Plot_'+str(Analysed_Setting)+'.png', dpi=800)
    plt.close()


def Plot_Statistik_new(Runs,Statistik_Parameter, Analysed_Setting):

    Analysed_Parameter_List=['Root_drymatter','StemLeaves_drymatter','Storage_drymatter']
    
    
    ax_Number=0#Start of Plot
    Setting_List  = load_Settings_for_all_files(Runs, Analysed_Setting)
    for Analysed_Parameter in range(len(Analysed_Parameter_List)):#3
        for plots in range(3):
 
            Statistik = load_Statistik_for_all_files(Runs,Statistik_Parameter,Analysed_Parameter_List[Analysed_Parameter], plots+1)      
         
            ax1 = plt.subplot(3,3,ax_Number)
            if Statistik_Parameter == 'Bias':
                ax1.set_ylim(-100,100)
            else:
                ax1.set_ylim(0,1)
            if Analysed_Setting=='tbase':
                ax1.set_xlim(-1,5)
            if Analysed_Setting=='Emergence':
                ax1.set_xlim(30,190)
            if Analysed_Setting=='LeafDevelopment':
                ax1.set_xlim(190,250)
            if Analysed_Setting=='Tillering':
                ax1.set_xlim(350,470)
            if Analysed_Setting=='StemElongation':
                ax1.set_xlim(550,725)
            if Analysed_Setting=='Anthesis':
                ax1.set_xlim(800,1000)
            if Analysed_Setting=='SeedFill':
                ax1.set_xlim(1050,1300)
            if Analysed_Setting=='DoughStage':
                ax1.set_xlim(1400,1670)
            if Analysed_Setting=='Maturity':
                ax1.set_xlim(1500,1832)
            if Analysed_Setting=='RUE':
                ax1.set_xlim(1,8)
            if Analysed_Setting=='k':
                ax1.set_xlim(0.2,0.8)
            if Analysed_Setting=='kcb1':
                ax1.set_xlim(0.05,0.4)
            if Analysed_Setting=='kcb2':
                ax1.set_xlim(0.5,1.5)
            if Analysed_Setting=='kcb3':
                ax1.set_xlim(0.075,0.225)
            if Analysed_Setting=='root_growth':
                ax1.set_xlim(0.5,4)
           
            for label in ax1.xaxis.get_ticklabels():
                label.set_fontsize(7)
            for label in ax1.yaxis.get_ticklabels():
                label.set_fontsize(7)
                
            #print Setting_List
            ax1.plot(Setting_List,Statistik,'bo',ms=1)
            divider = make_axes_locatable(ax1)
            axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=ax1)
            plt.setp(axHistx.get_xticklabels(),
                     visible=False)
            binwidth = 0.25
            xymax = np.max(Statistik)
            lim = ( int(xymax/binwidth) + 1) * binwidth
            
            bins = np.arange(-lim, lim + binwidth, binwidth)
            axHistx.hist(Setting_List, bins=bins)
            ax1.set_title(Statistik_Parameter+' for '+Analysed_Parameter_List[Analysed_Parameter]+'\n on Plot'+str(plots+1), fontsize=9)
            ax1.set_xlabel(Analysed_Setting, fontsize=7)
            ax1.set_ylabel(str(Statistik_Parameter), fontsize=7)
    
    plt.tight_layout(pad=0.4, w_pad=0.55, h_pad=2.0)
    plt.draw()
    plt.show()    
    #plt.savefig(Statistik_Parameter+'_Plot_'+str(Analysed_Setting)+'.png', dpi=800)
    #plt.close()

    
def load_Improvement(Statistik_values):
    GraphX=[]
    GraphY=[]
    
    GraphX.append(0)
    GraphY.append(Statistik_values[0])

    j=0

    for i in range(len(Statistik_values)):
        k=i+1

        if k==len(Statistik_values):
            pass  
        else:
            if Statistik_values[k] >= GraphY[j]:
                GraphX.append(k)
                GraphY.append(Statistik_values[k])
                j+=1

    plot(GraphX,GraphY)

    return None
    
def load_Good_File(Resultfile,Position):
    '''
    Gives Back EF, Bias and R_Squared for all Plots
    '''
    File=file(Resultfile)
    File_for_one_run=[]
    for Jump in range(Position):        
        for rows in range(58):
            File.readline()
    for rows in range(58):
        File_for_one_run.append(File.readline())
    
    Result = load_Result_Table(File_for_one_run)
    
    return Result

if __name__=='__main__':
    '''
    Ef,Bias,R_Squared
    
    1-3

    'Root_C','Root_drymatter','StemLeaves_C','StemLeaves_drymatter',
    'Storage_C','Storage_drymatter'
      
    
    'tbase','Emergence','LeafDevelopment','Tillering','TemElongation','Anthesis',
    'SeedFill','DoughStage','Maturity','RUE','k','kcb1','kcb2','kcb3',
    'leaf_specific_weight','root_growth','max_height','carbonfraction','max_depth'
    
    Results[Name][Plot][Calc/Meas][Single_Value]  
    Statistik[EF,Bias,R_Squared][Runs]['Name'][Plot]    
    '''
    
    #Dynamic change of working directory to data folder for uncertainty analysis
    working_directory = os.getcwd()
    #os.chdir(working_directory+'\\Results_PMF_Calibration')
    os.chdir(working_directory+'\\result100000')
    
    
    
    Min_EF        = 0.3
    Min_Bias      = -600
    Max_Bias      =  600
    Min_R_Squared =  0.8
    
    Runs          = 100
       
    

    
    Statistik_Parameter   = 'EF'    
    Plot                  = 1  
    Analysed_Parameter    = 'StemLeaves_drymatter'    
    #Analysed_Setting      = 'kcb2'
    #Resultfile            = 'Results23534Kersebaum_yield.csv' # for Plot1 ('Results33722Kersebaum_yield.csv')
    #Resultfile            = 'Results29748Kersebaum_yield_test.csv'#'Results15468Kersebaum_yield.csv' # for Plot2
    #Resultfile            = 'Results25422Kersebaum_yield_test.csv'  # for Plot3 ('Results2414Kersebaum_yield.csv', 'Results7453Kersebaum_yield.csv', 'Results15169Kersebaum_yield.csv', 'Results16915Kersebaum_yield.csv', 'Results23534Kersebaum_yield.csv', 'Results36324Kersebaum_yield.csv', 'Results36399Kersebaum_yield.csv', 'Results37785Kersebaum_yield.csv')
    
    '''
    Searches through runs to find a fitting set
    '''   
    #Good_Setting_Files = Overview(Runs,Min_EF,Min_Bias,Max_Bias,Min_R_Squared)
    #print Good_Setting_Files
    Name_of_Resultfile='Results80500.csv'
    Position_of_Resultfile=82
    Resultfile = load_Good_File(Name_of_Resultfile, Position_of_Resultfile)
    
    #print Resultfile
    #print load_Result_Table(Resultfile)
    '''
    Plots Statitik for one Analysed Setting over all runs
    '''
    #['tbase','Emergence','LeafDevelopment','Tillering','StemElongation','Anthesis',
    #'SeedFill','DoughStage','Maturity','RUE','k','kcb1','kcb2','kcb3',
    Parameter_List=[
    'root_growth']
    #for i in range(len(Parameter_List)):    
        #Analysed_Setting=Parameter_List[i]
        #Plot_Statistik_new(Runs,Statistik_Parameter, Analysed_Setting)        
        #Plot_Statistik(Runs,Statistik_Parameter, Analysed_Setting)

    '''
    Plots Results for one good run on one Plot
    '''    
    #
    #Plot_all_results_for_Good_run(Resultfile,Plot,Name_of_Resultfile,Position_of_Resultfile)
    
    
    '''
    Load all day simulated data for good run
    '''
    # for Result80500.csv, 82
    
    File = file('Results_Analyse_Manager_simulated.csv')
    for i in range(7):    
        File.readline()
    Result_Root_drymatter_Plot_1_sim=[]
    Result_Stem_and_Leave_drymatter_Plot_1_sim=[]
    Result_Storage_drymatter_Plot_1_sim=[]
    for i in range(2563-7):     
        Result = File.readline()
        Result_Root_drymatter_Plot_1_sim.append(Result.split(';')[1])
        Result_Stem_and_Leave_drymatter_Plot_1_sim.append(Result.split(';')[2])
        Result_Storage_drymatter_Plot_1_sim.append(Result.split(';')[3])
    File.close()
    
    DataStart_of_Sim=datetime(1992,1,1)
    DataStart_of_interest=datetime(1994,2,1)
    DataEnd_of_interest=datetime(1994,8,1)

    Days_of_interest=(DataEnd_of_interest-DataStart_of_interest).days
    Skip_days_for_sim_data=(DataStart_of_interest-DataStart_of_Sim).days
    
    Result_Root_drymatter_Plot_1_sim_of_interest=Result_Root_drymatter_Plot_1_sim[Skip_days_for_sim_data:Skip_days_for_sim_data+Days_of_interest]
    Result_Stem_and_Leave_drymatter_Plot_1_sim_of_interest=Result_Stem_and_Leave_drymatter_Plot_1_sim[Skip_days_for_sim_data:Skip_days_for_sim_data+Days_of_interest]
    Result_Storage_drymatter_Plot_1_sim_of_interest=Result_Storage_drymatter_Plot_1_sim[Skip_days_for_sim_data:Skip_days_for_sim_data+Days_of_interest]
    
    
    Datelist=[]
    for i in range((DataEnd_of_interest-DataStart_of_interest).days):
        Datelist.append(DataStart_of_interest+timedelta(days=i))
        
    
    File = file('Results_Analyse_Manager_default.csv')
    for i in range(7):    
        File.readline()
    Result_Root_drymatter_Plot_1_default=[]
    Result_Stem_and_Leave_drymatter_Plot_1_default=[]
    Result_Storage_drymatter_Plot_1_default=[]
    for i in range(2563-7):     
        Result = File.readline()
        Result_Root_drymatter_Plot_1_default.append(Result.split(';')[1])
        Result_Stem_and_Leave_drymatter_Plot_1_default.append(Result.split(';')[2])
        Result_Storage_drymatter_Plot_1_default.append(Result.split(';')[3])
    File.close()
    
    DataStart_of_default=datetime(1992,1,1)
    DataStart_of_interest=datetime(1994,2,1)
    DataEnd_of_interest=datetime(1994,8,1)

    Days_of_interest=(DataEnd_of_interest-DataStart_of_interest).days
    Skip_days_for_default_data=(DataStart_of_interest-DataStart_of_default).days
    
    Result_Root_drymatter_Plot_1_default_of_interest=Result_Root_drymatter_Plot_1_default[Skip_days_for_default_data:Skip_days_for_default_data+Days_of_interest]
    Result_Stem_and_Leave_drymatter_Plot_1_default_of_interest=Result_Stem_and_Leave_drymatter_Plot_1_default[Skip_days_for_default_data:Skip_days_for_default_data+Days_of_interest]
    Result_Storage_drymatter_Plot_1_default_of_interest=Result_Storage_drymatter_Plot_1_default[Skip_days_for_default_data:Skip_days_for_default_data+Days_of_interest]
    
    
    Datelist=[]
    for i in range((DataEnd_of_interest-DataStart_of_interest).days):
        Datelist.append(DataStart_of_interest+timedelta(days=i))    
    
    '''
    Make a nice big boxplot overview graph
    '''
    #Make_boxplot_Plot():
    Runs=100000
    Min_EF=-1000
    Min_Bias=-1000
    Max_Bias=1000
    Min_R_Squared=0.8
    Good_Setting_Files = Overview(Runs,Min_EF,Min_Bias,Max_Bias,Min_R_Squared)
    File_List_Plot1=Good_Setting_Files[0]    
    File_List_Plot2=Good_Setting_Files[1]
    File_list_Plot3=Good_Setting_Files[2]
    
    Plot1=0
    Root_drymatter=0
        
    Calculated=0
    Measured=1
    Date=0
    
    
    Results = load_Good_run_new2(Name_of_Resultfile,Position_of_Resultfile)
    Result_Parameter_List=['Root_drymatter','StemLeaves_drymatter','Storage_drymatter']
    #Datum   = load_Datetimes(Results, Result_Parameter_List[Root_drymatter])

    Simulated_List=[]    

    Simulated_List.append(Result_Root_drymatter_Plot_1_sim_of_interest)
    Simulated_List.append(Result_Stem_and_Leave_drymatter_Plot_1_sim_of_interest)
    Simulated_List.append(Result_Storage_drymatter_Plot_1_sim_of_interest)
    
    Default_List=[]
    Default_List.append(Result_Root_drymatter_Plot_1_default_of_interest)
    Default_List.append(Result_Stem_and_Leave_drymatter_Plot_1_default_of_interest)
    Default_List.append(Result_Storage_drymatter_Plot_1_default_of_interest)
        
    
    for Result_Parameter in range(len(Result_Parameter_List)):
        Datum   = load_Datetimes_new(Results, Result_Parameter_List[Result_Parameter])
        for i in range(len(File_List_Plot1)):
            if Result_Parameter==0:        
                Lenght = 4
                Calculated_on_days=[[],[],[],[]]
            if Result_Parameter==1:
                Lenght = 5
                Calculated_on_days=[[],[],[],[],[]]
            if Result_Parameter==2:
                Lenght = 2
                Calculated_on_days=[[],[]]
            for Dates in range(Lenght):
                #Calculated_on_days[Tage].append(load_Good_run_new(Dateiname,Position)[Plot1][Result_Parameter][Calculated][Dates]) 

                Calculated_on_days[Dates].append(load_Good_run_new2(File_List_Plot1[i][0],File_List_Plot1[i][1])[Plot1][Result_Parameter][Calculated][Dates]) 
        
        fig = plt.figure(figsize=(12,6))
        fig.canvas.set_window_title('Boxplots of uncertainty in Monte Carlo runs for '+str(Result_Parameter_List[Result_Parameter])+' [kg/ha]')
        ax1 = fig.add_subplot(111)
        plt.subplots_adjust(left=0.095, right=0.95, top=0.9, bottom=0.25)
        #boxplot(Calculated_on_days)
        
        #plt.plot(Datum, Results[Result_Parameter_List[Result_Parameter]][Plot][1],
        #       'bo', markeredgecolor='k',ms=5, label='Measured Data')
        #plt.plot(Datelist,Simulated_List[Result_Parameter], label='Simulated')
        #plt.plot(Datelist,Default_List[Result_Parameter],'k--', label='Default PMF')
        bp = plt.boxplot(Calculated_on_days, notch=0, sym='+', vert=1, whis=1.5,widths=5,positions=date2num(Datum))
        xlabels = []
        for dt in Datum:
            xlabels.append(dt.strftime('%d-%m-%Y'))
        ax1.set_title('Comparison of Simulation Uncertainty Across Measuring Points')
        ax1.set_xlabel('Datetime')
        ax1.set_ylabel(str(Result_Parameter_List[Result_Parameter])+' [kg/ha]')
        ax1.set_xlim(DataStart_of_interest,DataEnd_of_interest)
        if Result_Parameter==0:        
            top = 3000
        if Result_Parameter==1:
            top = 9000
        if Result_Parameter==2:
            top = 15000
        bottom = -5
        ax1.set_ylim(bottom, top)
        ax1.legend(loc='upper left', fancybox=True)
        #plt.setp(xtickNames, rotation=45, fontsize=8)
        ax1.xaxis.set_ticklabels(xlabels)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='blue')
        plt.setp(bp['fliers'], color='red', marker='+')
        ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
        # Hide these grid behind plot objects
        ax1.set_axisbelow(True)
        
        plt.savefig('Boxplots of uncertainty in Monte Carlo runs on Plot 1 with '+str(Name_of_Resultfile)+' on Position'+str(Position_of_Resultfile)+' with '+str(Result_Parameter_List[Result_Parameter])+'.png', dpi=900)
        plt.close()
        
    
    
    
    
    
    #Analysed_Parameter_List=['Root_drymatter','StemLeaves_drymatter','Storage_drymatter']
  
#    for i in range(len(Analysed_Parameter_List)):
#        Statistik_values = load_Statistik_for_all_files(Runs,Statistik_Parameter,Analysed_Parameter_List[i], Plot)
#    
#    load_Improvement(Statistik_values)
    
#    Stat = load_Result_Table('Results2414Kersebaum_yield.csv')
#    
#    EF=0
#    Bias=1
#    R_Squared=2
#    Plot=0
#    
#    Stat_mean_values=[]
#    
#    for Number in range(Runs):
#        try:
#            Stat = load_Result_Table('Results'+str(Number)+'Kersebaum_yield.csv')
#            for i in range(len(Analysed_Parameter_List)):
#                Stat_mean_values.append(Stat[EF][Analysed_Parameter_List[i]][Plot])
#        except: IOError
#        
#    Stat_min=[]
#    for i in range(len(Stat_mean_values)):
#        if i%6==0:
#            Stat_min.append(np.min(Stat_mean_values[i:i+6]))
#    
#    load_Improvement(Stat_min)
    
    
    
    
    
    
    
   
 








   
#    Statistik_Parameter_List=['EF','Bias','R_Squared']
#    for Plot_Number in range(3):#3
#        for Statistik_Parameter in range(len(Statistik_Parameter_List)):#3
#            for Analysed_Setting in range(len(Analysed_Setting_List)):#19
#                ax_Number=0#Start of Plot
#                for Analysed_Parameter in range(len(Analysed_Parameter_List)):#6
#                    Statistik = load_Statistik_for_all_files(Runs,Statistik_Parameter_List[Statistik_Parameter],Analysed_Parameter_List[Analysed_Parameter], Plot_Number+1)
#                    Setting_List  = load_Settings_for_all_files(Runs, Analysed_Setting_List[Analysed_Setting])
#                    ax_Number+=1
#                    ax1 = plt.subplot(3,2,ax_Number)
#                    if Statistik_Parameter==0:  #EF                  
#                        ax1.set_ylim(0,1)
#                    if Statistik_Parameter==1:  #Bias                  
#                        ax1.set_ylim(-100,100)
#                    if Statistik_Parameter==2:  #R_Squared                  
#                        ax1.set_ylim(0,1)
#                    
#                    ax1.plot(Setting_List,Statistik,'bo',ms=2)
#                    ax1.set_title(Statistik_Parameter_List[Statistik_Parameter]+' for '+Analysed_Setting_List[Analysed_Setting]+' on Plot'+str(Plot_Number))
#                    ax1.grid()
#                    ax1.set_xlabel(Analysed_Setting_List[Analysed_Setting])
#                    ax1.set_ylabel(str(Statistik_Parameter_List[Statistik_Parameter]), fontsize=9)
#    
#                plt.tight_layout()
#                plt.draw()
#                plt.show()
#                plt.savefig(str(Plot_Number)+str(Statistik_Parameter)+str(Analysed_Setting)+'.png', dpi=500)
##    plt.ylim(0,1)    
##    plt.show()
    

    
    
    

    #Plot_Good_Run(Results, Datum, Analysed_Parameter, Resultfile, Plot)
    
    
    
    

    
   
    