class Atmosphere:
    def __init__(self):
        self.etp=10.
        self.tmax=30
        self.tmin=20.0
    def get_etp(self):
        return self.etp
    def get_tmax(self):
        return self.tmax
    def get_tmin(self):
        return self.tmin
    
class Soil:
    def __init__(self):
        self.wetness=10
        self.bulkdensity=1
        self.nutrient=5
    def get_wetness(self):
        return self.wetness
    def get_bulkdensity(self):
        return self.bulkdensity
    def get_nutrients(self):
        return self.nutrient