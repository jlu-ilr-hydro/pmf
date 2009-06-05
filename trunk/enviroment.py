class Horizon:
    def __init__(self, lowerlimit,bulkdensity,wetness,nutrients):
        self.lowerlimit=lowerlimit
        self.bulkdensity=bulkdensity
        self.wetness=wetness
        self.nutrients=nutrients
        self.length=0.
        self.upperlimit=0.
            
class Soil:
    def __init__(self):
        self.horizon=[]
    def __getitem__(self,index):
        return self.horizon[index]
    def __iter__(self):
        for h in self.horizon:
            yield h
    def addhorizon(self, lowerlimit, bulkdensity,wetness,nutrients):
        self.horizon.append(Horizon(lowerlimit,bulkdensity,wetness,nutrients))
        self.calc_values()
    def calc_values(self):
        for horizon in self.horizon:
            if self.horizon.index(horizon) == 0:
                horizon.length = horizon.lowerlimit
                horizon.upperlimit=0
            else:
                horizon.length = horizon.lowerlimit - self.horizon[self.horizon.index(horizon)-1].lowerlimit
                horizon.upperlimit = horizon.lowerlimit-horizon.length
    def get_wetness(self,depth):
        for horizon in self.horizon:
            if horizon.upperlimit <= depth and horizon.lowerlimit >= depth:
                return horizon.wetness
    def get_nutrients(self,depth):
        for horizon in self.horizon:
            if horizon.upperlimit <= depth and horizon.lowerlimit >= depth:
                return horizon.nutrients
    def get_bulkdensity(self,depth):
        for horizon in self.horizon:
            if horizon.upperlimit <= depth and horizon.lowerlimit >= depth:
                return horizon.bulkdensity

class Atmosphere:
    def __init__(self):
        self.etp=[]
        self.tmin=[]
        self.tmax=[]
    def get_etp(self,time):
        return self.etp[time]
    def get_tmin(self,time):
        return self.tmin[time]
    def get_tmax(self,time):
        return self.tmax[time]
    def set_values(self,etp,tmin,tmax):
        self.etp=etp
        self.tmin=tmin
        self.tmax=tmax
        
