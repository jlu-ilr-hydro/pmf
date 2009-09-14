

class RootingZone:
    def __init__(self,lowerlimit=0.,upperlimit=0.,center=0.,depth=0.,penetration=0.):
        self.lowerlimit=lowerlimit
        self.upperlimit=upperlimit
        self.center=center
        self.depth=depth
        self.penetration=penetration
        self.rootingzone=[]
    def __getitem__(self,index):
        return self.rootingzone[index]
    def __iter__(self):
        for horizon in self.rootingzone:
            yield horizon
    def get_rootingzone(self,soil_profile):
        for i,layer in enumerate(soil_profile):
            self.rootingzone.append(RootingZone())
            self.rootingzone[i].lowerlimit=layer
            if i == 0: 
                self.rootingzone[i].upperlimit = 0.
            else: 
                self.rootingzone[i].upperlimit = (soil_profile[i-1])
            self.rootingzone[i].center = (self.rootingzone[i].lowerlimit + self.rootingzone[i].upperlimit) / 2.
            self.rootingzone[i].depth = self.rootingzone[i].lowerlimit - self.rootingzone[i].upperlimit 
    def __call__(self,rooting_depth):
        for layer in self.rootingzone:
            if layer.lowerlimit <= rooting_depth:
                layer.penetration = layer.depth
            elif layer.upperlimit>rooting_depth:
                layer_penetration = 0.
            else: 
                layer.penetration = rooting_depth - layer.upperlimit
                        

soil=[10.,20.,30,40,50]
root=RootingZone()
root.get_rootingzone(soil)

root(0)
    
for layer in root:
    print layer.upperlimit,layer.lowerlimit,layer.center,layer.depth,layer.penetration
   

