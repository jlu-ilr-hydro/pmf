import numpy as np
import matplotlib.pyplot as plt

root=[-.5 for i in range(364)]
shoot=[.5 for i in range(364)]
x=range(0,364,1)
plt.plot(x,shoot,color='k')
plt.fill_between(x,0,shoot,facecolor='green')
plt.grid()
plt.plot(x,root,color='k')
plt.fill_between(x,0,root,facecolor='brown')
plt.grid()






plt.show()
