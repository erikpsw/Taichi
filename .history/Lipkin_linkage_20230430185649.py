# import taichi as ti
# ti.init(arch=ti.gpu)
import numpy as np

theta=np.pi/4
R=5
a=8
b=3
print(((2*R*np.cos(theta))**2+a**2-b**2)/(2*a*2*R*np.cos(theta)))
