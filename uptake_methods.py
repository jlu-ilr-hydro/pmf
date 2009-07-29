from pylab import *
class Uptake():
    def __init__(self):
        self.p_a=[]
        self.a_a=[]
        self.s_h=[]
    def __call__(self,Z_r,T_p,R_p,h_plant,depth_step,soil,c_max=1.,K_m=0.,c_min=0.):
        """
        Description: Calculates the root water and nutrient uptake for a given timestep
                     in the root zone.
    
        Parameter: Z_r = Total rootingdepth at t, T_p = Potential transpiration,
                   R_p = Potential root nutrient uptake, h_plant = critical pressurehead of
                   plant for soil water extraction, depth_step = layer thickness for pressure-
                   head and nutrient_c request, soil = Soil-Instance, c_max = maximal allowed 
                   nutrient concentration,Mechaelis-Menten constant, c_min = minimum concetration 
                   at which no net influx occurs.
        
        Returns: Set p_a = Passive nutrient uptake per timestep, a_a = active nutrient uptake
                 per timestep, s_h = root extractable soil water
        """
        s_h_list=[];p_a_list=[];a_a_list=[]
        s_p=self.water_extractionrate(T_p, Z_r)#s_p = root water extraction rate
        for depth in arange(0.,Z_r,depth_step):
            alpha=self.sink_therm(soil.get_pressurehead(depth+depth_step), h_plant)#sink_therm alpha
            if depth+depth_step<=Z_r:s_h=s_p*alpha*depth_step#uptake from each layer, which are completely penetrated
            else: s_h=alpha*s_p*(Z_r-depth)##uptake from layer which are partly penetrated
            s_h_list.append(s_h)
            p_a=self.passive_nutrientuptake(s_h, soil.get_nutrients(depth+depth_step),c_max)
            p_a_list.append(p_a)          
            print 'Depth wetness,NO3_conc,s_h,p_a:',depth,soil.get_wetness(depth+depth_step),soil.get_nutrients(depth+depth_step),s_h,p_a
        print 'Daily s_h,p_a:',sum(s_h_list),sum(p_a_list)
        P_a=sum(p_a_list)
        A_p=max(R_p-P_a,0)#A_p = Potential acitve nutrient uptake
        a_p=A_p/Z_r#a_p = Potential acitve nutrient uptake from soil layer
        print 'Daily P_a,A_p,a_p:',P_a,A_p,a_p
        for depth in arange(0.,Z_r,depth_step):
            nutrient_c=soil.get_nutrients(depth+depth_step)
            if depth+depth_step<=Z_r:a_a=a_p*self.michaelis_menten(nutrient_c, K_m, c_min)*depth_step
            else: a_a=a_p*self.michaelis_menten(nutrient_c, K_m, c_min)*(Z_r-depth)
            a_a_list.append(a_a)
            print 'depth,Mechaelis_Menten,a_p,a_a:',depth,(soil.get_nutrients(depth+depth_step)-c_min)/(K_m+soil.get_nutrients(depth+depth_step)-c_min),a_p,a_a
        A_a=sum(a_a_list)#A_a = Actual acitve nutrient uptake
        R_a=P_a+A_a#R_a = Actual root nutrient uptake
        print 'A_a,P_a,R_a:',A_a,P_a,R_a
        self.a_a.append(a_a_list)
        self.p_a.append(p_a_list)
        self.s_h.append(s_h_list)
    def water_extractionrate(self,T_p,Z_r): 
        """
        Description:Calculates the maximum possible root water extraction rate over the rootingdepth.
        
        Parameter:T_p = potential transpiration, Z_r = total rootingdepth
            
        Returns:s_p = root water extraction rate
        """
        return T_p/Z_r
    def sink_therm(self,h_soil,h_plant): 
        """
        Description: Calculates alpha(h): a dimensionless prescribed function of soil water pressure head,
                     with values between or equal zero and one.
    
        Parameter:h_soil = pressure head in soil compartment, 
                           h_plant = list with critical pressureheads for the plant
        
        Returns: sink_therm alpha
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err
    def passive_nutrientuptake(self,s_p,c_nutrient,c_max):
        """
        Description: Calculates the passive uptake with water uptake. c_max is hte maximum allowed
                     solution concetration that can be taken up by plant roots during passive uptake.
        
    
        Parameter: s_p = root water extraction rate, c_nutrient = nutrient concentration in soil layer,
                   c_max = maximal allowed nutrient concentration.
        
        Returns: p_a = actual passive nutrient uptake from soil layer.
        """
        return s_p*min(c_nutrient,c_max)
    def michaelis_menten(self,nutrient_c,K_m,c_min):
        """
        Description: Calculates the uptake kinetics wit hthe michaelis menton function.
    
        Parameter: nutrient_c = soillayer nutrient concentration ,K_m = Mechaelis-Menten constant,
                   c_min = minimum concetration at which no net influx occurs.
        
        Returns: I_n = Relationship bewteen ion influx (uptake per unit root and unit time) and its
                 concetration at the root surface (nurient_c).
        """
        return (nutrient_c-c_min)/(K_m+nutrient_c-c_min)


from CG_environment import *
soil=Soil()
for depth in arange(10.,210.,10.): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,.5,400.) # lowerlimit,bulkdensity,wetness,nutrients,pressurehead
uptake=Uptake()
for days in range(5):
    uptake(55.,100.,100.,[0.,1.,500.,16000.],10.,soil)
for days in uptake.s_h:
    print 'S_h,P_a,A_a,R_a: ',sum(days),sum(uptake.p_a[uptake.s_h.index(days)]),sum(uptake.a_a[uptake.s_h.index(days)])