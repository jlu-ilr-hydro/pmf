# -*- coding:utf-8 -*-
"""
The Crop Database holds crop specific parameter. Theses parameter refer to
the requirements of the classes in the Process Library 

@author: Sebastian Multsch

@version: 0.1 (26.10.2010)

@copyright: 
 This program is free software; you can redistribute it and/or modify it under  
 the terms of the GNU General Public License as published by the Free Software  
 Foundation; either version 3 of the License, or (at your option) any later 
 version. This program is distributed in the hope that it will be useful, 
 but WITHOUT ANY  WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or  FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
 more details. You should have received a copy of the GNU General 
 Public License along  with this program;
 if not, see <http://www.gnu.org/licenses/>.
"""
class CropCoefficiants:
    """
    Holds crop specific parameters.
    """
    def __init__(self,
                 tbase = 0.,#!!
                 stage = [['Emergence',160.],#!!
                          ['Leaf development',208.],
                          #['Tillering',421.],
                          #['Stem elongation',659.],
                          ['Anthesis',901.],
                          #['Seed fill',1174.],
                          #['Dough stage',1556.],
                          ['Maturity',1665.]],
#                 stage = [['Emergence',160.],#!!
#                          ['Leaf development',208.],
#                          ['Anthesis',901.],
#                          ['Maturity',1665.]],
                 seasons =[160.0, 499.0, 897.0, 1006.0],
                 k=.4,#!!                 
                 kcb =[0.15,1.1,0.15],#!!                 
                 RUE=3.,#!!
                 #shoot_percent=[.0,.5,.5,.9,.95,1.,1.,1.],
                 shoot_percent=[.0,.5,.95,1.],
                 #root_percent=[.0,.5,.5,.1,.05,.0,.0,.0],                 
                 root_percent=[.0,.5,.05,.0],
                 #leaf_percent=[.0,.5,.5,.5,.0,.0,.0,.0],
                 leaf_percent=[.0,.5,.0,.0],
                 #stem_percent=[.0,.5,.5,.5,.5,.0,.0,.0],
                 stem_percent=[.0,.5,.5,.0],
                 #storage_percent=[.0,.0,.0,.0,.5,1.,1.,1.],                 
                 storage_percent=[.0,.0,.5,1.],                 
                 
                 pressure_threshold=[0.,1.,500.,16000.],
                 plantN=[[160.,0.043],[1200.,0.016]],
                 leaf_specific_weight=40.,#!!
                 root_growth=1.5,#!!
                 max_height=1.,#!!
                 stress_adaption=1.,
                 carbonfraction=.4,#!!
                 max_depth=150.):#!!
        
        
        self.tbase = tbase
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb
        self.RUE=RUE
        self.shoot_percent=shoot_percent #List with partitioning coefficiants for each development as fraction from the plant biomass in [-]
        self.root_percent=root_percent
        self.leaf_percent=leaf_percent
        self.stem_percent=stem_percent
        self.storage_percent=storage_percent
        self.pressure_threshold=pressure_threshold
        self.plantN=plantN
        self.leaf_specific_weight=leaf_specific_weight
        self.root_growth=root_growth
        self.max_height=max_height
        self.stress_adaption=stress_adaption
        self.carbonfraction=carbonfraction
        self.max_depth=max_depth
        

#stage = [['sftgs',343.],[],[]]
#RUE = [1],[2],[3],[4],[5],[6],[7],[8],[9],[10]
#RR = CropCoefficiants(RUE=RUE)
#WW = CropCoefficiants(stage=stage)