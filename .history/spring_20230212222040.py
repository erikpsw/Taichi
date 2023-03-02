import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

def get_norm(x):
    return np.sqrt(x[0]**2+x[1]**2)

def 

n=3
k=1
kf=0.2
vel=np.zeros((n,2))
a=np.zeros((n,2))
pos = np.random.random((n, 2))
l0=0.5
dt=0.1

gui = ti.GUI("circles", res=(400, 400))
while gui.running:
    gui.clear()
    gui.circles(pos, radius=15, color=0xFFFFFF)
    xb=pos[1]-pos[0]
    vb=vel[1]-vel[0]
    xe=pos[-2]-pos[-1]
    ve=vel[-2]-vel[-1]
    a[0]=k*xb/get_norm(xb)*(get_norm(xb)-l0)
    a[-1]=k*xe/get_norm(xe)*(get_norm(xe)-l0)
    for i in range(1,n-1):
        x1=pos[i-1]-pos[i]
        x2=pos[i+1]-pos[i]
        a[i]=k*x1/get_norm(x1)*(get_norm(x1)-l0)+k*x2/get_norm(x2)*(get_norm(x2)-l0)
    for i in range(n):
        vel[i]+=a[i]*dt
        pos[i]+=vel[i]*dt
    for i in range(n-1):
        gui.lines(begin=np.expand_dims(pos[i],0), end=np.expand_dims(pos[i+1],0), radius=2, color=0xFFFFFF)
    gui.show()