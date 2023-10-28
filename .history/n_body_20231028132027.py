# import numpy as np
# import taichi as ti
# import copy
# ti.init(ti.cpu)

# 轨迹
# N=2
# G=6.67e-11
# #1.5倍太阳质量
# M=2.9835e30
# R=1.5e7
# c=3e8
# # v0=3.1554e6/np.sqrt(2)
# v0=0.4*np.sqrt(G*M/R)


# dt=40e-3
# lamb=R*10
# pos = ti.Vector.field(2, ti.f32, N)
# vel = ti.Vector.field(2, ti.f32, N)
# acc = ti.Vector.field(2, ti.f32, N)

# pos=np.array([[0.5*lamb-(R),0.5*lamb],[0.5*lamb+(R),0.5*lamb]])
# vel=np.array([[0.,v0],[0.0,-v0]])
# mass=np.array([M,M])
# acc =np.array([[0.,0.],[0.0,0.0]])
# for i in range(N):
    #三个
    # pos[i] = [[0.2,0.5],[0.5,0.5],[0.8,0.5]][i]
    # vel[i] = [[1.0,1.0],[0.0,-1.0],[-1.0,1.0]][i]
    # mass[i]=[1.0,5.0,1.0][i]
    
    # pos[i] = [[0.5,0.8],[0.5,0.5]][i]
    # vel[i] = [[1.,0.],[0.0,0.0]][i]
    # mass[i]=[1.0,3.0][i]


#随机初始化
# def initialize():
#     for i in range(N):
#         # pos[i]=[0.5,0.5]
#         #全在中心
#         pos[i]=[ti.random(),ti.random()]
#         vel[i]=[lamb*(ti.random()-0.5),lamb*(ti.random()-0.5)]
#         mass[i]=1


# def compute_force(num):
#     acc[num]=[0,0]
#     for i in range(N):
#         if(i!=num):
#             d=pos[i]-pos[num]#位矢
#             acc[num]+=G*d*mass[i]/(np.linalg.norm(d)**3)

# def updater():
#     for i in range(N):
#         pos[i]+=vel[i]*dt
#         vel[i]+=acc[i]*dt
#         print(np.linalg.norm(vel[i]))
#         Er=(32*(G**4)*(M**4)*2*M)*dt/(5*(R)**5*c**5)
#         Ek=(mass[i]*np.linalg.norm(vel[i])**2)/2-Er
#         print(np.sqrt(2*Ek/mass[i])-np.linalg.norm(vel[i]))
#         vel[i]=vel[i]*np.sqrt(2*Ek/mass[i])/np.linalg.norm(vel[i])
        
        


# gui=ti.GUI("n body problem",(512,512))

# path=[copy.deepcopy(pos[0])/lamb]
# # initialize()
# while gui.running:
#     for i in range(N):
#         compute_force(i)
#     updater()
#     tmp=copy.deepcopy(pos[0])
#     # print(pos/lamb)
#     path.append(tmp/lamb)
#     # print(path)
#     gui.circles(pos/lamb,color=0xffffff,radius=4)
#     gui.lines(begin=np.array(path[:-1]),end=np.array(path[1:]),radius=2,color=0xffffff)
#     gui.show()
    
#老
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

import taichi as ti

ti.init(arch=ti.gpu)

N = 32
dt = 1e-4
dx = 1 / N
rho = 4e1
NF = 2 * N**2  # number of faces
NV = (N + 1) ** 2  # number of vertices
E, nu = 4e4, 0.2  # Young's modulus and Poisson's ratio
mu, lam = E / 2 / (1 + nu), E * nu / (1 + nu) / (1 - 2 * nu)  # Lame parameters
ball_pos, ball_radius = ti.Vector([0.5, 0.0]), 0.32
gravity = ti.Vector([0, -40])
damping = 12.5

pos = ti.Vector.field(2, float, NV, needs_grad=True)
vel = ti.Vector.field(2, float, NV)
f2v = ti.Vector.field(3, int, NF)  # ids of three vertices of each face
B = ti.Matrix.field(2, 2, float, NF)
F = ti.Matrix.field(2, 2, float, NF, needs_grad=True)
V = ti.field(float, NF)
phi = ti.field(float, NF)  # potential energy of each face (Neo-Hookean)
U = ti.field(float, (), needs_grad=True)  # total potential energy


@ti.kernel
def update_U():
    for i in range(NF):
        ia, ib, ic = f2v[i]
        a, b, c = pos[ia], pos[ib], pos[ic]
        V[i] = abs((a - c).cross(b - c))
        D_i = ti.Matrix.cols([a - c, b - c])
        F[i] = D_i @ B[i]
    for i in range(NF):
        F_i = F[i]
        log_J_i = ti.log(F_i.determinant())
        phi_i = mu / 2 * ((F_i.transpose() @ F_i).trace() - 2)
        phi_i -= mu * log_J_i
        phi_i += lam / 2 * log_J_i**2
        phi[i] = phi_i
        U[None] += V[i] * phi_i


@ti.kernel
def advance():
    for i in range(NV):
        acc = -pos.grad[i] / (rho * dx**2)
        vel[i] += dt * (acc + gravity)
        vel[i] *= ti.exp(-dt * damping)
    for i in range(NV):
        # ball boundary condition:
        disp = pos[i] - ball_pos
        disp2 = disp.norm_sqr()
        if disp2 <= ball_radius**2:
            NoV = vel[i].dot(disp)
            if NoV < 0:
                vel[i] -= NoV * disp / disp2
        # rect boundary condition:
        cond = (pos[i] < 0) & (vel[i] < 0) | (pos[i] > 1) & (vel[i] > 0)
        for j in ti.static(range(pos.n)):
            if cond[j]:
                vel[i][j] = 0
        pos[i] += dt * vel[i]


@ti.kernel
def init_pos():
    for i, j in ti.ndrange(N + 1, N + 1):
        k = i * (N + 1) + j
        pos[k] = ti.Vector([i, j]) / N * 0.25 + ti.Vector([0.45, 0.45])
        vel[k] = ti.Vector([0, 0])
    for i in range(NF):
        ia, ib, ic = f2v[i]
        a, b, c = pos[ia], pos[ib], pos[ic]
        B_i_inv = ti.Matrix.cols([a - c, b - c])
        B[i] = B_i_inv.inverse()


@ti.kernel
def init_mesh():
    for i, j in ti.ndrange(N, N):
        k = (i * N + j) * 2
        a = i * (N + 1) + j
        b = a + 1
        c = a + N + 2
        d = a + N + 1
        f2v[k + 0] = [a, b, c]
        f2v[k + 1] = [c, d, a]


def main():
    init_mesh()
    init_pos()
    gui = ti.GUI("FEM99")
    while gui.running:
        for e in gui.get_events():
            if e.key == gui.ESCAPE:
                gui.running = False
            elif e.key == "r":
                init_pos()
        for i in range(30):
            with ti.ad.Tape(loss=U):
                update_U()
            advance()
        gui.circles(pos.to_numpy(), radius=2, color=0xFFAA33)
        gui.circle(ball_pos, radius=ball_radius * 512, color=0x666666)
        gui.show()


if __name__ == "__main__":
    main()