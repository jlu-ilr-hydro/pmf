from pylab import *
from Fuzzy import *
from environment import *

sink_therm=FuzzySet([0.,1.,500.,16000.])
     

def perspire():#potential transpiration in cm*d^-1
    return 654
def homogeneous_root(T_p,Z_r):#T_P=potential transpiration (cm*d^-1), Z_r=root-zone depth (cm)
    return T_p/Z_r 
def heterogeneous_root(T_p,Z_r,z):#T_P=potential transpiration (cm*d^-1), Z_r=root-zone depth (cm), z=depth (cm)
    return 2.*T_p/Z_r*(1.-z/Z_r)
def non_homogeneous_root(T_p,L_r,l_r,z):#T_P=potential transpiration (cm*d^-1), L_r=root mass or the root length density(cm cm-3),z=depth(cm)
    return l_r/L_r*T_p


soil=Soil()
for depth in arange(10,210,10): # 200cm deep soil with 10cm horizons
    soil.add_horizon(depth,1,1,0.05,236.) # lowerlimit,bulkdensity,wetness,nutrients

S_p=[]
S_h=[]
rooting_depth=66


T_p=perspire()
Z_r=rooting_depth
for horizon in soil:
    if horizon.upper_limit<rooting_depth:
        if horizon.lower_limit<=rooting_depth:
            z=horizon.lower_limit
            S_p.append(homogeneous_root(T_p,Z_r)*horizon.depth)
            h=horizon.pressure_head
            alpha=sink_therm(h)
            S_h.append(homogeneous_root(T_p,Z_r)*horizon.depth*alpha)
        else:
            residual_depth=rooting_depth-horizon.upper_limit
            z=rooting_depth
            S_p.append(homogeneous_root(T_p,Z_r)*residual_depth)
            h=horizon.pressure_head
            alpha=sink_therm(h)
            S_h.append(homogeneous_root(T_p,Z_r)*residual_depth)
        print horizon.lower_limit,h,alpha,sum(S_p),sum(S_h)
        

    



'''

homogeneous=[]
heterogeneous=[]
depth=[1.,2.,3.,4.,5.,6.,7.,8.,9.,10.]

for d in depth:
    T_p=perspire()
    Z_r=depth[-1]
    z=d
    homogeneous.append(homogeneous_root(T_p,Z_r))
    heterogeneous.append(heterogeneous_root(T_p,Z_r,z))
    print homogeneous_root(T_p,Z_r),heterogeneous_root(T_p,Z_r,z)
    
print sum(homogeneous), sum(heterogeneous)
'''  