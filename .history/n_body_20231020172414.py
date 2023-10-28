import numpy as np
import taichi as ti
import copy
ti.init(ti.cpu)

N=2
G=6.67e-11
#1.5倍太阳质量
M=2.9835e30
R=2e7
c=3e8
v0=3.1554e6/np.sqrt(2)

dt=10e-3
lamb=R*10
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
acc = ti.Vector.field(2, ti.f32, N)

pos=np.array([[0.5*lamb-(R),0.5*lamb],[0.5*lamb+(R),0.5*lamb]])
vel=np.array([[0.,v0],[0.0,-v0]])
mass=np.array([M,M])
acc =np.array([[0.,0.],[0.0,0.0]])
# for i in range(N):
    #三个
    # pos[i] = [[0.2,0.5],[0.5,0.5],[0.8,0.5]][i]
    # vel[i] = [[1.0,1.0],[0.0,-1.0],[-1.0,1.0]][i]
    # mass[i]=[1.0,5.0,1.0][i]
    
    # pos[i] = [[0.5,0.8],[0.5,0.5]][i]
    # vel[i] = [[1.,0.],[0.0,0.0]][i]
    # mass[i]=[1.0,3.0][i]


#随机初始化
def initialize():
    for i in range(N):
        # pos[i]=[0.5,0.5]
        #全在中心
        pos[i]=[ti.random(),ti.random()]
        vel[i]=[lamb*(ti.random()-0.5),lamb*(ti.random()-0.5)]
        mass[i]=1


def compute_force(num):
    acc[num]=[0,0]
    for i in range(N):
        if(i!=num):
            d=pos[i]-pos[num]#位矢
            acc[num]+=G*d*mass[i]/((np.sqrt((d[0])**2+(d[1])**2))**3)

def updater():
    for i in range(N):
        pos[i]+=vel[i]*dt
        vel[i]+=acc[i]*dt
        print(np.linalg.norm(vel[i]))
        Ek=(mass[i]*np.linalg.norm(vel[i])**2)/2-(32*(G**4)*(M**4)*2*M)*(1+73/24+37/96)*dt/(2*5*(R)**5*c**5)
        vel[i]=vel[i]*np.sqrt(2*Ek/mass[i])/np.linalg.norm(vel[i])
        print(np.linalg.norm(vel[i]))
        


gui=ti.GUI("n body problem",(512,512))

path=[copy.deepcopy(pos[0])/lamb]
# initialize()
while gui.running:
    for i in range(N):
        compute_force(i)
    updater()
    tmp=copy.deepcopy(pos[0])
    # print(pos/lamb)
    path.append(tmp/lamb)
    # print(path)
    gui.circles(pos/lamb,color=0xffffff,radius=4)
    gui.lines(begin=np.array(path[:-1]),end=np.array(path[1:]),radius=2,color=0xffffff)
    gui.show()
    
# import numpy as np
# import taichi as ti
# ti.init(ti.gpu)

# N=30
# k=1
# g=-9.8
# pos = ti.Vector.field(2,float,N)
# vel = ti.Vector.field(2,float,N)
# acc = ti.Vector.field(2,float,N)
# mass=ti.field(float, N)

# @ti.kernel
# def init():
#     for i in range(N):
#         pos[i]+=ti.Vector([ti.random(),ti.random()])
#         vel[i]+= ti.Vector([0.,0.])
#         acc[i]+=ti.Vector([0.,0.])
#         mass[i]+=1.

# dt=10e-5
    
# @ti.kernel
# def updater():
#     for num in range(N):
#         acc[num]-=acc[num]
#         acc[num]+=ti.Vector([0,g])
#     for i, num in ti.ndrange(N, N):
#         if(i!=num):
#             d=pos[i]-pos[num]#位矢
#             acc[num]-=d*mass[i]/(ti.math.sqrt((d[0])**2+(d[1])**2))*10e-1
#         acc[num]+=ti.Vector([1.,0.])*(k/pos[num][0])
#         acc[num]+=ti.Vector([-1.,0.])*(k/(1-pos[num][0]))
#         acc[num]+=ti.Vector([0.,1.])*(k/pos[num][1])
#         acc[num]+=ti.Vector([0.,-1.])*(k/(1-pos[num][1]))
#         vel[num]+=acc[num]*dt
#         pos[num]+=vel[num]*dt
        
        


# gui=ti.GUI("n body problem",(512,512))
# init()
# while gui.running:
#     updater()
#     gui.clear(0x112F41)
#     gui.circles(pos.to_numpy(),color=0xffffff,radius=3)
#     gui.show()