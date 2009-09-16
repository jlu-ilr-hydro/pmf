from pylab import *
class CropEvapotranspiration:
    """ Calculation of crop evapotranspiration(ETc) with the dual crop coefficient (Kc = Kcb + Ke):
    
        Predicts the effects of specific wetting events on 
        the value for the crop coefficient Kc. The solution consists of 
        splitting Kc into two separate coefficients, one for crop transpiration, 
        i.e., the basal crop coefficient (Kcb), and one for soil evaporation (Ke)
        
        Steps:
        
        1. identifying the lengths of crop growth stages, and selecting the corresponding Kcb coefficients;
        
        2. adjusting the selected Kcb coefficients for climatic conditions during the stage;
        
        3. constructing the basal crop coefficient curve (allowing one to determine Kcb values for any 
           period during the growing period);
        
        4. determining daily Ke values for surface evaporation;
            The calculation procedure consists in determining:
        
                the upper limit Kc max;
                the soil evaporation reduction coefficient Kr (energy limting and falling rate stage)
                the exposed and wetted soil fraction few
        
        5. calculating ETc as the product of ETo and (Kcb + Ke).
    """
    def __init__(self):
        pass
    def calc_ETc(self,ETp,Kcb,Ke):
        """ Returns ETc in [mm] from basal crop coefficient (Kcb) and 
            and soil evaporation (Ke)
        """
        return ETp * (Kcb+Ke)
    def adjust_Kcb(self,Kcb_tab,windspeed,RHmin,h):
        """ - Kcb (Tab) the value for Kcb mid or Kcb end (if 0.45) taken from Table 17,
            - windspeed the mean value for daily wind speed at 2 m height over grass during the mid or late season growth stage [m s-1]
            - RHmin the mean value for daily minimum relative humidity during the mid- or late season growth stage
            - h the mean plant height during the mid or late season stage [m] (from Table 12)
        """
        return Kcb_tab + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3
    def calc_Kcb(self,day,Kcb_ini,Kcb_mid,Kcb_end,Lini,Ldev,Lmid,Llate):
        """ Constructed basal crop coefficient (Kcb) curve 
            using growth stage lengths.
            Lini - Length of initial season
            Ldev - Length of crop development season
            Lmid - Length of mid season
            Llate - Length of late season
            Kcb_ini - Kcb for initial season
            Kcb_mid - Kcb for mid season
            Kcb_end - Kcb for late season
            day - actual day
        """
        if day <=Lini: return Kcb_ini
        elif day <=Lini+Ldev: return Kcb_ini+(day-Lini)/Lini*(Kcb_mid-Kcb_ini)
        elif day <=Lini+Ldev+Lmid: return Kcb_mid
        elif day <= Lini+Ldev+Lmid: return Kcb_mid+(day-Lini+Ldev+Lmid)/Llate*(Kcb_end-Kcb_mid)
        else: return Kcb_end
    def example_Kbc_beans(self):
        Lini=25.
        Ldev=25.
        Lmid=30.
        Llate=20.
        Kcb_ini=0.15
        Kcb_mid=self.adjust_Kcb(1.1,2.2,30.,0.4)
        Kcb_end=0.25
        res=[]
        for i in range(120):
            res.append(self.calc_Kcb(i,Kcb_ini,Kcb_mid,Kcb_end,Lini,Ldev,Lmid,Llate))
        plot(res)
        grid()
        show()
    def calc_Ke(self,Kr,Kcmax,Kcb,few):
        """
        Ke - soil evaporation coefficient,
        Kcb - basal crop coefficient,
        Kcmax - maximum value of Kc following rain or irrigation,
        Kr - dimensionless evaporation reduction coefficient dependent
             on the cumulative depth of water depleted (evaporated) from the topsoil,
        few - fraction of the soil that is both exposed and wetted,
              i.e., the fraction of soil surface from which most evaporation occurs.
        """
        return min(Kr*(Kcmax - Kcb), few*Kcmax)
    def calc_Kcmax(self,Kcb,h,windspeed,RHmin):
        """ 
        Kc max represents an upper limit on the evaporation
        and transpiration from any cropped surface and is imposed
        to reflect the natural constraints placed on available
        energy represented by the energy balance difference
        Rn - G - H(Equation 1). Kc max ranges from about 1.05
        to 1.30 when using the grass reference ETo.
        
        h - mean maximum plant height during the period of calculation
        (initial, development, mid-season, or late-season) [m],
    
        Kcb - basal crop coefficient
        """
        return max((1.12 + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3),Kcb+0.05)
    def calc_TEW(self,qFC,qWP,Ze):
        """
        TEW total evaporable water = maximum depth of water 
        that can be evaporated from the soil when the topsoil
        has been initially completely wetted [mm],
        qFC - soil water content at field capacity [m3 m-3],
        q WP - soil water content at wilting point [m3 m-3],
        Ze - depth of the surface soil layer that is subject to
             drying by way of evaporation [0.10-0.15m].
        """
        return 1000(qFC-0.5*qWP)*Ze
    def calc_Kr(self,De,TEW,REW):
        """
        Kr - dimensionless evaporation reduction coefficient dependent on the soil 
             water depletion (cumulative depth of evaporation) from the topsoil layer
        De - cumulative depth of evaporation (depletion) from the soil surface
                     layer at the end of day i-1 (the previous day) [mm],
        TEW - maximum cumulative depth of evaporation (depletion) from the soil 
              surface layer when Kr = 0 (TEW = total evaporable water) [mm],
        REW - cumulative depth of evaporation (depletion) at the end of stage 1 
              (REW = readily evaporable water) [mm]
        """
        if De > REW:
            return (TEW-De)/(TEW-REW)
        else:
            return 1.
    def calc_Stage(self,De,REW):
        if De>REW:return 1
        else: return 0
    def example_ETc_baresoil(self):
        de=[0.00,4.73,9.45,13.98,16.57,18.04,18.88,19.36,19.64,19.79]
        for i in range(9):
            stage=self.calc_Stage(de[i],9.)
            kr=self.calc_Kr(de[i],20.,9.)#For Loam: TEW 20 mm and REW  9 mm
            ke=self.calc_Ke(kr,1.2,0.15,1.)#Kcb 0.15,Kc max = 1.20,few = 1 (bare soil)
            etc=self.calc_ETc(4.5,0.15,ke)#Kcb 0.15,ETo = 4.5 mm/day
            print 'De_start',de[i],'Stage',stage,'Kr',kr,'Ke',ke,'Etc',etc
    def calc_few(self,fc,fw=1.):#fw=1. - precipitation
        """
        1 - fc average exposed soil fraction not covered (or shaded) by vegetation [0.01 - 1],
        fw average fraction of soil surface wetted by irrigation or precipitation [0.01 - 1].
        """
        return min(1-fc,fw)
    def calc_fc_dynamic(self,Kcb,Kcmax,h,Kcmin=0.15):#Kcmin=0.15 - annual crops under nearly bare soil condition
        """ 
        !!! This equation should be used with caution and validated from field observations !!!
        fc - the effective fraction of soil surface covered by vegetation [0 - 0.99],
        Kcb - the value for the basal crop coefficient for the particular day or period,
        Kcmin - the minimum Kc for dry bare soil with no ground cover [0.15 - 0.20],
        Kcmax the maximum Kc immediately following wetting (Equation 72),
        h - mean plant height [m].
        """
        return ((Kcb-Kcmin)/(Kcmax-Kcmin))**(1+0.5*h) 
    def calc_fc_static(self,stage):
        """
        The value for fc is limited to < 0.99. The user should assume appropriate values
        for the various growth stages. Typical values for fc :
        """
        if stage == 'Initial': return 0.0 #0.0-0.1
        elif stage == 'CropDevelopment': return 0.5#0.1-0.8
        elif stage == 'Mid-season':return 1.#0.8-1.0
        elif stage == 'Late-season': return 0.5#0.2-0.2
    def calc_De(self,De,P,RO,I,fw,E,few,DP,Tew=0.):
        """
        The estimation of Ke in the calculation procedure requires a 
        daily water balance computation for the surface soil layer for
        the calculation of the cumulative evaporation or depletion from 
        the wet condition. The daily soil water balance equation for the 
        exposed and wetted soil fraction few is:
        
        To initiate water balance for evaporating layer: 
            De = 0. for topsoil near field capacity
            De = TEW for evaporated water has been depleted at beginning
        
        Returns: cumulative depth of evaporation (depletion) following complete wetting 
                 at the end of day i [mm]
                 
        De - cumulative depth of evaporation following complete wetting from 
             the exposed and wetted fraction of the topsoil at the end of day i-1 [mm],
        Pi - precipitation on day i [mm],
        RO - precipitation run off from the soil surface on day i [mm],
        I  - irrigation depth on day i that infiltrates the soil [mm],
        E  - evaporation on day i (i.e., Ei = Ke ETo) [mm],
        T  - depth of transpiration from the exposed and wetted fraction 
             of the soil surface layer on day i [mm],
        DP - deep percolation loss from the topsoil layer on day i if 
             soil water content exceeds field capacity [mm], fw fraction of 
             soil surface wetted by irrigation [0.01 - 1],
        few- exposed and wetted soil fraction [0.01 - 1]
        """
        return De-(P-RO)-(I/fw)+(E/few)+Tew+DP


