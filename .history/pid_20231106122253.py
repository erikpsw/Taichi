import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)


target=0.5
y=0.5
gui = ti.GUI('pid')

while gui.running:
    gui.circle([target,y], radius=2)
    gui.show()