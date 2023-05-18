import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

theta=np.pi/4
N=10
dy=1/N
n1=1.38
n2=1
n_list=np.linspace(n1,n2,N)
points=[[0,0]]
for i in range(N):
    l=dy/np.sin(theta)
    next_point=[points[-1][0]+l*np.cos(theta),points[-1][0]+dy]
    points.append(next_point)
    if(i!=N-1):
        theta=np.arccos(n_list[i]*np.cos(theta)/n_list[i+1])
window_width = 600
window_height = 600
print(points)
gui = ti.GUI("wave", res=(window_width, window_height))
while gui.running:
    gui.lines(begin=np.array(points[:-1]),end=np.array(points[1:]),radius=2,color=0xf87064)
    gui.show()