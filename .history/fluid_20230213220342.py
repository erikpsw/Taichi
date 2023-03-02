import numpy as np
import taichi as ti
ti.init(ti.gpu)

N=3
k=1
g=-9.8
pos = np.random.rand(N,2)
vel = ti.Vector.field(2, ti.f32, N)
acc = ti.Vector.field(2, ti.f32, N)
mass=np.ones(N)
# for i in range(N):
#     #三个
#     pos[i] = [[0.2,0.5],[0.5,0.5],[0.8,0.5]][i]
#     vel[i] = [[0.0,0.0],[0.0,0.],[0.,0.0]][i]
#     mass[i]=[1.0,5.0,1.0][i]
    
    # pos[i] = [[0.4,0.7],[0.5,0.4]][i]
    # vel[i] = [[0,-1.0],[0.0,0.0]][i]
    # mass[i]=[1.0,1.0][i]

dt=10e-4
lamb=10

@ti.func
def compute_force(num):
    acc[num]=[0,g]
    for i in range(N):
        if(i!=num):
            d=pos[i]-pos[num]#位矢
            acc[num]-=d*mass[i]/((ti.sqrt((d[0])**2+(d[1])**2))**2)*10e-1
    acc[num]+=ti.Vector([1.,0.])*(k/pos[num][0])
    acc[num]+=ti.Vector([-1.,0.])*(k/(1-pos[num][0]))
    acc[num]+=ti.Vector([0.,1.])*(k/pos[num][1])
    
@ti.kernel
def updater():
    for i in range(N):
        compute_force(i)
        vel[i]+=acc[i]*dt
        pos[i]+=vel[i]*dt
        
        


gui=ti.GUI("n body problem",(512,512))

while gui.running:
    updater()
    gui.clear(0x112F41)
    gui.circles(pos.to_numpy(),color=0xffffff,radius=3)
    gui.show()