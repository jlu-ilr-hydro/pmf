# -*- coding: utf-8 -*-
"""
This script applies a sensitivity anaylsis of PMF. It uses a Monte Carlo simulation
to estimate the effect of the Light-use efficiency (LUE) parameter on crop growth
simulation of summer wheat. ... : #!!!

Weather     : Giessen,

Soil texture: Silt

Soil        : SWC,

Atmosphere  : cliamte time series from Giessen,      

Simulation  : 1.1.1980 - 31.12.1980 and 

Management  : Sowing - 1.3.JJJJ, Harvest - 8.1.JJJJ.


@author: Tobias Houska 

@version: 0.1 (04.06.2012)

@copyright: 
 This program is free software; you can redistribute it and/or modify it under  
 the terms of the GNU General Public License as published by the Free Software  
 Foundation; either version 3 of the License, or (at your option) any later 
 version. This program is distributed in the hope that it will be useful, 
 but WITHOUT ANY  WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or  FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
 more details. You should have received a copy of the GNU General 
 Public License along  with this program;
 if not, see <http://www.gnu.org/licenses/>.
"""



#######################################
#######################################
### Runtime Loop

def run(t,res,plant,actual_set):
    if t.day==1 and t.month==3:        
        #actualPlant = PMF.createPlant_SWC()
        actualPlant = PMF.createPlant_fromCoefficiant (actual_set)
        plant = PMF.connect(actualPlant,soil,Station1_Giessen)
    if t.day==1 and t.month==8:
        plant =  None
    #Let grow
    if plant: 
        plant(t,'day',1.)
     
    
   
    ETc_adj = sum(plant.Wateruptake)+plant.et.evaporation if plant else baresoil.evaporation
    evaporation = plant.et.evaporation if plant else baresoil.evaporation
    rainfall = Station1_Giessen.get_rain(t)
    Zr = plant.root.depth/100. if plant else 0.
    soil(ETc_adj,evaporation,rainfall,Zr)
    
    res.water_stress.append(plant.water_stress) if plant else res.water_stress.append(0)
    res.potential_depth.append(plant.root.potential_depth) if plant else res.potential_depth.append(0)
    res.rooting_depth.append(plant.root.depth) if plant else res.rooting_depth.append(0)
    res.water_uptake.append(plant.Wateruptake) if plant else res.water_uptake.append([0])
    res.transpiration.append(plant.et.transpiration) if plant else res.transpiration.append(0)
    res.evaporation.append(plant.et.evaporation) if plant else  res.evaporation.append(0)
    res.biomass.append(plant.biomass.Total) if plant else res.biomass.append(0)
    res.pot_total.append(plant.biomass.pot_total) if plant else res.pot_total.append(0) #sebi
    
    #res.shoot_biomass.append(plant.shoot.leaf.Wtot) if plant else res.shoot_biomass.append(0)
    
    res.root_biomass.append(plant.root.Wtot) if plant else res.root_biomass.append(0)
    res.shoot_biomass.append(plant.shoot.Wtot) if plant else res.shoot_biomass.append(0)
    res.lai.append(plant.shoot.leaf.LAI) if plant else res.lai.append(0)
    res.ETo.append(plant.et.Reference) if plant else res.ETo.append(0)
    res.ETc.append(plant.et.Cropspecific) if plant else res.ETc.append(0)
    res.rain.append(rainfall)
    res.DAS.append(t-date(1980,3,1)) if plant else res.DAS.append(0)
    res.temperature.append(Station1_Giessen.get_tmean(t))
    res.radiation.append(Station1_Giessen.get_Rs(t))
    res.stress.append(plant.water_stress if plant else 0.)
    
    res.developmentstage.append(plant.developmentstage.Stage[0]) if plant else res.developmentstage.append("")
  
    if plant:
       
        if plant.developmentstage.Stage[0] != "D": 
            res.developmentindex.append(plant.developmentstage.StageIndex) if plant else res.developmentindex.append("")
        else:
            res.developmentindex.append("")
    else:
        res.developmentindex.append("")
    res.PotentialGrowth.append(plant.biomass.PotentialGrowth) if plant else res.PotentialGrowth.append(0)
    res.ActualGrowth.append(plant.biomass.ActualGrowth) if plant else res.ActualGrowth.append(0)
    
    res.leaf.append(plant.shoot.leaf.Wtot if plant else 0.)
    res.stem.append(plant.shoot.stem.Wtot if plant else 0.)
    res.storage.append(plant.shoot.storage_organs.Wtot if plant else 0.)
    res.Dr.append(soil.Dr) if plant else res.Dr.append(0)
    res.TAW.append(plant.water.TAW if plant else 0.)
    res.RAW.append(plant.water.RAW if plant else 0.)
    res.time.append(t)


    #time_step = timedelta(days=1) sebi

    return plant

