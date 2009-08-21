from pylab import *

s_h=[]

depth=[0,10,20,30,40]
s_h=[4,5,6,7,4,2,2,0,0,0]

    

ion()
hold(False)
for i in range(100):
    plot([0+i,3+i,5+i,3+i,8+i],depth)
    xlim(0,100)
    xlabel='water uptake [cm]'
    ylabel='depth [cm]'
show()


    