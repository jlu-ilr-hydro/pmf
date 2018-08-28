# -*- coding: utf-8 -*-
'''
Created on 25 sep 2014

:author: S. Multsch, modified by J. Kellner
'''

class Development:
    """
    Calculates the developmentstage of plant with the thermaltime concept.
    
    Development is an implementation of the plant interface
    development with the required functions.

    Implementation
    ==============
    A development instance must be hand over to plant for the 
    implementation of plant. Development for itself must be
    implemented with the crop specific developmentstages and the
    related total thermaltime for each stage.
    
    Call signature
    ==============
    Call development calculates thermaltime.
    """
    def __init__(self, stage, Rp, Rv, photo_on_off, verna_on_off):                                                 
        """
        Returns a development instance.
        
        Development is defined through the stage parameter. 
        this parameter holds a list with the name of each
        stage and the related total thermaltime. The total
        values are the thresholds for changing the stage.
        The total thermaltime values of the stages are 
        constant values. Variation of the amount of time,
        which is required to reach the next stage, is only
        possible through the variation of the daily calculated
        degree days.
        
        :type stage: list
        :param stage: List with names and total thermaltime requirement 
        for each stage in [°C].
        :type Rp: double
        :param Rp: crop specific parameter showing sensitivity to photoperiod [-]
        :type photo_on_off: double
        :param photo_on_off: Parameter to turn on (=1) or off (=0) photoperiodic response [-]
        :type Rv: double
        :param Rv: crop specific parameter showing sensitivity to vernalization [-]
        :type verna_on_off: double
        :param verna_on_off: Parameter to turn on (=1) or off (=0) vernalization function [-]
        :type photo: double
        :param photo: photoperiod factor between 0 and 1 [-]
        :type verna_sum: double
        :param verna_sum: total vernalization [-]
        :type verna_factor: double
        :param verna_factor: vernalization factor between 0 and 1 [-]
        :type tt: double
        :param tt: sum of degree days [°C days]
        :type rate: double
        :param rate: degree day (Tmean - Tbase) [°C days]
        :rtype: development
        :return: Development instance        
        """
        
        
        #constants
        self.stages = []
        self.Rp = Rp    
        self.Rv = Rv   
        self.photo_on_off=photo_on_off
        self.verna_on_off=verna_on_off 
        
        
        # state variable
        self.photo = 1.
        self.verna_sum = 0.
        self.verna_factor = 1.
        self.tt = 0.                                                       
        self.rate = 0.                                                                     
        for s in stage:
            self.__setitem__(s)
            
            
        stage_n = [i[0] for i in stage]
        self.index_anthesis = stage_n.index('Anthesis')
        self.index_stemelongationend = stage_n.index('Stem elongation')        

    @property
    def StageIndex(self):
        """
        Returns the index of the actual development stage in the stage 
        attribute of the development class
        
        :rtype: integer
        :return: Index of the actual development stage
        """
        
        return self.stages.index(self.Stage)
    @property
    def IsGrowingseason(self):
        """
        Returns True during growingseason.
        
        :rtype: boolean
        :return: True during growingseason.
        """
        return True if self.tt>=self.stages[0][1] and self.tt< self.stages[-1][1] else False
    @property
    def IsGerminated(self):
        """
        Return True, if germination is complete.
        
        :rtype: boolean
        :return: True, if germination is complete.
        """
        return True if self.tt > self.stages[0][1] else False
    @property
    def Thermaltime(self):
        """
        Return actual thermaltime.
        
        :rtype: double
        :return: Thermaltime in [°days].
        """
        return self.tt
    @property
    def Stage(self):
        """
        Returns the name of the actual development stage
        
        If development is finished, the function returns 'Development finished'
        
        :rtype: String
        :return: Actual developmentstage.
        """
        return filter(lambda i:i[1]>=self.tt, self.stages)[0] if self.tt<=self.stages[-1][1] else 'Development finished'
    def __setitem__(self,stage):
        self.stages.append(stage)
    def __getitem__(self,index):
        return self.stages[index]
    def __iter__(self):
        for s in self.stages:
            yield s
            
 
    def __call__(self,step,tmin,tmax,tbase,daylength,tmean):       
        """
        Calculates thermaltime.
        
        :type step: double
        :param step: Time step of the actual model period in [days or hours].
        :type tmin: double
        :param tmin: Daily minimum temperature in [°C].
        :type tmax: double
        :param tmax: Daily maximum temperature in [°C].
        :type tbase: double 
        :param tbase: Crop specific base temperature over which development 
        can occur in [°C].
        :type daylength: double
        :param daylength: daylight [h], calculated according to FAO irrigationa and drainage paper pp.48
        """       
        
        # from emergence till floral initiation: vernalization and photoperiodic effect      
        if self.tt < self.stages[0][1] or self.tt > self.stages[self.index_stemelongationend][1]:       
            self.rate = self.develop(tmin, tmax, tbase) * step                                   
            self.tt = self.tt + self.rate                                      
            
        else:
            self.rate = self.develop(tmin, tmax, tbase) * step
            # vernalization, the colder, the bigger verna_sum
            self.verna_sum = self.verna_sum + (self.vernalization_rate(tmin, tmax,tmean) - self.devernalization(self.verna_sum, tmax))
            #factor between 0 and 1
            self.verna_factor = max(1-self.verna_on_off, max(0, 1 - (0.0054545 * self.Rv + 0.0003)*(50 - self.verna_sum)))
            # photoperiod factor between 0 and 1
            self.photo = max(1-self.photo_on_off, max(0, self.photoperiod(daylength, self.Rp))) 
            self.rate = self.rate * min(self.photo, self.verna_factor)          
            self.tt = self.tt + self.rate        
        
        
    def photoperiod(self, daylength, Rp):
        """ Calculates a photoperiod factor [-].
        
        Calculates a photoperiod factor between 0 and 1, which adjusts development by letting thermal time get affected by day length.
        This concept follows the APSIM approach (source: "The APSIM-Wheat module (7.5 R3008)", March 2014)
        
        :type Rp: double
        :param Rp: crop specific parameter showing sensitivity to photoperiod [-]
        :type dl: double
        :param dl: day length [h]
        
        :rtype: double
        :return: Photoperiod factor which is used to adjust development by letting thermal time get affected by day length. [-]
        """
        return 1.-0.002*Rp*(20. - daylength)**2.
                 
        
    def vernalization_rate(self,tmin,tmax,temp_crown):
        """ Calculates the daily rate of vernalization [-].
        
        Calculates the daily rate of vernalization [-].
        This concept follows the CERES approach and was extracted from APSIM documentation (source: "The APSIM-Wheat module (7.5 R3008)", March 2014)
        
        :type tmin: double
        :param tmin: Daily minimum temperature in [°C].
        :type tmax: double
        :param tmax: Daily maximum temperature in [°C].
        :type temp_crown: double
        :param temp_crown: Daily temperature in plant crown [°C].
        :rtype: double
        :return: daily vernalization based on daily temperature minimum and maximum [-].
        """
        if tmin < 15. and tmax < 30.:
