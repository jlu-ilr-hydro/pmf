gs=Growingseason()
gs.__setitem__(0,'Emergence',160) #GDD in Celisus
gs.__setitem__(1,'Leaf development',208)
gs.__setitem__(2,'Tillering',421)
gs.__setitem__(3,'Stem elongation',659)
gs.__setitem__(4,'Anthesis',901)
gs.__setitem__(5,'Seed fill',1174)
gs.__setitem__(6,'Dough stage',1556)
gs.__setitem__(7,'Maturity complete',1665)

class Growingseason:
    """
    Development depends on daily temperature (tmax, tmin) and a crop associated base temperature (tb)
    over which development can occur. A development stage is defined by the cumulative sum of GDD (Growing Degree Day)
    """    
    def __init__(self):
        self.stage=[]
    def __setitem__(self,index,name,tt):
        self.stage.append(Stage(name,tt))
    def __getitem__(self,index):
        return self.stage[index]
    def __iter__(self):
        for s in self.stage:
            yield s
    def thermaltime(self,tmin,tmax,tb):
        """
        GDD = (tmax+tmin)/2.0-tb),
        
        where GGD [Celsius] is the difference between daily mean temperature [Celsius]  and tbase [Celsius].
        For tmax or tmin < tb, GDD is set to zero. 
        """
        if tmax < tb or tmin < tb:
            return 0
        else:
            return ((tmax+tmin)/2.0-tb)
    def getstage(self,gdd):
        """
        Returns the actual stage depending on the actual amounbt of GDD.
        """
        for stage in self.stage:
            if gdd <= stage.gdd:
                return stage.name
                break        

class Stage:
    """
    The stage class definese deveopment stages with name and accumulated GDDs.
    """
    def __init__(self,name,gdd):
        self.name=name
        self.gdd=gdd