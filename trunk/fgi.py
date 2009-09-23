from pylab import *

def get_fgi(s_h,ETp,R_a,R_p,nitrogen,alpha):
        w=1-s_h/ETp
        n=1-(R_a/R_p) if R_p>0. else 0.
        if  w >= n:
            return [a/sum(alpha) for a in alpha]
        else:
            return [n/sum(nitrogen) for n in nitrogen]
def compensate():
    pass

a=[];b=[];c=[]         
res=[]
for i in range(10):
    A=exp(-i*0.5)
    B=exp(-i*0.005)
    C=1.
    print '%4.2f' % A,'%4.2f' % B
    fgi= get_fgi(10,10,1,1,[1,1,1,1],[A,B,1.,1.])
    print ['%4.2f' % f for f in fgi],sum(fgi)
    res.append(fgi)

imshow(transpose(res),cmap=cm.RdYlBu,vmin=0.0,vmax=1.0)
grid()
colorbar()
show()