import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

theta=np.pi/4
R=5
a=8
b=3
print(((2*R*np.cos(theta))**2+a**2-b**2)/(2*a*2*R*np.cos(theta)))
