import numpy as np
import taichi as ti
ti.init(ti.gpu)

N=150
k=1
g=-9.8
pos = ti.field(ti.f32,(N,2))
vel = ti.field(ti.f32,(N,2))
acc = ti.field(ti.f32,(N,2))
mass=ti.Vector(np.ones(N))

@ti.kernel
def init():
    for i in range(N):
        pos[i]+=[ti.random(),ti.random()]
        vel[i]+= ti.Vector([0.,0.])
        acc[i]+=ti.Vector([0.,0.])

dt=10e-4
lamb=10
    
@ti.kernel
def updater():
    for num in ti.static(range(N)):
        acc[num]-=acc[num]
        acc[num]+=ti.Vector([0,g])
        for i in ti.static(range(N)):
            if(i!=num):
                d=pos[i]-pos[num]#位矢
                acc[num]-=d*mass[i]/((ti.sqrt((d[0])**2+(d[1])**2))**2)*10e-1
        acc[num]+=ti.Vector([1.,0.])*(k/pos[num][0])
        acc[num]+=ti.Vector([-1.,0.])*(k/(1-pos[num][0]))
        acc[num]+=ti.Vector([0.,1.])*(k/pos[num][1])
        acc[num]+=ti.Vector([0.,-1.])*(k/(1-pos[num][1]))
        vel[num]+=acc[num]*dt
        pos[num]+=vel[num]*dt
        
        


gui=ti.GUI("n body problem",(512,512))
init()
while gui.running:
    updater()
    gui.clear(0x112F41)
    gui.circles(pos.to_numpy(),color=0xffffff,radius=3)
    gui.show()