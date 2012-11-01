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

def load_Settings_for_all_files(Runs, Setting_Parameter):
    if Setting_Parameter == 'tbase':
        Step=1
    if Setting_Parameter == 'Emergence':
        Step=2
    if Setting_Parameter == 'LeafDevelopment':
        Step=3
    if Setting_Parameter == 'Tillering':
        Step=4
    if Setting_Parameter == 'TemElongation':
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
    if Setting_Parameter == 'leaf_specific_weight':
        Step=15
    if Setting_Parameter == 'root_growth':
        Step=16
    if Setting_Parameter == 'max_height':
        Step=17
    if Setting_Parameter == 'carbonfraction':
        Step=18
    if Setting_Parameter == 'max_depth':
        Step=19
    
    Settings_List=[]   
    for Number in range(Runs):
        try:
            Resultfile = file('Results'+str(Number)+'Kersebaum_yield.csv')
            Resultfile.readline()#Setting:
            Resultfile.readline()#tbase,stage, etc.
            Settings = Resultfile.readline()
            Settings_List.append(Settings.split(';')[Step])
        except: IOError
    return Settings_List




def load_Settings_for_one_file(Resultfile):
    Resultfile=file(Resultfile)
    Setting_List=[]   
    Resultfile.readline()#Setting:
    Resultfile.readline()#tbase,stage, etc.
    Setting = Resultfile.readline()
    Setting_List.append(Setting.split(';'))
    
    Setting_Names=['tbase','Emergence','LeafDevelopment','Tillering','StemElongation','Anthesis',
    'SeedFill','DoughStage','Maturity','RUE','k','kcb1','kcb2','kcb3',
    'leaf_specific_weight','root_growth','max_height','carbonfraction','max_depth']
    Setting_String=''
    

    for i in range(len(Setting_Names)):
        if i==0:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '
        if i==1:
            Setting_String+='Stage=['+str(int(round(float(Setting_List[0][1+1]),0)))+', '+str(int(round(float(Setting_List[0][2+1]),0)))+', '+str(int(round(float(Setting_List[0][3+1]),0)))+', '+str(int(round(float(Setting_List[0][4+1]),0)))+', '+str(int(round(float(Setting_List[0][5+1]),0)))+', '+str(int(round(float(Setting_List[0][6+1]),0)))+', '+str(int(round(float(Setting_List[0][7+1]),0)))+', '+str(int(round(float(Setting_List[0][8+1]),0)))+'], '
        if i==9:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '             
        if i==10:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '            
        if i==11:
            Setting_String+='kcb=['+str(round(float(Setting_List[0][11+1]),2))+', '+str(round(float(Setting_List[0][12+1]),2))+', '+str(round(float(Setting_List[0][13+1]),2))+'],\n'        
        if i==14:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '        
        if i==15:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '        
        if i==16:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '        
        if i==17:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))+', '
        if i ==18:
            Setting_String+=Setting_Names[i]+'='+str(round(float(Setting_List[0][i+1]),2))

        
        
        
        
    return Setting_String



    
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

    for Number in range(Runs):
        try:
            Resultfile = file('Results'+str(Number)+'Kersebaum_yield.csv')
            Statistik = load_Result_Table('Results'+str(Number)+'Kersebaum_yield.csv')   
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
                        Good_Setting_Files_Plot1.append(Resultfile.name)
                    if Plot == 1:
                        Good_runs_Plot2+=1
                        Good_Setting_Files_Plot2.append(Resultfile.name)
                    if Plot == 2:
                        Good_runs_Plot3+=1
                        Good_Setting_Files_Plot3.append(Resultfile.name)
        except: IOError
        
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
    Resultfile=file(Resultfile)
    Resultfile.readline()
    columns=[]    
    for line in Resultfile:
        columns.append(line.split(';'))
        #zeilen = line.split(';')
        #print zeilen
        
    EF       =np.zeros((3),dtype=[('Root_C', 'f8'),('Root_drymatter', 'f8'), ('StemLeaves_C', 'f8'),('StemLeaves_drymatter', 'f8'),('Storage_C', 'f8'),('Storage_drymatter', 'f8')])              
    Bias     =np.zeros((3),dtype=[('Root_C', 'f8'),('Root_drymatter', 'f8'), ('StemLeaves_C', 'f8'),('StemLeaves_drymatter', 'f8'),('Storage_C', 'f8'),('Storage_drymatter', 'f8')])              
    R_Squared=np.zeros((3),dtype=[('Root_C', 'f8'),('Root_drymatter', 'f8'), ('StemLeaves_C', 'f8'),('StemLeaves_drymatter', 'f8'),('Storage_C', 'f8'),('Storage_drymatter', 'f8')])              
    
    for Plot in range(3):
        EF_Jump=(Plot+1)*13
        EF['Root_C'][Plot]               = columns[EF_Jump][1]
        EF['Root_drymatter'][Plot]       = columns[EF_Jump][4]
        EF['StemLeaves_C'][Plot]         = columns[EF_Jump][7]
        EF['StemLeaves_drymatter'][Plot] = columns[EF_Jump][10]
        EF['Storage_C'][Plot]            = columns[EF_Jump][13]
        EF['Storage_drymatter'][Plot]    = columns[EF_Jump][16]
        
        Bias_Jump=EF_Jump+1
        Bias['Root_C'][Plot]               = columns[Bias_Jump][1]
        Bias['Root_drymatter'][Plot]      = columns[Bias_Jump][4]
        Bias['StemLeaves_C'][Plot]         = columns[Bias_Jump][7]
        Bias['StemLeaves_drymatter'][Plot] = columns[Bias_Jump][10]
        Bias['Storage_C'][Plot]            = columns[Bias_Jump][13]
        Bias['Storage_drymatter'][Plot]    = columns[Bias_Jump][16]
    
        R_Squared_Jump=EF_Jump+2
        R_Squared['Root_C'][Plot]               = columns[R_Squared_Jump][1]
        R_Squared['Root_drymatter'][Plot]      = columns[R_Squared_Jump][4]
        R_Squared['StemLeaves_C'][Plot]         = columns[R_Squared_Jump][7]
        R_Squared['StemLeaves_drymatter'][Plot] = columns[R_Squared_Jump][10]
        R_Squared['Storage_C'][Plot]            = columns[R_Squared_Jump][13]
        R_Squared['Storage_drymatter'][Plot]    = columns[R_Squared_Jump][16]
    
    file.close(Resultfile)
