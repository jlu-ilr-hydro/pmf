# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

@author: kellner-j
'''
import math

class ET_ShuttleworthWallace:
    """
    Calculates potential Evaporation and transpiration.
    
    ET_ShuttleworthWallace calculates the potential evapotranspiration. 
    Shuttleworth and Wallace (1985) further developed the Penman-Monteith
    method (cv. ET_FAO) to sparse vegeation. In the P-M-method the ET for a 
    reference plant (grass) is determined, which is than adapted to target crops 
    via four crop speficic parameters (Kc_x). In the S-W-method there is no refernce 
    ET. The calculated potential ET depends on weather conditions as well as on crop 
    variable that are temporarily varying (LAI, vegetation height..). 
    All equations and concepts implemented in this class are taken from
    "Estimating potential evapotranspiration using Shuttleworth-Wallace model 
    and NOAA-AVHRR NDVI data to feed a distributed hydrological model over the 
    Mekong River basin" from Zhou et al. (2006).
    All coefficients used in this approach can be received from
    this paper.
       
    
    Implementation
    ==============
    ET_ShuttleworthWallace must be implemented with the crop specific parameter.
    These parameter are related to the development of the plant.

    
    Call signature
    ==============
    ET_ShuttleworthWallace must be called with crop specific values like LAI and 
    plant height and the actual weather conditions. For the calculation
    of the evaporation the calculation of a daily soil water balance is needed. For
    that the FAO water balance model can be used. This model is 
    implemented in the class SWC - SoilWaterContainer. It is possible
    to use other water balance models, if they match the interface requirements.    
    
    @see: [Zhou et al. (2006)]
    """

    
    def __init__(self,
                 w_leafwidth=0.01,
                 z_0w = 0.005,
                 z_0g = 0.01,
                 z_w = 2.,
                 kappa=0.41,
                 r_st_min = 115.):
        """
        Returns a ET_ShuttleworthWallace instance.
        
        @type w_leafwidth: double
        @param w_leafwidth: Width of leaves [m]; for perennial w_leafwidth = w_leafwidth_max.    
        @type z_0w: double
        @param z_0w: Roughness length over weather station ground [m]
        @type z_0g: double
        @param z_0g: Roughness length of substrate ground [m]
        @type z_w: double
        @param z_w: Height of weather observation [m]
        @type kappa: double
        @param kappa: von Karman's constant [-]
        @rtype r_st_min: double
        @return r_st_min: Minimal stomatal resistance of individual leaves under optimal conditions [s m-1] 
                          extracted from Zhou et al. (2006) for grasslands               
        """

        #Constant variables
        self.w_leafwidth = w_leafwidth  #= 0.01 # for perennial according to Zhou 2006 page 175 (for annual w_leafwidth= w_max(1-math.exp(-0.6LAI))) 
        self.z_0w = z_0w
        self.z_0g = z_0g
        self.z_w = z_w
        self.kappa = kappa
        self.r_st_min = r_st_min

        #State variables
        self._Tpot_penmanmonteith = 0.
        self._Epot_penmanmonteith = 0.
        self._Tpot_SW = 0.  
        self._Epot_SW = 0.  
        self._ETpot_SW= 0.
        

    @property
    def Tpot_PenmanMonteith(self):
        """
        Returns potential transpiration
        
        Pot_Transpiration_PenmanMonteith is similar to the transpiration by 
        applying the Penman-Monteith equation to a closed canopy.        
        
        @rtype: double
        @return: Transpiration [MJ m-2 d-1]
        """
        return self._Tpot_penmanmonteith
    @property
    def Epot_PenmanMonteith(self):   
        """
        Returns potential evaporation
        
        Pot_Evaporation_PenmanMonteith is similar to the evaporation by 
        applying the Penman-Monteith equation to a bare substrate.
        
        @rtype: double
        @return: Evaporation [MJ m-2 d-1]
        """
        return self._Epot_penmanmonteith
   
    @property
    def Transpiration_pot_SW(self):
        """
        Returns potential transpiration from canopy calculated according to 
        Shuttleworth-Wallace 1989.

        @rtype: double
        @return: Transpiration in [mm d-1].
        """
        return self._Tpot_SW
        
    @property
    def Evaporation_pot_SW(self):
        """
        Returns potential evaporation from soil calculated according to 
        Shuttleworth-Wallace 1989.

        @rtype: double
        @return: evaporation in [mm d-1].
        """
        return self._Epot_SW
        
    @property
    def Evapotranspiration_pot_SW(self):
        """
        Returns potential evapotranspiration calcutlated according to 
        Shuttleworth-Wallace 1989.
        
        @rtype: double
        @return: Evapotranspiration [mm d-1]
        """
        return self._ETpot_SW
    
    def __call__(self,T,Rn,Rsn,e_s,e_a,windspeed,LAI,vegH,CO2_measured):     #Rn und Rsn beschreiben     
        """
        Calculates potential Evapotranspiration, Evaporation and Tranpiration.
        
        The user can call the transpiration coefficiEnts with the corresonding 
        properties of the class.

        @type T: double
        @param T: Mean daily air temperature at 2 m height [°C]       
        @type Tmax: double
        @param Tmax: Maximum daily air temperature at 2 m height [°C]   
        @type Tmin: double
        @param Tmin: Minimum daily air temperature at 2 m height [°C]   
        @type Rs: double
        @param Rs: Solar radiation that reaches the earth surface [MJ m-2]
        @type Rs_clearsky: double
        @param Rs_clearsky: Solar that reaches the earth surface under clear sky conditions [MJ m-2]
        @type e_s: double
        @param e_s: Saturation vapour pressure [kPa]
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa]
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1]
        @type LAI: double
        @param LAI: Leaf are index [m2 m-2]
        @type vegH: double
        @param vegH: Vegetation height [m]
        """

        
        LAI_e = self.calc_LAI_e(LAI)
        d_p = self.calc_d_p(vegH)    
        n_eddy = self.calc_n_eddy(vegH)
        z_a = self.calc_z_a(vegH)
        Z_0 = self.calc_Z_0(vegH)
        z_0c = self.calc_z_0c(vegH)
        c_d = self.calc_c_d(vegH,z_0c)
        d_0 = self.calc_d_0(LAI,vegH,c_d,z_0c)
        z_0 = self.calc_z_0(LAI,vegH,d_0,self.z_0g,c_d)
        z_b = self.calc_z_b(self.z_0w)    
        u_a = self.calc_u_a(windspeed,z_b,self.z_0w,z_a,d_0,z_0,self.z_w)
        u_h = self.calc_u_h(windspeed,vegH,z_b,self.z_0w,d_0,z_0,self.z_w)
        u_stern = self.calc_u_stern(self.kappa,u_a,z_a,d_0,z_0)
        k_h = self.calc_k_h(vegH,self.kappa,u_stern,d_0)  
        lambda1 = self.calc_lambda(T)   
        
        #Calculates stress functions for stomatal resistance (r_c_s)
        CO2_response = self.calc_CO2_response_stomata(CO2_measured)
        VPD_response = self.calc_VPD_response_stomata(e_s,e_a)
        Temp_response = self.calc_Temp_response_stomata(T)
    
        #Calculates the different resistances
        r_b = self.calc_r_b(self.w_leafwidth,u_h,n_eddy)    
        r_c_s = self.calc_r_c_s(LAI_e,self.r_st_min,CO2_response,VPD_response,Temp_response)
        r_c_a = self.calc_r_c_a(LAI,r_b)
        r_a_a = self.calc_r_a_a(vegH,self.kappa,u_stern,z_a,d_0,n_eddy,k_h,Z_0,d_p)
        r_s_a = self.calc_r_s_a(vegH,n_eddy,k_h,self.z_0g,Z_0,d_p)    
        r_s_s = self.calc_r_s_s()
 
        C_c = self.calc_C_c(T,lambda1,r_a_a,r_s_a,r_s_s,r_c_s,r_c_a)
        C_s = self.calc_C_s(T,lambda1,r_a_a,r_s_a,r_s_s,r_c_s,r_c_a)
        
        self._Tpot_penmanmonteith = self.calc_Transpi(T,Rn, Rsn, e_s, e_a, lambda1,r_c_a, r_a_a, r_c_s)
        self._Epot_penmanmonteith = self.calc_Evapor(T,Rn, Rsn, e_s, e_a, lambda1,r_a_a, r_s_a, r_s_s)
                                            
        #potential Transpiration and Evaporation [mm d-1]
        self._Tpot_SW = (self._Tpot_penmanmonteith * C_c/lambda1)   
        self._Epot_SW = (self._Epot_penmanmonteith * C_s/lambda1)
        
        #Calculates potential evapotranspiration [mm d-1]
        self._ETpot_SW = self._Tpot_SW + self._Epot_SW
        #self.ET=self.calc_ET(T,Rs,Rn,e_s,e_a,windspeed,LAI,self.vegH,self.CO2stomata,self.etc,self.ets)
        return self._Tpot_SW
        
        
    def calc_Transpi(self, T, R_n, R_s_n, e_s, e_a,lat_heat, r_c_a, r_a_a, r_c_s, alt=172.):                   #vegH, z_w=Messhöhe Windspeed, h_w =messhöhe andere meteorologische parameter
        """
        Calculates potential transpiration in (MJ m-2 d-1).
    
        @type T: double
        @param T: Mean daily air temperature at 2 m height [°C]       
        @type Rsn: double
        @param Rsn: Net radiation at the soil surface [MJ m-2]
        @type Rn: double
        @param Rn: Net radiation at the crop surface [MJ m-2]
        @type e_s: double
        @param e_s: Saturation vapour pressure [kPa]
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa]
        @type r_c_a: double
        @param r_c_a: bulk resistance of boundary layer [m s-1].
        @type r_a_a: double
        @param r_a_a: aerodynamic resistance from canopy to reference height [m s-1]
        @type r_c_s: double
        @param r_c_s: bulk resistance of canopy stomatal [m*s-1]        
        @type alt: double
        @param alt: Geographical altitude [decimal degrees]
        @rtype: double
        @return: Potential transpiraton [MJ m-2 d-1]
        """
        
        delta1 = 4098.*(0.6108*math.exp(17.27*T/(T + 237.3)))/((T + 237.3)**2.)  # slope of saturation vapour pressure curve [kPa °C-1]
        G =0.  #soil heat flux
        timeconverter = 24.*3600.
        R=0.287 # specific gas constant [kJ kg-1 K-1]
        P=101.3*((293.-0.0065*alt)/293.)**5.26  #atmospheric pressure (kPa)
        rho_a = (P/(1.01*(T + 273.)*R)) # mean air density at constant pressure [kg m-3]
        c_p=0.001013  # specific heat of moist air [MJ kg-1 °C-1]
        vapour = (e_s - e_a) # [kPa]
        epsilon=0.622 # ratio of molecular weight of water vapour to that of dry air [-]
        gamma1=c_p*P/(lat_heat*epsilon) #psychromeitc constant [kPa °C-1]
        
        return (delta1*(R_n-G)+(timeconverter*rho_a*c_p*vapour-delta1*r_c_a*(R_s_n-G))/(r_a_a+r_c_a))/(delta1 + gamma1*(1+r_c_s/(r_a_a+r_c_a)))

    
    def calc_Evapor(self, T, R_n,R_s_n, e_s, e_a,lat_heat, r_a_a,r_s_a,r_s_s, alt=172.):
        """
        Calculates potential evaporation in (MJ m-2 d-1).
    
        @type T: double
        @param T: Mean daily air temperature at 2 m height [°C]      
        @type Rsn: double
        @param Rsn: Net radiation at the soil surface [MJ m-2]
        @type Rn: double
        @param Rn: Net radiation at the crop surface [MJ m-2]
        @type e_s: double
        @param e_s: Saturation vapour pressure [kPa]
        @type e_a: double
        @type e_a: Actual vapour pressure [kPa]
        @type r_c_a: double
        @param r_c_a: bulk resistance of boundary layer [m s-1]
        @type r_a_a: double
        @param r_a_a: aerodynamic resistance from canopy to reference height [m s-1]        
        @type r_s_a: double
        @param r_s_a: aerodynamic resistance from soil to canopy [m s-1] 
        @type r_s_s: double
        @param r_s_s: soil surface resistance [m s-1]        
        @type alt: double
        @param alt: Geographical altitude [decimal degrees]
        @rtype: double
        @return: Potential evaporation which is similar to PenmanMonteith by applying it to a bare soil [MJ m-2 d-1].
        """
        
        delta1 = 4098.*(0.6108*math.exp(17.27*T/(T + 237.3)))/((T + 237.3)**2.)   # slope of saturation vapour pressure curve [kPa °C-1]
        G =0.
        timeconverter = 24.*3600.
        R=0.287 # specific gas constant [kJ kg-1 K-1]
        P=101.3*((293.-0.0065*alt)/293.)**5.26  #atmospheric pressure (kPa)
        rho_a = (P/(1.01*(T + 273.)*R)) # mean air density at constant pressure [kg m-3]
        c_p=0.001013  # specific heat of moist air [MJ kg-1 °C-1]
        vapour = (e_s - e_a) # [kPa]
        epsilon=0.622 # ratio of molecular weight of water vapour to that of dry air [-]
        gamma1=c_p*P/(lat_heat*epsilon) #psychromeitc constant [kPa °C-1]

        return (delta1*(R_n-G)+(timeconverter*rho_a*c_p*vapour-delta1*r_s_a*(R_n-R_s_n))/(r_a_a+r_s_a))/(delta1 + gamma1*(1.+r_s_s/(r_a_a+r_s_a)))
        

    def calc_C_c(self,T,lat_heat,r_a_a, r_s_a, r_s_s, r_c_s, r_c_a, alt=172.):
        """
        Calculates the weighting coefficient C_c for transpiration.
    
        @type T: double
        @param T: Mean daily air temperature at 2 m height [°C]        
        @type r_c_a: double
        @param r_c_a: bulk resistance of boundary layer [m s-1].
        @type r_a_a: double
        @param r_a_a: aerodynamic resistance from canopy to reference height [m s-1]
        @type r_c_s: double
        @param r_c_s: bulk resistance of canopy stomatal [m s-1]           
        @type r_s_a: double
        @param r_s_a: aerodynamic resistance from soil to canopy [m s-1] 
        @type r_s_s: double
        @param r_s_s: soil surface resistance [m s-1]            
        @type alt: double
        @param alt: Geographical altitude [decimal degrees]
        @rtype: double
        @return: Weightig factor for potential transpiration [-].
        """
            
        delta1 = 4098.*(0.6108*math.exp(17.27*T/(T + 237.3)))/((T + 237.3)**2.)  # slope of saturation vapour pressure curve [kPa °C-1]
        P=101.3*((293.-0.0065*alt)/293.)**5.26 # atmospheric pressure [kPa]
        c_p=0.001013  # specific heat of moist air [MJ kg-1 °C-1]
        epsilon=0.622 # ratio of molecular weight of water vapour to that of dry air [-]
        gamma1=c_p*P/(lat_heat*epsilon) #psychromeitc constant [kPa °C-1]

        R_a = (delta1+gamma1)*r_a_a
        R_c = (delta1+gamma1)*r_c_a + gamma1*r_c_s
        R_s = (delta1+gamma1)*r_s_a + gamma1*r_s_s
        
        return 1./(1.+(R_c*R_a)/(R_s*(R_c+R_a)))


    
    def calc_C_s(self,T,lat_heat,r_a_a, r_s_a, r_s_s, r_c_s, r_c_a, alt=172.):
        """
        Calculates the weighting factor C_s for evaporation. 
        
        @type T: double
        @param T: Mean daily air temperature at 2 m height [°C]        
        @type r_c_a: double
        @param r_c_a: bulk resistance of boundary layer [m s-1]
        @type r_a_a: double
        @param r_a_a: aerodynamic resistance from canopy to reference height [m s-1]
        @type r_c_s: double
        @param r_c_s: bulk resistance of canopy stomatal [m s-1]           
        @type r_s_a: double
        @param r_s_a: aerodynamic resistance from soil to canopy [m s-1] 
        @type r_s_s: double
        @param r_s_s: soil surface resistance [m s-1]            
        @type alt: double
        @param alt: Geographical altitude in [decimal degrees]
        @rtype: double
        @return: Weightig factor for potential evaporation [-].
        """
           
        delta1 = 4098.*(0.6108*math.exp(17.27*T/(T + 237.3)))/((T + 237.3)**2.)  # slope of saturation vapour pressure curve [kPa °C-1]
        P=101.3*((293.-0.0065*alt)/293.)**5.26 # atmospheric pressure [kPa]
        c_p=0.001013  # specific heat of moist air [MJ kg-1 °C-1]
        epsilon=0.622 # ratio of molecular weight of water vapour to that of dry air [-]
        gamma1=c_p*P/(lat_heat*epsilon) #psychromeitc constant [kPa °C-1]

        R_a = ((delta1+gamma1)*r_a_a)
        R_c = ((delta1+gamma1)*r_c_a + gamma1*r_c_s)
        R_s = ((delta1+gamma1)*r_s_a + gamma1*r_s_s)
        
        return 1./(1.+(R_s*R_a)/(R_c*(R_s+R_a)))


    def calc_c_d(self,vegH,z_0c):
        """
        Calculates mean drag coefficients for indiviual crops.

        @type vegH: double
        @param vegH: Vegetation height [m]     
        @type z_0c: double
        @param z_0c: Roughness length of a closed canopy [m] 
        @rtype: double
        @return: Mean drag coefficients for indiviual crops [m].
        """
        if vegH <= 0.0:    c_d=1.4*0.001
        else : c_d=((-1.+math.exp(0.909 - 3.03*z_0c/vegH))**4.)/4. 
        return c_d


    def calc_d_0(self,LAI,vegH,c_d,z_0c):
        """
        Calculates the zero plane displacement of canopy.

        @type LAI: double
        @param LAI: leaf area index [m2 m-2]
        @type vegH: double
        @param vegH: Vegetation height [m]    
        @rtype: double
        @return: Zero plane displacement of canopy [m].
        """
        if LAI<4.:   d_0 =1.1*vegH*math.log(1+(c_d*LAI)**0.25)
        else : d_0 = vegH-z_0c/0.3        
        return d_0
        
        
    def calc_d_p(self,vegH):
        """
        Calculates the "preferred" zero plane displacement.

        @type vegH: double
        @param vegH: Vegetation height [m]    
        @rtype: double
        @return: "Preferred" zero plane displacement [m].
        """
        return 0.63*vegH
        
        
    def calc_k_h(self,vegH,kappa,u_stern,d_0):
        """
        Calculates the eddy diffusion coefficient at the top of canopy.

        @type vegH: double
        @param vegH: Vegetation height [m]
        @type kappa: double
        @param kappa: von Karman's constant [-] 
        @type u_stern: double
        @param u_stern: friction velocity [m s-1] 
        @type d_0: double
        @param d_0: Zero plane displacement of canopy [m]
        @rtype: double
        @return: Eddy diffusion coefficient at the top of canopy [m2 s-1].
        """
        return kappa * u_stern*(vegH - d_0)
        

    def calc_LAI_e(self,LAI):  
        """
        Calculates the effective LAI.

        @type LAI: double
        @param LAI: Leaf area index [m2 m-2]
        @rtype: double
        @return: Effective leaf area index [m2 m-2].       
        """
        if LAI <=2.: LAI_e=LAI
        elif LAI >=4.: LAI_e=LAI/2.
        else: LAI_e=2. 
        return LAI_e
 
 
    def calc_lambda(self,T):
        """
        Calculates the latent heat of water vapourisation (MJ/kg), called lambda.
        
        @type T: double
        @param T: Mean daily air temperature at 2 m height [°C].
        @rtype: double
        @return: latent heat of water vapourisation [MJ/kg].
        """
        return (2.501 - 0.002361*T)     
        
        
    def calc_n_eddy(self,vegH):
        """
        Calculates eddy diffusivity decay constant of the vegetation.

        @type vegH: double
        @param vegH: Vegetation height [m]
        @rtype: double
        @return: Eddy diffusivity decay constant of the vegetation [-].
        """
        if vegH <= 1.: n_eddy = 2.5                               # vegH = h_c                 
        else : n_eddy = 2.306 + 0.194* vegH  
        return n_eddy


    def calc_r_a_a(self,vegH,kappa,u_stern,z_a,d_0,n_eddy,k_h,Z_0,d_p):
        """
        Calculates aerodynamic resistance from canopy to reference height.

        @type vegH: double
        @param vegH: Vegetation height [m]
        @type kappa: double
        @param kappa: von Karman's constant [-]   
        @type u_stern: double
        @param u_stern: Friction velocity [m s-1]
        @type z_a: double
        @param z_a: Reference height [m]        
        @type d_0: double
        @param d_0: Zero plane displacement of canopy [m]        
        @type n_eddy: double
        @param n_eddy: Eddy diffusivity decay constant of the vegetation [-] 
        @type k_h: double
        @param k_h: Eddy diffusion coefficient at the top of canopy [m2 s-1]
        @type Z_0: double
        @param Z_0: "Preferred" roughness length [m]
        @type d_p: double
        @param d_p: "Preferred" zero plane displacement [m]
        @rtype: double
        @return: Aerodynamic resistance from canopy to reference height [m s-1].
        """
        return 1./(kappa*u_stern)*math.log((z_a-d_0)/(vegH-d_0))+vegH/(n_eddy*k_h)*(math.exp(n_eddy*(1.-(Z_0+d_p)/vegH))-1.)


    def calc_r_b(self,w_leafwidth,u_h,n_eddy):
        """
        Calculates r_b which is needed for calculation of r_c_a
        
        @type w_leafwidth: double
        @param w_leafwidth: Width of leaves [m]; for perennial w_leafwidth = w_leafwidth_max        
        @type u_h: double
        @param u_h: Wind speed at the top of canopy [m s-1]
        @type n_eddy: double
        @param n_eddy: Eddy diffusivity decay constant of the vegetation [-]           
        @rtype: double
        @return: r_b which is needed for calculation of r_c_a [s m-1].
        """       
        return (100./n_eddy*(w_leafwidth/u_h)**0.5 * (1.-math.exp(-n_eddy/2.))**(-1.))

        
    def calc_r_c_a(self,LAI,r_b):  
        """
        Calculates bulk resistance of boundary layer.
        
        @type LAI: double
        @param LAI: Leaf area index [m2 m-2]
        @type r_b: double
        @param r_b: r_b [s m-1]
        @rtype: double
        @return: Bulk resistance of boundary layer [m s-1].
        """
        return r_b * 0.5/LAI
        
        
    def calc_r_c_s(self,LAI_e,r_st_min,CO2_response, VPD_response, Temp_response):
        """
        Calculates the bulk stomatal resistance of canopy.
        
        In case, that one or more of the stress or response function is zero, 
        the stomatal resistance of the canopy is limited to 50000 [s/m], because 
        of the molecular diffusivity of water vapour through leaf cuticula. 
        This limit is also extracted from Zhou et al. (2006) and based on Tourula and 
        Heikinheimo (1998).

        @type LAI_e: double
        @param LAI_e: Effective leaf area index [m2 m-2]
        @type r_st_min: double
        @param r_st_min: Minimal stomatal resistance of individual leaves under optimal conditions [s m-1]        
        @type CO2_stress: double
        @param CO2_stress: Stomatal stress due to atmospheric CO2 [-]
        @type VPD_stress: double
        @param VPD_stress: Stomatal stress due to vapor pressure deficit [-]
        @type Temp_stress: double
        @param Temp_stress: Stomatal stress due to temperature [-]
        @rtype: double
        @return: Bulk stomatal resistance of canopy [m s-1].
        """
        
        return max(50000. , r_st_min/(LAI_e*(CO2_response * VPD_response * Temp_response)))  
        
        
    def calc_CO2_response_stomata(self, CO2_measured):
        """
        Calculates the response of stomata to atmospheric CO2.
        
        The function returns a value between 0 and 1, where 0 = stomatal closure (conductance=0)
        and 1 = stomata are completely opened (resistance=0).
        The function = 1 at 330 ppm and reduces linearly to 0 1150 ppm.
        But, the function is only valid in the range of 330-660 ppm.   
        At 660 ppm calc_CO2_response_stomata = 0.6 [-]
        --> with increasing CO2 the stomata close linearly.
        
        This approach was taken based on Stockle 1992, p.233.
        
        @type CO2_measured: double
        @param CO2_measured: atmospheric CO2 concentration in rings [ppm].
        @rtype: double
        @return: Stomatal response to atmospheric CO2 [-].          
        """        
    
        return 1.4 - 0.4*(CO2_measured/330.) 


    def calc_VPD_response_stomata(self, e_s, e_a):
        """
        Calculates the response of stomata to vapor pressure deficit (VPD).
        
        The function returns a value between 0 and 1, where 0 = stomatal closure (conductance=0)
        and 1 = stomata are completely opened (resistance=0).
        With increasing vapor pressure deficit the stomata close.  
        
        This approach was taken from Zhou et al. 2006, p.155.
        
        @type e_s: double
        @param e_s: Saturation vapour pressure [kPa]
        @type e_a: double
        @param e_a: Actual vapour pressure [kPa] 
        @rtype: double
        @return: Stomatal response to vapor pressure deficit [-].          
        """
        vapor = e_s - e_a
        vpd_response = 1. - 0.409 * vapor
        return vpd_response


    def calc_Temp_response_stomata(self,T):
        """
        Calculates the response of stomata to temperature.
        
        The function returns a value between 0 and 1, where 0 = stomatal closure (conductance=0)
        and 1 = stomata are completely opened (resistance=0).
        When the air temperature is higher than 25°C  the stomatal openness is not limited. 
        Is the air temperature less than 0°C the stomata close completely.
        This approach was taken from Zhou et al. 2006, p.155.
        
        @type T: double
        @param T: Daily mean air temperature [°C] 
        @rtype: double
        @return: Stomatal response to temperature [-].         
        """
        T_kelvin = T + 273.16
        
        if T_kelvin >= 298.: temp_response = 1.
        elif T_kelvin <= 273.: temp_response = 0.
        else: temp_response = 1. - 1.6 * 10.**(-3.) * (298. - T_kelvin)**2.   # linear opening of stomata with increasing temperature    
        
        return temp_response


    def calc_r_s_a(self,vegH,n_eddy,k_h,z_0g,Z_0,d_p):
        """
        Calculates aerodynamic resistance from soil to canopy.
        
        @type vegH: double
        @param vegH: Vegetation height [m]  
        @type n_eddy: double
        @param n_eddy: Eddy diffusivity decay constant of the vegetation [-]   
        @type k_h: double
        @param k_h: Eddy diffusion coefficient at the top of canopy [m2 s-1]
        @type z_0g: double
        @param z_0g: Roughness length of substrate ground [m]
        @type Z_0: double
        @param Z_0: "Preferred" roughness length [m]
        @type d_p: double
        @param d_p: "Preferred" zero plane displacement [m]
        @rtype: double
        @return: Aerodynamic resistance from soil to canopy [m s-1].
        """
        return (vegH*math.exp(n_eddy)/(n_eddy*k_h)*(math.exp(-n_eddy*z_0g/vegH)-math.exp(-n_eddy*(Z_0+d_p)/vegH)))
        
        
    def calc_r_s_s(self):
        """
        Calculates soil surface resistance.  
        
        @rtype: double
        @return: Soil surface resistance [m s-1].
        """
        return 500.     

    
    def calc_u_a(self,windspeed,z_b,z_0w,z_a,d_0,z_0,z_w):
        """
        Calculates the wind speed at the reference height.
        
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1]
        @type z_b: double
        @param z_b: Height of the internal boundary layer [m]
        @type z_0w: double
        @param z_0w: Roughness length over weather station ground [m]
        @type z_a: double
        @param z_a: Reference height [m]
        @type d_0: double
        @param d_0: Zero plane displacement of canopy [m]
        @type z_0: double
        @param z_0: Roughness length of the ground [m]
        @type z_w: double
        @param z_w: Height of weather observation [m]
        @rtype: double
        @return: Wind speed at the reference height [m s-1].
        """
        return windspeed*((math.log(z_b/z_0w)*math.log((z_a-d_0)/z_0))/(math.log(z_b/z_0)*math.log(z_w/z_0w)))


    def calc_u_h(self,windspeed,vegH,z_b,z_0w,d_0,z_0,z_w): 
        """
        Calculates the wind speed at the top of canopy.
        
        @type windspeed: double
        @param windspedd: Wind speed at 2 m height [m s-1]
        @type z_b: double
        @param z_b: Height of the internal boundary layer [m]
        @type z_0w: double
        @param z_0w: Roughness length over weather station ground [m]
        @type vegH: double
        @param vegH: Vegetation height [m]  
        @type d_0: double
        @param d_0: Zero plane displacement of canopy [m]
        @type z_0: double
        @param z_0: Roughness length of the ground [m]
        @type z_w: double
        @param z_w: Height of weather observation [m]
        @rtype: double
        @return: Wind speed at the top of canopy [m s-1].
        """
        if vegH <= 0.:  u_h = windspeed*((math.log(z_b/z_0w)*math.log((0.1)/z_0))/(math.log(z_b/z_0)*math.log(z_w/z_0w))) 
        else : u_h =windspeed*((math.log(z_b/z_0w)*math.log((vegH-d_0)/z_0))/(math.log(z_b/z_0)*math.log(z_w/z_0w))) 
        return u_h
        

    def calc_u_stern(self,kappa,u_a,z_a,d_0,z_0):
        """
        Calculates friction velocity.

        @type u_a: double
        @param u_a: Wind speed at the reference height [m s-1]
        @type kappa: double
        @param kappa: von Karman's constant [-]   
        @type z_a: double
        @param z_a: Reference height [m]
        @type d_0: double
        @param d_0: Zero plane displacement of canopy [m]
        @type z_0: double
        @param z_0: Roughness length of the ground [m]
        @rtype: double
        @return: Friction velocity [m s-1].
        """
        return kappa*u_a/(math.log((z_a-d_0)/z_0))
            
            
    def calc_Z_0(self,vegH):
        """
        Calculates the "preferred" roughness length.

        @type vegH: double
        @param vegH: Vegetation height [m]  
        @rtype: double
        @return: "Preferred" roughness length [m].
        """
        return 0.13*vegH


    def calc_z_0(self,LAI,vegH,d_0,z_0g,c_d):
        """
        Calculates the roughness length of the ground.

        @type vegH: double
        @param vegH: Vegetation height [m]  
        @rtype: double
        @return: Roughness length of the ground [m].
        """
        if vegH <= 0.:    z_0 = 0.01        # aus dem origial Shuttle-Paper, p.847
        else : z_0 =  min(0.3*(vegH-d_0), z_0g + 0.3*vegH*(c_d*LAI)**0.5)
        return z_0
    
    
    def calc_z_0c(self,vegH):
        """
        Calculates roughness length of a closed canopy.

        @type vegH: double
        @param vegH: Vegetation height [m]
        @rtype: double
        @return: Roughness length of a closed canopy [m].
        """
        if vegH<=1.:    z_0c = 0.13*vegH
        else : z_0c = 0.139*vegH - 0.009*vegH**2. 
        return z_0c


    def calc_z_a(self,vegH):
        """
        Calculates reference height, which is 2 m above vegetation.

        @type vegH: double
        @param vegH: Vegetation height [m]
        @rtype: double
        @return: Reference height [m].
        """
        return vegH + 2.
        
        
    def calc_z_b(self,z_0w):      
        """
        Calculates the height of the internal boundary layer.

        @type z_0w: double
        @param z_0w: Roughness length over weather station ground [m]       
        @rtype: double
        @return: Height of the internal boundary layer [m].
        """
        return 0.334 * 5000.**0.875 * z_0w**0.125