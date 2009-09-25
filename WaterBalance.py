class WaterBalance_MatrixPotential:
    def __init__(self,max_compensation_capacity=2.):
        self.max_compensation_capacity=max_compensation_capacity
        self.s_h=[]
        self.alpha=[]
        self.compensation=[]
        self.s_h_compensated=[]
    @property
    def uptake(self):
        return self.s_h
    @property
    def uptake_comp(self):
        return self.compensation
    @property
    def stress(self):
        return self.alpha
    def __call__(self,s_p,matrix_potential,pressure_threshold):
        self.s_h =[s * self.sink_term(matrix_potential[i], pressure_threshold)for i,s in enumerate(s_p)]
        self.alpha = [self.sink_term(m,pressure_threshold)for m in matrix_potential]
        self.compensation = self.compensate(self.s_h,s_p,matrix_potential, self.alpha, pressure_threshold[2],
                                               self.max_compensation_capacity)
        self.s_h_compensated=[s_h + self.compensation[i] for i,s_h in enumerate(self.s_h)]
    def compensate(self,s_h,s_p,matrix_potential,alpha,max_opt_pressure,max_compensation_capacity):
        remaining_alpha= [max(1-(m/max_opt_pressure),0.) for i,m in enumerate(matrix_potential)] 
        remaining_uptake=sum(s_p)-sum(s_h)
        return [min(r/sum(remaining_alpha)*remaining_uptake,max_compensation_capacity*s_h[i])for i,r in enumerate(remaining_alpha)]     
    def sink_term(self,h_soil,h_plant): 
        """
        call signature:
        
            sink_therm(h_soil,h_plant)
        
        Calculates alpha(h): a dimensionless prescribed function of s
        oil water pressure head with values between or equal zero and one.
    
        h_soil = pressure head in soil compartment and h_plant = list 
        with critical pressureheads for the plant. Both variables
        are list with the following structure:
        h_plant is a list with four values with the criticall pressurehead for water
        uptake, e.g. [0.,100.,500.,16000.](float-values). plant_N is a list with four 
        values with crop coefficiants for the phenological depending decline of 
        the biomass nitrogen content, e.g. [100,0.43,1000,0.16].
        """
        try:
            if h_soil<h_plant[0] or h_soil>h_plant[-1]: return 0
            if h_soil>=h_plant[1] and h_soil<=h_plant[2]: return 1
            elif h_soil<h_plant[1]: return (h_soil-h_plant[0])/(h_plant[1]-h_plant[0])
            else: return (h_plant[-1]-h_soil)/(h_plant[-1]-h_plant[-2])
        except ValueError, err:
            print err
            
class WaterBalance_ContainerApproach:
    pass

class ET_FAO:
    def __init__(self):
        self.ETo=0.
        self.ETc=0.
        self.ETc_adj=0.
    @property
    def reference(self):
        return self.ETo
    @property
    def cropspecific(self):
        return self.ETc
    @property
    def adjusted(self):
        return self.ETc_adjusted
    @property
    def __call__(self,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance):
        self.ETo = self.reference_ET(Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0)
    def reference_ET(self,Rn,T,e_s,e_a,windspeed,vegH,LAI,stomatal_resistance,alt=0,printSteps=0,daily=True):
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