#    Bias_Plot1      = columns[14]
#    R_squared_Plot1 = columns[15]
#    
#    EF_Plot2        = columns[26]
#    Bias_Plot2      = columns[27]
#    R_squared_Plot2 = columns[28]
#    
#    EF_Plot3        = columns[39]
#    Bias_Plot3      = columns[40]
#    R_squared_Plot3 = columns[41]
    
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
    for Number in range(Runs):
        try:
            Statistik = load_Result_Table('Results'+str(Number)+'Kersebaum_yield.csv')
            Statistik_Parameter_List.append(Statistik[Statistik_Parameter_Value][Analysed_Parameter][Plot])
        except: IOError        
    return Statistik_Parameter_List

    
def load_Good_run(Good_run_file):
    Good_run_file = file(Good_run_file)    
    Good_run_file.readline()
    columns=[]    
    for line in Good_run_file:
        columns.append(line.split(';'))
        
    Results = np.zeros((3),dtype=[('Root_C', 'f8',(2,4)),('Root_drymatter', 'f8',(2,4)), ('StemLeaves_C', 'f8',(2,5)),('StemLeaves_drymatter', 'f8',(2,6)),('Storage_C', 'f8',(2,2)),('Storage_drymatter', 'f8',(2,3)),('Date', 'int16',(6,3))])
    for Plot in range(3):
        for Calc_Meas in range(2):
            for Steps in range(6): 
                Jump =6+Steps+Plot*13
                Results['StemLeaves_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+10]                
                if Steps <4:
                    Results['Root_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+1]
                    Results['Root_drymatter'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+4]                               
                if Steps <5: 
                    Results['StemLeaves_C'][Plot][Calc_Meas][Steps] = columns[Jump][Calc_Meas+7]                
                if Steps >=3:
                    Short_Step=Steps-3
                    Results['Storage_drymatter'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+16] 
                    if Steps <5:
                        Results['Storage_C'][Plot][Calc_Meas][Short_Step] = columns[Jump][Calc_Meas+13]
                for Date in range(3):
                    Results['Date'][Plot][Steps][Date] = columns[Jump][19+Date]         
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

def Plot_all_results_for_Good_run(Resultfile,Plot):
    Default_PMF_Results=load_Good_run('Default_Results_Kersebaum_yield.csv')
    Results = load_Good_run(Resultfile)    
    EF_List        =load_Result_Table(Resultfile)[0][Plot-1]
    Bias_List      =load_Result_Table(Resultfile)[1][Plot-1]      
    R_Squared_List =load_Result_Table(Resultfile)[2][Plot-1]
    Setting_String = load_Settings_for_one_file(Resultfile)    
    Result_Parameter_List=['Root_C','Root_drymatter','StemLeaves_C','StemLeaves_drymatter',
    'Storage_C','Storage_drymatter']
    ax_Number=0
    for row in range(3):
        for columen in range(2):
            ax_Number+=1
            ax1 = plt.subplot(3,2,ax_Number)#Root_C
            #ax2 = plt.subplot(612)#Root_drymatter
            #ax3 = plt.subplot(613)#Stem_Leaves_C
            #ax4 = plt.subplot(621)#Stem_Leaves_drymatter
            #ax5 = plt.subplot(622)#Storage_C
            #ax6 = plt.subplot(623)#Storage_drymatter

            Biggest_value1 = np.max(Results[Result_Parameter_List[ax_Number-1]][Plot-1])
            Biggest_value2 =np.max(Default_PMF_Results[Result_Parameter_List[ax_Number-1]][Plot-1])         
            Biggest_value= np.max([Biggest_value1, Biggest_value2])
            Datum   = load_Datetimes(Results, Result_Parameter_List[ax_Number-1])
            ax1.set_xlim(datetime(1994,1,1),datetime(1999,1,1))
            ax1.set_ylim(0,Biggest_value*1.1)
            ax1.plot(Datum,Results[Result_Parameter_List[ax_Number-1]][Plot-1][0],'bo', ms=4,label='PMF')
            ax1.plot(Datum,Results[Result_Parameter_List[ax_Number-1]][Plot-1][1],'gs', ms=4,label='Kersebaum')
            ax1.plot(Datum,Default_PMF_Results[Result_Parameter_List[ax_Number-1]][Plot-1][0],'k.', ms=8,label='Default_PMF')
            if ax_Number==1:            
                leg = ax1.legend(bbox_to_anchor=(1.34, -2.1), loc='best', fancybox=True)
                leg.get_frame().set_alpha(0.5)
                props = dict(boxstyle='round',facecolor='white', alpha=0.5)
                ax1.text(0.56,-0.39,Setting_String, transform=ax1.transAxes, fontsize=10, verticalalignment='top', bbox=props)
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
            
        
    plt.tight_layout()
    plt.draw()
    plt.show()
    plt.savefig('Picture_'+Resultfile+'_on_Plot'+str(Plot)+'.png', dpi=500)



def Plot_Statistik(Runs, Plot, Statistik_Parameter, Analysed_Setting):

    Analysed_Parameter_List=['Root_C','Root_drymatter','StemLeaves_C','StemLeaves_drymatter',
    'Storage_C','Storage_drymatter']
    
    
    ax_Number=0#Start of Plot
    Setting_List  = load_Settings_for_all_files(Runs, Analysed_Setting) 
    for Analysed_Parameter in range(len(Analysed_Parameter_List)):#6
        Statistik = load_Statistik_for_all_files(Runs,Statistik_Parameter,Analysed_Parameter_List[Analysed_Parameter], Plot)      
        ax_Number+=1
        ax1 = plt.subplot(3,2,ax_Number)
        ax1.set_ylim(0,1)
        ax1.plot(Setting_List,Statistik,'bo',ms=2)
        ax1.set_title(Statistik_Parameter+' for '+Analysed_Parameter_List[Analysed_Parameter]+' on Plot'+str(Plot), fontsize=12)
        ax1.set_xlabel(Analysed_Setting, fontsize=9)
        ax1.set_ylabel(str(Statistik_Parameter), fontsize=9)
    
    plt.tight_layout()
    plt.draw()
    plt.show()

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
    os.chdir(working_directory+'\\Results_PMF_Calibration')
    
    
    
    Min_EF        = 0.4
    Min_Bias      = -500
    Max_Bias      =  500
    Min_R_Squared =  0.8
    
    Runs          = 40589
       
    

    
    Statistik_Parameter   = 'R_Squared'    
    Plot                  = 3  
    Analysed_Parameter    = 'Storage_C'    
    Analysed_Setting      = 'max_depth'
    #Resultfile            = 'Results23534Kersebaum_yield.csv' # for Plot1 ('Results33722Kersebaum_yield.csv')
    #Resultfile            = 'Results15468Kersebaum_yield.csv' # for Plot2
    Resultfile            = 'Results2414Kersebaum_yield.csv'  # for Plot3 ('Results2414Kersebaum_yield.csv', 'Results7453Kersebaum_yield.csv', 'Results15169Kersebaum_yield.csv', 'Results16915Kersebaum_yield.csv', 'Results23534Kersebaum_yield.csv', 'Results36324Kersebaum_yield.csv', 'Results36399Kersebaum_yield.csv', 'Results37785Kersebaum_yield.csv')
    
    '''
    Searches through runs to find a fitting set
    '''   
    #Good_Setting_Files = Overview(Runs,Min_EF,Min_Bias,Max_Bias,Min_R_Squared)
    #print Good_Setting_Files
   
    '''
    Plots Statitik for one Analysed Setting over all runs
    '''  
    #Plot_Statistik(Runs, Plot, Statistik_Parameter, Analysed_Setting)
    '''
    Plots Results for one good run on one Plot
    '''    
    Plot_all_results_for_Good_run(Resultfile,Plot)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
 








   
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
    
    
    
    

    
   
    