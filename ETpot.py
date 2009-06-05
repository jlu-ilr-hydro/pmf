from math import *
from pylab import *
def Radiation(daily=1,DOY=1,lat=50.6,lon=8.1,timezone=1,height=155,Tmax=25.,Tmin=12.,e_a=1.33,sunshine=None,clouds=0.5,albedo=0.23):
    phi=lat*pi/180
    delta=0.409*sin(2*pi/365*DOY-1.39)
    try :
        hour=array([24*(doy-int(doy)) for doy in DOY])
    except TypeError:
        hour=24*(DOY-int(DOY))
    sunset_angle=arccos(-tan(phi)*tan(delta))
    G_sc=0.082
    d_r=1+0.033*cos(2*pi*DOY/365)
    b=2*pi*(DOY-81)/364
    S_c=0.1645*sin(2*b)-0.1255*cos(b)-0.025*sin(b)
    solar_time=pi/12*(hour+lon/15.-timezone+S_c-12)
    xx=sin(phi)*sin(delta)
    yy=cos(phi)*cos(delta)
    GG_sc=24*60/pi*G_sc
    if daily:
        R_a=GG_sc*d_r*(sunset_angle*xx+sin(sunset_angle)*yy)
    else :
        start_angle=solar_time-pi/24
        end_angle=solar_time+pi/23
        R_a=12*GG_sc*d_r*((end_angle-start_angle)*xx+(sin(end_angle)-sin(start_angle))*yy)
    R_a=greater(R_a,0)*R_a
        
    if sunshine==None :
        n_N=clouds
    else :
        N=24/pi*sunset_angle
        n_N=sunshine/N
    R_s=(0.25+0.5*n_N)*R_a
    R_so=(0.75+2e-5*height)*R_a
    R_ns=(1-albedo)*R_s
    sigmaT=2.45e-9*((Tmax+273.16)**4+(Tmin+273.16)**4)
    emissivity=0.34-0.14*sqrt(e_a)
    clear_sky=(0.1+0.9*n_N)
    R_nl=sigmaT*emissivity*clear_sky*greater(R_a,-9999)
    R_n=R_ns-R_nl
#    plot(array([R_n,R_ns,R_nl,R_s,R_so,R_a]).transpose(),hold=0)
#    legend(['R_n','R_ns','R_nl','R_s','R_so','R_a'])
    return R_n,R_ns,R_nl,R_s,R_so,R_a
def ETpot(daily,Rn,T,e_s,e_a,windspeed=2.,alt=0,vegH=0.12,LAI=24*0.12,printSteps=0):
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
    return AeroTerm+RadTerm,RadTerm,AeroTerm
def vp_sat(T):
    return 0.6108*exp(17.27*T/(T+237.3))
def vapor_pressure(rHmean,Tmin,Tmax,T=None):
    if T==None :
        T=0.5*(Tmin+Tmax)
        e_s=0.5*(vp_sat(Tmin)+vp_sat(Tmax))
    else :
        e_s=vp_sat(T)
    e_a=rHmean/100.*e_s
    return e_s,e_a
    
def interpolateMonthlyData(doy,monthlyarray):
    m=(doy+15)*12./365.
    try:
        m_last=array([int(m_scalar) for m_scalar in m])-1
    except TypeError:
        m_last=int(m)        
    m_next=m_last+1
    m_part=m-m_next
    v_last=monthlyarray[m_last % 12]
    v_next=monthlyarray[m_next % 12]
    return v_next*m_part+v_last*(1-m_part)

