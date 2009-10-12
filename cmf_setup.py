import cmf
from cmf.soil import layer as ka4_soil
import numpy as np
class cmf1d(object):
    def __init__(self,sand=70,silt=20,clay=10,c_org=2.0,bedrock_K=0.01,layercount=50,layerthickness=0.1):
        # Create a cmf project
        self.project=cmf.project()
        #self.project.debug=1
        # Add a cell add the origin (pos=(0,0,0)) with 1000m2 area. The area has the advantage 1m3 = 1mm * Area
        self.cell=self.project.NewCell(0,0,0,1000)
        c=self.cell
        KA4_soil=ka4_soil(0.1,clay,silt,sand,Corg=c_org)
        
        r_curve=cmf.BrooksCoreyRetentionCurve(KA4_soil.KSat , KA4_soil.porosity, KA4_soil.b, KA4_soil.fieldcap)
        # Add 50 layers with 10cm thickness, and 50 Neumann boundary conditions
        self.__bc=[]
        for i in range(1,layercount+1):
            c.add_layer(i*layerthickness,r_curve) # Create the layer
            # Create a boundary condition
            nbc=cmf.NeumannBoundary(self.project,cmf.point(0.0,0.0,-i*layerthickness))
            nbc.Name="Boundary condition #%i" % i
            nbc.connect_to(c.layers[-1])
            self.__bc.append(nbc)
        # Add a bedrock layer
        c.add_layer(7,cmf.BrooksCoreyRetentionCurve(bedrock_K,0.1,1,0.01))
        # Add a groundwater boundary (potential=-5.0 m)
        self.groundwater=cmf.DricheletBoundary(self.project,c.layers[-1].gravitational_potential)
        self.groundwater.Name="Groundwater"
        # Connect bedrock layer with groundwater boundary, using Richards equation
        cmf.connect(cmf.Richards,c.layers[-1],self.groundwater,c.area,c.layers[-1].thickness)
        
        # Use Richards equation for percolation
        c.install_connection(cmf.Richards)
        self.integrator=cmf.CVodeIntegrator(self.project,1e-6)
        self.integrator.LinearSolver=0
    def run(self,dt=cmf.h):
        self.integrator(self.integrator.t+dt)
    def __get_t(self):
        """The model time"""
        return self.integrator.t.AsPython()  
    def __set_t(self,time):
        self.integrator.t=time        
    t=property(__get_t,__set_t)
    def layer(self,depth):
        pos=min(int(depth/0.1),len(self.cell.layers)-1)
    @property
    def matrix_potential(self):
        """Returns the capillary suction in m for each layer (including the bedrock layer)"""
        return [l.matrix_potential for l in self.cell.layers]
    @property
    def pF(self):
        """The pF value for each layer """
        return [l.pF for l in self.cell.layers]
    @property
    def potential(self):
        """ The actual water head of each layer """
        return [l.potential for l in self.cell.layers]
    @property
    def wetness(self):
        """ The wetness (water content per pore volume) for each layer """
        return [l.wetness for l in self.cell.layers]
    @property 
    def depth(self):
        """ Returns the center depth of each layer (including the bedrock layer) """
        return np.array([-0.5*(l.boundary[0]+l.boundary[1]) for l in self.cell.layers])
    @property
    def groundwater_flux(self):
        return -self.groundwater.water_balance(self.t)
    @property
    def percolation(self):
        return [self.cell.layers[i].flux_to(self.cell.layers[i+1] if i+1< self.cell.layer_count() else self.groundwater,self.t) for i in range(self.cell.layer_count())]
    def __get_flux(self):
        return np.array([-bc.water_balance(cmf.Time()) for bc in self.__bc])
    def __set_flux(self,fluxes):
        try:
            for i,bc in enumerate(self.__bc):
                if i<len(fluxes):
                    bc.flux=cmf.timeseries(fluxes[i])
                else:
                    bc.flux=cmf.timeseries(0.0)
        except TypeError:
            raise TypeError("Fluxes is not a sequence of floats. Fluxes needs to be a sequence with %i float values" % self.cell.layer_count())            
    flux=property(__get_flux,__set_flux,"The boundary fluxes. A sequence with as many elements as layers")

