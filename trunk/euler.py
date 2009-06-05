from pylab import *
"""
###Example
f = lambda x,y: -2*x*y**2
h=0.1
u0 = 1
u1 = u0 + h * f(0,u0)
u2 = u1 + h * f(0.1,u1)
u3 = u2 + h * f(0.2,u2)
u4 = u3 + h * f(0.3,u3)
u5 = u4 + h * f(0.4,u4)
u6 = u5 + h * f(0.5,u5)
example_result=[u0,u1,u2,u3,u4,u5,u6]
"""
###Eulers equation
def euler(x,delta_t,f_x):
    return x + delta_t * f_x
"""  
x=[0,0.1,0.2,0.3,0.4,0.5]
euler_result=[]
euler_result.append(1)

for i in range(6):
    func = f(x[i],euler_result[i])
    euler_result.append(euler(euler_result[i],0.1,func))
 
print example_result
print euler_result
x.append(0.6)
plot(x,example_result,label='example_result')
plot(x,euler_result,'ro',label='euler_result')
legend(loc=0)
show()"""

###Growth equation
def assimilate(W_total):
        return 0.1*W_total*(1.0-W_total/100)
    
W_total=[]
W_total.append(1)
W_euler=[]
W_euler.append(1)

for i in arange(100):    
    W_total.append(assimilate(W_total[i])+W_total[i])


i=0 
timestep=1
timeseries=arange(0,100,1)
for steps in timeseries:
    W_euler.append(euler(W_euler[i],timestep,assimilate(W_euler[i])))
    i+=1



fig=figure()
fig.add_subplot(211)
plot(W_euler,'ro',label='W_euler')
legend(loc=0)
fig.add_subplot(212)
plot(W_total, label='W_total')
legend(loc=0)
show()
    
    


