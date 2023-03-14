import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
canvas_width=10
canvas_width=10
canvas=np.zeros((canvas_width*pixel_size,canvas_width*pixel_size,3))

gui=ti.GUI("grid",(canvas_width*pixel_size,canvas_width*pixel_size))
while gui.running:
    gui.set_image(canvas)
    gui.show()