import taichi as ti
import numpy as np
ti.init(ti.gpu)

gui=ti.GUI("deformation",(512,512))

#参数
N=1
dt=1e-4
dx=1/N
rho = 4e1
NF = 2 * N**2  # 面数
NV = (N + 1) ** 2  # 顶点数
E, nu = 4e4, 0.2  # Young's modulus and Poisson's ratio
mu, lam = E / 2 / (1 + nu), E * nu / (1 + nu) / (1 - 2 * nu)  # Lame parameters
# ball_pos, ball_radius = ti.Vector([0.5, 0.0]), 0.32
gravity = ti.Vector([0, -40])
damping = 12.5

B = ti.Matrix.field(2, 2, float, NF)
F = ti.Matrix.field(2, 2, float, NF, needs_grad=True) #NF个2*2的矩阵
phi = ti.field(float, NF)  # 势能 密度
pos=ti.Vector.field(2, dtype=ti.f32, shape=NV, needs_grad=True)
vel = ti.Vector.field(2, float, NV)
f2v = ti.Vector.field(3, int, 2)  # 每个面的顶点索引
U = ti.field(float, (), needs_grad=True)  # 总势能

pos.from_numpy(np.array([[0.3,0.3],[0.3,0.6],[0.6,0.3],[0.6,0.6]],dtype=np.float32))
f2v.from_numpy(np.array([[0,1,2],[1,2,3]]))

@ti.kernel
def init_pos():
    for i in range(NF):
        ia, ib, ic = f2v[i]
        a, b, c = pos[ia], pos[ib], pos[ic] #提前计算B
        B_i_inv = ti.Matrix.cols([a - c, b - c])
        B[i] = B_i_inv.inverse()


V = ti.field(float, NF)

@ti.kernel
def update_U():
    for i in range(NF):
        ia, ib, ic = f2v[i]
        a, b, c = pos[ia], pos[ib], pos[ic]
        V[i] = abs((a - c).cross(b - c))
        D_i = ti.Matrix.cols([a - c, b - c]) # 增广矩阵
        F[i] = D_i @ B[i]
    for i in range(NF):
        F_i = F[i]
        log_J_i = ti.log(F_i.determinant())
        phi_i = mu / 2 * ((F_i.transpose() @ F_i).trace() - 2)
        phi_i -= mu * log_J_i
        phi_i += lam / 2 * log_J_i**2
        phi[i] = phi_i #利用neo-Hookean公式计算给定梯度的势能密度
        U[None] += V[i] * phi_i

@ti.kernel
def advance():
    for i in range(NV):
        acc = -pos.grad[i] / (rho * dx**2) # 对总能量的梯度除以质量
        vel[i] += dt * (acc + gravity)
        vel[i] *= ti.exp(-dt * damping)
    for i in range(NV):
        # 墙壁边界条件 矩阵的逻辑运算
        cond = (pos[i] < 0) & (vel[i] < 0) | (pos[i] > 1) & (vel[i] > 0)
        for j in ti.static(range(pos.n)):
            if cond[j]:
                vel[i][j] = 0
        pos[i] += dt * vel[i]

while gui.running:
    init_pos()
    for i in range(1):
        with ti.ad.Tape(loss=U):# 设置总体函数
            update_U()
        # print(pos)
        advance()
    gui.circles(pos.to_numpy(),color=0xffffff,radius=4)
    gui.show()