class Res(object):
    def __init__(self): # units
        self.water_uptake = [] # mm
        self.transpiration = [] # mm
        self.evaporation = [] # mm
        self.biomass = [] # g m-2
        self.root_biomass = [] # g m-2 
        self.shoot_biomass = [] # g m-2
        self.lai = [] # m2 m-2
        self.ETo = [] # mm
        self.ETc = [] # mm
        self.rain = [] # mm
        self.temperature = [] # °C
        self.radiation = [] # MJ m2
        self.DAS = [] # days
        self.leaf=[] # g m-2
        self.stem=[] # g m-2
        self.storage=[] # g m-2
        self.Dr=[] # mm (SWC)
        self.TAW=[] # mm (SWC)
        self.RAW=[] # mm (SWC)
        self.stress=[] # dimensionless
        self.fc=[] # (SWC)
        self.wp=[] # (SWC)
        self.rooting_depth=[] # cm or meter
        self.potential_depth=[] # cm or meter 
        self.water_stress=[] # -
        self.time=[] # date
        self.developmentstage = [] # class
        self.PotentialGrowth = [] # g m2
        self.ActualGrowth = [] # g m2
        self.developmentindex=[] # dd (degree days)
        self.pot_total = [] # MJ m² (sebi)

   

#########
#Weist den Ausgabewerten der Klasse Res Einheiten zu
#########
        
get_Units_Res = {'water_uptake': ' [mm]', 'transpiration': ' [mm]', 'evaporation': ' [mm]', 'biomass': ' [g/m2]', 'root_biomass': ' [g/m2]', 'shoot_biomass': ' [g/m2]',
             'lai': ' [m2/m2]', 'ETo': ' [mm]', 'ETc': ' [mm]', 'rain': ' [mm]', 'temperature': ' [°C]]',
             'radiation': ' [MJ/m2]', 'DAS': ' [days]', 'leaf': ' [g/m2]', 'stem': ' [g/m2]', 'storage': ' [g/m2]',
             'Dr': ' [mm]', 'TAW': ' [mm]', 'RAW': ' [mm]', 'stress': ' [-]', 'fc': ' [-]', 'wp': ' [-]', 'rooting_depth': ' [cm or m]',
             'potential_depth': ' [cm or m]', 'water_stress': ' [-]', 'time': ' [date]', 'developmentstage': ' [level]',
             'PotentialGrowth': ' [g/m2]', 'ActualGrowth': ' [g/m2]', 'developmentindex': ' [dd]'}

    
def Zuweisung(value):    
    run=np.sum(value)
    y_axis.append(run)


werte = [0,#transpiration
                     1,#radiation
                     2,#biomass
                     3,#evaporation
                     4,#water_uptake
                     5,#shoot_biomass
                     6,#PotentialGrowth
                     7,#root_biomass
                     9,#leaf
                     12,#storage
                     13,#ETc
                     16,#ETo
                     18,#lai
                     19,#water_stress
                     20,#potential_depth
                     22,#stem
                     25,#stress
                     26,#rooting_depth
                     27]#ActualGrowth


Namen = ['transpiration','radiation','biomass','evaporation','water_uptake','shoot_biomass','PotentialGrowth','root_biomass','leaf','storage','ETc','ETo','lai','water_stress','potential_depth','stem','stress','rooting_depth','ActualGrowth']

