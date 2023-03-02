import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

def get_norm(x):
    return np.sqrt(x[0]**2+x[1]**2)

def get_unit(x):
    return x/np.sqrt(x[0]**2+x[1]**2)

n=3
k=1
kf=0.002
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
    vb=vel[0]-vel[1]
    xe=pos[-2]-pos[-1]
    ve=vel[-1]-vel[-2]
    xbunit=get_unit(xb) 
    xeunit=get_unit(xe) 
    afb=np.dot(vb,get_unit(xb))*-xbunit
    afe=np.dot(ve,get_unit(xe))*-xeunit
    a[0]=k*xbunit*(get_norm(xb)-l0)+afb
    a[-1]=k*xeunit*(get_norm(xe)-l0)+afe
    for i in range(1,n-1):
        x1=pos[i-1]-pos[i]
        x2=pos[i+1]-pos[i]
        a[i]=k*get_unit(x1)*(get_norm(x1)-l0)+k*get_unit(x2)*(get_norm(x2)-l0)
    for i in range(n):
        vel[i]+=a[i]*dt
        pos[i]+=vel[i]*dt
    for i in range(n-1):
        gui.lines(begin=np.expand_dims(pos[i],0), end=np.expand_dims(pos[i+1],0), radius=2, color=0xFFFFFF)
    gui.show()