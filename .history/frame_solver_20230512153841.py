import taichi as ti
import numpy as np

ti.init(arch=ti.cuda)
N=500
gui = ti.GUI("wave", res=(N , N),fast_gui=True)
pos=np.array([[0,0],[4,0],[2,2/np.sqrt(3)],[2,0]])
pos=pos/5+0.1
sitcks=np.array()
while gui.running:
    gui.show()