import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

pos = np.random.random((2, 2))

gui = ti.GUI("circles", res=(400, 400))
while gui.running:
    gui.circles(pos, radius=15, color=0xFFFFFF)
    gui.show()