if __name__=='__main__':
### Setup script   
    from pylab import *
    import numpy as np
    from datetime import *
    import PMF
    from Atmosphere import ClimateStation
    from matplotlib.pyplot import figure, show
    import matplotlib.pyplot as plt
    import csv
    
    
    
    #create atmosphere interface from cliamte stsation in giessen
    Station1_Giessen = ClimateStation() #!!!
    Station1_Giessen.load_weather('climate_giessen.csv') #!!!
    #create soil interface with defaulkt settings    
    soil = PMF.ProcessLibrary.SWC()
    #set evaporation class for baresoil
    baresoil = PMF.ProcessLibrary.ET_FAO([0.,0.,0.,0.],[0.,0.,0.,0.],kcmin = 0.)
    #set management
    sowingdate = set(datetime(i,3,1) for i in range(1980,2100))
    harvestdate = set(datetime(i,8,1) for i in range(1980,2100))
    #set simulation period
    start = date(1999,01,01)
    end = date(1999,12,31)


    #create list of cropcoefficiants
    FaktorRUE = [PMF.CropCoefficiants(RUE=i) for i in np.arange(1,11,1.)]
    FaktorK = [PMF.CropCoefficiants(k=i) for i in np.arange(0.2,0.9,0.1)]

    

######################################################
######################################################    
######## Auswahl von zu varierendem Parameter ########
    
    setX = FaktorRUE
    
######################################################
######################################################
######################################################


    setX_res=[]
    setX_plants=[]
    y_axis=[]
    
    for actual_CropCoefficiant in setX:
        #Simulation
        res = Res()
        plant = None
        print "Run ... "    
        time_step = timedelta(days=1)
        actual_time = start
    
        while actual_time<end:
            plant=run(actual_time,res,plant,actual_CropCoefficiant)
            actual_time += time_step
        setX_res.append(res)
        setX_plants.append(plant)
        #########
        #Bildet die jährliche Summe ausgewaehlter Parameter
        #und speichert sie in y_axis ab.
        #########
#        for i,sets in enumerate(setX_res):
#            values = [value  for attr, value in sets.__dict__.iteritems()]
#        for i in werte:
#            Zuweisung(values[i])
        

        
    
    
    
#    #########
#    #Erstellt Tabellen für alle Ausgabewerte 
#    #für die Variation von RUE (FaktorRUE oben auswählen) oder k (FaktorK oben wählen)
#    #########     
#    EndpunktY_Achse = len(y_axis) 
#    Schritte = len(werte)
#    if setX == FaktorRUE:
#        Tabelle_RUE = open('Tabelle_RUE.csv', 'w')
#        Tabelle_RUE.writelines('RUE,transpiration,radiation,biomass,evaporation,water_uptake,shoot_biomass,PotentialGrowth,root_biomass,leaf,storage,ETc,ETo,lai,water_stress,potential_depth,stem,stress,rooting_depth,ActualGrowth')       
#        for i,n in enumerate(np.arange(0,EndpunktY_Achse,Schritte)):
#            Tabelle_RUE.writelines('\n')
#            Tabelle_RUE.writelines(str(i+1)+',')
#            for j in range(Schritte):
#                Tabelle_RUE.writelines(str(y_axis[j+n])+',')            
#        Tabelle_RUE.close()
#        
#    if setX == FaktorK:
#        Tabelle_k = open('Tabelle_k.csv', 'w')
#        Tabelle_k.writelines('k,transpiration,radiation,biomass,evaporation,water_uptake,shoot_biomass,PotentialGrowth,root_biomass,leaf,storage,ETc,ETo,lai,water_stress,potential_depth,stem,stress,rooting_depth,ActualGrowth')       
#        for i,n in enumerate(np.arange(0,EndpunktY_Achse,Schritte)):
#            Tabelle_k.writelines('\n')
#            Tabelle_k.writelines(str(i+1)+',')
#            for j in range(Schritte):
#                Tabelle_k.writelines(str(y_axis[j+n])+',')            
#        Tabelle_k.close()
#    
#
#            
#    #########
#    #Erstellt Plots für alle Ausgabewerte 
#    #für die Variation von RUE (set1 oben auswählen) oder k (set2 oben wählen)
#    #########
#    
#        
#    EndpunktNamen=len(Namen)
#
#    if setX == FaktorRUE:            
#        RUE = np.arange(1,11,1.) #für RUE                
#        for i,n in enumerate(np.arange(0,EndpunktNamen,1.)):
#            liste=[]        
#            for f,k in enumerate(np.arange(0,EndpunktY_Achse,Schritte)):
#                liste.append(y_axis[int(k)+i])  
#            fig = figure()        
#            plt.plot(RUE,liste)
#            plt.grid()
#            xlabel("RUE")
#            Unit = Namen[i]+get_Units_Res[Namen[i]]
#            ylabel(Unit)
#            fig.savefig(Namen[i]+'_RUE'+'.png',dpi=300)
#            plt.close(fig)
#    
#    if setX == FaktorK:    
#        k = np.linspace(0.2, 0.8, num=7)               
#        for i,n in enumerate(np.arange(0,EndpunktNamen,1.)):
#            liste=[]        
#            for f,g in enumerate(np.arange(0,EndpunktY_Achse,Schritte)):
#                liste.append(y_axis[int(g)+i])  
#            fig = figure()        
#            plt.plot(k,liste)
#            plt.grid()
#            xlabel("k")
#            Unit = Namen[i]+get_Units_Res[Namen[i]]
#            ylabel(Unit)
#            fig.savefig(Namen[i]+'_k'+'.png',dpi=300)
#            plt.close(fig)    
#    
#    
    


