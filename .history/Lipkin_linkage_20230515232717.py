import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np
from numpy import *

window_width = 600
window_height = 600

gui = ti.GUI("wave", res=(window_width, window_height))

while gui.running:
    gui.show()
    