import taichi as ti
import numpy as np

ti.init(arch=ti.cuda)
N=500
gui = ti.GUI("wave", res=(N , N),fast_gui=True)