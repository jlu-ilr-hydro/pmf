from datetime import *
from pylab import *

class Horizon:
    def __init__(self, lower_limit,bulkdensity,wetness,nutrients,pressure_head):
        self.lower_limit=lower_limit
        self.bulkdensity=bulkdensity
        self.wetness=wetness
        self.nutrients=nutrients
        self.depth=0.
        self.upper_limit=0.
        self.pressure_head=pressure_head
        
class Soil:
    def __init__(self):
        self.horizon=[]
    def __getitem__(self,index):
        return self.horizon[index]
    def __iter__(self):
        for h in self.horizon:
            yield h
    def add_horizon(self, lower_limit, bulkdensity,wetness,nutrients,pressure_head):
        self.horizon.append(Horizon(lower_limit,bulkdensity,wetness,nutrients,pressure_head))
        self.calc_values()
    def calc_values(self):
        for horizon in self.horizon:
            if self.horizon.index(horizon) == 0:
                horizon.depth = horizon.lower_limit
                horizon.upper_limit=0
            else:
                horizon.depth = horizon.lower_limit - self.horizon[self.horizon.index(horizon)-1].lower_limit
                horizon.upper_limit = horizon.lower_limit-horizon.depth
    def get_wetness(self,depth):
        if depth==0:
            return 0
        else:
            for horizon in self.horizon:
                if horizon.upper_limit <= depth and horizon.lower_limit >= depth:
                    return horizon.wetness
    def get_nutrients(self,depth):
        if depth==0:
            return 0
        else:
            for horizon in self.horizon:
                if horizon.upper_limit <= depth and horizon.lower_limit >= depth:
                    return horizon.nutrients
    def get_bulkdensity(self,depth):
        if depth==0:
            return 1
        else:
            for horizon in self.horizon:
                if horizon.upper_limit <= depth and horizon.lower_limit >= depth:
                    return horizon.bulkdensity
    def get_pressurehead(self,depth):
        if depth==0:
            return 1
        else:
            for horizon in self.horizon:
                if horizon.upper_limit <= depth and horizon.lower_limit >= depth:
                    return horizon.pressure_head
                 
class Atmosphere:
    def __init__(self):
        self.time=[]
        self.etp=[]
        self.tmax=[]
        self.tmin=[]
    def get_tmin(self,act_time):
        for i in range(len(self.tmin)):
            if act_time == self.time[i]:
                return self.tmin[i]
                break
    def get_tmax(self,act_time):
        for i in range(len(self.tmin)):
            if act_time == self.time[i]:
                return self.tmax[i]
                break
    def get_etp(self,act_time):
        for i in range(len(self.tmin)):
            if act_time == self.time[i]:
                return self.etp[i]
                break
    def default_values(self):
        time=[]
        for i in range(365):
            time.append(datetime(2009,1,1)+timedelta(i))
        etp=arange(364.)
        tmax=arange(364.)
        tmin=arange(364.)
        etp[0:364]=100.
        tmin[0:364]=5.
        tmax[0:364]=20.
        self.time=time
        self.etp=etp
        self.tmin=tmin
        self.tmax=tmax

