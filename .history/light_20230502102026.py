import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

theta=np.pi/4
N=2
dy=1/N
n1=1.38
n2=1
n_list=np.linspace(n1,n2,N)
points=[[0,0]]
for i in range(N):
    l=dy/np.sin(theta)
    next_point=[points[-1][0]+l*np.cos(theta),points[-1][0]+dy]
    if(i!=N-1):
        theta=np.arcsin(n_list[i]*np.sin(theta)/n_list[i+1])
points