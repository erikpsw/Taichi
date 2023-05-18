import taichi as ti
import numpy as np

ti.init(arch=ti.cuda)
N=500
gui = ti.GUI("wave", res=(N , N),fast_gui=True)

while gui.running:
    gui.set_image(canvas)
    gui2.set_image(board)
    gui.show()