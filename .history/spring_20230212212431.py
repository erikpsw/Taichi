import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)

pos = np.random.random((50, 2))
# Create an array of 50 integer elements whose values are randomly 0, 1, 2
# 0 corresponds to 0x068587
# 1 corresponds to 0xED553B
# 2 corresponds to 0xEEEEF0
indices = np.random.randint(0, 2, size=(50,))
gui = ti.GUI("circles", res=(400, 400))
while gui.running:
    gui.circles(pos, radius=5, palette=[0x068587, 0xED553B, 0xEEEEF0], palette_indices=indices)
    gui.show()