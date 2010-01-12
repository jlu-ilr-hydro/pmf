# -*- coding:utf-8 -*-
"""
Plant interface to the environmental models

@author: Sebastian Multsch

@version: 1.0 (01.10.2009)

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
 
@summary: Plant interface to the environmental models
"""

def get_pressurehead(self,depth):
    """ Depth in cm; Returns the capillary suction for a given depth in [cm]."""
    pass
def get_nutrients(self,depth):
    """ Depth in cm; Returns the nitrogen concentration in the soil solution in [mol l-1] """
    pass
def soilprofile(self):
    """ Returns a list with the lower limits of the layers in the whole soilprofile in [cm]. """
    pass
def get_fc(self,depth):
    """ soil water content at field capacity [m3 m-3] """
    pass
def get_wp(self,depth):
    """ soil water content at wilting point [m3 m-3] """
    pass
def get_wetness(self,depth):
    """ wetness in the top soil layer in [m3 m-3] """
    pass
def get_tmean(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns mean temperature in [°C]."""
    pass
def get_tmin(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns minimal temperature in [°C]."""
    pass
def get_tmax(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns maximal temperature in [°C]."""
    pass
def get_Rs(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
    pass
def get_Rn(self,time,albedo,daily=True):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns total solar radiation in [MJ m-2]"""
    pass
def get_ea(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns actual vapor pressure in [kPa]"""
    pass
def get_es(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns saturated vapor pressure in [kPa] """
    pass
def get_windspeed(self,time):
    """ Time as datetime instance: datetime(JJJJ,MM,DD); Returns windspeed in [m s-1]"""
    pass
def Kr(self):
    pass