#########
#Erstellt Tabelle für alle Ausgabewerte 
#von PMF im laufe der Runtime
#########            
   
    with open('Tabelle_gesamt.csv', 'wb') as f:    
         writer = csv.writer(f,delimiter='\t', quotechar='"',quoting=csv.QUOTE_ALL) # sebi: bitte ein Komma als Trennzeichen
         writer.writerow(['Year','Month','Day','Rainfall','Temperature','Radiation','Stage','StageIndex','Transpiration','Evaporation','Wateruptake','Root biomass','Shoot biomass','PotentialGrowth','ActualGrowht','LAI','RootingDepth','Stress'])
         for i,day in enumerate(res.time):
             writer.writerow([day.year,day.month,day.day,
                   res.rain[i],res.temperature[i],res.radiation[i],res.developmentstage[i],res.developmentindex[i],res.transpiration[i],res.evaporation[i],sum(res.water_uptake[i]),res.root_biomass[i],res.shoot_biomass[i],res.PotentialGrowth[i],res.ActualGrowth[i],res.lai[i],res.rooting_depth[i]]) #res.stress[i][0]])
    
    
###############################################################################
###############################################################################
### sebi

# Ein dicker Fehler geht auf meien Kappe. Der Wert plant.biomass.total beziffert
# die akteulle gesamte Biomasse an jeden Tag. Wenn man wie oben die täglichen
# Werte in eine Liste abspeichert, muss man das maximum der Liste nehmen und NICHT
# die Summe: [np.max(i.biomass) for i in setX_res].
# Der Wert plant.biomass.ActualGrowth sowie plant.biomass.PotentialGrowth gibt die 
# täglichen WachstumsRATEN an. Diese Werte können summiert werden:
# [np.sum(i.ActualGrowth) for i in setX_res].   
# [np.sum(i.PotentialGrowth) for i in setX_res].  (ohne Wasserstress)   

# Die gesamte Analyse könnte eine Funktion sein, welche als Rückgabewert die 
# Ergenisstabelle hat. Das könnte so aussehen:

# def makeAnalsis(setX,pathTables,pathPictures)
       #dein Quelltext
       # return setX_res (Der Rückgabewert sollte ein structured - array sein, siehe unten)

# dann noch die beiden Aufrufe:
# OFAT_RUE_results = makeAnalyis(FaktorRUE,".../TableFolderRUE",".../PicturesFolderRUE")
# OFAT_k_results = makeAnalyis(FaktorK,".../TableFolderK",".../PicturesFolderK")