#            temp_crown = ((tmax+tmin)/2.0 * 1.2)   
            verna_rate = min(1.4 - 0.0778 * temp_crown, 0.5 + 13.44 * (temp_crown/(tmax - tmin +3)**2))
        else:
            verna_rate = 0.
        
        return verna_rate    
        
        
    def devernalization(self, verna_sum, tmax):
        """ Calculates daily devernalization [-].
        
        Calculates the daily devernalization if the daily maximum temperature is higher than 30°C and the total vernalization is smaller than 10. 
        Else, devernalization is set to zero.
        This concept follows the CERES approach and was extracted from APSIM documentation (source: "The APSIM-Wheat module (7.5 R3008)", March 2014)
        
        :type verna_sum: double
        :param verna_sum: total vernalization
        :type tmax: double
        :param tmax: Daily maximum temperature in [°C].
        
        :rtype: double
        :return: daily devernalization 
        """
        if tmax > 30. and verna_sum < 10.:       
            devernali = min(verna_sum, 0.5*(tmax - 30.))
        else: 
            devernali = 0.
        
        return devernali 
                                                    
                                
    def develop(self,tmin,tmax,tbase):
        """
        Returns thermaltime rate.
        
        If tmax or tmin smaller than tbase, the rate is defined to be zero.
        Else the rate is computed as (tmax+tmin/2 - tbase).
        
        :type tmin: double
        :param tmin: Daily minimum temperature in [°C].
        :type tmax: double
        :param tmax: Daily maximum temperature in [°C].
        :type tbase: double 
        :param tbase: Crop specific base temperature over which development 
        can occur in [°C].
        
        :rtype: double
        :return: Development rate as thermatime in [°C].
         
        :see: [Bonhomme, 2000, McMaster & Wilhelm, 1997] 
        """
        if tmax < tbase or tmin < tbase:
            return 0
        else:
            return ((tmax+tmin)/2.0-tbase)