#qFC = 0.23#sandyloam
#qWp = 0.1#sandyloam
#Ze = 0.1
#h = 0.3
#windspeed = 1.6#average windspeed in 2m
#RHmin = 35 #35%
#Kcb on day 1 0.1, increases to 40 by day 10

get_Kcb = lambda day: 0.3+(0.4-0.3)/(10-1)*day
get_exposed_fc = lambda day: 0.92+(0.86-0.92)/(10.-1.)*day
De=[0,5,11,14,16,11,13,16,17,18]
ETp=[4.5,5.0,3.9,4.2,4.8,2.7,5.8,5.1,4.7,5.2]
c=CropEvapotranspiration()
Kc_res=[]
Ke_res=[]
Kcb_res=[]
for i in range(1,10):
    print i
    Kcb=get_Kcb(i)
    h=0.3
    Kcmax=c.calc_Kcmax(Kcb, 0.3, 1.6, 35)
    fc = get_exposed_fc(i)
    fw = 0.8 if i<=5 else 1.
    few = min(fc,fw)#richtig
    Kr = c.calc_Kr(De[i-1], 18., 8.)
    Ke = c.calc_Ke(Kr, Kcmax, Kcb, few)
    E = ETp[i]*c.calc_Ke(Kr, Kcmax, Kcb, few)
    DP = 0. if i != 1 else 32.
    P = 0. if i!=6 else 6.
    I = 0. if i!=1 else 40.
    RO=0.
    Tew=0. #???????
    #de = c.calc_De(De[i-1], P, RO, I, fw, E, few, DP,Tew)
    #De.append(de)
    ETc = c.calc_ETc(ETp[i], Kcb, Ke)
    Kc_res.append((Ke+Kcb))
    Ke_res.append(Ke)
    Kcb_res.append(Kcb)
    print 'day',i,'ETp','%4.2f' % ETp[i],'P-RO','%4.2f' % P,'I/fw','%4.2f' % (I/fw),'1-fc','%4.2f' % fc,'fw','%4.2f' % fw,'few','%4.2f' % few,'Kcb', '%4.2f' % Kcb,'De_start', '%4.2f' % De[i-1],'Kr', '%4.2f' % Kr,'Ke', '%4.2f' % Ke,'E/few', '%4.2f' % (E/few),'DP', '%4.2f' % DP,'De_end', '%4.2f' % De[i],'E', '%4.2f' % E,'Kc', '%4.2f' % (Kcb+Ke),'ETc', '%4.2f' % ETc                                                           

plot(Kc_res,label='Kc')
plot(Ke_res,label='Ke')
plot(Kcb_res,label='Kcb')
legend(loc=0)
show()

        
        
        
        
        
        
        
        
        
        
        