# Generell solltest du dir überlegen, ob du nicht die Klasse "Res" durch einen
# Numpy structured-array ersetzt (http://docs.scipy.org/doc/numpy/user/basics.rec.html).
# Numpy - arrays sind doppelt bis 10mal so schnelll, wenn es später darum geht, 
#größere Datenmengen zu verarbeiten. Hier ein Beispiel, wo ich die Ergebnisse aus
# der RES - Klasse in einen structured - array kopiere.
    
     # Beispiel: numpy structured array (sebi)
    OFAT_RUE_results = np.empty([len(FaktorRUE)],dtype=[('ID', '|S10'),('OFAT_factor', '|S10'),('OFAT_value', 'f8'),('Pot.biomass', 'f'),('Act.biomass', 'f')])
    OFAT_RUE_results['ID'] = tuple(["OFAT"+np.str(i+1) for i in np.arange(len(FaktorRUE))])
    OFAT_RUE_results['OFAT_factor'] = tuple(["RUE" for i in np.arange(len(FaktorRUE))])
    OFAT_RUE_results['OFAT_value'] = tuple([i for i in np.arange(1,11,1.)])
    OFAT_RUE_results['Pot.biomass'] = tuple([np.max(i.pot_total) for i in setX_res])
    OFAT_RUE_results['Act.biomass'] = tuple([np.max(i.biomass) for i in setX_res])

    # ein paar Aufrufe und Beispiele:  (sebi)   
#    for i in OFAT_RUE_results:
#        print i['OFAT_factor'],i['OFAT_value'],np.str(i['Biomass'])
#
#    print OFAT_RUE_results['Biomass'][ OFAT_RUE_results['OFAT_value']==3.0]
#    test = OFAT_RUE_results['Biomass'][ OFAT_RUE_results['OFAT_value']>2.0]
#    print "All value with RUE > 2.0: ", test
#    test2 = OFAT_RUE_results['Biomass'][(OFAT_RUE_results['OFAT_value']>2.0)&(OFAT_RUE_results['OFAT_value']<4.0)]
#    print "All values with 2.0 < RUE < 4.0: ",test2
    
    
    # und ein plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ind = np.arange(len(OFAT_RUE_results['Pot.biomass']))  
    width = 0.35 
    rect1 = ax1.bar(ind,OFAT_RUE_results['Pot.biomass'], width, color='LightGreen',label='Potential biomass')
    rects2 = ax1.bar(ind+width, OFAT_RUE_results['Act.biomass'], width, color='DarkGreen',label='Actual biomass')
    # add some
    ax1.set_ylabel('Plant biomass [g/m2]')
    ax1.set_title('OFAT - Radiation-Use-Efficiency')
    ax1.set_xticks(ind+width)
    ax1.set_xticklabels(OFAT_RUE_results['OFAT_value'] )
    ax1.set_xlabel('Radiation-Use-Efficiency [MJ/m2]')
    ax1.legend(loc=0)    
    fig.savefig('OFAT_RUE.png')
























##############################################################
#Nicht benoetigte Dinge
##############################################################


       
#with open('Tabelle.csv', 'wb') as f:    
#     writer = csv.writer(f,delimiter='\t', quotechar='"',quoting=csv.QUOTE_ALL)
#     writer.writerow(['Year','Month','Day','Rainfall','Temperature','Radiation','Wetness','Stage','StageIndex','Transpiration','Evaporation','Wateruptake','Root biomass','Shoot biomass','PotentialGrowth','ActualGrowht','LAI','RootingDepth','Stress'])
#     for i,day in enumerate(res.time):
#         writer.writerow([day.year,day.month,day.day,
#                          res.rain[i],res.temperature[i],res.radiation[i],sum(res.wetness[i]),
#                          res.developmentstage[i],res.developmentindex[i],res.transpiration[i],res.evaporation[i],sum(res.water_uptake[i]),res.root_biomass[i],res.shoot_biomass[i],res.PotentialGrowth[i],res.ActualGrowth[i],res.lai[i],res.rooting_depth[i],res.stress[i][0]])
#   
#    
#    plot(test)
#    plot(biomass_set23)
#    show()
    
    
#######################################
#######################################
### Show results

#timeline=drange(start,end,timedelta(1))
#subplot(311)
#plot_date(timeline,res.RAW,'k',label='Readily available Water')
#plot_date(timeline,res.Dr,'r--',label='Depletion')
#legend(loc=0)
#ylabel('Water balance [mm]')   
#subplot(312)
#plot_date(timeline,res.water_stress,'b',label='Drought stress')
#ylabel('Stress index [-]')
#ylim(0,1)
#legend(loc=0)
#subplot(313)
#plot_date(timeline,[-r for r in res.rooting_depth],'g',label='Actual')
#plot_date(timeline,[-r for r in res.potential_depth],'k--',label='Potential')
#ylabel('Rooting depth [mm]')
#legend(loc=0)
#show()
   



      
