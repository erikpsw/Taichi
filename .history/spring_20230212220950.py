import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

def get_norm(x):
    return np.sqrt(x[0]**2+x[1]**2)

n=2
k=1
vel=np.zeros((n,2))
a=np.zeros((n,2))
pos = np.random.random((n, 2))
l0=0.5
dt=0.1

gui = ti.GUI("circles", res=(400, 400))
while gui.running:
    gui.clear()
    gui.circles(pos, radius=15, color=0xFFFFFF)
    x=pos[1]-pos[0]
    a[0]=k*x/get_norm(x)*(get_norm(x)-l0)
    a[1]=-a[0]
    for i in range(n):
        vel[i]+=a[i]*dt
        pos[i]+=vel[i]*dt
    gui.lines(begin=np.expand_dims(pos[0],0), end=np.expand_dims(pos[1],0), radius=2, color=0xFFFFFF)
    gui.show()