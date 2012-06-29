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
                 tbase = 0.,
                 stage = [['Emergence',160.],
                          ['Leaf development',208.],
                          ['Tillering',421.],
                          ['Stem elongation',659.],
                          ['Anthesis',901.],
                          ['Seed fill',1174.],
                          ['Dough stage',1556.],
                          ['Maturity',1665.]],
                 RUE=3.,
                 k=.4,
                 seasons =[160.0, 499.0, 897.0, 1006.0],
                 kcb =[0.15,1.1,0.15] ):
        self.tbase = tbase
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb
        self.RUE=RUE
        

stage = [['sftgs',343.],[],[]]
WW = CropCoefficiants(stage=stage)