import taichi as ti
import numpy as np
ti.init(ti.gpu)
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

gui=ti.GUI("deformation",(512,512))

NV=2*2
pos=[]
pos=ti.Vector.field(2, dtype=ti.f32, shape=NV, needs_grad=True)
vel = ti.Vector.field(2, float, NV)
f2v = ti.Vector.field(3, int, 2)  # ids of three vertices of each face
pos.from_numpy(np.array([[0,0],[0,1],[1,0],[1,1]],dtype=np.float32))
f2v.from_numpy(np.array([[0,1,2],[1,2,3]],dtype=np.float32))

def phi(X):
    A=np.array([[1,0],[-0.1,1]])
    B=np.array([0.1,0.1])
    res=(A@X.T).T+B  #广播机制
    return res

while gui.running:
    gui.circles(phi(pos),color=0xffffff,radius=4)
    gui.show()