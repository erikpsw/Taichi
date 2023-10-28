import taichi as ti
import numpy as np


gui=ti.GUI("deformation",(512,512))

pos=[]
for i in np.linspace(0,0.5,5):
    for j in np.linspace(0,0.5,5):
        pos.append([i,j])
pos=np.array(pos)

def phi(X):
    print(X)
    A=np.array([[1,0],[-0.5,1]])
    B=np.array([0.1,0.1])

    res=A@X.T
    print(res)
    return res

while gui.running:
    gui.circles(phi(pos),color=0xffffff,radius=4)
    gui.show()