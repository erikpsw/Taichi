import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

n=2
vel=np.zeros((n,2))
pos = np.random.random((n, 2))
l0=0.5

gui = ti.GUI("circles", res=(400, 400))
while gui.running:
    gui.circles(pos, radius=15, color=0xFFFFFF)
    b=
    gui.lines(begin=np.expand_dims(pos[0],0), end=np.expand_dims(pos[1],0), radius=2, color=0xFFFFFF)
    gui.show()