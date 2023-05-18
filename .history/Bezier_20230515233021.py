import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

window_width = 600
window_height = 600

gui = ti.GUI("wave", res=(window_width, window_height))


P=np.random.rand((3,2))
print(P)

while gui.running:
    gui.show()
    