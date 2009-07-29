from pylab import *
from Fuzzy import *
from CG_environment import *
from datetime import *

class Root():
    def __init__(self):
        pass
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
    soil.add_horizon(depth,1,1,0.5,400.) # lowerlimit,bulkdensity,wetness,nutrients,pressurehead

for horizon in soil:
    if horizon.lower_limit>=45:horizon.pressure_head=400.

critical_pressurehead=[0.,1.,500.,16000.]
Z_r=55.
T_p=100.
nutrient_period=[]
water_period=[]
step=10.
R_p=100

time_act=datetime(2009,1,1);time_step=timedelta(1);time_period=timedelta(1);run_end=time_act+time_period
while time_act<run_end:
    s_h_daily=[]
    nutrient_daily=[]
    p_a_daily=[]
    S_p=r.homogeneous_root(T_p,Z_r)
    for depth in arange(0.,Z_r,step):
        h=soil.get_pressurehead(depth+step)
        alpha=r.sink_therm(h,critical_pressurehead)
        if depth+step<=Z_r:s_h=S_p*alpha*step
        else: s_h=alpha*S_p*(Z_r-depth)
        s_h_daily.append(s_h);
        p_a=s_h*min(soil.get_nutrients(depth+step),100)
        p_a_daily.append(p_a)
        print '1Depth wetness,NO3_conc,s_h,p_a:',depth,soil.get_wetness(depth+step),soil.get_nutrients(depth+step),s_h,p_a
    print '2Daily s_h,p_a:',sum(s_h_daily),sum(p_a_daily)
    P_a=sum(p_a_daily)
    A_p=max(R_p-P_a,0)
    a_p=A_p/Z_r
    print '2Daily P_a,A_p,a_p:',P_a,A_p,a_p
    K_m=0.;c_min=0.
    a_a_daily=[]
    for depth in arange(0.,Z_r,step): 
        if depth+step<=Z_r:a_a=a_p*(soil.get_nutrients(depth+step)-c_min)/(K_m+soil.get_nutrients(depth+step)-c_min)*step
        else:a_a=a_p*(soil.get_nutrients(depth+step)-c_min)/(K_m+soil.get_nutrients(depth+step)-c_min)*(Z_r-depth)
        a_a_daily.append(a_a)
        print '3depth,Mechaelis_Menten,a_p,a_a:',depth,(soil.get_nutrients(depth+step)-c_min)/(K_m+soil.get_nutrients(depth+step)-c_min),a_p,a_a
    A_a=sum(a_a_daily)
    R_a=P_a+A_a
    print '4A_a,P_a,R_a:',A_a,P_a,R_a
    time_act+=time_step

    
