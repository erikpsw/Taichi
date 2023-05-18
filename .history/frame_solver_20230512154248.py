import taichi as ti
import numpy as np

ti.init(arch=ti.cuda)
N=500
gui = ti.GUI("wave", res=(N , N))
pos=np.array([[0,0],[4,0],[2,2/np.sqrt(3)],[2,0]])
pos=pos/5+0.1
pos[:,1]+=0.3
Adj=np.array([[0,2],[0,3],[1,2],[1,3],[2,3]])
print(pos[Adj[:,1]])
while gui.running:
    gui.lines(pos[Adj[:,0]],pos[Adj[:,1]],radius=3,color=0x51acea)
    gui.show()