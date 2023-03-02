from math import sqrt
import taichi as ti
ti.init(ti.gpu)

N=2
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
acc = ti.Vector.field(2, ti.f32, N)
mass=ti.field(ti.f32, N)
for i in range(N):
    #三个
    # pos[i] = [[0.2,0.5],[0.5,0.5],[0.8,0.5]][i]
    # vel[i] = [[1.0,1.0],[0.0,-1.0],[-1.0,1.0]][i]
    # mass[i]=[1.0,5.0,1.0][i]
    
    pos[i] = [[0.4,0.7],[0.5,0.4]][i]
    vel[i] = [[0,-1.0],[0.0,0.0]][i]
    mass[i]=[1.0,50.0][i]

dt=10e-4
lamb=10

@ti.kernel
#随机初始化
def initialize():
    for i in range(N):
        # pos[i]=[0.5,0.5]
        #全在中心
        pos[i]=[ti.random(),ti.random()]
        vel[i]=[lamb*(ti.random()-0.5),lamb*(ti.random()-0.5)]
        mass[i]=1


@ti.kernel
def compute_force(num:ti.i32):
    acc[num]=[0,0]
    for i in range(N):
        if(i!=num):
            d=pos[i]-pos[num]#位矢
            acc[num]-=d*mass[i]/((ti.sqrt((d[0])**2+(d[1])**2))**2)*10e-1

@ti.kernel
def updater():
    for i in range(N):
        pos[i]+=vel[i]*dt
        vel[i]+=acc[i]*dt
        


gui=ti.GUI("n body problem",(512,512))

      
# initialize()
while gui.running:
    for i in range(N):
        compute_force(i)
    updater()
    gui.clear(0x112F41)
    gui.circles(pos.to_numpy(),color=0xffffff,radius=3)
    gui.show()