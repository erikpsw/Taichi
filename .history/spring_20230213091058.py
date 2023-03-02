import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

def get_norm(x):
    return np.sqrt(x[0]**2+x[1]**2)

def get_unit(x):
    return x/np.sqrt(x[0]**2+x[1]**2)

n=3
k=5
kfs=0
kf=1.5
M=np.ones((n))
M[-1]=1.5
g=np.array([0,-1])
vel=np.zeros((n,2))
a=np.zeros((n,2))
pos = np.random.random((n, 2))
pos[0]=np.array([0.5,1])
l0=0.05
dt=0.1

gui = ti.GUI("circles", res=(600, 600))
while not gui.get_event(ti.GUI.ESCAPE):
    if(gui.get_event(gui.))
    gui.clear()
    xe=pos[-2]-pos[-1]
    ve=vel[-2]-vel[-1]
    xeunit=get_unit(xe) 
    afe=kfs*np.dot(ve,get_unit(xe))*xeunit
    a[-1]=(k*xeunit*(get_norm(xe)-l0)+afe-kf*vel[-1])/M[-1]
    for i in range(1,n-1):
        x1=pos[i-1]-pos[i]
        x2=pos[i+1]-pos[i]
        x1unit=get_unit(x1)
        x2unit=get_unit(x2)
        v1=vel[i-1]-vel[i]
        v2=vel[i+1]-vel[i]
        af=kfs*(np.dot(v1,get_unit(x1))*x1unit+np.dot(v2,get_unit(x2))*x2unit)
        a[i]=(k*get_unit(x1)*(get_norm(x1)-l0)+k*get_unit(x2)*(get_norm(x2)-l0)+af-kf*vel[i])/M[i]
    for i in range(n):
        if(i!=0):
            vel[i]+=(a[i]+g)*dt
        pos[i]+=vel[i]*dt
    gui.circles(pos, radius=15, color=0xFFFFFF)
    for i in range(n-1):
        gui.lines(begin=np.expand_dims(pos[i],0), end=np.expand_dims(pos[i+1],0), radius=2, color=0xFFFFFF)
    gui.show()