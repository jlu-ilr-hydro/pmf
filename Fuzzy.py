class FuzzySet(object):
    """FuzzySet
    FuzzySet description:
        FuzzySet is a fuzzy functions. y_min is 0 and y_max is 1 per default.
    
    FuzzySet parameters:
    Fuzzy_Set as List [x1,x2,x3,x4]
    
    FuzzySet examples:

    """
    
    """Constructor"""
    def __init__(self, FuzzySet):
        """Parameter List"""
        self.__FuzzySet = FuzzySet
    
    """Properties"""
    #Property: function
    def get_FuzzySet(self):
        return self.__FuzzySet
    def set_FuzzySet(self,newFuzzySet):
        try:
            #checks newFuzzySet
            assert(type(newFuzzySet) in (List)), "Value must be a List"
            assert(len(newFuzzySet)!=4), "List must be lenght 4"
            
            self.__FuzzySet = newFuzzySet
                
        except AssertionError, err:
            print err
    FuzzySet = property(get_FuzzySet,set_FuzzySet,None,"A FuzzySet")
    
    """Functions"""
    def __call__(self,x_value):
        """Function
        __call__ description:
        Returns the fuzzy value of a given x value!
    
        __call__ parameters:
        x_value
        
        __call__ examples:
 
        """
        try:
            if x_value<self.__FuzzySet[0] or x_value>self.__FuzzySet[-1]: return 0
            if x_value>=self.__FuzzySet[1] and x_value<=self.__FuzzySet[2]: return 1
            elif x_value<self.__FuzzySet[1]: return (x_value-self.__FuzzySet[0])/(self.__FuzzySet[1]-self.__FuzzySet[0])
            else: return (self.__FuzzySet[-1]-x_value)/(self.__FuzzySet[-1]-self.__FuzzySet[-2])
        
        except ValueError, err:
            print err

