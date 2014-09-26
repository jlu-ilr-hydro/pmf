# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

@author: kellner-j
'''
import math
import pylab as pylab
class ET_FAO:
    """
    Calculates crop specific Evapotranspiration.
    
    ET_FAO calculates the crop specific Evapotranspiration.
    This concept based on the Penmnan-Monteith equation. 
    Reference Evapotranspiration (ETo) is adjusted with crop 
    specific values. The resulting crop specific Evapotranspiration (ETc)
    is divided into a transpiration and a evaporation component.
    All equations and concepts implemented in this class are taken from
    "Crop evapotranspiration Guidelines for computing crop water requirements 
    FAO Irrigation and drainage paper 56"
    except for the calculation of the fieldcover. In this case the calculation
    based on the leaf area index and not on the FAO-concept.
    All coefficients used in this approach can be received from
    these guidelines.
       
    
    Implementation
    ==============
    ET_FAO must be implemented with the crop specific parameter.
    These parameter are related to the development of the plant.
    For the description of influences of the development the development
    of the plant is divided into four seasons. This arrangement
    can be taken form the plant development class. For the calculation
    of the transpiration crop specific transpiration coefficients for 
    each season are required, which can be received from the FAO-guidelines.
    
    Call signature
    ==============
    ET_FAO must be called with crop specific values describing vegetation
    structure and development and the actual weather conditions. For the calculation
    of the evaporation the calculation of a daily oil water balance is needed. For
    that the FAO water balance model can be used. These model is 
    implemented in the class SWC - SoilWaterContainer. It is possible
    to use other water balance models, if they match the interface requirements.    
    
    @see: [Allen et al, 1998]
    """
    def __init__(self,kcb_values,seasons, kcmin = 0.15):
        """
        Returns a ET_FAO instance.
        
        @type seasons: list
        @param seasons: List with the length of the four development seasons in [°C].
        @type kcb_values: list
        @param kcb_values: List with basal crop coefficients for each season in seasons parameter in [-].
        @type Kcmin: double
        @param Kcmin: Minimum Kc for dry bare soil with no ground cover [0.15 - 0.20] in [-].
        
        @rtype: ET_FAO
        @return: ET_FAO instance
        
        @todo: Calculation of seasons!!!
        """
        #Constant variables
        self.kcb_values=kcb_values
        self.seasons=seasons
        self.kcmin = kcmin
        #State vairables
        self.eto=0.
        self.kcb=0.
        self.ke=0.
        self.fw=1.
        self.fc=0.
#    @property
#    def trans(self):
#        return self.eto1
    @property
    def transpiration(self):
        """
        Returns transpiration
        
        @rtype: double
        @return: Transpiration in [mm].
        """
        return self.eto * self.kcb
    @property
    def evaporation(self):
        """
        Returns evaporation
        
        @rtype: double
        @return: evaporation in [mm].
        """
        return self.eto * self.ke
    @property
    def Reference(self):
        """
        Returns reference Evapotranspiration.
        
        @rtype: double
        @return: Reference Evapotranspiration in [mm].
        """
        return self.eto
    @property
    def Cropspecific(self):
        """
        Returns Cropspecific Evapotranspiration.
        
        @rtype: double
        @return: Cropspecific Evapotranspiration in [mm].
        """
        return self.eto * (self.kcb+self.ke)
    @property
    def Adjusted(self):
        """
        Returns Adjusted cropspecific Evapotranspiration to water stress.
        
        @rtype: double
        @return: Adjusted cropspecific Evapotranspiration to water stress in [mm].
        """
        return self.eto * (self.kcb*self.ks+self.ke)
    def __call__(self,Kr,thermaltime,Rn,T,e_s,e_a,windspeed,LAI,alt=0.,RHmin=30.,h=1.):
        """
        Calculates reference Evapotranspiration and the crop specific adjustment 
        factors Kcb and Ke.
        
        The user can call the transpiration coefficiEnts with the corresonding 
        properties of the class.
        
        @type Kr: double 
        @param Kr: evaporation reduction coefficient dependent on the soil water
        depletion from the topsoil layer in [-].
        @type thermaltime: double
        @param thermaltime: Thermaltime in [degreedays].
        @type Rn: double
        @param Rn: Net radiation at the crop surface in [MJ m-2].
        @type T: double
        @param T: Mean daily air temperature at 2 m height in  [°c].
        @type e_s: double
        @param e_s: Saturation vapour pressure in [kPa].
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type vegH: double
        @param vegH: Vegetation height in [m].
        @type LAI: double
        @param LAI: Leaf are index in [m2 m-2].
        @type stomatal_resistance: double
        @param stomatal_resistance: Stomatal ristance in [s m-1].
        @type RHmin: double
        @param RHmin: Mean value for daily minimum relative humidity during the 
        mid- or late season growth stage in [percent].
        @type h: double
        @param h: mean maximum plant height during the period of calculation 
        (initial, development, mid-season, or late-season) in [m].
        """
        #Calculates reference Evapotranspiration
#        self.eto1 = self.calc_ETo1(Rn,T,e_s,e_a,windspeed)
        self.eto = self.calc_ETo(Rn,T,e_s,e_a,windspeed)
        #Calculates basal crop coefficaint for thhe transpiration calculation
        self.kcb = self.calc_Kcb(thermaltime, self.kcb_values[0], self.kcb_values[1],
                                 self.kcb_values[2], self.seasons[0], self.seasons[1], 
                                 self.seasons[2], self.seasons[3])
        
        #Calculates upper limit on the evaporation and transpiration from any cropped surface
        kcmax = self.calc_Kcmax(self.kcb, h, windspeed, RHmin)
        
        #Calcultes fieldcover afte FAO and exposed and wetted soil fraction
        self.fc = self.fc_from_LAI(LAI,fullcover = 3.) #self.calc_fc_dynamic(self.kcb, kcmax, vegH,self.kcmin)  
        few = self.calc_few(self.fc, self.fw)
        
        #Calculates evaporation coefficiant
        self.ke = self.calc_Ke(Kr, kcmax, self.kcb, few)
        return self.eto * self.kcb

    def calc_ETo(self,Rn,T,e_s,e_a,windspeed=2.,LAI=24*0.12,stomatal_resistanc=100,alt=0,printSteps=0,vegH=0.12,daily=True):
        """
        Calculates the reference Evapotranspiration.
        
        The reference surface is a hypothetical grass reference crop with an 
        assumed crop height of 0.12 m, a fixed surface resistance of 70 s m-1 
        and an albedo of 0.23. The reference surface closely resembles an 
        extensive surface of green, well-watered grass of uniform height, 
        actively growing and completely shading the ground. The fixed surface 
        resistance of 70 s m-1 implies a moderately dry soil surface resulting 
        from about a weekly irrigation frequency. 
        
        @type Rn: double
        @param Rn: Net radiation at the crop surface in [MJ m-2].
        @type T: double
        @param T: Mean daily air temperature at 2 m height in  [Celsius].
        @type e_s: double
        @param e_s: Saturation vapour pressure in [kPa].
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type vegH: double
        @param vegH: Vegetation height in [m].
        @type LAI: double
        @param LAI: Leaf are index in [m2 m-2].
        @type stomatal_resistance: double
        @param stomatal_resistance: Stomatal ristance in [s m-1].
        @type alt: double
        @param alt: Geographical altitude in [decimal degrees].
        @rtype: double
        @return: Reference evapotranspiration in [mm].
        
        @todo: defintion of altitude
        """
        delta=4098*(0.6108*pylab.exp(17.27*T/(T+237.3)))/(T+237.3)**2
        if daily:   G=0
        else : G=(0.5-pylab.greater(Rn,0)*0.4)*Rn
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
        r_a_u= pylab.log((2-d)/z_om)*pylab.log((2-d)/z_oh)/k**2
        r_a=r_a_u/windspeed
        r_s=100./(0.5*LAI) # LAIactive = LAI * 0.5
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
        """ 
        Calculates crop specific Evapotranspiration.
        
        @type ETo: double
        @param ETo: Reference Evapotranspiration in [mm].
        @type Kcb: double
        @param Kcb: Basal crop coefficient (Kcb) in [-].
        @type Ke: double
        @type Ke: evaporation coefficiant in [-].
        @rtype: double
        @return: Crop specific evapotranspiration in [mm].
        """
        return ETo * (Kcb+Ke)
    def adjust_Kcb(self,Kcb_tab,windspeed,RHmin,h):
        """ 
        Adjust basal crOP coefficiant (Kcb) to environmental conditions.
        
        @type Kcb_tab: double
        @param Kcb_tab: Constant basal crop coefficient (Kcb) related to the 
        development season in [-].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type RHmin: double
        @param RHmin: Mean value for daily minimum relative humidity during 
        the mid- or late season growth stage in [percent].
        @type h: double
        @param h: mean maximum plant height during the period of calculation 
        (initial, development, mid-season, or late-season) in [m].
        @rtype: double
        @return: Kcb adjusted with windspeed, plant height and relative 
        humidity in [-].
        """
        return Kcb_tab + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3
    def calc_Kcb(self,time,Kcb_ini,Kcb_mid,Kcb_end,Lini,Ldev,Lmid,Llate):
        """ 
        Constructs basal crop coefficient (Kcb) curve. 
            
        @type time: double 
        @param time: Day is the actual day or thermaltime in [days] or [°days]. 
        @type Kcb_ini: double 
        @param Kcb_ini: Kcb for initial season  
        @type Kcb_mid: double 
        @param Kcb_mid: Kcb for mid season 
        @type Kcb_end: double 
        @param Kcb_end: Kcb for late season   
        @type Lini: double 
        @param Lini: Length of initial season  
        @type Ldev: double 
        @param Ldev: Length of crop development season  
        @type Lmid: double 
        @param Lmid: Length of mid season
        @type Llate: double 
        @param Llate: Length of late season     
        @rtype: double
        @return: Kbc depending on the actual time in [-].
        """
        if time <=Lini: return Kcb_ini
        elif time <=Lini+Ldev: return Kcb_ini+(time-Lini)/Ldev*(Kcb_mid-Kcb_ini)
        elif time <=Lini+Ldev+Lmid: return Kcb_mid
        elif time <= Lini+Ldev+Lmid+Llate: return Kcb_mid+(time-(Lini+Ldev+Lmid))/Llate*(Kcb_end-Kcb_mid)
        else: return Kcb_end
    def calc_Ke(self,Kr,Kcmax,Kcb,few):
        """
        Calculates evaporation coefficiant.
        
        @type Kr: double
        @param Kr: evaporation reduction coefficient dependent on the cumulative
        depth of water depleted (evaporated) from the topsoil.
        @type Kcmax: double
        @param Kcmax: Maximum value of Kc following rain or irrigation in [-].
        @type Kcb: double
        @param Kcb: Basal crop coefficient in [mm].
        @type few: double
        @param few: Fraction of the soil that is both exposed and wetted, i.e.,
        the fraction of soil surface from which most evaporation occurs.
        @rtype: double
        @return: evaporation coefficiant in [mm].
        """
        return min(Kr*(Kcmax - Kcb), few*Kcmax,)
    def calc_Kcmax(self,Kcb,h,windspeed,RHmin):
        """ 
        Calculates maximum value of Kc following rain or irrigation.
        
        @type Kcb: double
        @param Kcb: Basal crop coefficient in [mm].
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1].
        @type RHmin: double
        @param RHmin: Mean value for daily minimum relative humidity during the 
        mid- or late season growth stage in [percent].
        @type h: double
        @param h: mean maximum plant height during the period of calculation 
        (initial, development, mid-season, or late-season) in [m].
        @rtype: double
        @return: Maximum value of Kc following rain or irrigation in [-].
        """
        return max((1.2 + (0.04*(windspeed-2.)-0.004*(RHmin-45))*(h/3.)**0.3),Kcb+0.05)
    def calc_TEW(self,qFC,qWP,Ze):
        """
        Calculates total evaporable water.
        
        TEW total evaporable water = maximum depth of water 
        that can be evaporated from the soil when the topsoil
        has been initially completely wetted.
        
        @type qFC: double
        @param qFC: Soil water content at field capacity in [m3 m-3].
        @type qWP: double
        @param qWP: Soil water content at wilting point in [m3 m-3].
        @type Ze: double
        @param Ze: Depth [0.10-0.15m] of the surface soil layer that is subject 
        to drying by way of evaporation in [m].
        @rtype: double
        @return: Total evaporable water in [mm].
        """
        return 1000(qFC-0.5*qWP)*Ze
    def calc_Kr(self,De,TEW,REW):
        """
        Calculates evaporation reduction coefficient
        
        Kr is the dimensionless evaporation reduction coefficient dependent 
        on the soil  water depletion (cumulative depth of evaporation) 
        from the topsoil layer.
        
        @type De: double
        @param De:  Cumulative depth of evaporation (depletion) from the soil 
        surface layer at the end of the previos day in [mm].
        @type TEW: double
        @param TEW: Total evaporable water in [mm] 
        @type param: double
        @param param: cumulative depth of evaporation (depletion) at the end of 
        stage 1 (REW = readily evaporable water)in [mm].
        @rtype: double
        @return: Dimensionless evaporation reduction coefficient in [-].
        """
        if De > REW:
            return (TEW-De)/(TEW-REW)
        else:
            return 1.
    def calc_few(self,fc,fw=1.):#fw=1. - precipitation
        """
        Calculates fraction of the soil that is both exposed and wetted.
        
        fc and fw: [0.01 - 1], for precipitation fw = 1.0
        
        @type fc: double
        @param gc: Effective fraction of soil surface covered by vegetation 
        in [-].
        @type fw: double
        @param fw: Average fraction of soil surface wetted by irrigation or 
        precipitation in [-].
        @rtype: double
        @return: Fraction of the soil that is both exposed and wetted in [-].
        """
        return min(1-fc,fw)
    def calc_fc_dynamic(self,Kcb,Kcmax,h,Kcmin):#
        """ 
        Dynamic calculates effective fraction of soil surface covered by 
        vegetation.
        
        Kcmin =0.15 - annual crops under nearly bare soil conditions
        
        @type Kcb: double
        @param Kcb: Basal crop coefficient in [mm].
        @type Kcmax: double
        @param Kcmax: Maximum value of Kc following rain or irrigation in [-].
        @type h: double
        @param h: mean maximum plant height during the period of calculation 
        (initial, development, mid-season, or late-season) in [m].
        @type Kcmin: double
        @param Kcmin: Minimum Kc for dry bare soil with no ground cover 
        [0.15 - 0.20] in [-].
        @rtype: double
        @return: Effective fraction of soil surface covered by vegetation 
        in [-].
        """
        return ((Kcb-Kcmin)/(Kcmax-Kcmin))**(1+0.5*h) 
    def calc_fc_static(self,thermaltime,seasons):
        """
        Calculates effective fraction of soil surface covered by vegetation.
        The value for fc is limited to < 0.99. The user should assume 
        appropriate values for the various growth stages. 
        Typical values for fc :
        Season    fc
        1        0.0-0.1
        2        0.1-0.8
        3        0.8-1.
        4        0.2-0.8
        
        @type thermaltime: double
        @param thermaltime: Thermaltime in [degreedays].
        @type seasons: list
        @param seasons: List with the length of the four development seasons 
        in [°C].
        @rtype: double
        @return: Effective fraction of soil surface covered by vegetation 
        in [-].
        """
        if thermaltime <= seasons[0]: return 0.1 
        elif thermaltime <= seasons[0]+seasons[1]: return 0.8
        elif thermaltime <= seasons[0]+seasons[1]+seasons[2]:return 1.
        else: return 0.8
    def fc_from_LAI(self,LAI,fullcover = 3.):
        """
        Returns fieldcover calculated from LAI.
        
        LAI 3.0 can be assumed as maximum fieldcover.
        For LAI > 3.0 fc equals one, for values under 3.0
        fc is computed as fraction from full cover.
        
        @type LAI: double
        @param LAI: Leaf area index in [m2 m-2].
        @type fullcover: double
        @param fullcover: LAI which leads to full fieldcover in [m2 m-2].
        
        @rtype: double
        @return: Effective fraction of soil surface covered by vegetation in [-].
        """ 
        return min(LAI / fullcover,1.)
