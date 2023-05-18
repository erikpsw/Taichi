import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

theta=np.pi/4
N=2
n1=1.38
n2=1
print(np.linspace(0,1,N+1))