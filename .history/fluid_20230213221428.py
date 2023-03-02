import numpy as np
import taichi as ti
ti.init(ti.gpu)

N=3
k=1
g=-9.8
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
acc = ti.Vector.field(2, ti.f32, N)
mass=ti.Vector(np.ones(N))
for i in range(N):
    #三个
    pos[i] = [[0.2,0.5],[0.5,0.5],[0.8,0.5]][i]
    vel[i] = [0,0]
    # pos[i] = [[0.4,0.7],[0.5,0.4]][i]
    # vel[i] = [[0,-1.0],[0.0,0.0]][i]
    # mass[i]=[1.0,1.0][i]

dt=10e-4
lamb=10
    
d=ti.Vector([0.,0.])
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
        vel[i]+=acc[i]*dt
        pos[i]+=vel[i]*dt
        
        


gui=ti.GUI("n body problem",(512,512))

while gui.running:
    updater()
    gui.clear(0x112F41)
    gui.circles(pos.to_numpy(),color=0xffffff,radius=3)
    gui.show()