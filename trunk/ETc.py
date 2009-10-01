from pylab import *
class WaterPool:
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
    def __call__(self):
        pass
    def ETo(self,daily,Rn,T,e_s,e_a,windspeed=2.,alt=0,vegH=0.12,LAI=24*0.12,stomatal_resistance=100,printSteps=0):
        """Calculates the potential ET using the famous Penmonteith (FAO 1994) eq.
        daily = if True, the daily average will be calculated, else the hourly
        Rn = Net radiation in MJ/m2
        T = Avg. Temp. for the timespan
        e_s,e_a Sat. vap. press, act. vap. press, Pa
        windspeed = in m/s
        alt = Altitude in m o.s.l.
        vegH = Height of the vegetation in m
        LAI = Leaf area index (both sides) in m2/m2
        stomatal_resistance = Resistance of open stomata against transpiration s/m
        print_steps = if true, some debiug info 
        """
        delta=4098*(0.6108*exp(17.27*T/(T+237.3)))/(T+237.3)**2
        if daily:   G=0
        else : G=(0.5-greater(Rn,0)*0.4)*Rn
        P=101.3*((293-0.0065*alt)/293)**5.253
        c_p=0.001013
        epsilon=0.622
        lat_heat=2.45
        gamma=c_p*P/(lat_heat*epsilon)
        R=0.287
        rho_a=P/(1.01*(T+273)*R)
        d=0.6666667*vegH
        z_om=0.123*vegH
        z_oh=0.1*z_om
        k=0.41
        r_a_u= log((2-d)/z_om)*log((2-d)/z_oh)/k**2
        r_a=r_a_u/windspeed
        r_s=100./(0.5*LAI)
        nominator=(delta+gamma*(1+r_s/r_a))
        ATcoeff=epsilon*3.486*86400/r_a_u/1.01
        #AeroTerm=(rho_a*c_p*(e_s-e_a)/r_a)/nominator
        AeroTerm=gamma/nominator*ATcoeff/(T+273)*windspeed*(e_s-e_a)
        RadTerm=(delta*(Rn-G))/(nominator*lat_heat)
        if printSteps:
           print "ET= %0.2f,AT= %0.2f,RT=   %0.2f" % (AeroTerm+RadTerm,AeroTerm,RadTerm)
           print "Rn= %0.2f,G=  %0.2f,Dlt=  %0.2f" % (Rn,G,delta)
           gamma_star=gamma*(1+r_s/r_a)
           print "gamma*=%0.2f,dl/(dl+gm*)=%0.2f,gm/(dl+gm*)=%0.2f" % (gamma_star,delta/(delta+gamma_star),gamma/(delta+gamma_star))
           print "r_a=%0.2f,r_s=%0.2f,gamma=%0.2f" % (r_a,r_s,gamma)
           print "rho_a=%0.2f,c_p=%0.2f" % (rho_a,c_p)
           print "P=  %0.2f,e_a=%0.2f,e_s=  %0.2f" % (P,e_a,e_s)
        return AeroTerm+RadTerm
    def calc_ETc(self,ETo,Kcb,Ke):
        """ Returns ETc in [mm] from basal crop coefficient (Kcb) and 
            and soil evaporation (Ke)
        """
        return ETo * (Kcb+Ke)
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
        return max((1.2 + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3),Kcb+0.05)
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
    def calc_EvaporationLayer(self,De,P,RO,I,fw,E,few,DPe,Tew=0.):
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
             soil water content exceeds field capacity [mm],
        fw - fraction of 
             soil surface wetted by irrigation [0.01 - 1],
        few- exposed and wetted soil fraction [0.01 - 1]
        """
        return De-(P-RO)-(I/fw)+(E/few)+Tew+DPe
    def example_ETc(self):
        FC=0.23;WP=0.1
        Ze=0.1
        windspeed=1.6
        RHmin=35
        Kcb=[.3,.31,.32,.33,.34,.36,.37,.38,.39,.40]
        ETo=[4.5,5.0,3.9,4.2,4.8,2.7,5.8,5.1,4.7,5.2]
        calc_fc= lambda day: 0.92+(0.86-0.92)/(10.-1.)*day
        De=[18.]
        REW=8
        TEW=18
        Kcmax=1.21
        day=1
        while day<=10:
            I = 40 if day == 1 else 0.
            P = 6 if day == 6 else 0.
            Kcmax=1.21
            fc=calc_fc(day)
            fw=0.8 if day <=5 else 1
            few=min(fc,fw)
            De_start=max(De[day-1]-I/fw-P,0)
            Kr=self.calc_Kr(De_start, 18.,8.)
            Ke=self.calc_Ke(Kr, Kcmax, Kcb[day-1], few)
            E=ETo[day-1]*Ke
            DPe=max(P + I/fw - De[day-1],0)
            De_end=(self.calc_EvaporationLayer(De[day-1], P, 0., I, fw, E, few, DPe, 0.))
            De.append(De_end)
            Kc=Ke+Kcb[day-1]
            ETc=self.calc_ETc(ETo[day-1], Kcb[day-1], Ke)
            print 'day %i, ETo %4.1f, P %i, I/fw %i, 1-fc %4.2f, fw %4.1f, few %4.2f, Kcb % 4.2f, De_start %4.2f, Kr % 4.2f, Ke % 4.2f, E/few %4.1f, DPe %i,De_end %4.2f, E %4.2f, Kc %4.2f, ETc %4.2f' % (day,ETo[day-1],P,I/fw,fc,fw,few,Kcb[day-1],De_start,Kr,Ke,E/few,DPe,De_end,E,Kc,ETc)
            day+=1
    def ETc_adj(self,Ks,Kcb,Ke,ETc):
        """ When the potential energy of the soil water drops below a 
            threshold value, the crop is said to be water stressed. The 
            effects of soil water stress are described by multiplying the
            basal crop coefficient by the water stress coefficient, Ks.
            
             For soil water limiting conditions, Ks < 1. 
             Where there is no soil water stress, Ks = 1.    
        """
        return (Ks*Kcb+Ke)*ETc
    def calc_TAW(self,FC,WP,Zr):
        """ the total available water in the root zone is the difference 
            between the water content at field capacity and wilting point.
            TAW is the amount of water that a crop can extract from its root zone,
            and its magnitude depends on the type of soil and the rooting depth
            
            TAW the total available soil water in the root zone [mm],
            FC - ater content at field capacity [m3 m-3],
            WP - water content at wilting point [m3 m-3],
            Zr - the rooting depth [m].
        """
        return 1000*(FC-WP)*Zr
    def calc_RAW(self,p,TAW):
        """ The fraction of TAW that a crop can extract from the root zone 
            without suffering water stress is the readily available soil water.
            
            RAW- the readily available soil water in the root zone [mm],
            p - average fraction of Total Available Soil Water (TAW) that can be depleted 
            from the root zone before moisture stress (reduction in ET) occurs [0-1].
            
            The factor p differs from one crop to another. The factor p normally varies 
            from 0.30 for shallow rooted plants at high rates of ETc (> 8 mm d-1) to 0.70
            for deep rooted plants at low rates of ETc (< 3 mm d-1). A value of 0.50 for 
            p is commonly used for many crops.
        """
        return p*TAW
    def adjust_p(self,p_table,ETc):
        """ The values for p apply for ETc 5 mm/day can be adjusted. 

        p - fraction and ETc as mm/day. 
        """
        return p_table + 0.04*(5-ETc)
    def calc_Ks(self,TAW,Dr,RAW):
        """ Water content in me root zone can also be expressed by root zone depletion,
        Dr, i.e., water shortage relative to field capacity. At field capacity, the root 
        zone depletion is zero (Dr = 0). When soil water is extracted by evapotranspiration, 
        the depletion increases and stress will be induced when Dr becomes equal to RAW. After 
        the root zone depletion exceeds RAW (the water content drops below the threshold q t), 
        the root zone depletion is high enough to limit evapotranspiration to less than potential 
        values and the crop evapotranspiration begins to decrease in proportion to the amount of 
        water remaining in the root zone.
        
        Ks - dimensionless transpiration reduction factor dependent on available soil water [0 - 1],
        Dr - root zone depletion [mm],
        TAW- total available soil water in the root zone [mm],
        p  - fraction of TAW that a crop can extract from the root zone without suffering
             water stress [-].
        
        When the root zone depletion is smaller than RAW, Ks = 1
        For Dr > RAW, Ks:
        """
        return (TAW-Dr)/(TAW-RAW) if Dr > RAW else 1.
    def calc_WaterBalance(self,Dr_previous_day,P,RO,I,CR,ETc,DP):
        """ Returns Dr - root zone depletion at the end of day i [mm]
            
            the root zone can be presented by means of a container in which the water 
            content may fluctuate. To express the water content as root zone depletion 
            is useful. It makes the adding and subtracting of losses and gains straightforward 
            as the various parameters of the soil water budget are usually expressed in terms of 
            water depth. Rainfall, irrigation and capillary rise of groundwater towards the root 
            zone add water to the root zone and decrease the root zone depletion. Soil evaporation, 
            crop transpiration and percolation losses remove water from the root zone and increase 
            the depletion.
            
            Dr_previous_day - water content in the root zone at the end of the previous day, i-1 [mm],
            P  - precipitation on day i [mm],
            RO - runoff from the soil surface on day i [mm],
            I  - net irrigation depth on day i that infiltrates the soil [mm],
            CR - capillary rise from the groundwater table on day i [mm],
            ETc- crop evapotranspiration on day i [mm],
            DP - water loss out of the root zone by deep percolation on day i [mm]
            
            By assuming that the root zone is at field capacity following heavy rain or 
            irrigation, the minimum value for the depletion Dr is zero. At that moment no water is 
            left for evapotranspiration in the root zone, Ks becomes zero, and the root zone 
            depletion has reached its maximum value TAW.
            
            TAW > Dr >= 0
            
            The daily water balance, expressed in terms of depletion at the end of 
            the day is
        """
        return Dr_previous_day - (P-RO) - I - CR + ETc + DP
    def calc_InitialDepletion(self,FC,q,Zr):
        """ To initiate the water balance for the root zone, the initial depletion Dr, i-1 should 
        be estimated. 
        
        where q i-1 is the average soil water content for the effective root zone. Following heavy 
        rain or irrigation, the user can assume that the root zone is near field capacity, 
        i.e., Dr, i-1  0
        
        The initial depletion can be derived from measured soil water content by:
        """
        return 1000*(FC-q)*Zr
    def calc_DP(self,P,RO,I,ETc,Dr_previous_day):
        """ Returns DP
            Following heavy rain or irrigation, the soil water content in the root zone might 
            exceed field capacity. In this simple procedure it is assumed that the soil water content 
            is at q FC within the same day of the wetting event, so that the depletion Dr 
            becomes zero. Therefore, following heavy rain or irrigation.
            
            
            The DP calculated for calc_WaterBalance() is independent of the DP calculted in
            calc_De().As long as the soil water content in the root zone is below field 
            capacity (i.e., Dr, i > 0), the soil will not drain and DPi = 0.
        """
        return max(P - RO + I - ETc - Dr_previous_day,0)
    def example_irrigation(self): 
        """ Plan the irrigation applications. It is assumed that:

            - irrigations are to be applied when RAW is depleted,
            
            - the depletion factor (p) is 0.6,
            
            - all irrigations and precipitations occur early in the day,
            
            - the depth of the root zone (Zr) on day 1 is 0.3 m and increases to 0.35 m by day 10,
            
            - the root zone depletion at the beginning of day 1 (Dr, i-1) is RAW.
            
            From Eq. 82
                
            
            TAW = 1000 (0.23 - 0.10) Zr, i = 130 Zr, i [mm]
            
            From Eq. 83
                
            
            RAW = 0.6 TAW = 78 Zr, i [mm]
            
            On day 1,
                
            
            when Zr = 0.3 m: Dr, i-1 = RAW = 78 (0.3) = 23 mm
        """
        ETo=[4.5,5.0,3.9,4.2,4.8,2.7,5.8,5.1,4.7,5.2]#[mm]
        Zr=[.3,.31,.31,.32,.32,.33,.33,.34,.34,.35]#[m]
        I=[40.,0.,0.,0.,0.,0.,0.,0.,0.,27.]
        day=1
        ETc=[]
        Dr=[23.]
        Ke=[.91,.9,.72,.37,.18,.64,.45,.17,.08,.81]
        Kcb=[.3,.31,.32,.33,.34,.36,.37,.38,.39,.40]
        #Constant parameter
        FC=0.23;WP=0.1
        p=0.6        
        De=[18.]
        
        while day <= 10:
            #Get rain:
            P = 0. if day != 6 else 6.
            Dr_start=round(max(Dr[day-1]-I[day-1]-P,0.))          
            
            #Calculation of Ks paramter:
            #Total and readiely available water (FC,WP,p are constant)
            TAW=self.calc_TAW(FC, WP, Zr[day-1])
            RAW=round(self.calc_RAW(p, TAW))
            Ks=self.calc_Ks(TAW, Dr_start, RAW)
            
            #Calc ETc
            Kc=Kcb[day-1]+Ke[day-1]
            ETc=self.calc_ETc(ETo[day-1], Kcb[day-1], Ke[day-1])
            
           
            
            #Calc soil water balance
            DP=self.calc_DP(P, 0., I[day-1], 0., Dr[day-1]) if Dr_start == 0. else 0.
            Dr_end=round(self.calc_WaterBalance(Dr[day-1], P, 0., I[day-1], 0., ETc, DP))
            
            #Results end
            Dr.append(Dr_end)
            print 'day %i, ETp %4.1f,Zr %4.2f, RAW %4.2f, TAW %4.2f, Dr_start %4.2f, P %4.2f, I %4.2f, Ks %4.2f, Kcb %4.2f, Ke %4.2f, Kc %4.2f, ETc %4.1f, DP %4.2f, Dr_end %4.2f' % (day,ETo[day-1],Zr[day-1],RAW,TAW,Dr_start,P,I[day-1],Ks,Kcb[day-1],Ke[day-1],Kc,ETc,DP,Dr_end)
            day+=1
water=WaterPool()
water.example_Kbc_beans()





















         