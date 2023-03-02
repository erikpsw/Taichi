import numpy as np
import taichi as ti
ti.init(ti.gpu)

gui=ti.GUI("n body problem",(512,512))
while gui.running: