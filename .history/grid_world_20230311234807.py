import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
canvas_width=10
canvas_width=10
canvas=np.zeros((canvas_width,canvas_width,3))
