import taichi as ti
import numpy as np


gui=ti.GUI("deformation",(512,512))

pos=[]
for i in np.linspace(0,0.5,5):
    for j in np.linspace(0,0.5,5):
        pos.append([i,j])
pos=ti.Vector.field(2, dtype=ti.f32, shape=2*2, needs_grad=True)
pos

def phi(X):
    A=np.array([[1,0],[-0.1,1]])
    B=np.array([0.1,0.1])
    res=(A@X.T).T+B  #广播机制
    return res

while gui.running:
    gui.circles(phi(pos),color=0xffffff,radius=4)
    gui.show()