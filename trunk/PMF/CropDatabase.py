# -*- coding:utf-8 -*-
"""
The Crop Database holds crop specific parameter. Theses parameter refer to
the requirements of the classes in the Process Library 

:author: Sebastian Multsch

:version: 0.1 (26.10.2010)

:copyright: 
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
class CropCoefficiants_wheat:
    """
    Holds crop specific parameters for summer wheat.
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
                 RUE=3.,    #Stockle 1992 Table1  #RUE=2.2source : Soltani & Sinclair (2012), p.3#RUE at reference CO2 concentration
                 C_0=350., #ppm reference atmospheric CO2 concentration
                 k=.4,
                 seasons = [160.0, 499.0, 897.0, 1006.0],  #für baresoi,[0,0,0,0], 
                 kcb = [0.15,1,1,0.15],  #  für baresoil [0,0,0,0],  # für fullcover [1,1,1,1], #
                 FRDR = 0.5,
                 Cr = 0.5,          #  extinction coefﬁcient of the vegetation for net radiation
                 albedo_m = 0.23): #albedo for closed canopy of grass
        self.tbase = tbase
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb
        self.RUE=RUE
        self.C_0=C_0
        self.FRDR = FRDR
        self.Cr = Cr
        self.albedo_m = albedo_m
               
        
class CropCoefficiants_c4grass:
    """
    Holds crop specific parameters for C4 grass..
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
                 RUE=3.6, #RUE at reference CO2 concentration
                 C_0=350, #ppm reference atmospheric CO2 concentration
                 k=.4,
                 seasons = [160.0, 499.0, 897.0, 1006.0],  #für baresoi,[0,0,0,0], 
                 kcb = [0.15,1,1,0.15],  
                 FRDR = 0.5,
                 Cr = 0.5,          #extinction coefﬁcient of the vegetation for net radiation
                 albedo_m = 0.23):   #albedo for closed canopy of grass
        self.tbase = tbase
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb
        self.RUE=RUE
        self.C_0=C_0
        self.FRDR = FRDR
        self.Cr = Cr
        self.albedo_m = albedo_m



class CropCoefficiants_c3grass:
    """
    Holds crop specific parameters for C3 grass.
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
                 RUE=2.6,#RUE at reference CO2 concentration
                 C_0=350, #ppm reference atmospheric CO2 concentration
                 k=.4,
                 seasons = [160.0, 499.0, 897.0, 1006.0],  #für baresoi,[0,0,0,0], 
                 kcb = [0.15,1,1,0.15],  
                 FRDR = 0.5,
                 Cr = 0.5,          #extinction coefﬁcient of the vegetation for net radiation
                 albedo_m = 0.23):   #albedo for closed canopy of grass
        self.tbase = tbase
        self.stage=stage
        self.seasons = seasons
        self.k=k
        self.kcb=kcb
        self.RUE=RUE
        self.C_0=C_0
        self.FRDR = FRDR
        self.Cr = Cr
        self.albedo_m = albedo_m

        

stage = [['sftgs',343.],[],[]]
WW = CropCoefficiants_wheat(stage=stage)