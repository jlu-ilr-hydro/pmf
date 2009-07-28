from pylab import *
from Fuzzy import *
from CG_environment import *
from datetime import *
class Root():
    def __init__(self):
        pass
    def nutrient_passive(self,water_uptake,nutrient_c,c_max=10.): #c_max: maximal allowed nutrient concentration, if zero, passive uptake is neglegated
        nutrient_passive=water_uptake*min(nutrient_c,c_max)
        return nutrient_passive
    def nutrient_active(self,nutrient_demand,nutrient_passive,nutrient_c,K_m,c_min=0.):#c_min: min concentration in solution for active uptake
        nutrient_active_potential=max(nutrient_demand-nutrient_passive,0)
        michaelis_menten=(nutrient_c-c_min)/(K_m+nutrient_c-c_min)
        nutrient_active_actual=nutrient_active_potential*michaelis_menten
        return nutrient_active_actual
    def nutrient_total(self,nutrient_passive,nutrient_active):
        nutrient_total=nutrient_passive+nutrient_active
        return nutrient_total
    def homogeneous_root(self,T_p,Z_r):#T_P=potential transpiration (cm*d^-1), Z_r=root-zone depth (cm)
        return T_p/Z_r
    def sink_therm(self,h_soil,h_plant): # h_soil = pressure head in soil compartment (cm), list with critical pressureheads for the plant
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err 
    
    def vertical_growth(self,Root_pot,rootibility,nutrient_water_deficit):
        return Root_pot*rootibility*nutrient_water_deficit     
    def root_distribution(self,Root_act,W_root):
        pass
    def root_partitioning(self,W_plant,Root_percent,ratio_modifier):
        return W_plant*Root_percent*stress_modifier
    def rootibility(self,mechanical_impedance,water_stress,oxygen_deficiency):
        return min(mechanical_impedance,water_stress,oxygen_deficiency)

r=Root()
soil=Soil()
for depth in arange(10.,210.,10.): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,1,400.) # lowerlimit,bulkdensity,wetness,nutrients,pressurehead
for horizon in soil:
    if horizon.lower_limit>=45:horizon.pressure_head=400.

critical_pressurehead=[0.,1.,500.,16000.]
Z_r=85.
T_p=100.
nutrient_period=[]
water_period=[]
step=10.
nutrient_demand=20.

time_act=datetime(2009,1,1);time_step=timedelta(1);time_period=timedelta(1);run_end=time_act+time_period
while time_act<run_end:
    water_daily=[]
    nutrient_daily=[]
    S_p=r.homogeneous_root(T_p,Z_r)
    for depth in arange(1.,Z_r+1.,step):
        h=soil.get_pressurehead(depth)
        alpha=r.sink_therm(h,critical_pressurehead)
        if depth+step<=Z_r:S_h=S_p*alpha*step
        else: S_h=(Z_r-depth)*alpha*S_p
        water_daily.append(S_h);
        
        nutrient_passive=r.nutrient_passive(S_h,soil.get_nutrients(depth))
        nutrient_active=r.nutrient_active(nutrient_demand,nutrient_passive,soil.get_nutrients(depth),1.)
        nutrient_total=r.nutrient_total(nutrient_passive,nutrient_active)
        print nutrient_passive,nutrient_active,nutrient_total
        nutrient_daily.append(nutrient_total)
    nutrient_period.append(nutrient_daily)
    water_period.append(water_daily)
    time_act+=time_step
    

